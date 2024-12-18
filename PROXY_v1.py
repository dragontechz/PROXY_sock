#coding:utf-8
import threading
import socket
import select

IP = ""
PORT = 9090
default_HOST = '0.0.0.0:22'
MSG = '@Dragontechz on telegram'
RESPONSE = b'HTTP:// 200 OK' + MSG.encode('utf-8')
buffer = 1024*1024

def handler(self, client_conn, tls_client):
        try:
            if tls_client and self.tls_mode == "stunnel":
                # Handle stunnel mode here (if needed)
                pass
            # Send handshake response
            client_conn.sendall(b"HTTP/1.1 200 OK \r\n\r\n")
            # Connect to the destination serve
            with socket.create_connection(self.dst_address) as ssh_conn:
                 # Start bi-directional stream copying
                threading.Thread(target=self.copy_streams, args=(ssh_conn, client_conn)).start()
                threading.Thread(target=self.copy_streams, args=(client_conn, ssh_conn)).start()
                
        except Exception as e:
            print(f"Error in handler: {e}")
        finally:
            client_conn.close()
            
def copy_streams(source, destination):
     try:
            while True:
                data = source.recv(2048)
                if not data:
                    break
                destination.sendall(data)
     except Exception as e:
            print(f"Error copying streams: {e}")
     finally:
            source.close()
            destination.close()


def findhost(payload):
     index = payload.find("Host:")
     if index != -1:
          debut = index + 5
          fin = payload.find("\r\n",debut)
          if fin != -1:
               host = payload[debut:fin].strip()
               return host
          return None

def sock():
     sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     return sock

def handle_data(data):
     if len(data.decode()) == -1:
          return None
     data = data.decode()
     print("handling request ...")
     host = findhost(data)
     if len(host) != -1:
          print("request on host : {}".format(host))
          sock2host = sock()
          try:
               if ":" in host:
                    host_dest , port = host.split(":")
                    print("connecting to {} on port : {}".format(host_dest,port))
                    
                    try:
                         sock2host.connect((host_dest,int(port)))
                         sock2host.send(data.encode('utf-8'))
                         response = sock2host.recv(buffer)
                         return response
                    
                    except socket.gaierror:
                         print("cann't connect to host: {}".format(host))
                         response = b'cannot connect to ' + host.encode('utf-8')
                         return response
                    
               else:
                    try:
                         sock2host.connect((host,80))
                         sock2host.send(data.encode('utf-8'))
                         response = sock2host.recv(buffer)
                         return response
                    except socket.gaierror:
                         print("cann't connect to host: {}".format(host))
                         response = b'cannot connect to ' + host.encode('utf-8')
                         return response

          except ConnectionRefusedError:
               return b'cannot connect to requested host'

     elif type(host) == None:
          return None
     
def handle_conn(conn):
     while True:
          data = conn.recv(buffer)
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
          self.dst_address = ('127.0.0.1',22)
          self.list =[]

     def run(self):
        try:
            # Send handshake response
            self.conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            # Connect to the destination serve
            with socket.create_connection(self.dst_address) as ssh_conn:
                 # Start bi-directional stream copying
                threading.Thread(target=copy_streams, args=(self.conn,ssh_conn)).start()
                threading.Thread(target=copy_streams, args=(ssh_conn,self.conn )).start()
                
        except Exception as e:
            print(f"Error in handler: {e}")
        finally:
            self.conn.close()
             
                    
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
