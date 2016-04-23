# coding: utf-8

#
# creating a window which has the smallest size to display the text
#

text = "Hello, World!"
text = "こんにちは世界！"

import wx

app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, text, style=wx.CLOSE_BOX)
panel = wx.Panel(frame, wx.ID_ANY)
message = wx.StaticText(panel, wx.ID_ANY, text, (8, 8))
font = wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
message.SetFont(font)
dc = wx.ScreenDC()
dc.SetFont(font)
size = dc.GetTextExtent(text)
frame.SetSize(size)
frame.Show(True)
app.MainLoop()
