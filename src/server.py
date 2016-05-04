import wx
from ltkit.network import server
from ltkit.panel.server import post
from ltkit.panel.server import questionnaire

class ServerFrame(wx.Frame):
    """ Main program. (Server)
    This class includes the main code.
    """

    def __init__(self):
        """ Initializes a new frame """
        # Create a new frame
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
        #self.Bind(wx.EVT_CLOSE, self.on_exit)
        # Create server
        self.inet = server.Network(self)
        # Create a new tab control
        self.tab_control = wx.Notebook(self,
                                       id = wx.ID_ANY,
                                       style = wx.NB_TOP,
                                       size = self.GetSize())
        self.panel_post = post.Panel(self.tab_control, self.inet)
        self.panel_questionnaire = questionnaire.Panel(self.tab_control, self.inet)
        self.tab_control.AddPage(self.panel_post, "Post")
        self.tab_control.AddPage(self.panel_questionnaire, "Questionnaire")
        # Show this frame
        self.Center()
        self.Show()

    def __del__(self):
        """ Destoructor """
        self.server.running = False
        return

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
