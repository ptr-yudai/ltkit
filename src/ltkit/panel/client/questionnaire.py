import wx

class Panel(wx.Panel):
    """ Creates a panel of the questionnaire
    This class is a panel which has all functions for the questionaries.
    """
    def __init__(self, parent):
        """ Initializes Panel """
        # Inits variables
        self.message_color = (240, 240, 240)
        self.socket = None
        # new panel
        wx.Panel.__init__(self,
                          parent)
        # new font
        DEFAULT_FONT = wx.Font(12,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL)
        # Creates sizer
        self.layout_main = wx.BoxSizer(wx.VERTICAL)
        self.layout = [wx.BoxSizer(wx.HORIZONTAL),
                       wx.BoxSizer(wx.VERTICAL),
                       wx.BoxSizer(wx.HORIZONTAL)]
        # text = "No questionnaire"
        self.label_question = wx.StaticText(self,
                                            id = wx.ID_ANY,
                                            label = "No questionnaire.")
        self.label_question.SetFont(DEFAULT_FONT)
        self.layout[0].Add(self.label_question,
                           flag = wx.EXPAND | wx.ALIGN_LEFT | wx.ALL,
                           border = 8)
        # Prepare for radio buttons
        
        # Create a button to post the answer
        self.button_answer = wx.Button(self,
                                       id = wx.ID_ANY,
                                       label = "Answer",
                                       size = (96, 32))
        self.button_answer.SetFont(DEFAULT_FONT)
#        self.button_connect.Bind(wx.EVT_BUTTON, self.inet.create_socket)
        self.layout[2].Add(self.button_answer,
                           flag = wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL,
                           border = 8)
        # Sets sizer
        self.layout_main.Add(self.layout[0],
                             flag = wx.ALIGN_TOP)
        self.layout_main.Add(self.layout[1],
                             proportion = 1,
                             flag = wx.EXPAND | wx.ALIGN_CENTER)
        self.layout_main.Add(self.layout[2],
                             flag = wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
        self.SetSizer(self.layout_main)
        return

    def display_questionnaire(self, message):
        """ Display the questionnaire """
        # new font
        DEFAULT_FONT = wx.Font(12,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL)
        try:
            if message['available'] == True:
                # Clear all
                self.clear_questionnaire(message['date'])
                # Set new questionnaire
                self.label_question.SetLabel(message['question'])
                # Set choices
                for choice in message['choice']:
                    radio_choice = wx.RadioButton(self,
                                                  id = wx.ID_ANY,
                                                  label = choice)
                    radio_choice.SetFont(DEFAULT_FONT)
                    self.layout[1].Add(radio_choice,
                                       flag = wx.ALIGN_LEFT | wx.ALL)
                self.layout_main.Layout()
            else:
                # Clear all
                self.clear_questionnaire(message['date'])
        except:
            pass
        return

    def clear_questionnaire(self, date):
        """ Clear current questionnaire """
        # Set empty label
        self.label_question.SetLabel("No questionnaire. (Closed on {0})".format(date))
        # Destroy all the radio buttons
        self.layout[1].DeleteWindows()
        return
