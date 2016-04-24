# coding: utf-8
import wx

class MessageViewer:
    """displays received text on the screen.
    This class is for displaying a text on a screen.
    A hollowed window (like a window region in Windows)
    is used to display a text.
    
    Attributes:
        parent_frame ... main invisible frame
        text_frames .... a list of message windows
    """
    def __init__(self, app):
        """initializes MessageViewer"""
        # new invisible frame (parent)
        self.parent_frame = wx.Frame(None, wx.ID_ANY, u"ltkit")
        # a list of message windows
        self.text_frames = []
        ### [DEBUG] SHOWS WINDOW FOR DEBUGGING
        self.parent_frame.Show(True)
        return None

    def __del__(self):
        """deletes MessageViewer"""
        print("[DEBUG] MessageViewer is deleted.")
        return None

    def display_text(self, message_struct):
        """creates new comment window"""
        # append new comment window to text_frames
        self.text_frames.append(
            MessageViewer.MessageWindow(message_struct)
        )
        return None

    class MessageWindow:
        """manages each window.
        This class is used in CommentViewer.
        
        Attributes:
            frame ... a window frame which has a message on
            panel ... a panel to put a message on
        """
        def __init__(self, message_struct):
            """initializes MessageWindow"""
            # new visible frame (message)
            self.frame = wx.Frame(None,
                                  wx.ID_ANY,
                                  message_struct["message"],
                                  style=wx.CLOSE_BOX)
            # new font
            font = wx.Font(message_struct["size"],
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
            # new panel to put the message on
            self.panel = wx.Panel(self.frame,
                                  wx.ID_ANY)
            message = wx.StaticText(self.panel,
                                    wx.ID_ANY,
                                    message_struct["message"],
                                    (0, 0))
            message.SetForegroundColour(message_struct["color"])
            message.SetFont(font)
            # calculates window size
            dc = wx.ScreenDC()
            dc.SetFont(font)
            size = dc.GetTextExtent(message_struct["message"])
            self.frame.SetPosition(message_struct["position"])
            self.frame.SetSize(size)
            # shows this frame
            self.frame.Show(True)
            return None
