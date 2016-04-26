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
            # new panel
            wx.Panel.__init__(self,
                              parent)
            # new font
            DEFAULT_FONT = wx.Font(12,
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
            # Creates sizer
            layout_top = wx.BoxSizer(wx.HORIZONTAL)
            # text = "Connect to:"
            text_connect_to = wx.StaticText(self,
                                            id = wx.ID_ANY,
                                            label = u"Connect to ",
                                            style = wx.ALIGN_RIGHT,
                                            size = (96, -1))
            text_connect_to.SetFont(DEFAULT_FONT)
            # Creates an text control to enter the hostname into
            self.hostname = wx.TextCtrl(self,
                                        id = wx.ID_ANY,
                                        size = (256, 32))
            self.hostname.SetFont(DEFAULT_FONT)
            # Sets sizer
            layout_top.Add(text_connect_to)
            layout_top.Add(self.hostname)
            self.SetSizer(layout_top)
            return

    class HistoryPanel(wx.Panel):
        """ Creates a panel of the comment list
        This class is a panel of the comment list on the tab control.
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
