#!/usr/bin/env python3

import re

# Number constant i.e. '123'
NUMBER = 1

# Symbol constant i.e. 'LOOP', 'END'
SYMBOL = 2

# Operation constant i.e. = ; ( ) @ + - & | !
OPERATION = 3

# Error constant
ERROR = 4


class Lex(object):
    """
    A simple lexer that uses regular expressions to detect Numbers, Symbols (Labels) and Operations. It loads the whole
    program (source code text file .asm) into memory for scanning.
    TODO: Exception handling.
    TODO: Error checking on the tokens.
    """
    # Internal regular expression patterns
    _number_re = r'\d+'
    _symbol_start_re = r'\w_.$:'
    _symbol_re = '[' + _symbol_start_re + '][' + _symbol_start_re + r'\d]*'
    _operation_re = r'[=;()@+\-&|!]'
    _word = re.compile(_number_re + '|' + _symbol_re + '|' + _operation_re)
    _comment = re.compile('//.*$')

    def __init__(self, asm_file_name):
        file = open(asm_file_name, 'r')
        self._lines = file.read()
        self._tokens = self._tokenize(self._lines.split('\n'))
        # List of tokens for current instruction
        self.curr_instr_tokens = []
        # Current token of current instruction
        self.curr_token = (ERROR, 0)

    def _is_operation(self, word):
        return self._is_match(self._operation_re, word)

    def _is_number(self, word):
        return self._is_match(self._number_re, word)

    def _is_symbol(self, word):
        return self._is_match(self._symbol_re, word)

    def _is_match(self, re_str, word):
        return re.match(re_str, word) is not None

    def _tokenize(self, lines):
        return [t for t in [self._tokenize_line(l) for l in lines] if t]

    def _tokenize_line(self, line):
        return [self._token(word) for word in self._split(self._remove_comment(line))]

    def _remove_comment(self, line):
        return self._comment.sub('', line)

    def _split(self, line):
        return self._word.findall(line)

    def _token(self, word):
        if self._is_number(word):
            return NUMBER, word
        elif self._is_symbol(word):
            return SYMBOL, word
        elif self._is_operation(word):
            return OPERATION, word
        else:
            return ERROR, word

    def has_more_instructions(self):
        return self._tokens != []

    def next_instruction(self):
        self.curr_instr_tokens = self._tokens.pop(0)
        self.next_token()
        return self.curr_instr_tokens

    def has_next_token(self):
        return self.curr_instr_tokens != []

    def next_token(self):
        if self.has_next_token():
            self.curr_token = self.curr_instr_tokens.pop(0)
        else:
            self.curr_token = ERROR, 0
        return self.curr_token

    def peek_token(self):
        if self.has_next_token():
            return self.curr_instr_tokens[0]
        else:
            return ERROR, 0

