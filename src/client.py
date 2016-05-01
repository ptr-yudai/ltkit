import wx
from ltkit.network import client
from ltkit.panel.client import post
from ltkit.panel.client import questionary

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
        # Internetworking Module
        self.inet = client.Network(self)
        # Create a new tab control
        self.tab_control = wx.Notebook(self,
                                       id = wx.ID_ANY,
                                       style = wx.NB_TOP,
                                       size = self.GetSize())
        self.panel_post = post.Panel(self.tab_control, self.inet)
        self.panel_questionary = questionary.Panel(self.tab_control)
        self.tab_control.AddPage(self.panel_post, "Post")
        self.tab_control.AddPage(self.panel_questionary, "Questionary")
        # Show this frame
        self.Center()
        self.Show()

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
