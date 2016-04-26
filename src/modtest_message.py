# coding: utf-8
import wx
from ltkit import mod_viewer

def main():
    ltkit = wx.App(False)
    message_viewer = mod_viewer.MessageViewer(ltkit)

    # debug data
    message = {"message":"This is a sample message...!",
               "position":(wx.DisplaySize()[0], 0),
               "size":48,
               "color":(255, 0, 255),
               "speed":5}
    message_viewer.display_text(message)
    """
    message = {"message":"Are you sure?",
               "position":(wx.DisplaySize()[0], 0),
               "size":32,
               "color":(255, 0, 0),
               "speed":50}
    message_viewer.display_text(message)
    """
    ltkit.MainLoop()
    return

if __name__ == '__main__':
    main()

