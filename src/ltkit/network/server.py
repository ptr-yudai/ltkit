import multiprocessing
import wx
from ..module import message

class Network:
    def __init__(self, parent, host, port):
        """ Initialize Network class """
        self.host = host
        self.port = port
        # Thread
        self.thread = multiprocessing.Process(target = self.establish)
        self.thread.start()
        # Messanger
        self.message_viewer = message.MessageViewer(parent)
        return

    def __del__(self):
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
            # 
            for socket in read_sockets:
                if socket == self.server_socket:
                    # New audience
                    socket_fd, address = self.server_socket.accept()
                    self.socket_list.append(socket_fd)
                else:
                    try:
                        # Receive message
                        recv_data = packet.decompress(socket.recv(4096))
                        # Process the message
                        self.proc_message(recv_data)
                    except:
                        # Connection refused
                        socket.close()
                        self.socket_list.remove(socket)
        return

    def proc_message(self, recv_data):
        import packet
        """ Process received message """
        # Check type
        if recv_data.get(u'type', None) == None:
            return
        # Append some data
        if recv_data[u'type'] == "message":
            # Message
            recv_data[u'id'] = "unknown"
            recv_data[u'date'] = wx.DateTime.Now().Format("%H:%M:%S")
            self.broadcast(packet.compress(recv_data))
            # Dispay the message (avoid assertionerror)
            wx.CallAfter(self.display_message, recv_data)
        else:
            # Invalid
            return
        # [DEBUG] Print debug string
        return

    def broadcast(self, send_data):
        """ Broadcast message """
        # Check data
        if send_data == "":
            return
        # Broadcast
        for socket in self.socket_list:
            if socket != self.server_socket:
                try:
                    socket.send(send_data)
                except:
                    socket.close()
                    self.socket_list.remove(socket)
        return

    def display_message(self, recv_data):
        """ Display a message on the desktop screen (with using the MessageViewer class)"""
        self.message_viewer.display_message(recv_data)
        return
