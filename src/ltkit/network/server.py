import SocketServer
import socket
import threading
import wx
import packet

class Handler(SocketServer.BaseRequestHandler, object):
    def handle(self):
        print("HERE I AM!")
        recv_data = self.request.recv(4096)
        print(packet.decompress(recv_data))
        return

class Server(SocketServer.ThreadingTCPServer, object):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        return

class Network:
    def __init__(self, host, port):
        """ Initializes Network class """
        self.host = host
        self.port = port
        self.thread = threading.Thread(target = self.establish)
        self.thread.start()
        return

    def establish(self):
        """ Establish a server and run it forever """
        self.server = Server((self.host, self.port), Handler)
        self.server.serve_forever()
        return