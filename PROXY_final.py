#coding:utf-8
#coding:utf-8
import threading
import socket
import select

IP = ""
PORT = 9090
default_HOST = '0.0.0.0:22'
MSG = '@Dragontechz on telegram'
RESPONSE = (f'HTTP/1.1 200 OK\r\nmessage: {MSG}\r\n\r\n').encode("utf-8")
buffer = 1024*1024


def findhost(payload):
     index = payload.find("Host:")
     if index != -1:
          debut = index + 5
          fin = payload.find("\r\n",debut)
          if fin != -1:
               host = payload[debut:fin].strip()
               return host
          return None
i = '127.0.0.1'
def sock():
     sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     return sock

def handle_data(data):
                    try:
                         host =i
                         sock2host = sock()
                         sock2host.connect((host,22))
                         sock2host.send(data)
                         response = sock2host.recv(buffer)
                         return response
                    except socket.gaierror:
                         print("cann't connect to host: {}".format(host))
                         response = b'cannot connect to ' + host.encode('utf-8')
                         return response
def handle_conn(conn):
     data = conn.recv(buffer)
     print(data)
     conn.send(RESPONSE)
     while True:
          data = conn.recv(buffer)
          print(data)
          if data:
               response = handle_data(data)
               print('sending respond to client')
               conn.send(response)
               continue
          else:
               conn.send(b'')

class threadforclient(threading.Thread):
     def __init__(self,conn,addr):
          threading.Thread.__init__(self)
          self.conn = conn
          self.ip,self.port = addr
          self.client = {self.ip:self.conn}
          self.list =[]

     def run(self):
          try:
               if self.client in self.list:
                    handle_conn(self.conn)
               else:
                    self.list.append(self.client)
                    print("client {} has bieng added".format(self.ip))
                    handle_conn(self.conn) 
          except ConnectionResetError:
               if self.client in self.list:
                    self.list.remove(self.client)
                    print("connection closed by {}".format(self.ip))
                    print("client {} has being remove".format(self.ip))
                    self.conn.close()
                    pass
                    
def client_handling(socks):
     while True:
          conn , addr = socks.accept()
          print("connnection established by {}".format(addr))
          try:
               client = threadforclient(conn,addr).start()
               continue
          except ConnectionResetError:
               print("closing connection of host {}".format(addr))
               conn.close()
               continue


def sock_server(port):
     socks = sock()
     socks.bind(("",port))
     socks.listen(5)
     print("waiting for connection on port {}".format(port))
     client_handling(socks)

sock_server(8080)
