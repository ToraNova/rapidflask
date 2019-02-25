#--------------------------------------------------
# mapio.py
# this file contains the socketio class for the
# interface/mapping library
# introduced 3/2/2019
#--------------------------------------------------

#flask socket io
from flask_socketio import Namespace, emit
from pkg.resource import rdef as res #resource importing
from pkg.database.fsqlite import db_session

import datetime

#namespace Zfence
#(USED FOR ZFENCE with an IMAGE)
# IMAGE IS USED SIMILARLY LIKE A MAP
class Zfence(Namespace):
	def on_connect(self):
		pass

	def on_disconnect(self):
		pass

	def on_segmentrequest(self,json):
		self.sendSegment(json.get("hostid"),json.get('branch'))

	def on_segmentdraw(self,json):
		self.addSegment(json['sx'],json['sy'],json['ex'],json['ey'],json['width'],
		json['hostid'],json['branch'])

	def on_delsegment(self,json):
		try:
			target_host = res.seghost.SegmentHost.query.filter(res.seghost.SegmentHost.id == json['hostid']).first()
			c1 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg1).first()
			c2 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg2).first()
			target_host.g_fdrawseg1 = None
			target_host.g_fdrawseg2 = None
			db_session.delete(c1)
			db_session.delete(c2)
			db_session.add(target_host)
			db_session.commit()
		except Exception as e:
			db_session.rollback()

	def addSegment(self,sx,sy,ex,ey,width,hostid,branch):
		#vanilla add segment, fixed width, trig color
		insert_list = {
			"startx":sx,
			"starty":sy,
			"endx":ex,
			"endy":ey,
			"width":width,
			"color":"#000000",
			"tcolor":"#FF0000"
		}
		new_canvasline = res.canvas_line.CanvasLine(insert_list)
		target_host = res.seghost.SegmentHost.query.filter(res.seghost.SegmentHost.id == hostid).first()
		db_session.add(new_canvasline)
		db_session.commit()
		if(branch == 1):
			target_host.g_fdrawseg1 = new_canvasline.id
		elif(branch == 2):
			target_host.g_fdrawseg2 = new_canvasline.id
		else:
			return
		db_session.add(target_host)
		db_session.commit()

	def sendSegment(self,hostid,branch):
		targets = []
		if(hostid != None):
			target_host = res.seghost.SegmentHost.query.filter(res.seghost.SegmentHost.id == hostid).first()
			if(branch != None):
				if(branch==1):
					target_line1 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg1).first()
					targets.append(target_line1.id)
				elif(branch==2):
					target_line2 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg2).first()
					targets.append(target_line2.id)
				else:
					target_line1 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg1).first()
					target_line2 = res.canvas_line.CanvasLine.query.filter(res.canvas_line.CanvasLine.id == target_host.g_fdrawseg2).first()
					targets.append(target_line1.id)
					targets.append(target_line2.id)

		canvasline_list = res.canvas_line.CanvasLine.query.all()
		list = []
		for lines in canvasline_list:
			data_dict = {}
			data_dict["sx"] = lines.startx
			data_dict["sy"] = lines.starty
			data_dict["ex"] = lines.endx
			data_dict["ey"] = lines.endy
			data_dict["width"] = lines.width
			if( lines.id in targets):
				if(branch==1):
					data_dict["stroke"] = "#3366ff"
				elif(branch==2):
					data_dict["stroke"] = "#66ff66"
				else:
					data_dict["stroke"] = "#cc33ff"
			else:
				data_dict["stroke"] = lines.color
			data_dict["stroke_sp"] = lines.tcolor
			list.append(data_dict)
		emit('segmentline_data',{"segmentlines":list})

#namespace class MapPointSocket
#migrated from socketio.py since u6
#handles display of geopoints on a map. (USED FOR GEOPOINTS WITH LEAFLET)
class MapPointSocket(Namespace):
	def on_connect(self):
		#upon connection
		self.sendPointData()

	def on_disconnect(self):
		#on disconnect callback
		pass

	def on_update(self):
		#on_update callback
		self.sendPointData()

	def on_pointAdd(self,json):
		self.addPointData(json["lati"],json["long"])

	def addPointData(self,lati,long):
		insert_list = {
		"long":long,
		"lati":lati,
		"time":datetime.datetime.now()
		}
		newmark = res.geopoint.Geopoint(insert_list)
		db_session.add(newmark)
		db_session.commit()

	def sendPointData(self):
		#code to send out all geopoints from the db
		pointlist = res.geopoint.Geopoint.query.all()
		list = []

		for points in pointlist:
			data_dict = {}
			data_dict["id"] = points.id
			data_dict["long"] = points.long
			data_dict["lati"] = points.lati
			data_dict["time"] = points.time.strftime('%m/%d/%Y %H:%M:%S')
			route = res.georoute.Georoute.query.filter(
			res.georoute.Georoute.id == points.route_id ).first()
			if route == None:
				data_dict["route"] = "Unassigned"
			else:
				data_dict["route"] = route.name
			list.append(data_dict)
		#list = str(list)[1:-2]
		#out = json.dumps({"points":list})
		emit('point_data',{"points":list})
