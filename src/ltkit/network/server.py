import threading
import wx

class Network:
    def __init__(self, host, port):
        """ Initialize Network class """
        self.host = host
        self.port = port
        self.thread = threading.Thread(target = self.establish)
        self.thread.start()
        return

    def establish(self):
        import select
        import socket
        import packet
        """ Establish a server and run it forever """
        self.socket_list = []
        # Open the port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.socket_list.append(self.server_socket)
        # Listen
        while True:
            read_sockets, wrote_sockets, error_sockets = select.select(self.socket_list, [], [])
            for socket in read_sockets:
                if socket == self.server_socket:
                    # New audience
                    socket_fd, address = self.server_socket.accept()
                    self.socket_list.append(socket_fd)
                else:
                    try:
                        # Receive message
                        recv_data = packet.decompress(socket.recv(4096))
                        recv_data[u'id'] = "unknown"
                        recv_data[u'date'] = wx.DateTime.Now().Format("%H:%M:%S")
                        print(recv_data)
                        self.broadcast(packet.compress(recv_data))
                    except:
                        # Connection refused
                        socket.close()
                        self.socket_list.remove(socket)
        return

    def broadcast(self, send_data):
        """ Broadcast message """
        for socket in self.socket_list:
            if socket != self.server_socket:
                try:
                    socket.send(send_data)
                except:
                    socket.close()
                    self.socket_list.remove(socket)
        return
