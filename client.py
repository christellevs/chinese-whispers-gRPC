import grpc
import fileinput
import threading
import tkinter as tk

import sys
sys.path.insert(1, 'proto')

# local imports
import grpc_chat_pb2 as chat
import grpc_chat_pb2_grpc as rpc

import config as cfg
# -----------------------------------------------------------------------

class Client:
    
    def __init__(self, username: str, window):
        # the frame to put ui components on
        self.window = window
        self.username = username
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(cfg.ADDRESS + ':' + str(cfg.PORT))
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._listen_for_messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()
        
        # self.username = username
        
        # # open a gRPC channel
        # channel = grpc.insecure_channel(cfg.ADDRESS + ':' + str(cfg.PORT))
        #  # create a stub (client)
        # stub = rpc.ChatServiceStub(channel)
        # # create a valid request send_message
        # number = chat.Number(value=16)
        # # make the call
        # response = stub.SquareRoot(number)

        # print(response.value)
         
    def _listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for chat_message in self.conn.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            print("R[{}] {}".format(chat_message.name, chat_message.message))  # debugging statement
            self.chat_list.insert(tk.END, "[{}] {}\n".format(chat_message.name, chat_message.message))  # add the message to the UI   
    
    def send_message(self, event):
        """
        This method is called when user enters something into the textbox
        """
        message = self.entry_message.get()  # retrieve message from the UI
        if message is not '':
            n = chat.Note()  # create protobug message (called Note)
            n.name = self.username  # set the username
            n.message = self._modify_message(message)  # set the actual message of the note # TODO
            print("S[{}] {}".format(n.name, n.message))  # debugging statement
            self.conn.SendNote(n)  # send the Note to the server
            
    def _modify_message(self, message:str):
        """Modify's a message"""
        if len(message) < 2:
            pass
        else:
            message = self._replace_letter(message)
        return message
        
        
    def _replace_letter(self, message:str):
        """Replaces letter in messae"""
        return message.replace(message[0], 'a')
    
    # --------------------------------------------
    
    def __setup_ui(self):
        self.chat_list = tk.Text()
        self.chat_list.pack(side=tk.TOP)
        self.lbl_username = tk.Label(self.window, text=self.username)
        self.lbl_username.pack(side=tk.LEFT)
        self.entry_message = tk.Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=tk.BOTTOM)
    
# -----------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()  # I just used a very simple Tk window for the chat UI, this can be replaced by anything
    frame = tk.Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        # retrieve a username so we can distinguish all the different clients
        username = tk.simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()  # don't remember why this was needed anymore...
    c = Client(username, frame)  # this starts a client and thus a thread which keeps connection to server open

# -----------------------------------------------------------------------