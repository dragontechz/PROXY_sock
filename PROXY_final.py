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
buffer = 1024

i = '127.0.0.1'
def sock():
     sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     return sock

class threadforclient(threading.Thread):
     def __init__(self,conn,addr):
          threading.Thread.__init__(self)
          self.conn = conn
          self.ip,self.port = addr

     def run(self):
          self.conn.send(RESPONSE)
          self.conn.recv(buffer)
          conn_to_ssh = sock().connect(('127.0.0.1',22))
          try:
                    print("client {} has bieng added".format(self.ip))
                    while self.conn:
                         if conn_to_ssh:
                              data = self.conn.recv(buffer)
                              print(f'client sent :{data}')
                              conn_to_ssh.send(data)
                              response = conn_to_ssh.recv(buffer)
                              print(f'server responded by {response}')
                              self.conn.send(response)
                              continue

                         else:
                              try:
                                   conn_to_ssh = sock().connect(('127.0.0.1',22))
                                   continue
                              except Exception as e:
                                   print(e)
                                   self.conn.close()

          except ConnectionResetError:
               if conn_to_ssh:
                    conn_to_ssh.close()
                    self.conn.close()
               self.conn.close
                    
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
