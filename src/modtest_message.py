# coding: utf-8
import wx
from ltkit import mod_viewer

def main():
    ltkit = wx.App(False)
    message_viewer = mod_viewer.MessageViewer(ltkit)

    # debug data
    message = {"message":"PythonでLTのやつ",
               "position":(0, 0),
               "size":48,
               "color":(255, 0, 0)}
    message_viewer.display_text(message)

    ltkit.MainLoop()
    return

if __name__ == '__main__':
    main()

