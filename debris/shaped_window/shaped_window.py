#
# creates a shaped window
#
import wx

def OnCreate(self):
    global frame
    global bmp
    reg = wx.RegionFromBitmap(bmp)
    frame.SetShape(reg)
    print(frame)
    return

def OnPaint(self):
    global frame
    global bmp
    dc = wx.PaintDC(frame)
    dc.DrawBitmap(bmp, 0, 0, True)
    return

app = wx.App()

frame = wx.Frame(None, wx.ID_ANY, "Shaped Window",
                 style = wx.FRAME_SHAPED | wx.NO_BORDER | wx.CLOSE_BOX)
img = wx.Image("./faceman.png", wx.BITMAP_TYPE_PNG)
img.SetMaskColour(255, 255, 255)
img.SetMask(True)
bmp = wx.BitmapFromImage(img)

frame.SetClientSize((bmp.GetWidth(), bmp.GetHeight()))
dc = wx.ClientDC(frame)
dc.DrawBitmap(bmp, 0, 0, True)
reg = wx.RegionFromBitmap(bmp)
frame.SetShape(reg)

frame.Bind(wx.EVT_PAINT, OnPaint)
frame.Bind(wx.EVT_WINDOW_CREATE, OnCreate)

frame.Show(True)

app.MainLoop()

