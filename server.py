import grpc

from concurrent import futures
import os
import time

import sys
sys.path.insert(1, 'proto')

# local imports
import proto.grpc_chat_pb2 as chat
import proto.grpc_chat_pb2_grpc as rpc

import config as cfg
from whisper import Whisper

w = Whisper()
# -----------------------------------------------------------------------------

class ChatServer(rpc.ChatServerServicer): # passing in the generate rpc file

    def __init__(self):
        self.chats = []

    def ChatStream(self, request_iterator, context):
        """
        A response-stream, so the server can continually send messages.
        """
        lastindex = 0
        while True:
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        """
        Method called when Client sends ChatMessage to server.
        """
        request.message = w.modify_message(request.message)  # modifies message
        self.chats.append(request)
        return chat.Empty()  # returns empty message to protobuf

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # the workers == number of threads that can be opened at the same time
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=cfg.MAX_WORKERS)) 
    rpc.add_ChatServerServicer_to_server(ChatServer(), server)
    print(f'Starting server. Listening on port: {cfg.PORT}')
    server.add_insecure_port('[::]:' + str(cfg.PORT))
    server.start()
    # Server starts in background (in another thread)
    # wait here otherwise all threads will end
    # otherwise server can be stopped by keyboard interrupt
    try:  
        time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        print('Stopping server...')
        try:
            server.stop(0)
            sys.exit(0)
        except SystemExit:
            os._exit(0)
         
# -----------------------------------------------------------------------------