import random
from string import ascii_letters

# local imports
import config as cfg

# -----------------------------------------------------------------------------

def modify_message(message:str) -> str:
    """
    Completes all the modifications to a message.
    """
    # checks if message is less than desired number of letters to swap
    if len(message) < cfg.SWAP_LETTERS: 
        pass
    else:
        message = replace_letter(message)
    return message
    
    
def replace_letter(message:str) -> str:
    """
    Replaces n random letters in the message with n random letters.
    """
    indexes = [i for i,_ in enumerate(message) if not message.isspace()]
    letters =  iter(random.sample(ascii_letters, cfg.SWAP_LETTERS))
    lst = list(message)
    for idx in random.sample(indexes, cfg.SWAP_LETTERS):
        lst[idx] = next(letters)
    return ''.join(lst)


def drop_letter(message:str) -> str:
    """
    Drops a random letter in the message
    """
    return message.replace(message[0], '') # TODO add randoomness

# -----------------------------------------------------------------------------