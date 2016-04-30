import socket
import wx

class Network:
    """ Networking System. (Server)
    This class is used for any kind of connection from client.
    """
    def __init__(self, client):
        # Inherit
        self.client = client
        # Socket
        self.socket = None
        return

    def create_socket(self, event):
        """ Connects to the server """
        panel_post = self.client.panel_post
        # Gets the hostname
        host = panel_post.text_ip.GetValue()
        # Gets the port number
        try:
            port = int(panel_post.text_port.GetValue())
        except ValueError:
            wx.MessageBox("The port number is invalid.\nOnly numeric characters can be used.",
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Disables 'connect' button
        panel_post.button_connect.Disable()
        # Creates new socket
        if self.socket != None:
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10.0) # timeout
        # Tries to connect to the host
        try:
            self.socket.connect((host, port))
        except socket.timeout:
            # Timeout
            wx.MessageBox("The connection to {0}:{1} has timed out.\nPlease make sure that the hostname and the port number you entered is correct and try again.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.socket = None
            # Enables 'connect' button
            panel_post.button_connect.Enable()
            return
        except:
            # Failed to connect
            wx.MessageBox("Failed to connect to {0}:{1}.\nPlease make sure that the hostname and the port number you entered is correct.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.socket = None
            # Enables 'connect' button
            panel_post.button_connect.Enable()
            return
        self.socket.close()
        # Enables 'connect' button
        panel_post.button_connect.Enable()
        return
    
    def destroy_socket(self):
        return
