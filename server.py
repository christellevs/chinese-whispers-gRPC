import grpc
from concurrent import futures
import time


import sys
sys.path.insert(1, 'proto')

# local imports
import grpc_chat_pb2 as chat
import grpc_chat_pb2_grpc as rpc

import config as cfg

# -----------------------------------------------------------------------

class ChatService(rpc.ChatServiceServicer):
    
    def __init__(self):
        # List with all the chat history
        self.chats = []

    # The stream which will be used to send new messages to clients
    def chat_stream(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n # used to return a generator
        

    def SendMessage(self, request: chat.ChatMessage, context):
        """
        This method is called when a clients sends a ChatMessage to the server.

        :param request:
        :param context:
        :return:
        """
        # # this is only for the server console
        # print("[{}] {}".format(request.name, request.message))
        # Add it to the chat history
        self.chats.append(request)
        # return chat.Empty()  # something needs to be returned required by protobuf language, we just return empty msg

if __name__ == '__main__':
    
    # creating grpc server
    # max workers is related to the amount of threads allowed to be opened concurrently.
    # e.g. if max workers = 10, then no more than 10 clients are able to be connected at once.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=cfg.MAX_WORKERS))
    
    # addding the defined class to the server
    rpc.add_ChatServiceServicer_to_server(ChatService(), server)

    # setting up the port and starting server
    print(f'Starting server. Listening on port {cfg.PORT})')
    server.add_insecure_port('[::]:' + str(cfg.PORT))
    server.start()

    # In another thread sever will start in background
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

# -----------------------------------------------------------------------