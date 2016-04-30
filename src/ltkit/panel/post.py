import select
import socket
import wx

class Panel(wx.Panel):
    """ Creates a panel of the audience
    This class is a panel which has all functions for the audience.
    """
    def __init__(self, parent):
        """Initializes ListenPanel class"""
        # Inits variables
        self.message_color = (240, 240, 240)
        self.socket = None
        # new panel
        wx.Panel.__init__(self,
                          parent)
        # new font
        DEFAULT_FONT = wx.Font(12,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL)
        # Creates sizer
        self.layout_main = wx.BoxSizer(wx.VERTICAL)
        self.layout = []
        for i in range(3):
            self.layout.append(wx.BoxSizer(wx.HORIZONTAL))
        # Creates a button to create a soket
        self.button_connect = wx.Button(self,
                                        id = wx.ID_ANY,
                                        label = u"Connect",
                                        size = (96, 32))
        self.button_connect.SetFont(DEFAULT_FONT)
        self.button_connect.Bind(wx.EVT_BUTTON, self.connect)
        self.layout[0].Add(self.button_connect,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # text = "to"
        label = wx.StaticText(self,
                              id = wx.ID_ANY,
                              label = u"to")
        label.SetFont(DEFAULT_FONT)
        self.layout[0].Add(label,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Creates a text control to enter the hostname into
        self.text_ip = wx.TextCtrl(self,
                                   id = wx.ID_ANY,
                                   value = u"127.0.0.1",
                                   size = (256, 32))
        self.text_ip.SetFont(DEFAULT_FONT)
        self.text_ip.SetToolTipString(u"Hostname or IP address")
        self.layout[0].Add(self.text_ip,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # text = "through port"
        label = wx.StaticText(self,
                              id = wx.ID_ANY,
                              label = u"through port")
        label.SetFont(DEFAULT_FONT)
        self.layout[0].Add(label,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Creates a text control to enter the port number into
        self.text_port = wx.TextCtrl(self,
                                     id = wx.ID_ANY,
                                     value = u"8080",
                                     size = (64, 32))
        self.text_port.SetFont(DEFAULT_FONT)
        self.text_port.SetToolTipString(u"Port number")
        self.layout[0].Add(self.text_port,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Creates a list control to display the history on
        self.list_history = wx.ListCtrl(self,
                                        id = wx.ID_ANY,
                                        style = wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list_history.Show(True)
        self.list_history.InsertColumn(0, u"Message", width = 320)
        self.list_history.InsertColumn(1, u"Date", width = 196)
        self.list_history.InsertColumn(2, u"ID")
        self.layout[1].Add(self.list_history,
                           proportion = 1,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Creates a button to configure the message color
        self.button_color = wx.Button(self,
                                      id = wx.ID_ANY,
                                      label = u"COLOR",
                                      size = (64, 32))
        self.button_color.SetBackgroundColour(self.message_color)
        self.button_color.SetForegroundColour(self.message_color)
        self.button_color.SetToolTipString(u"Message color")
        self.button_color.Bind(wx.EVT_BUTTON, self.configure_color)
        self.layout[2].Add(self.button_color,
                           flag = wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Creates a button to configure the character size
        self.button_size = wx.SpinCtrl(self,
                                       id = wx.ID_ANY,
                                       size = (64, 32),
                                       min = 8, max = 32, initial = 16)
        self.button_size.SetToolTipString(u"Message size")
        self.layout[2].Add(self.button_size,
                           flag = wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Creates a text control to enter the message into
        self.text_message = wx.TextCtrl(self,
                                        id = wx.ID_ANY,
                                        style = wx.TE_PROCESS_ENTER,
                                        size = (320, 32))
        self.text_message.Bind(wx.EVT_TEXT_ENTER, self.post_message)
        self.text_message.SetFont(DEFAULT_FONT)
        self.text_message.SetMaxLength(60)
        self.text_message.SetToolTipString("Message")
        self.layout[2].Add(self.text_message,
                           proportion = 1,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Creates a button to post a message
        self.button_send = wx.Button(self,
                                     id = wx.ID_ANY,
                                     label = u"Post",
                                     size = (64, 32))
        self.button_send.SetFont(DEFAULT_FONT)
        self.button_send.Bind(wx.EVT_BUTTON, self.post_message)
        self.layout[2].Add(self.button_send,
                           flag = wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Sets sizer
        self.layout_main.Add(self.layout[0], flag = wx.ALIGN_TOP)
        self.layout_main.Add(self.layout[1],
                             proportion = 1,
                             flag = wx.EXPAND | wx.ALIGN_CENTER)
        self.layout_main.Add(self.layout[2], flag = wx.ALIGN_BOTTOM)
        self.SetSizer(self.layout_main)
        return
        
    def configure_color(self, event):
        """ Asks the message color """
        # Creates a new color dialog
        dialog = wx.ColourDialog(None)
        dialog.GetColourData().SetChooseFull(True)
        dialog.GetColourData().SetColour(wx.Colour(self.message_color[0],
                                                   self.message_color[1],
                                                   self.message_color[2]))
        # Asks the message color
        if dialog.ShowModal() == wx.ID_OK:
            # Reflects the new color
            data = dialog.GetColourData()
            self.message_color = data.GetColour().Get()
            self.button_color.SetBackgroundColour(self.message_color)
            self.button_color.SetForegroundColour(self.message_color)
        dialog.Destroy()
        return

    def connect(self, event):
        """ Connects to the server """
        print(event)
        # Gets the hostname
        host = self.text_ip.GetValue()
        # Gets the port number
        try:
            port = int(self.text_port.GetValue())
        except ValueError:
            wx.MessageBox("The port number is invalid.\nOnly numeric characters can be used.",
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Disables 'connect' button
        self.button_connect.Disable()
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
            wx.MessageBox("Timeout!",
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.socket = None
            # Enables 'connect' button
            self.button_connect.Enable()
            return
        except:
            # Failed to connect
            wx.MessageBox("Failed to connect to {0}:{1}.\nPlease make sure that the hostname and the port number you entered is correct.".format(host, port),
                          "LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            self.socket = None
            # Enables 'connect' button
            self.button_connect.Enable()
            return
        self.socket.close()
        # Enables 'connect' button
        self.button_connect.Enable()
        return
    
    def post_message(self, event):
        self.text_message.Clear()
        return
