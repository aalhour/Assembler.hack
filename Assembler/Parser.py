#!/usr/bin/env python3

import Lex


class Parser:
    """
    Parses the assembly program by looking ahead one or two tokens to determine the type of instruction. This is very
    naive and dead simple, it assumes there are no errors in the program source code and no invalid instructions are used.
    TODO: Exception handling.
    TODO: Validate the program rules for invalid instructions.
    TODO: A descent parsing algorithm, i.e. recursive-descent parsing.
    """
    ###
    # Types of Instructions as integer constants
    A_INSTRUCTION = 0   # Addressing Instruction.
    C_INSTRUCTION = 1   # Computation Instruction.
    L_INSTRUCTION = 2   # Label-Declaration pseudo-Instruction.

    def __init__(self, file):
        self.lexer = Lex.Lex(file)
        self._init_instruction_info()

    def _init_instruction_info(self):
        """
        Helper method. Initializes the instruction data stores.
        """
        self._instruction_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''

    def _a_instruction(self):
        """
        Addressing Instruction. Possible structures:
          * @number, examples: @21, @256
          * @symbol, examples: @i, @n, @LOOP, @END; where i, n could be variables, where LOOP and END could be labels
                               previously declared with an L-Instruction.
        """
        self._instruction_type = Parser.A_INSTRUCTION
        tok_type, self._symbol = self.lexer.next_token()

    def _l_instruction(self):
        """
        Symbol Declaration instruction. Symbolic syntax: (LABEL_NAME), where LABEL_NAME is any desired name for the
        label. Example: (LOOP), (END).
        """
        self._instruction_type = Parser.L_INSTRUCTION
        tok_type, self._symbol = self.lexer.next_token()

    def _c_instruction(self, token, value):
        """
        Computation instruction. Possible structures:
          * dest=comp;jump      the full c-instruction case
          * dest=comp           c-instruction with no JUMP part
          * comp;jump           c-instruction with no DEST part
          * comp                c-instruction with only a COMP part
        """
        self._instruction_type = Parser.C_INSTRUCTION
        comp_tok, comp_val = self._get_dest(token, value)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    def _get_dest(self, token, value):
        """
        Gets the 'dest' part of the instruction, if any.
        :return: First token of the 'comp' part.
        """
        tok2, val2 = self.lexer.peek_token()
        if tok2 == Lex.OPERATION and val2 == '=':
            self.lexer.next_token()
            self._dest = value
            comp_tok, comp_val = self.lexer.next_token()
        else:
            comp_tok, comp_val = token, value
        return comp_tok, comp_val

    def _get_comp(self, token, value):
        """
        Gets the 'comp' part of the instruction (mandatory).
        """
        if token == Lex.OPERATION and (value == '-' or value == '!'):
            tok2, val2 = self.lexer.next_token()
            self._comp = value + val2
        elif token == Lex.NUMBER or token == Lex.SYMBOL:
            self._comp = value
            tok2, val2 = self.lexer.peek_token()
            if tok2 == Lex.OPERATION and val2 != ';':
                self.lexer.next_token()
                tok3, val3 = self.lexer.next_token()
                self._comp += val2+val3

    def _get_jump(self):
        """
        Gets the 'jump' part of the instruction, if exists.
        """
        token, value = self.lexer.next_token()
        if token == Lex.OPERATION and value == ';':
            jump_tok, jump_val = self.lexer.next_token()
            self._jmp = jump_val

    @property
    def instruction_type(self):
        """
        The extracted instruction type.
        """
        return self._instruction_type

    @property
    def symbol(self):
        """
        The extracted Symbol from instruction.
        """
        return self._symbol

    @property
    def dest(self):
        """
        The extracted 'dest' part of instruction.
        """
        return self._dest

    @property
    def comp(self):
        """
        The extracted 'comp' part of instruction.
        """
        return self._comp

    @property
    def jmp(self):
        """
        The extracted 'jmp' part of instruction.
        """
        return self._jmp

    def has_more_instructions(self):
        return self.lexer.has_more_instructions()

    def advance(self):
        """
        Gets the next instruction (entire line). Each instruction reside on a physical line.
        """
        self._init_instruction_info()

        self.lexer.next_instruction()
        token, val = self.lexer.curr_token

        if token == Lex.OPERATION and val == '@':
            self._a_instruction()
        elif token == Lex.OPERATION and val == '(':
            self._l_instruction()
        else:
            self._c_instruction(token, val)

