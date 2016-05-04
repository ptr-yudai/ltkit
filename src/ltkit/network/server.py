import threading
import wx
from ..module import message

class Network:
    def __init__(self, parent):
        """ Initialize Network class """
        # Inherit
        self.server = parent
        # Messanger
        self.message_viewer = message.MessageViewer(parent)
        return

    def __del__(self):
        # Kill thread
        self.thread_stop.set()
        self.thread.join()
        return
    

    def post_message(self, event):
        """ Post a message to all the clients """
        import packet
        panel_post = self.server.panel_post
        # Create a message structure
        message = {
            "type": "message",
            "message": panel_post.text_message.GetValue(),
            "size": int(panel_post.spin_size.GetValue()),
            "color": panel_post.message_color,
            "date": wx.DateTime.Now().Format("%H:%M:%S"),
            "id": "<master>"
        }
        # Check if the message is empty
        if message['message'] == "":
            return
        # Post the message
        self.broadcast(packet.compress(message))
        # Append the message onto the listview
        wx.CallAfter(panel_post.append_message, message)
        # Dispay the message (avoid assertionerror)
        wx.CallAfter(self.display_message, message)
        # Clear text control
        panel_post.text_message.Clear()
        return

    def create_socket(self, event):
        """ Listen to the clients """
        panel_post = self.server.panel_post
        # Get the hostname
        self.host = panel_post.text_ip.GetValue()
        # Get the port number
        try:
            self.port = int(panel_post.text_port.GetValue())
        except ValueError:
            wx.MessageBox(u"The port number is invalid.\nOnly numeric characters can be used.",
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Disable 'standby' button
        panel_post.button_standby.Disable()
        # Start new thread
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target = self.establish)
        self.thread.setDaemon(True)
        self.thread.start()
        # Enable 'standby' button
        panel_post.button_standby.SetLabel(u"Stop")
        panel_post.button_standby.Bind(wx.EVT_BUTTON, self.destroy_socket)
        panel_post.button_standby.Enable()
        return

    def destroy_socket(self, event):
        """ Stop listening """
        panel_post = self.server.panel_post
        # Disable 'disconnect' button
        panel_post.button_standby.Disable()
        # Kill thread
        self.thread_stop.set()
        self.thread.join()
        # Enable 'connect' button
        panel_post.button_standby.SetLabel(u"Standby")
        panel_post.button_standby.Bind(wx.EVT_BUTTON, self.create_socket)
        panel_post.button_standby.Enable()
        return

    def establish(self):
        import select
        import socket
        import packet
        """ Establish a server and run it forever """
        self.socket_list = []
        self.id_list = {}
        # Open the port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.host, self.port))
        except:
            # Failed to open the port
            wx.MessageBox(u"Failed to open the port {0}.\nPlease make sure that the port is not in use now.".format(self.port),
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        self.server_socket.listen(10)
        self.socket_list.append(self.server_socket)
        # Listen
        while True:
            read_sockets, wrote_sockets, error_sockets = select.select(self.socket_list, [], [], 1)
            # Process
            for socket in read_sockets:
                if socket == self.server_socket:
                    # New audience
                    socket_fd, address = self.server_socket.accept()
                    self.socket_list.append(socket_fd)
                    self.id_list[socket_fd] = self.calculate_id()
                else:
                    try:
                        # Receive message
                        recv_data = packet.decompress(socket.recv(4096))
                        # Process the message
                        self.proc_message(socket, recv_data)
                    except:
                        # Connection refused
                        socket.close()
                        self.socket_list.remove(socket)
            # Check the thread is killed
            if self.thread_stop.is_set():
                for socket in self.socket_list:
                    socket.close()
                break
            # Clear
            read_sockets = wrote_sockets = error_sockets = []
        return

    def proc_message(self, socket, recv_data):
        """ Process received message """
        import packet
        panel_post = self.server.panel_post
        # Check type
        if recv_data.get(u'type', None) == None:
            return
        # Append some data
        if recv_data[u'type'] == "message":
            # Create message structure
            if self.id_list.get(socket, None) == None:
                recv_data[u'id'] = u"<unknown>"
            else:
                recv_data[u'id'] = self.id_list[socket]
            recv_data[u'date'] = wx.DateTime.Now().Format("%H:%M:%S")
            # Send to all client
            self.broadcast(packet.compress(recv_data))
            # Append the message onto the listview
            wx.CallAfter(panel_post.append_message, recv_data)
            # Dispay the message (avoid assertionerror)
            wx.CallAfter(self.display_message, recv_data)
        else:
            # Invalid
            return
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
    
    def calculate_id(self):
        """ Calculate ID """
        import string
        import random
        return "".join([random.choice(string.ascii_letters + string.digits) for i in range(8)])

    def display_message(self, recv_data):
        """ Display a message on the desktop screen (with using the MessageViewer class)"""
        self.message_viewer.display_message(recv_data)
        return
