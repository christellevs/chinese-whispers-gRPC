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
