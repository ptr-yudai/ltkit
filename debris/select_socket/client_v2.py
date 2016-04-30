import socket
import threading
import wx

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,
                          None,
                          id = wx.ID_ANY,
                          title = u"Sample",
                          style = wx.MINIMIZE_BOX
                          | wx.CLOSE_BOX
                          | wx.SYSTEM_MENU
                          | wx.CAPTION
                          | wx.CLIP_CHILDREN,
                          size = (640, 480))
        # Socket
        self.thread = threading.Thread(target = self.connect)
        self.thread.start()
        # Shows this frame
        self.Center()
        self.Show()

    def connect(self):
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect(("127.0.0.1", 8001))
        print(socket_client.recv(4096))
        socket_client.send("hoge")
        print(socket_client.recv(4096))
        socket_client.close()
        return

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
