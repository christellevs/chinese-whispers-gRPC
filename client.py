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
        self.window   = window   # UI components frame
        
        channel   = grpc.insecure_channel(cfg.ADDRESS + ':' + str(cfg.PORT))
        self.conn = rpc.ChatServerStub(channel)
        
        # creates listening thread for when new message streams come in
        threading.Thread(target=self._listen_for_messages, daemon=True).start()
        self._setup_gui()
        self.window.mainloop()

    def _listen_for_messages(self):
        """
        Ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for chat_message in self.conn.ChatStream(chat.Empty()):
            # inserting message in GUI
            self.chat_list.insert(END, f'[{chat_message.name}] {chat_message.message}\n')

    def send_message(self, event):
        """
        This method is called when user enters something into the textbox.
        """
        # retrieve message from GUI
        message = self.entry_message.get()  
        if message != '':
            # create protobug chat message 
            n = chat.ChatMessage()          
            n.name = self.username      
            n.message = message
            self.conn.SendChatMessage(n)
            self._clear_text()

    def _setup_gui(self):
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
        
    def _clear_text(self):
        """
        Clears message from entry box in GUI after user presses eturn/enter
        """
        self.entry_message.delete(0, 'end')

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        username = simpledialog.askstring("Username", "Enter username", parent=root)
    root.deiconify()
    
    # starts a client and thread to keep connection to server open
    client = Client(username, frame)  
    
    # -----------------------------------------------------------------------------