# MBDPI async receiver with threading support
# based off Jason Loh's token / tls middlebox
# DPI library. mailto:jasonlohjc@gmail.com

# 2019 Toranova mailto: chia_jason96@live.com

import threading
import socket
import ssl
import time
from flask_socketio import emit

from mb_dpi.sslconn import SSLestablish, SSLkeyextract
from mb_dpi.server import ver_method_1,ver_method_2,ver_method_3

class MBDPI_receiver(threading.Thread):

    def __init__(self,addr,portn,scheme,emit_namespace):
        # initilize the threading obj
        threading.Thread.__init__(self)
        self._kill_event = threading.Event() #allows stopping, this flag is the stop flag
        # socket creation
        self.token_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.token_sock.bind( (addr,portn) )
        self.token_sock.listen(5)
        self.TLS_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TLS_sock.bind( (addr,portn+1) )
        self.TLS_sock.listen(5)
        # setting up flask_socketio emit namespaces, schemes
        self.emit_ns = emit_namespace
        self.scheme = scheme

        # emit a status change msg
        emit("status_change",{"status":"Waiting for incoming conn. on {} on ports {},{}".format(
			self.token_sock.getsockname()[0],self.token_sock.getsockname()[1],
            self.TLS_sock.getsockname()[1])}, namespace=self.emit_ns)

    def killthread(self):
        self._kill_event.set()

    def run(self):
        # main thread body
        block_size = 16
        buff_size = 1024
        server_cert = 'server.crt'
        server_key = 'server.key'

        token_conn, token_addr = self.token_sock.accept() #blocking
        TLS_conn, TLS_addr = self.TLS_sock.accept() #blocking
        emit("status_change",{"status":"Connection from {}:{}".format( token_addr[0],token_addr[1])},
           namespace=self.emit_ns)

        # setup vars
        sslsock = SSLestablish(self.TLS_sock,server_cert,server_key)   # establish the ssl conn, 3-way handshake
        sesskey = SSLkeyextract(sslsock)        # extract the keys from the socket
        counter_table = OrderedDict()           # create the counter table
        sk = ""
        pairing = ""

        try:
            while not self._kill_event.is_set() :
                # RECEIVER CODE GOES HERE

                ssl_traffic = b''
                # loop and wait until all packets is received
                while not self._kill_event.is_set():
                    if not ssl_traffic: break
                    rbuff = sslsock.recv()
                    ssl_traffic += rbuff

                emit("status_change",{"status":"SSL Traffic received."},
                namespace=self.emit_ns)

                ssl_traffic = ssl_traffic.decode('utf-8') # decode to string

                tok_traffic = b''
                # loop and wait until all packets is received
                while not self._kill_event.is_set():
                    if not tok_traffic: break
                    rbuff = token_conn.recv()
                    tok_traffic += rbuff

                emit("status_change",{"status":"Enc Token Traffic received."},
                namespace=self.emit_ns)

                if scheme == "blindbox":
                    resval = ver_method_1(msg_data, token_data_list,
                        sesskey.get("client_write_key"), sesskey.get("client_write_IV"), counter_table)
                elif scheme == "embark":
                    resval = ver_method_2(msg_data, token_data_list)
                elif scheme == "pairing":
                    resval = ver_method_3(msg_data, token_data_list, pairing, sk, counter_table)

                if(resval):
                    emit("token_validate",{"status":"Valid tokens"}, namespace=self.emit_ns)
                else:
                    emit("token_validate",{"statis":"Invalid tokens"},namespace=self.emit_ns)

        except Exception as e:
            emit("status_change",{"status":"Exception has occurred in recv thread {}".format(str(e))}, namespace=self.emit_ns)
        finally:
            self.TLS_sock.close()
            self.token_sock.close()
