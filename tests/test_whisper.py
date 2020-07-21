import pytest
import random

import sys
sys.path.insert(0, "/")

# local imports
import whisper as w

# -----------------------------------------------------------------------------

seed = random.seed(273)

message1 = "Hello there Anakin"
message2 = "I have the higher ground"

# -----------------------------------------------------------------------------

def test_modify_message():
    """
    """
    result1 = w.modify_message(message1)
    result2 = w.modify_message(message2)


def test_replace_letter():
    """
    """
    result1 = w.replace_letter(message1)
    result2 = w.replace_letter(message2)
    


# -----------------------------------------------------------------------------