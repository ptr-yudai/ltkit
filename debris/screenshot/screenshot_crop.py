#
# take a screenshot and crop it
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
img = bmp.ConvertToImage()
rect = (64, 128, 256, 512)
cropped = img.GetSubImage(rect)
bmp = cropped.ConvertToBitmap()
bmp.SaveFile("cropped_screenshot.png", wx.BITMAP_TYPE_PNG)

