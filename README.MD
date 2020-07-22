# Chinese Whispers gRPC Chat Prototype Technical Test

A chinese whispers chat prototype where 2 clients are able to view and send messages to each other.

Before the message is sent to the other client, it is slightly modified:

1. A random word is swapped for one of its random synonyms (if that synonym exist)
1. A chosen number of random letters are replaced with the same chosen number of random letters in the message.
1. A chosen number of random letters are dropped from the message.

----------------------------------------------------------------
## Running program

In a terminal run:

    python server.py


Open a 2nd terminal and run:

     python client.py


Opent 3rd terminal and run:

     python client.py


A Tkinter dialog box will appear for each client asking for a username.

After a username is input and enter is pressed, a message box will appear.

Any clients using the same server will be able to communicate.


----------------------------------------------------------------

## Running tests

To run tests, in any terminal run:

    pytest

----------------------------------------------------------------

### NB

Please note that the first message from a client often takes a while to appear in the
message box. This is due to the chinese whispers feature of swapping a random word
in the message for its synonym. More work would need to be done on this to optimize.

----------------------------------------------------------------