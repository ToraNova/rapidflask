#namespace Zfence
#(USED FOR ZFENCE with an IMAGE)
# IMAGE IS USED SIMILARLY LIKE A MAP
from flask_socketio import Namespace, emit
from flask import copy_current_request_context
import paho.mqtt.client as mqtt #MQTT
from pkg.resource import rdef as res #resource importing
from pkg.database.fsqlite import db_session

import datetime, time

class Zfence(Namespace):

    c = mqtt.Client()

    def startMQclient(self,verbose=False):
        self.c.on_connect = self.mqconn
        self.c.on_message = self.mqrecv
        self.sublist = []
        self.verboseprint = self.pkgprint if verbose else lambda *a, **k: None
        self.c.connect('0.0.0.0',1883)
        self.c.loop_start()

    def mqconn(self,client, userdata, flags, rc):
        #subscribe to all RPi in the database
        self.resub()
        self.verboseprint("Connected and subscribed to "+str(len(self.sublist))+ " hosts")
        self.c.subscribe('zfence/wire') #
        self.c.subscribe('zfence/gz') #alert subscriptions

    def updateGThreshold(self,hid,bid,sid,ith,v=True):
        if(sid==0):
            targetlist = res.gsensor.GSensor.query.filter(res.gsensor.GSensor.rpi_id == hid).filter(
                res.gsensor.GSensor.branch_n == bid).all()
            for t in targetlist:
                t.config_verify = v
                t.threshold = ith
                db_session.add(t)
        else:
            target = res.gsensor.GSensor.query.filter(res.gsensor.GSensor.rpi_id == hid and
                res.gsensor.GSensor.branch_n == bid and
                res.gsensor.GSensor.segment_n == sid).first()
            target.config_verify = v
            target.threshold = ith
            db_session.add(target)
        db_session.commit()

    def insertGAlert(self,hostid,branch,segment,magnitude,wcut=False):
        insert_list = {
        "rpi_id":hostid,
        "branch_n":branch,
        "segment_n":segment,
        "magnitude":magnitude,
        "wcut":wcut,
        "time":datetime.datetime.now()
        }
        target = res.gsensor_alert.GSensorAlert(insert_list)
        db_session.add(target)
        db_session.commit()

    def mqrecv(self,client, userdata, msg):
        #process topic
        try:
            strpayload = msg.payload.decode('utf-8')
            hostid = strpayload.split(',')[0]
            subtopic = msg.topic.split('/')[1]
            self.verboseprint('MSG received...'+subtopic+' '+strpayload+" hid:"+hostid)
            if(subtopic == 'rep'):
                repres = strpayload.split(',')[1]
                #emit('mqreply',{'hostid':hostid,"rep":repres},namespace='/zfence')
                if(userdata != None):
                    if(repres == '0' and userdata[1] == 3):
                        #success
                        self.updateGThreshold(
                        userdata[0].get("hid"),userdata[0].get("bid"),
                        userdata[0].get("sid"),userdata[0].get("ith"))
            elif(subtopic == 'gz'):
                #alert detected
                branch = strpayload.split(',')[1]
                sensor = strpayload.split(',')[2]
                magntd = strpayload.split(',')[3]
                self.insertGAlert(hostid,branch,sensor,magntd,False)

            elif(subtopic == 'wire'):
                #wirecut event
                res = int(strpayload.split(',')[1])
                if(res != 0):
                    #error has occurred,
                    self.insertGAlert(hostid,res,0,'wire_cut',True)
                else:
                    #no error. all OK
                    pass
        except Exception as e:
            self.verboseprint("mqrecv exception has occurred:"+str(e))

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_alertquery(self):
        g_alert = res.gsensor_alert.GSensorAlert.query.filter( res.gsensor_alert.GSensorAlert.reason == None ).all()
        r_alert = res.radar_alert.PRadarAlert.query.filter( res.radar_alert.PRadarAlert == None ).all()

        sp_alertlist = []
        for g in g_alert:
            data_dict={}
            data_dict["atype"] = "gaccel"
            data_dict["id"] = g.id
            data_dict["hostid"] = g.rpi_id
            data_dict["atime"] = str(g.time)
            data_dict["branch"] = g.branch_n
            data_dict["segment"] = g.segment_n
            data_dict["magnitude"] = g.magnitude
            sp_alertlist.append(data_dict)
        for r in r_alert:
            data_dict={}
            data_dict["atype"] = "radar"
            data_dict["id"] = r.id
            data_dict["hostid"] = r.rpi_id
            data_dict["atime"] = str(r.time)
            data_dict["branch"] = r.branch_n
            data_dict["segment"] = r.segment_n
            data_dict["magnitude"] = str(r.stepval)+'_'+str(r.magnitude)
            sp_alertlist.append(data_dict)

        if(len(sp_alertlist) > 0):
            emit('alertupdate',{"alerts":sp_alertlist})

    def on_alerthandle(self,json):
        cam1 = res.segcam.SegmentCamera.query.filter( res.segcam.SegmentCamera.trig_seghst == json.get("hostid")).filter(
            res.segcam.SegmentCamera.trig_branch == 1).first()
        f1 = res.ipcam_model.IPCameraModel.query.filter( res.ipcam_model.IPCameraModel.id == cam1.model_id).first()
        cam2 = res.segcam.SegmentCamera.query.filter( res.segcam.SegmentCamera.trig_seghst == json.get("hostid")).filter(
            res.segcam.SegmentCamera.trig_branch == 2).first()
        f2 = res.ipcam_model.IPCameraModel.query.filter( res.ipcam_model.IPCameraModel.id == cam2.model_id).first()
        emit('alertpanel',{"ip1":cam1.ip_address,"ip2":cam2.ip_address,
            "furl1":f1.ffmpeg_url,"furl2":f2.ffmpeg_url})

    def on_reasonregister(self,json):
        #obtain the alert from json and register a reason to it.
        g_alert = res.gsensor_alert.GSensorAlert.query.filter( res.gsensor_alert.GSensorAlert.id == json.get("alertid") ).first()
        g_alert.reason = json.get("reason")
        db_session.add(g_alert)
        db_session.commit()

    def on_thresholdupdate0(self,json):
        pubstr = 'threshold,{},{},{}'.format(json.get('bid'),json.get('sid'),json.get('ith'))
        #print('zfence/cmd/'+str(json.get('hid')),pubstr)
        self.updateGThreshold(json.get('hid'),json.get('bid'),json.get('sid'),json.get('ith'),v=False)
        self.on_panelupdate({"type":3,"id":json.get('hid')})
        self.c.user_data_set([json,3])
        #unverify the sensor first
        self.c.publish('zfence/cmd/'+str(json.get('hid')),pubstr)
        emit('remit',{"time":5,"target":"thresholdupdate1","type":3,"hid":json.get("hid")})

    def on_thresholdupdate1(self,json):
        self.on_panelupdate({"type":3,"id":json.get('hid')})
        self.c.user_data_set(None)

    def getchkstr(self,hostid,branch,chain_chkstr,stroke_e=None):
        chkstr = chain_chkstr #for chaining
        target_host = res.seghost.SegmentHost.query.filter(res.seghost.SegmentHost.id == hostid).first()
        if(branch==1):
            target_line1 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg1).first()
            chkstr[target_line1.id] = "#66ff66" if stroke_e == None else stroke_e #BLUE FOR SEG 1
        elif(branch==2):
            target_line2 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg2).first()
            chkstr[target_line2.id] = "#3366ff" if stroke_e == None else stroke_e  #GREEN FOR SEG 2
        else:
            target_line1 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg1).first()
            target_line2 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg2).first()
            chkstr[target_line1.id] = "#cc33ff" if stroke_e == None else stroke_e
            chkstr[target_line2.id] = "#cc33ff" if stroke_e == None else stroke_e
        return chkstr

       ########################################################################################################################
       # SEGMENT OPERATION CALLBACK / REQUEST , ADD , REMOVE
       ########################################################################################################################
    def on_segmentrequest(self,json):
        #On segment request, send back the line data
        id = json.get("id")
        branch = json.get('branch')
        chkstr = {}
        if(json.get('type') ==1 ):
            #segment host requesting line stroke

            if(branch != None):
                chkstr = self.getchkstr(id,branch,chkstr)
            self.sendSegment(chkstr)
        elif(json.get('type') ==2 ):
            #segment cam requesting line stroke
            target_cam = res.segcam.SegmentCamera.query.filter(res.segcam.SegmentCamera.id == id).first()
            target_line = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_cam.los_segment).first()
            if(target_cam.trig_branch == 1):
                self.sendSegment({target_line.id:"#3366cc"})
            elif(target_cam.trig_branch == 2):
                self.sendSegment({target_line.id:"#00cc99"}) #send
            else:
                self.sendSegment({target_line.id:"#ffff66"})
        #type 3 is for threshold update
        elif(json.get('type')==4):
            #obtain the list of segment that are on alert
            for uid in json.get('uid'):
                chkstr = self.getchkstr(uid.get('hostid'),uid.get('branch'),chkstr,'#')
            self.sendSegment(chkstr)
        elif(json.get('type')==5):
            #focus alerts (details and highlighting)
            target_cam = res.segcam.SegmentCamera.query.filter(res.segcam.SegmentCamera.trig_seghst == id).all()
            for c in target_cam:
                target_line = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == c.los_segment).first()
                if(c.trig_branch == 1):
                    chkstr[target_line.id]="#3366cc"
                elif(c.trig_branch == 2):
                    chkstr[target_line.id]="#00cc99" #send
                else:
                    chkstr[target_line.id]="#ffff66"
            if(branch != None):
                chkstr = self.getchkstr(id,branch,chkstr)
            self.sendSegment(chkstr)

        else:
            self.sendSegment({})
            pass

    def on_segmentdraw(self,json):
    	#draw onto the segment
    	#try:
    	id = json.get("id")
    	if(json.get('type')==1 and json.get("branch") != None):
    		#type 1 used for shost
    		nid = self.addSegment(json['sx'],json['sy'],json['ex'],json['ey'],json['width'],"#000000","#ff0000")
    		target_host = res.seghost.SegmentHost.query.filter(res.seghost.SegmentHost.id == id).first()
    		if(json.get("branch") == 1 ):
    			target_host.g_fdrawseg1 = nid
    		elif(json.get("branch") == 2):
    			target_host.g_fdrawseg2 = nid
    		db_session.add(target_host)
    		db_session.commit()
    	elif(json.get('type')==2):
    		nid = self.addSegment(json['sx'],json['sy'],json['ex'],json['ey'],json['width'],"#6600ff","#ff0066")
    		target_cam = res.segcam.SegmentCamera.query.filter(res.segcam.SegmentCamera.id == id).first()
    		target_cam.los_segment = nid
    		db_session.add(target_cam)
    		db_session.commit()
    	else:
    		pass
    	#except Exception as e:
    		#print("Exception during segmentdraw :",str(e))

    def on_delsegment(self,json):
    	#deletes a segment canvas_line
    	try:
    		id = json.get("id")
    		if(json.get('type')==1):
    			target_host = res.seghost.SegmentHost.query.filter(res.seghost.SegmentHost.id == id ).first()
    			self.deleteSegment(target_host.g_fdrawseg1)
    			self.deleteSegment(target_host.g_fdrawseg2)
    			target_host.g_fdrawseg1 = None
    			target_host.g_fdrawseg2 = None
    			db_session.add(target_host)
    			db_session.commit()
    		elif(json.get('type')==2):
    			target_cam = res.segcam.SegmentCamera.query.filter(res.segcam.SegmentCamera.id == id).first()
    			self.deleteSegment(target_cam.los_segment)
    			target_cam.los_segment = None
    			db_session.add(target_cam)
    			db_session.commit()
    		else:
    			pass
    	except Exception as e:
    		print("Exception on delete segment",str(e))
    		db_session.rollback()
   ########################################################################################################################
   # //SEGMENT
   ########################################################################################################################

    def on_panelupdate(self,json):
        #update the panel
        type = json.get("type")
        list = []
        hid = None
        if(type==1):
            rawlist = res.seghost.SegmentHost.query.all()
        elif(type==2):
            rawlist = res.segcam.SegmentCamera.query.all()
        elif(type==3):
            hid = json.get('id')
            rawlist = res.gsensor.GSensor.query.filter(res.gsensor.GSensor.rpi_id == hid).all()

        if(type==1 or type==2):
            for ent in rawlist:
                data_dict = {}
                data_dict["id"] =  ent.id
                data_dict["ip"] =  ent.ip_address
                if(type==1):
                    data_dict["seg1"] =  ent.g_fdrawseg1
                    data_dict["seg2"] =  ent.g_fdrawseg2
                elif(type==2):
                    data_dict["seg1"] = ent.los_segment
                list.append(data_dict)
        elif(type == 3):
            for ent in rawlist:
                data_dict = {}
                data_dict['snum'] = ent.segment_n
                data_dict['bnum'] = ent.branch_n
                data_dict['threshold'] = ent.threshold
                data_dict['cverify'] = ent.config_verify
                list.append(data_dict)
        emit('regen_panel',{"panelist":list,"type":type,"id":hid})

    def addSegment(self,sx,sy,ex,ey,width,dcolor,tcolor):
    	#returns the newly added ID
    	#vanilla add segment, fixed width, trig color
    	try:
    		#attempt to add the new segment, using an insert_list
    		insert_list = {
    			"startx":sx,
    			"starty":sy,
    			"endx":ex,
    			"endy":ey,
    			"width":width,
    			"color":dcolor,
    			"tcolor":tcolor
    		}
    		new_canvasline = res.canvas_line.CanvasLine(insert_list)
    		db_session.add(new_canvasline)
    		db_session.commit()
    	except Exception as e:
    		db_session.rollback()
    		raise ValueError('Failed to add canvas_line')#fail
    	return new_canvasline.id

    def sendSegment(self,strkchg):
    	canvasline_list = res.canvas_line.CanvasLine.query.all()
    	list = []
    	for lines in canvasline_list:
    		data_dict = {}
    		data_dict["sx"] = lines.startx
    		data_dict["sy"] = lines.starty
    		data_dict["ex"] = lines.endx
    		data_dict["ey"] = lines.endy
    		data_dict["width"] = lines.width
    		if( lines.id in strkchg):
    			if(strkchg[lines.id] == '#'):
    				data_dict['stroke'] = lines.tcolor
    			else:
    				data_dict['stroke'] =  strkchg[lines.id]
    		else:
    			data_dict["stroke"] = lines.color
    		list.append(data_dict)
    	emit('segmentline_data',{"segmentlines":list})

    def deleteSegment(self,id):
    	try:
    		c1 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == id).first()
    		db_session.delete(c1)
    		db_session.commit()
    	except Exceptiona as e:
    		db_session.rollback()

    # MQTT FUNCTION
       # HOUSEKEEPING FUNCTIONS -- PLEASE DO NOT TOUCH THESE ! LACK OF DEBUGGING MSG FROM PAHO MQTT !
    def pkgprint(self,str):
        print("{}[MQTSOCKIO]".format(datetime.datetime.now()),str)

    def unsuball(self):
        for s in self.sublist: #unsubscribe all
            self.c.unsubscribe(s)

    def subdb(self):
        try:
            seghost_list = res.seghost.SegmentHost.query.all()
            for host in seghost_list:
                subtopic = 'zfence/rep/'+str(host.id) #subscribe to all the host's reply channel
                self.sublist.append(subtopic)
                self.c.subscribe(subtopic)
        except Exception as e:
            self.verboseprint("Exception has occurred "+str(e))

    def resub(self):
        #resubscribe to all known hosts in the database
        self.unsuball() #unsub all
        self.subdb() #resub all db hosts
