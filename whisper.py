import re

# -----------------------------------------------------------------------------

def modify_message(self, message:str) -> str:
    """
    Completes all the modifications to a message.
    """
    if len(message) < 2:
        pass
    else:
        message = replace_letter(message)
    return message
    
    
def replace_letter(self, message:str) -> str:
    """
    Replaces a random letter in the message with another random letter.
    """
    return message.replace(message[0], 'a')


def drop_letter(self, message:str) -> str:
    """
    Drops a random letter in the message
    """
    return message.replace(message[0], '') # TODO add randoomness

# -----------------------------------------------------------------------------