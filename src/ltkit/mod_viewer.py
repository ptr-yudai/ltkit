# coding: utf-8
import wx
import mod_screenshot

class MessageViewer:
    """displays received text on the screen.
    This class is used to display a text on a screen.
    A shaped window is used to make a message window.
    
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
            # new Screenshot class
            self.screenshot = mod_screenshot.Screenshot()
            # new visible frame (message)
            self.frame = wx.Frame(None,
                                  wx.ID_ANY,
                                  message_struct["message"],
                                  style = wx.FRAME_SHAPED | wx.NO_BORDER | wx.CLOSE_BOX )
            # creates message bitmap
            self.message_bitmap = self.create_bitmap_message(message_struct)
            self.OnCreate("")
            # calculates window size
            self.frame.SetPosition(message_struct["position"])
            self.frame.SetClientSize(self.message_bitmap.GetSize())
            # sets shape
            self.create_shape()
            self.frame.Bind(wx.EVT_PAINT, self.OnPaint)
            self.frame.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
            # shows this frame
            self.frame.Show(True)
            return None

        def OnPaint(self, obj):
            """on paint"""
            dc = wx.PaintDC(self.frame)
            dc.DrawBitmap(self.message_bitmap, 0, 0, True)
            return None

        def OnCreate(self, obj):
            """on create"""
            self.frame.SetShape(wx.RegionFromBitmap(self.message_bitmap))
            return None

        def create_shape(self):
            dc = wx.ClientDC(self.frame)
            dc.DrawBitmap(self.message_bitmap, 0, 0, True)
            self.frame.SetShape(wx.RegionFromBitmap(self.message_bitmap))
            return None

        def create_bitmap_message(self, message_struct):
            """creates bitmap of the message"""
            mask_color = (255, 255, 255)
            print mask_color
            # new font
            font = wx.Font(message_struct["size"],
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
            # calculates message width and height
            dc = wx.MemoryDC()
            dc.SetFont(font)
            size = dc.GetTextExtent(message_struct['message'])
            # new bitmap
            bitmap = wx.EmptyBitmap(size[0], size[1])
            # draws text for shaping
            dc.SelectObject(bitmap)
            dc.Clear()
            dc.SetTextForeground(message_struct['color'])
            #dc.SetAntialiasMode(wx.ANTIALIAS_NONE)
            dc.DrawText(message_struct['message'], 0, 0)
            del dc
            # sets mask
            image = bitmap.ConvertToImage()
            image.SetMaskColour(255, 255, 255)
            image.SetMask(True)
            bitmap = image.ConvertToBitmap()
            return bitmap
