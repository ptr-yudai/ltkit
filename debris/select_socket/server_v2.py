import SocketServer
import socket
import threading
import wx

class ServerHandler(SocketServer.BaseRequestHandler, object):
    def handle(self):
#        address = self.client_address[0]
        self.request.send("Your name > ")
        name = self.request.recv(4096).strip()
        self.request.send("Welcome {0}.\n".format(name))
        return

class Server(SocketServer.ThreadingTCPServer, object):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        return

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
        self.thread = threading.Thread(target = self.connect)
        self.thread.start()
        # Shows this frame
        self.Center()
        self.Show()

    def connect(self):
        server = Server(("127.0.0.1", 8001), ServerHandler)
        server.serve_forever()
        return

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
