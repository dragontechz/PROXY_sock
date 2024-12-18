#coding:utf-8

import socket
import ssl
import threading

class Proxy:
    def __init__(self, address, dst_address):
        self.address = address
        self.dst_address = dst_address
    def start(self):
        try:
            threading.Thread(target=self.server_http).start()
        except Exception as e:
            print(f"couldn't start because of exception {e}")
                
    def server_http(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()
            print(f"HTTP Server listening on {self.address} redirect to -> {self.dst_address}")
            while True:
                client_conn, addr = sock.accept()
                print(f"Accepted HTTP connection from {addr}")
                threading.Thread(target=self.handler, args=(client_conn, False)).start()
    def handler(self, client_conn, tls_client):
        try:
            client_conn.sendall(b"HTTP/1.1 200 ok\r\n\r\n")
            # Connect to the destination serve
            with socket.create_connection(self.dst_address) as ssh_conn:
                 # Start bi-directional stream copying
                threading.Thread(target=self.copy_streams, args=(ssh_conn, client_conn)).start()
                threading.Thread(target=self.copy_streams, args=(client_conn, ssh_conn)).start()
                
        except Exception as e:
            print(f"Error in handler: {e}")
        finally:
            client_conn.close()
            
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
    # Exemple d'utilisation
    proxy = Proxy(
        address=('127.0.0.1', 8080),
        dst_address=('127.0.0.1', 22),)
    proxy.start()