import pytest
import random

import sys
sys.path.insert(0, '')

# local imports
from whisper import Whisper
import config as cfg

# -----------------------------------------------------------------------------

seed = random.seed(273)

w = Whisper()
message1 = "Hello there Anakin"
message2 = "I have the higher ground"
message3 = "Hi"
message4 = "The Guinea fowl flies through the air with all the grace of a turtle."

# -----------------------------------------------------------------------------

def test_modify_message():
    """
    Asserts to check the message is modified correctly
    Uses Random seed due to randomly changing letters within the message.
    - If the message is shorter than the numbers of letters to be swapped, returns False
    - Otherwise returns TRUE
    """
    result1 = w.modify_message(message1)
    result2 = w.modify_message(message2)
    result3 = w.modify_message(message3)
    result4 = w.modify_message(message4)
    
    print(result1)
    print(result2)
    print(result3)
    print(result4)
    
    assert result1 != message1
    assert result2 != message1
    assert result3 == message3
    assert result4 != message4


def test_replace_letter():
    """
    Asserts to check that after n random letters are replaced,
    the result is different to the original message.
    Asserts the length of the message after n letters are replaced.
    """
    result1 = w._replace_letter(message1)
    result2 = w._replace_letter(message2)
    result3 = w._replace_letter(message3)
    result4 = w._replace_letter(message4)
    
    assert result1 != message1
    assert result2 != message1
    assert result3 != message3
    assert result4 != message4
    
    assert len(result1) == len(message1)
    assert len(result2) == len(message2)
    assert len(result3) == len(message3)
    assert len(result4) == len(message4)
    
    
def test_drop_letter():
    """
    Asserts to check that after n random letters are dropped,
    the result is different to the original message.
    Asserts the length of the message after they n letters are dropped.
    """
    result1 = w._drop_letter(message1)
    result2 = w._drop_letter(message2)
    result3 = w._drop_letter(message3)
    result4 = w._drop_letter(message4)
    
    assert result1 != message1
    assert result2 != message1
    assert result3 != message3
    assert result4 != message4
    
    assert len(result1) == len(message1) - cfg.SWAP_LETTERS
    assert len(result2) == len(message2) - cfg.SWAP_LETTERS
    assert len(result3) == len(message3) - cfg.SWAP_LETTERS
    assert len(result4) == len(message4) - cfg.SWAP_LETTERS
    
# ------------------------------------------------------

def test_get_non_whitespace_idxs():
    """
    Asserts to check if the number of non-whitespaces indices are correctly
    added to the indices list.
    """
    result1 = w._get_non_whitespace_idxs(message1)
    result2 = w._get_non_whitespace_idxs(message2)
    result3 = w._get_non_whitespace_idxs(message3)
    result4 = w._get_non_whitespace_idxs(message4)
    
    assert len(result1) == 16
    assert len(result2) == 20
    assert len(result3) == 2
    assert len(result4) == 56
    
    
def test_get_random_idx_sample():
    """
    Asserts for returning a random sample equating to the number of letters to be swapped.
    """
    # list of ints
    idx_result1 = w._get_random_idx_sample(w._get_non_whitespace_idxs(message1))
    idx_result2 = w._get_random_idx_sample(w._get_non_whitespace_idxs(message2))
    idx_result3 = w._get_random_idx_sample(w._get_non_whitespace_idxs(message3))
    idx_result4 = w._get_random_idx_sample(w._get_non_whitespace_idxs(message4))
    
    msg_result1 = w._get_random_idx_sample(message1)
    msg_result2 = w._get_random_idx_sample(message2)
    msg_result3 = w._get_random_idx_sample(message3)
    msg_result4 = w._get_random_idx_sample(message4)
    
    # asserting for list of int
    assert len(list(idx_result1)) == cfg.SWAP_LETTERS
    assert len(list(idx_result2)) == cfg.SWAP_LETTERS
    assert len(list(idx_result3)) == cfg.SWAP_LETTERS
    assert len(list(idx_result4)) == cfg.SWAP_LETTERS
    
    # asserting for list of str
    assert len(list(msg_result1)) == cfg.SWAP_LETTERS
    assert len(list(msg_result2)) == cfg.SWAP_LETTERS
    assert len(list(msg_result3)) == cfg.SWAP_LETTERS
    assert len(list(msg_result4)) == cfg.SWAP_LETTERS
    
# -----------------------------------------------------------------------------
