# MBDPI async transmitter with threading support
# based off Jason Loh's token / tls middlebox
# DPI library. mailto:jasonlohjc@gmail.com

# 2019 Toranova mailto: chia_jason96@live.com

import threading
import socket
import time
from flask_socketio import emit

from mb_dpi.sslconn import SSLestablish, SSLkeyextract
from mb_dpi.client import send_method_1,send_method_2,send_method_3

class MBDPI_transmitter(threading.Thread):

    def __init__(self,rx_addr,mb_addr,portn,portn_mb,scheme,emit_namespace):
        # initilize the threading obj
        threading.Thread.__init__(self)
        self._kill_event = threading.Event() #allows stopping, this flag is the stop flag
        self._msg_avail = threading.Event()
        # setting up flask_socketio emit namespaces, schemes
        self.emit_ns = emit_namespace
        self.scheme = scheme            # obtain the scheme from here

        emit('display_update',{'panel':'entoken','content':'hello world!'},namespace=self.emit_ns)

        token_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if token_conn.connect_ex((mb_addr, portn))!=0:
            token_conn.close()

            emit("status_change", {"status":"no connection to middlebox"} )
            self._kill_event.set()
        else:
            emit("status_change", {"status":"connected to middlebox"} )
            conn_param = rx_addr.encode() + b':' + str(portn_mb).encode()
            token_conn.send(conn_param) #specify to MB who we want to connect and to which port
            handshake_ready = token_conn.recv(4) # receive HSOK flag



            if handshake_ready == b'HSOK':

                TLS_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if TLS_conn.connect_ex(( mb_addr, target_port+1))!=0:
                    emit("status_change",{"status":"no connection to middlebox (via Rx)"})
                    TLS_conn.close()
                    token_conn.close()
                    self._kill_event.set()
                else:
                    emit("status_change",{"status":"connected to middlebox (Mb) and receiver (Rx) through middlebox"})
                    self.TLS_conn = TLS_conn
                    self.token_conn = token_conn
            else:
                emit("status_change",{"status":"Did not receive clearance for handshake with Rx through middlebox"})


    def killthread(self):
        self._kill_event.set()

    def pushmsg(self,msg_string):
        self.push_string = msg_string
        self._msg_avail.set() #set the flag to allow the main body to run

    def run(self):
        # main thread body

        if(not self._kill_event.is_set()):
            block_size = 16
            buff_size = 1024

            client_cert = 'client.crt'
            client_key = 'client.key'

            sslsock = SSLestablish(self.TLS_conn,client_cert,client_key)   # establish the ssl conn, 3-way handshake
            sesskey = SSLkeyextract(sslsock)        # extract the keys from the socket
            counter_table = OrderedDict()           # create the counter table

            if scheme == "pairing":
                pairing, sk = on_Setup_Pairing(client_write_key)
            else:
                sk = ""
                pairing = ""

            try:
                while not self._kill_event.is_set() :
                    # SENDER CODE GOES HERE

                    self._msg_avail.wait() #threading block mechanism
                    self._msg_avail.reset()

                    if method == "blindbox":
                        enclist = send_method_1(self.push_string,
                            sesskey.get('client_write_key'), sesskey.get('client_write_IV'),
                            self.token_conn, sslsock, counter_table)
                    elif method == "embark":
                        enclist = send_method_2(self.push_string,
                        sesskey,get('client_write_key'), sesskey.get('client_write_IV'),
                        self.token_conn, sslsock)
                    elif method == "pairing":
                        enclist = send_method_3(self.push_string, pairing, sk, self.token_conn, sslsock, counter_table)

                    emit('status_message',{"status_message":"Message and Tokens send success"},namespace=self.emit_ns)

                    emit('display_update',{'panel':'entoken','content':enclist},namespace=self.emit_ns)

            except Exception as e:
                emit("status_change",{"status":"Exception has occurred in send thread".format(str(e))}, namespace=self.emit_ns)
            finally:
                self.TLS_sock.close()
                self.token_sock.close()
