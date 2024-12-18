#coding:utf-8

import socket
import threading

def sock():
    sock1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return sock1
class server():
    def __init__(self,port):
        self.port = port
        self.host = ''
        self.ssh = ('localhost',22)
    def run(self):
        server_sock = sock()
        server_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server_sock.bind((self.host,self.port))
        server_sock.listen()
        print(f'listening on port {self.port} redirecting to {self.ssh}')
        while True:
            conn , addr = server_sock.accept()
            if conn:
                sock_ssh = sock()
                sock_ssh.connect(self.ssh)

                ip,_ = addr
                print(f'connection initialised by client , ip adress : {ip} forwarding traffic to {self.ssh}')
                conn.recv(1080)
                conn.sendall(b'HTTP/1.1 200 OK \r\n\r\n')
                threading.Thread(target=self.copy_streams, args=(sock_ssh, conn)).start()
                threading.Thread(target=self.copy_streams, args=(conn, sock_ssh)).start()
    def copy_streams(self, source, destination):
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
if __name__ == "__main__":
    server(8080).run()