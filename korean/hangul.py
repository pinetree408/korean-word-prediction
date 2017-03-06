# -*- coding: utf-8 -*-
import re
import copy

# option 0 : default analyze
# option 1 : bigram analyze
# option 2 : all analye


class KE(object):
    """korean & english regular expersion analyze class
    Attributes:
        en_h (str): Header of korean
        en_b (dict): Body of korean
        en_f (dict): Footer of korean
        reg_h (str): regular expression of korean Header
        reg_b (str): regular expression of korean Body
        reg_f (str): regular expression of korean footer
    """

    en_h = "rRseEfaqQtTdwWczxvg"
    en_b_list = [
        'k', 'o', 'i', 'O', 'j',
        'p', 'u', 'P', 'h', 'hk',
        'ho', 'hl', 'y', 'n', 'nj',
        'np', 'nl', 'b', 'm', 'ml',
        'l'
    ]
    en_f_list = [
        '', 'r', 'R', 'rt', 's',
        'sw', 'sg', 'e', 'f', 'fr',
        'fa', 'fq', 'ft', 'fx', 'fv',
        'fg', 'a', 'q', 'qt', 't',
        'T', 'd', 'w', 'c', 'z',
        'x', 'v', 'g'
    ]
    en_jm_list = [
        '', 'r', 'R', 'rt', 's', 'sw', 'sg', 'e',
	'E', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv',
        'fg', 'a', 'q', 'Q', 'qt', 't', 'T', 'd',
        'w', 'W', 'c', 'z', 'x', 'v', 'g', 'k',
        'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h',
	'hk', 'ho', 'hl', 'y', 'n', 'np', 'nl', 'b',
	'm', 'ml', 'l'
    ]

    reg_h = "[rRseEfaqQtTdwWczxvg]"
    reg_b = "hk|ho|hl|nj|np|nl|ml|k|o|i|O|j|p|u|P|h|y|n|b|m|l"
    reg_f = "rt|sw|sg|fr|fa|fq|ft|fx|fv|fg|qt|r|R|s|e|f|a|q|t|T|d|w|c|z|x|v|g|"

    def __init__(self):
        """Initialize KE class
        this method initialize all attributes of this class
        """
        reg_h_block = "("+self.reg_h+")"
        reg_b_block = "("+self.reg_b+")"
        reg_f_item_first = "("+self.reg_f+")"
        reg_f_item_second = "(?=("+self.reg_h+")("+self.reg_b+"))|("+self.reg_f+")"
        reg_f_block = "(" + reg_f_item_first + reg_f_item_second + ")"

        self.regex = reg_h_block + reg_b_block + reg_f_block
        self.hangul_reg = re.compile('[^가-힣]+')

    def decompose(self, word):
        """chnage korean word to korean letter list
        Args:
            word (str): target word
        Return:
            len (int): length of target word's letter
        """
        result = []
        for char in word.decode('utf-8'):
            char_code = ord(char)
            if char_code < 44032 or char_code > 55203:
                char_code = char_code - 12592
                result.append(self.en_jm_list[char_code])
                continue
            char_code = char_code - 44032
            en_h_code = char_code / 588
            en_bf_code = char_code % 588
            en_b_code = en_bf_code / 28
            en_f_code = en_bf_code % 28
            en_h_char = self.en_h[en_h_code]
            en_b_char = self.en_b_list[en_b_code]
            en_f_char = self.en_f_list[en_f_code]

            result.append(en_h_char)
            result.append(en_b_char)
            if en_f_code != 0:
                result.append(en_f_char)
        return ''.join(result)

    def compose(self, word):
        length = len(word)
        temp_word = word
        result = ''
        while length != 0:
            m = re.search(self.regex, temp_word)
	    if m is None:
                try:
                    not_completed = unichr(self.en_jm_list.index(temp_word) + 12592)
                except ValueError as e:
                    raise ValueError
                if len(word) < 6:
                    result = not_completed + result
                else:
                    raise ValueError
                break

            if m.group(0) != None:
                korean_letter = m.group(0)
                char_code = self.en_h.index(korean_letter[0]) * 588
                if len(korean_letter) > 2:
                    if korean_letter[2] in self.en_f_list:
                        char_code += self.en_b_list.index(korean_letter[1]) * 28
                        char_code += self.en_f_list.index(korean_letter[2])
                    else:
                        char_code += self.en_b_list.index(korean_letter[1:]) * 28
                else:
                    char_code += self.en_b_list.index(korean_letter[1]) * 28
                char_code += 44032
                result += unichr(char_code)
            temp_word = temp_word.replace(m.group(0), '')
	    length = len(temp_word)
	return result
