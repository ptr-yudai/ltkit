import wx
from ltkit.network import server

class ServerFrame(wx.Frame):
    """ Main program. (Server)
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
        # Creates server
        self.server = server.Network("127.0.0.1", 8001)
        # Shows this frame
        self.Center()
        self.Show()

def main():
    # Initializes a new application
    server_application = wx.App()
    # Creates the frame
    ServerFrame()
    # Main loop
    server_application.MainLoop()
    return

if __name__ == "__main__":
    main()
