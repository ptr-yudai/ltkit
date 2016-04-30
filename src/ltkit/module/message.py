# coding: utf-8
import wx

class MessageViewer(wx.Frame):
    """ Manages a message frame.

    This class is a window manager.
    Used to create several frames (messages) onto the desktop screen.
    
    Attributes:
        text_frames .... a list of message windows
    """
    
    def __init__(self):
        """ Initializes MessageViewer class """
        # Creates a new frame (main frame)
        wx.Frame.__init__(self,
                          None,
                          wx.ID_ANY,
                          u"ltkit",
                          size = (32, 32))
        ### DEBUG : Shows the main frame ###
        self.Show(True)
        return None

    def __del__(self):
        """ Destroys MessageViewer class """
        print("[DEBUG] MessageViewer is deleted.")
        return None

    def display_message(self, message):
        """ Creates new message window """
        # Creates a new message frame
        MessageViewer.MessageWindow(message)
        return None

    class MessageWindow(wx.Frame):
        """ Displays some messages onto the screen. (Interface)
        
        Each MessageWindow class has a message frame.
        Once a MessageWindow class is created, it will be managed by itself.
        
        Attributes:
            frame_pos : the position where the frame is right now
            frame_size : the size of the width and the height of the frame
            timer_move : a timer that is called when the frame needs to move
        """
        def __init__(self, message):
            """ Initializes MessageWindow """
            # Filter (Fixes message structure and blocks banned words.)
            self.filter_message(message)
            # new visible frame (message)
            wx.Frame.__init__(self,
                              None,
                              wx.ID_ANY,
                              message["message"],
                              style = wx.FRAME_SHAPED
                              | wx.NO_BORDER
                              | wx.CLOSE_BOX
                              | wx.STAY_ON_TOP
                              | wx.FRAME_NO_TASKBAR)
            # creates message bitmap
            self.message_bitmap = self.create_message_bitmap(message)
            self.OnCreate(None)
            # Sets a shape
            self.frame_pos = list(message["position"])
            self.create_shape()
            # Sets a new timer to move the frame itself
            self.timer_move = wx.Timer(self)
            self.Bind(wx.EVT_PAINT, self.OnPaint, id = wx.ID_ANY)
            self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
            self.Bind(wx.EVT_TIMER, self.OnTimer, id = wx.ID_ANY)
            # Starts the timer
            self.timer_move.Start(message['speed'])
            # Shows this frame
            self.Show(True)
            return None

        def OnTimer(self, event):
            """on timer"""
            # Moves the frame
            self.frame_pos[0] -= 1
            self.SetPosition((self.frame_pos[0], self.frame_pos[1]))
            if self.frame_pos[0] <= -self.frame_size[0]:
                # Kills the frame when it goes out of the screen
                self.timer_move.Stop()
                self.Destroy()
                del self
            return None

        def OnPaint(self, event):
            """on paint"""
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self.message_bitmap, 0, 0, True)
            return None

        def OnCreate(self, event):
            """on create"""
            self.SetShape(wx.RegionFromBitmap(self.message_bitmap))
            return None

        def create_shape(self):
            """ Creates a shaped window """
            # Sets the window position and size
            self.SetPosition(self.frame_pos)
            self.SetClientSize(tuple(self.frame_size))
            # Sets a new shape
            dc = wx.ClientDC(self)
            dc.DrawBitmap(self.message_bitmap, 0, 0, True)
            self.SetShape(wx.RegionFromBitmap(self.message_bitmap))
            return None

        def create_message_bitmap(self, message):
            """ Creates a bitmap data which has a masked image of the message """
            # Calculates the mask color
            mask_color = self.create_mask_color(message['color'])
            # Creates new font
            font = wx.Font(message['size'],
                           wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL)
            # Calculates the width and the height of the message
            dc = wx.MemoryDC()
            dc.SetFont(font)
            self.frame_size = list(dc.GetTextExtent(message['message']))
            self.frame_size[0] += message['size'] / 10 # adds
            self.frame_size[1] += message['size'] / 10 # shadow size
            # Expands frame size
            if self.frame_size[0] <= wx.DisplaySize()[0]:
                self.frame_size[0] = wx.DisplaySize()[0] + 1
            # Creates and selects a new bitmap
            bitmap = wx.EmptyBitmap(self.frame_size[0], self.frame_size[1])
            dc.SelectObject(bitmap)
            dc.Clear()
            # Fill the background with mask_color
            dc.SetPen(wx.Pen(mask_color, 0))
            dc.SetBrush(wx.Brush(mask_color, wx.SOLID))
            dc.DrawRectangle(0, 0, self.frame_size[0], self.frame_size[1])
            # Draws the shadow of the text
            dc.SetTextForeground((16, 16, 16))
            dc.DrawText(message['message'], message['size']/10, message['size']/10)
            # Draws the text
            dc.SetTextForeground(message['color'])
            dc.DrawText(message['message'], 0, 0)
            del dc
            # sets mask
            image = bitmap.ConvertToImage()
            image.SetMaskColour(mask_color[0], mask_color[1], mask_color[2])
            image.SetMask(True)
            bitmap = image.ConvertToBitmap()
            return bitmap

        def create_mask_color(self, mask_color):
            """ Creates a mask color from the message color """
            mask_color = list(mask_color)
            if mask_color[0] == 0xFF:
                # if the first element of the color is 255
                mask_color[0] -= 1
            else:
                # if the first element of the color is not 255
                mask_color[0] += 1
            return tuple(mask_color)

        def filter_message(self, message):
            """ Fixes the message structure and checks the banned words """
            # Fixes the message structure
            if message.get('message', None) == None:
                return False
            if message.get('position', None) == None:
                return False
            if message.get('size', None) == None:
                message['size'] = 32
            if message.get('color', None) == None:
                message['color'] = (240, 240, 240)
            if message.get('speed', None) == None:
                message['speed'] = 5
            # Checks the banned expressions
            return True
