# codinf: utf-8
import wx

class Screenshot:
    """takes a screenshot of the desktop.
    This class is used for taking and cropping a screenshot.
    """
    def __init__(self):
        """initializes Screenshot"""
        self.screen_dc = wx.ScreenDC()
        self.screen_size = self.screen_dc.GetSize()

        return None

    def take(self):
        """takes a screenshot and stores bitmap data"""
        bitmap = wx.EmptyBitmap(self.screen_size[0], self.screen_size[1])
        memory = wx.MemoryDCFromDC(self.screen_dc)
        memory.SelectObject(bitmap)
        memory.Blit(0, 0, self.screen_size[0], self.screen_size[1], self.screen_dc, 0, 0)
        memory.SelectObject(wx.NullBitmap)
        return bitmap
        
    def crop(self, bitmap, rect):
        """crops a bitmap"""
        image = bitmap.ConvertToImage()
        cropped_image = image.GetSubImage(rect)
        bitmap = cropped_image.ConvertToBitmap()
        return bitmap
