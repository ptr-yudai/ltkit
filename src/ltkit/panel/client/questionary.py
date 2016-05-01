import wx

class Panel(wx.Panel):
    """ Creates a panel of the questionary
    This class is a panel which has all functions for the questionaries.
    """
    def __init__(self, parent):
        """ Initializes Panel """
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
        # text = "No questionary"
        label = wx.StaticText(self,
                              id = wx.ID_ANY,
                              label = u"No questionary.")
        label.SetFont(DEFAULT_FONT)
        self.layout[0].Add(label,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
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
