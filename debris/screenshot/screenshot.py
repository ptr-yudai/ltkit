#
# taking a screenshot
#

import wx

app = wx.App(False)

screen = wx.ScreenDC()
size = screen.GetSize()
bmp = wx.EmptyBitmap(size[0], size[1])
mem = wx.MemoryDCFromDC(screen)
mem.SelectObject(bmp)
mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
mem.SelectObject(wx.NullBitmap)
bmp.SaveFile("screenshot.png", wx.BITMAP_TYPE_PNG)
