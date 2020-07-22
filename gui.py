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
from whisper import Whisper

# -----------------------------------------------------------------------------

class Gui():
    
    def __init__(self):
        self.window = window   # UI components frame
        self._setup_gui()
        self.window.mainloop() 
        
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