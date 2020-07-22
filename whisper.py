import random
from string import ascii_letters
from typing import List

# local imports
import config as cfg

# -----------------------------------------------------------------------------

class Whisper:
    
    def modify_message(self, message:str) -> str:
        """
        Completes all the modifications to a message.
        """
        # checks if message is less than desired number of letters to swap
        if len(message) <= cfg.SWAP_LETTERS: 
            return message
        else:
            message = self._replace_letter(message)
            message = self._drop_letter(message)
            return message
        
        
    def _replace_letter(self, message:str) -> str:
        """
        Replaces n random letters (non-whitespace) in the message with n random letters.
        """
        indexes = self._get_non_whitespace_idxs(message)
        lst = list(message)
        for idx in self._get_random_idx_sample(indexes):
            lst[idx] = next(self._get_random_idx_sample(ascii_letters))
        return ''.join(lst)


    def _drop_letter(self, message:str) -> str:
        """
        Drops a random n letters (non-whitespace) in the message.
        """
        indexes = self._get_non_whitespace_idxs(message)
        lst = list(message)
        for idx in self._get_random_idx_sample(indexes):
            lst[idx] = ''
        return ''.join(lst)

    # ------------------------------------------------------

    def _get_non_whitespace_idxs(self, message:str) -> List[int]:
        """
        Returns the indexes of non-whitespace characteres in a message
        """
        return [i for i, v in enumerate(message) if not v.isspace()]


    def _get_random_idx_sample(self, list_of_items):
        """
        Returns a random sample of a given list of letters
        """
        return iter(random.sample(list_of_items, cfg.SWAP_LETTERS))

# -----------------------------------------------------------------------------