# coding: utf-8
import wx
from ltkit import mod_viewer

def main():
    ltkit = wx.App(False)
    message_viewer = mod_viewer.MessageViewer()

    # debug data
    message = {"message":"チョコはおいしい(哲学)",
               "position":(wx.DisplaySize()[0], 0),
               "size":96,
               "color":(255, 255, 255),
               "speed":3}
    message_viewer.display_message(message)

    message = {"message":"This is a sample message!",
               "position":(wx.DisplaySize()[0], 0),
               "size":32,
               "color":(255, 0, 0),
               "speed":5}
    message_viewer.display_message(message)
    
    ltkit.MainLoop()
    return

if __name__ == '__main__':
    main()

