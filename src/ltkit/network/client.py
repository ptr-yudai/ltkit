import socket
import packet
import wx

class Client:
    """ Networking System. (Server)
    This class is used for any kind of connection from client.
    """
    def __init__(self, client):
        # Inherit
        self.client = client
        # Socket
        self.socket = None
        return

    def post_message(self, event):
        """ Post a message to the server """
        panel_post = self.client.panel_post
        # Check if it's already connected
        if self.socket == None:
            wx.MessageBox(u"You are not connected to the host.\nPlease connect to the host first.",
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Create a message structure
        message = {
            "message": panel_post.text_message.GetValue(),
            "size": int(panel_post.spin_size.GetValue()),
            "color": panel_post.message_color
        }
        send_data = packet.compress(message)
        # Post the message
        print send_data
        self.socket.send(send_data)
        # Clear text control
        panel_post.text_message.Clear()
        return

    def create_socket(self, event):
        """ Connects to the server """
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
        if self.socket != None:
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10.0) # timeout
        # Try to connect to the host
        try:
            self.socket.connect((host, port))
        except socket.timeout:
            # Timeout
            wx.MessageBox("The connection to {0}:{1} has timed out.\nPlease make sure that the hostname and the port number you entered is correct and try again.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.socket = None
            # Enable 'connect' button
            panel_post.button_connect.Enable()
            return
        except:
            # Failed to connect
            wx.MessageBox("Failed to connect to {0}:{1}.\nPlease make sure that the hostname and the port number you entered is correct.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.socket = None
            # Enable 'connect' button
            panel_post.button_connect.Enable()
            return
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
        if self.socket != None:
            self.socket.close()
            self.socket = None
        # Enable 'connect' button
        panel_post.button_connect.SetLabel(u"Connect")
        panel_post.button_connect.Bind(wx.EVT_BUTTON, self.create_socket)
        panel_post.button_connect.Enable()
        return
