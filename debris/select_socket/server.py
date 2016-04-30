import select
import socket
import threading
import wx
import wx.lib.pubsub

class IPCThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', 8001))
        self.socket.listen(5)
        self.setDaemon(True)
        self.start()
        return
        
    def run(self):
        while True:
            try:
                client, addr = self.socket.accept()
                ready = select.select([client], [], [], 2)
                if ready[0]:
                    received = client.recv(4096)
                    wx.CallAfter(wx.lib.pubsub.Publisher().sendMessage,
                                 "update",
                                 received)
            except:
                break
        # Quit
        try:
            self.socket.shutdown(socket.SHUT_DOWN)
        except:
            pass
        self.socket.close()
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
        panel = wx.Panel(self)
        self.ipc = IPCThread()
        
        wx.lib.pubsub.Publisher().subscribe(self.updateDisplay, "update")
        # Shows this frame
        self.Center()
        self.Show()

    def updateDisplay(self, msg):
        print msg.data


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
