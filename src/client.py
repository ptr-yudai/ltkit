import wx
from ltkit import panel_audience

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
                          | wx.MAXIMIZE_BOX
                          | wx.CLOSE_BOX
                          | wx.SYSTEM_MENU
                          | wx.CAPTION
                          | wx.RESIZE_BORDER
                          | wx.CLIP_CHILDREN,
                          size = (640, 480))
        self.SetMinSize((640, 480))
        # Creates a new tab control
        self.tab_control = wx.Notebook(self,
                                       id = wx.ID_ANY,
                                       style = wx.NB_TOP,
                                       size = self.GetSize())
        page1 = panel_audience.PanelAudience(self.tab_control)
        page3 = ClientFrame.HistoryPanel(self.tab_control)
        self.tab_control.AddPage(page1, "Audience")
        self.tab_control.AddPage(page3, "History")
        # Shows this frame
        self.Center()
        self.Show()

    

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
