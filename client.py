import grpc

import threading
from tkinter import *
from tkinter import simpledialog

import sys
sys.path.insert(1, 'proto')

# local imports
import proto.grpc_chat_pb2 as chat
import proto.grpc_chat_pb2_grpc as rpc

import config as cfg

# -----------------------------------------------------------------------------

class Client:

    def __init__(self, username:str, window):
        self.username = username
        self.window   = window   # the frame to put ui components on
        
        # create a gRPC channel + stub
        channel   = grpc.insecure_channel(cfg.ADDRESS + ':' + str(cfg.PORT))
        self.conn = rpc.ChatServerStub(channel)
        
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._listen_for_messages, daemon=True).start()
        self._setup_ui()
        self.window.mainloop()

    def _listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for chat_message in self.conn.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            self.chat_list.insert(END, "[{}] {}\n".format(chat_message.name, chat_message.message))  # add the message to the UI

    def send_message(self, event):
        """
        This method is called when user enters something into the textbox
        """
        message = self.entry_message.get()  # retrieve message from the UI
        if message != '':
            n = chat.Note()  # create protobug message (called Note)
            n.name = self.username  # set the username
            n.message = message  # set the actual message of the note
            self.conn.SendNote(n)  # send the Note to the server

    def _setup_ui(self):
        """
        Sets up a simple tkinter GUI to enter username and messages.
        """
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    root = Tk()  # I just used a very simple Tk window for the chat UI, this can be replaced by anything
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        # retrieve a username so we can distinguish all the different clients
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    client = Client(username, frame)  # this starts a client and thus a thread which keeps connection to server open
    
    # -----------------------------------------------------------------------------