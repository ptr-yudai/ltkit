import wx

class ClientFrame(wx.Frame):
    """ Main program. (Client)
    This class includes the main code.
    """

    def __init__(self):
        """ Initializes a new frame """
        # Creates a new frame
        wx.Frame.__init__(self,
                          None,
                          id = wx.ID_ANY,
                          title = u"LT Toolkit",
                          style = wx.MINIMIZE_BOX
                          | wx.CLOSE_BOX
                          | wx.SYSTEM_MENU
                          | wx.CAPTION
                          | wx.CLIP_CHILDREN,
                          size = (640, 480))
        # Creates a new tab control
        self.tab_control = wx.Notebook(self,
                                       id = wx.ID_ANY,
                                       style = wx.NB_TOP,
                                       size = self.GetSize())
        page1 = ClientFrame.ListenPanel(self.tab_control)
        page3 = ClientFrame.HistoryPanel(self.tab_control)
        self.tab_control.AddPage(page1, "Audience")
        self.tab_control.AddPage(page3, "History")
        # Shows this frame
        self.Center()
        self.Show()

    class ListenPanel(wx.Panel):
        """ Creates a panel of the audience
        This class is a panel which has all functions for the audience.
        """
        def __init__(self, parent):
            """Initializes ListenPanel class"""
            # variable
            self.message_color = (240, 240, 240)
            # new panel
            wx.Panel.__init__(self,
                              parent)
            # new font
            DEFAULT_FONT = wx.Font(12,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
            # Creates sizer
            layout_main = wx.BoxSizer(wx.VERTICAL)
            layout = []
            for i in range(3):
                layout.append(wx.BoxSizer(wx.HORIZONTAL))
            # text = "Connect to:"
            label = wx.StaticText(self,
                                  id = wx.ID_ANY,
                                  label = u"Connect to ",)
            label.SetFont(DEFAULT_FONT)
            layout[0].Add(label,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 8)
            # Creates a text control to enter the hostname into
            self.text_ip = wx.TextCtrl(self,
                                       id = wx.ID_ANY,
                                       value = u"127.0.0.1",
                                       size = (256, 32))
            self.text_ip.SetFont(DEFAULT_FONT)
            layout[0].Add(self.text_ip,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 0)
            # text = "with port"
            label = wx.StaticText(self,
                                  id = wx.ID_ANY,
                                  label = u"with port")
            label.SetFont(DEFAULT_FONT)
            layout[0].Add(label,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 8)
            # Creates a text control to enter the port number into
            self.text_port = wx.TextCtrl(self,
                                         id = wx.ID_ANY,
                                         value = u"8080",
                                         size = (64, 32))
            self.text_port.SetFont(DEFAULT_FONT)
            layout[0].Add(self.text_port,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 0)
            # Creates a list control to display the history on
            self.list_history = wx.ListCtrl(self,
                                            id = wx.ID_ANY,
                                            style = wx.LC_REPORT | wx.SUNKEN_BORDER,
                                            size = (-1, -1))
            self.list_history.Show(True)
            self.list_history.InsertColumn(0, u"Message")
            self.list_history.InsertColumn(1, u"Date")
            self.list_history.InsertColumn(2, u"ID")
            layout[1].Add(self.list_history,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 0)
            # Creates a button to configure the comment color
            self.button_color = wx.Button(self,
                                          id = wx.ID_ANY,
                                          label = u"COLOR",
                                          size = (64, 32))
            self.button_color.SetForegroundColour(self.message_color)
            self.button_color.SetToolTipString(u"message color")
            self.button_color.Bind(wx.EVT_BUTTON, self.configure_color)
            layout[2].Add(self.button_color,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 0)
            # Creates a text control to enter the message into
            self.text_message = wx.TextCtrl(self,
                                            id = wx.ID_ANY,
                                            size = (256, 32))
            self.text_message.SetFont(DEFAULT_FONT)
            self.text_message.SetToolTipString("message")
            layout[2].Add(self.text_message,
                          flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                          border = 0)
            # Sets sizer
            layout_main.Add(layout[0])
            layout_main.Add(layout[1])
            layout_main.Add(layout[2])
            self.SetSizer(layout_main)
            return

        def configure_color(self, event):
            """ Asks the message color """
            data = wx.ColourData()
            dialog = wx.ColourDialog(None)
            dialog.GetColourData().SetChooseFull(True)
            dialog.GetColourData().SetColour(wx.Colour(self.message_color[0],
                                                       self.message_color[1],
                                                       self.message_color[2]))
            if dialog.ShowModal() == wx.ID_OK:
                data = dialog.GetColourData()
                self.message_color = data.GetColour().Get()
                self.button_color.SetForegroundColour(self.message_color)
            dialog.Destroy()
            return

    class HistoryPanel(wx.Panel):
        """ Creates a panel of the message list
        This class is a panel of the message list on the tab control.
        """
        def __init__(self, parent):
            """Initializes HistoryPanel class"""
            wx.Panel.__init__(self, parent)
            return


def main():
    # Initializes a new application
    client_application = wx.App()
    # Creates the frame
    ClientFrame()
    # Main loop
    client_application.MainLoop()
    return

if __name__ == "__main__":
    main()
