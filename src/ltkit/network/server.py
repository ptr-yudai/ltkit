import threading
import wx
from ..module import message
import packet

class Network:
    def __init__(self, parent):
        """ Initialize Network class """
        # var init
        self.thread_stop = True
        self.socket_list = []
        self.id_list = {}
        # Inherit
        self.server = parent
        # Messanger
        self.message_viewer = message.MessageViewer(parent)
        return

    def __del__(self):
        # Kill thread
        if self.thread_stop != True: # but not False!
            self.thread_stop.set()
            self.thread.join()
        return
    
    def post_questionnaire(self, event):
        """ Post a questionnaire to all the clients """
        panel_questionnaire = self.server.panel_questionnaire
        # Disable button
        panel_questionnaire.button_post.Disable()
        # Create a message structure
        message = {
            "type": "questionnaire",
            "available": True,
            "question": panel_questionnaire.text_question.GetValue(),
            "choice": [panel_questionnaire.list_choice.GetString(index)
                       for index
                       in range(panel_questionnaire.list_choice.GetCount())],
            "date": wx.DateTime.Now().Format("%H:%M:%S")
        }
        # Post the questionnaire
        self.broadcast(packet.compress(message))
        # Disable interfaces
        panel_questionnaire.text_question.Disable()
        panel_questionnaire.button_add.Disable()
        panel_questionnaire.button_delete.Disable()
        panel_questionnaire.button_clear.Disable()
        panel_questionnaire.list_choice.Disable()
        # Enable 'post' button
        panel_questionnaire.button_post.SetLabel(u"Close")
        panel_questionnaire.button_post.Bind(wx.EVT_BUTTON, self.close_questionnaire)
        panel_questionnaire.button_post.Enable()
        # Answer dict
        self.questionnaire_answer = {}
        return

    def close_questionnaire(self, event):
        """ Close the questionnaire """
        panel_questionnaire = self.server.panel_questionnaire
        # Disable button
        panel_questionnaire.button_post.Disable()
        # Create a message structure
        message = {
            "type": "questionnaire",
            "available": False,
            "date": wx.DateTime.Now().Format("%H:%M:%S")
        }
        # Post the questionnaire
        self.broadcast(packet.compress(message))
        # Enable interfaces
        panel_questionnaire.text_question.Enable()
        panel_questionnaire.button_add.Enable()
        panel_questionnaire.button_delete.Enable()
        panel_questionnaire.button_clear.Enable()
        panel_questionnaire.list_choice.Enable()
        # Enable 'post' button
        panel_questionnaire.button_post.SetLabel(u"Post")
        panel_questionnaire.button_post.Bind(wx.EVT_BUTTON, self.post_questionnaire)
        panel_questionnaire.button_post.Enable()
        # Show the result
        wx.CallAfter(self.display_questionnaire_result)
        return

    def post_message(self, event):
        """ Post a message to all the clients """
        import packet
        panel_post = self.server.panel_post
        # Create a message structure
        message = {
            "type": "message",
            "message": panel_post.text_message.GetValue(),
            "size": int(panel_post.spin_size.GetValue()),
            "color": panel_post.message_color,
            "date": wx.DateTime.Now().Format("%H:%M:%S"),
            "id": "<master>"
        }
        # Check if the message is empty
        if message['message'] == "":
            return
        # Post the message
        self.broadcast(packet.compress(message))
        # Append the message onto the listview
        wx.CallAfter(panel_post.append_message, message)
        # Dispay the message (avoid assertionerror)
        wx.CallAfter(self.display_message, message)
        # Clear text control
        panel_post.text_message.Clear()
        return

    def create_socket(self, event):
        """ Listen to the clients """
        panel_post = self.server.panel_post
        # Get the hostname
        self.host = panel_post.text_ip.GetValue()
        # Get the port number
        try:
            self.port = int(panel_post.text_port.GetValue())
        except ValueError:
            wx.MessageBox(u"The port number is invalid.\nOnly numeric characters can be used.",
                          u"LT Toolkit",
                          style = wx.OK | wx.ICON_ERROR)
            return
        # Disable 'standby' button
        panel_post.button_standby.Disable()
        # Start new thread
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target = self.establish)
        self.thread.setDaemon(True)
        self.thread.start()
        # Enable 'standby' button
        panel_post.button_standby.SetLabel(u"Stop")
        panel_post.button_standby.Bind(wx.EVT_BUTTON, self.destroy_socket)
        panel_post.button_standby.Enable()
        return

    def destroy_socket(self, event):
        """ Stop listening """
        panel_post = self.server.panel_post
        # Disable 'disconnect' button
        panel_post.button_standby.Disable()
        # Kill thread
        self.thread_stop.set()
        self.thread.join()
        # Enable 'connect' button
        panel_post.button_standby.SetLabel(u"Standby")
        panel_post.button_standby.Bind(wx.EVT_BUTTON, self.create_socket)
        panel_post.button_standby.Enable()
        return

    def establish(self):
        import select
        import socket
        import packet
        """ Establish a server and run it forever """
        # Open the port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind((self.host, self.port))
        except:
            # Failed to open the port
            wx.CallAfter(self.establish_fail)
            return
        self.server_socket.listen(10)
        self.socket_list.append(self.server_socket)
        # Listen
        while True:
            read_sockets, wrote_sockets, error_sockets = select.select(self.socket_list, [], [], 1)
            # Process
            for socket in read_sockets:
                if socket == self.server_socket:
                    # New audience
                    socket_fd, address = self.server_socket.accept()
                    self.socket_list.append(socket_fd)
                    self.id_list[socket_fd] = self.calculate_id()
                else:
                    try:
                        # Receive message
                        recv_data = packet.decompress(socket.recv(4096))
                        # Process the message
                        self.proc_message(socket, recv_data)
                    except:
                        # Connection refused
                        socket.close()
                        self.socket_list.remove(socket)
            # Check the thread is killed
            if self.thread_stop.is_set():
                for socket in self.socket_list:
                    socket.close()
                break
            # Clear
            read_sockets = wrote_sockets = error_sockets = []
        return

    def establish_fail(self):
        """ Failed to establish a server. """
        # Dialog
        wx.MessageBox(u"Failed to open the port {0}.\nPlease make sure that the port is not in use now.".format(self.port),
                      u"LT Toolkit",
                      style = wx.OK | wx.ICON_ERROR)
        # Enable 'standby' button
        panel_post.button_standby.SetLabel(u"Standby")
        panel_post.button_standby.Bind(wx.EVT_BUTTON, self.create_socket)
        panel_post.button_standby.Enable()
        return

    def proc_message(self, socket, recv_data):
        """ Process received message """
        import packet
        panel_post = self.server.panel_post
        panel_questionnaire = self.server.panel_questionnaire
        # Check type
        if recv_data.get('type', None) == None:
            return
        # Append some data
        if recv_data['type'] == "message":
            # Create message structure
            if self.id_list.get(socket, None) == None:
                recv_data['id'] = "<unknown>"
            else:
                recv_data['id'] = self.id_list[socket]
            recv_data['date'] = wx.DateTime.Now().Format("%H:%M:%S")
            # Send to all client
            self.broadcast(packet.compress(recv_data))
            # Append the message onto the listview
            wx.CallAfter(panel_post.append_message, recv_data)
            # Dispay the message (avoid assertionerror)
            wx.CallAfter(self.display_message, recv_data)
        elif recv_data['type'] == "questionnaire":
            # Set choice
            self.questionnaire_answer[socket] = recv_data['choice']
            # Count up
            wx.CallAfter(panel_questionnaire.proc_new_answer, self.questionnaire_answer)
            return
        return

    def broadcast(self, send_data):
        """ Broadcast message """
        # Broadcast
        for socket in self.socket_list:
            if socket != self.server_socket:
                try:
                    socket.send(send_data)
                except:
                    socket.close()
                    self.socket_list.remove(socket)
        return
    
    def calculate_id(self):
        """ Calculate ID """
        import string
        import random
        return "".join([random.choice(string.ascii_letters + string.digits) for i in range(8)])

    def display_message(self, recv_data):
        """ Display a message on the desktop screen (with using the MessageViewer class)"""
        self.message_viewer.display_message(recv_data)
        return
        
    def display_questionnaire_result(self):
        """ Display the result of the questionnaire """
        panel_questionnaire = self.server.panel_questionnaire
        # Get number of items
        num_item = panel_questionnaire.list_choice.GetCount()
        # Create a modal frame
        self.dialog = wx.Dialog(parent = self.server,
                                title = "Aggregate Results - LT Toolkit",
                                size = (400, 250),
                                style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.dialog.SetMinSize((400, 250))
        panel = wx.ScrolledWindow(self.dialog, id = wx.ID_ANY)
        # new font
        DEFAULT_FONT = wx.Font(12,
                               wx.FONTFAMILY_DEFAULT,
                               wx.FONTSTYLE_NORMAL,
                               wx.FONTWEIGHT_NORMAL)
        # new sizer
        dialog_layout_main = wx.BoxSizer(wx.VERTICAL)
        dialog_layout = [wx.FlexGridSizer(num_item + 1, 2),
                         wx.BoxSizer(wx.HORIZONTAL)]
        # Qeustion
        label = wx.StaticText(self.dialog,
                              id = wx.ID_ANY,
                              label = panel_questionnaire.text_question.GetValue())
        label.SetFont(DEFAULT_FONT)
        dialog_layout[0].Add(label,
                             flag = wx.ALL | wx.GROW,
                             border = 16)
        label = wx.StaticText(self.dialog,
                              id = wx.ID_ANY)
        dialog_layout[0].Add(label,
                             flag = wx.GROW)
        # Add the results
        for i in range(num_item):
            label_choice = wx.StaticText(self.dialog,
                                         id = wx.ID_ANY,
                                         label = panel_questionnaire.list_choice.GetString(i))
            label_number = wx.StaticText(self.dialog,
                                         id = wx.ID_ANY,
                                         label = "--> " + str(self.questionnaire_answer.values().count(i)))
            label_choice.SetFont(DEFAULT_FONT)
            label_number.SetFont(DEFAULT_FONT)
            dialog_layout[0].Add(label_choice,
                                 flag = wx.ALL | wx.GROW,
                                 border = 4)
            dialog_layout[0].Add(label_number,
                                 flag = wx.ALL | wx.GROW,
                                 border = 4)
        # Close button
        button_close = wx.Button(self.dialog,
                                 id = wx.ID_ANY,
                                 label = "Close",
                                 size = (96, 32))
        button_close.SetFont(DEFAULT_FONT)
        button_close.Bind(wx.EVT_BUTTON, self.destroy_dialog)
        dialog_layout[1].Add(button_close,
                             flag = wx.ALIGN_CENTER | wx.ALL)
        # Set layout
        dialog_layout[0].AddGrowableCol(0)
        dialog_layout_main.Add(dialog_layout[0],
                               proportion = 1,
                               flag = wx.EXPAND | wx.ALL,
                               border = 4)
        dialog_layout_main.Add(dialog_layout[1],
                               flag = wx.ALIGN_CENTER | wx.ALL,
                               border = 8)
        self.dialog.SetSizer(dialog_layout_main)
        self.dialog.Layout()
        self.dialog.Center(wx.BOTH)
        # Show the dialog
        self.dialog.ShowModal()
        return

    def destroy_dialog(self, event):
        """ Destroy modal dialog """
        self.dialog.Destroy()
        return
