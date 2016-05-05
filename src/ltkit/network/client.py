import socket
import threading
import wx
import packet

class Network:
    """ Networking System. (Server)
    This class is used for any kind of connection from client.
    """
    def __init__(self, client):
        # Inherit
        self.client = client
        # Socket
        self.client_socket = None
        return

    def post_answer(self, event):
        """ Post an answer to the server """
        panel_questionnaire = self.client.panel_questionnaire
        # Check if it's already connected
        if self.client_socket == None:
            wx.MessageBox(u"You are not connected to the host.\nPlease connect to the host first.",
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Ask
        dialog = wx.MessageDialog(None,
                                  "Are you sure that you want to send your answer now?",
                                  "LT Toolkit",
                                  style = wx.YES_NO | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_NO:
            return
        # Get selected item
        checked = 0
        for (checked, obj) in enumerate(panel_questionnaire.radio_choice):
            if obj.GetValue() == True: break
        # Create a message structure
        message = {
            "type": "questionnaire",
            "choice": checked
        }
        # Compress the message
        send_data = packet.compress(message)
        # Post the message
        self.client_socket.send(send_data)
        # Display message
        wx.MessageBox("You answer was sent successfully.",
                      "LT Toolkit",
                      style = wx.OK | wx.ICON_INFORMATION)
        return

    def post_message(self, event):
        """ Post a message to the server """
        panel_post = self.client.panel_post
        # Check if it's already connected
        if self.client_socket == None:
            wx.MessageBox(u"You are not connected to the host.\nPlease connect to the host first.",
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Create a message structure
        message = {
            "type": "message",
            "message": panel_post.text_message.GetValue(),
            "size": int(panel_post.spin_size.GetValue()),
            "color": panel_post.message_color
        }
        # Check if the message is empty
        if message['message'] == "":
            return
        # Compress the message
        send_data = packet.compress(message)
        # Post the message
        self.client_socket.send(send_data)
        # Clear text control
        panel_post.text_message.Clear()
        return

    def listen(self):
        """ Receive data from the server """
        import select
        import socket
        import packet
        # Panel class of the post tab
        panel_post = self.client.panel_post
        # Receive
        while True:
            read_sockets, wrote_sockets, error_sockets = select.select([self.client_socket], [], [])
            # Receive new message
            try:
                recv_data = packet.decompress(self.client_socket.recv(4096))
            except:
                self.client_socket.close()
                break
            # Invalid message
            if recv_data == {}:
                break
            if recv_data.get(u'type', None) == None:
                continue
            # Process message depending on its type
            self.proc_message(recv_data)
        return

    def proc_message(self, recv_data):
        """ Process the received message """
        panel_post = self.client.panel_post
        panel_questionnaire = self.client.panel_questionnaire
        # Process
        if recv_data[u'type'] == u"message":
            # Insert the message into the listview (in order to avoid assertionerror)
            wx.CallAfter(panel_post.append_message, recv_data)
        elif recv_data[u'type'] == u"questionnaire":
            # Displays the new questionnaire
            wx.CallAfter(panel_questionnaire.display_questionnaire, recv_data)
        return

    def create_socket(self, event):
        """ Connect to the server """
        panel_post = self.client.panel_post
        # Get the hostname
        host = panel_post.text_ip.GetValue()
        # Get the port number
        try:
            port = int(panel_post.text_port.GetValue())
        except ValueError:
            wx.MessageBox(u"The port number is invalid.\nOnly numeric characters can be used.",
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Disable 'connect' button
        panel_post.button_connect.Disable()
        # Create new socket
        if self.client_socket != None:
            self.client_socket.close()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(10.0) # timeout
        # Try to connect to the host
        try:
            self.client_socket.connect((host, port))
        except socket.timeout:
            # Timeout
            wx.MessageBox("The connection to {0}:{1} has timed out.\nPlease make sure that the hostname and the port number you entered is correct and try again.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.client_socket = None
            # Enable 'connect' button
            panel_post.button_connect.Enable()
            return
        except:
            # Failed to connect
            wx.MessageBox("Failed to connect to {0}:{1}.\nPlease make sure that the hostname and the port number you entered is correct.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.client_socket = None
            # Enable 'connect' button
            panel_post.button_connect.Enable()
            return
        # Create listen thread
        self.thread_listen = threading.Thread(target = self.listen)
        self.thread_listen.setDaemon(True)
        self.thread_listen.start()
        # Enable 'connect' button
        panel_post.button_connect.SetLabel(u"Disconnect")
        panel_post.button_connect.Bind(wx.EVT_BUTTON, self.destroy_socket)
        panel_post.button_connect.Enable()
        return
    
    def destroy_socket(self, event):
        """ Disconnect from the server """
        panel_post = self.client.panel_post
        # Disable 'disconnect' button
        panel_post.button_connect.Disable()
        # Disconnect
        if self.client_socket != None:
            self.client_socket.close()
            self.client_socket = None
        # Enable 'connect' button
        panel_post.button_connect.SetLabel(u"Connect")
        panel_post.button_connect.Bind(wx.EVT_BUTTON, self.create_socket)
        panel_post.button_connect.Enable()
        return
