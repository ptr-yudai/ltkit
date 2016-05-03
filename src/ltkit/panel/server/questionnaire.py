import wx

class Panel(wx.Panel):
    """ Creates a panel of the questionnaire
    This class is a panel which has all functions for the questionaries.
    """
    def __init__(self, parent):
        """ Initialize Panel class """
        # new panel
        wx.Panel.__init__(self,
                          parent)
        # new font
        DEFAULT_FONT = wx.Font(12,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL)
        # Create sizer
        self.layout_main = wx.BoxSizer(wx.VERTICAL)
        self.layout = [wx.BoxSizer(wx.HORIZONTAL) for i in range(4)]
        # text = "No questionnaire"
        label = wx.StaticText(self,
                              id = wx.ID_ANY,
                              label = u"Question : ")
        label.SetFont(DEFAULT_FONT)
        self.layout[0].Add(label,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Create a text control to enter the question
        self.text_question = wx.TextCtrl(self,
                                         id = wx.ID_ANY,
                                         size = (400, 32))
        self.text_question.SetFont(DEFAULT_FONT)
        self.text_question.SetToolTipString(u"Qeustion")
        self.layout[0].Add(self.text_question,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 0)
        # Create a button to add a new item
        self.button_add = wx.Button(self,
                                    id = wx.ID_ANY,
                                    label = u"New",
                                    size = (128, 32))
        self.button_add.SetFont(DEFAULT_FONT)
        self.button_add.Bind(wx.EVT_BUTTON, self.new_choice)
        self.layout[1].Add(self.button_add,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Create a button to delete an item
        self.button_delete = wx.Button(self,
                                    id = wx.ID_ANY,
                                    label = u"Delete",
                                    size = (128, 32))
        self.button_delete.SetFont(DEFAULT_FONT)
        self.button_delete.Bind(wx.EVT_BUTTON, self.delete_choice)
        self.layout[1].Add(self.button_delete,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Create a list control
        self.list_choice = wx.ListBox(self,
                                      wx.ID_ANY,
                                      choices = (),
                                      style = wx.LB_SINGLE
                                      | wx.LB_HSCROLL
                                      | wx.LB_NEEDED_SB)
        self.list_choice.SetFont(DEFAULT_FONT)
        self.layout[2].Add(self.list_choice,
                           proportion = 1,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Create a button
        self.button_post = wx.Button(self,
                                    id = wx.ID_ANY,
                                     label = u"Post",
                                    size = (128, 32))
        self.button_post.SetFont(DEFAULT_FONT)
#        self.button_add.Bind(wx.EVT_BUTTON, self.inet.create_socket)
        self.layout[3].Add(self.button_post,
                           flag = wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL,
                           border = 8)
        # Set sizer
        self.layout_main.Add(self.layout[0], flag = wx.ALIGN_TOP)
        self.layout_main.Add(self.layout[1], flag = wx.ALIGN_LEFT)
        self.layout_main.Add(self.layout[2],
                             proportion = 1,
                             flag = wx.EXPAND | wx.ALIGN_CENTER)
        self.layout_main.Add(self.layout[3], flag = wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT) 
        self.SetSizer(self.layout_main)
        return

    def new_choice(self, event):
        """ Add new choice """
        # Ask the string
        dialog = wx.TextEntryDialog(self,
                                    message = "Please enter the string of the choice.",
                                    caption = "New choise")
        if dialog.ShowModal() != wx.ID_OK:
            return
        # Add new label
        self.list_choice.Append(dialog.GetValue())
        return

    def delete_choice(self, event):
        """ Delete the selected choice """
        
        return
        
