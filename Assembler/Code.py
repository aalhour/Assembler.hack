#!/usr/local/bin/python3


class Code:
    """
    Code is responsible for generating the bits-strings that correspond to the parsed instructions parts: dest, comp and jmp.
    It generates A-Instructions and C-Instructions via the gen_a_instruction() and gen_c_instruction() methods as strings
    of binary characters of 1's and 0's.
    """
    # The JUMP part codes
    _jump_codes = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

    # The DEST part codes
    _dest_codes = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']

    # The COMP part codes
    _comp_codes = {'0': '0101010', '1': '0111111', '-1':'0111010', 'D':'0001100', 'A': '0110000', '!D': '0001101',
                   '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
                   'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D':'0000111',
                   'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001', '-M': '1110011',
                   'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
                   'D&M': '1000000', 'D|M': '1010101'}

    def __init__(self):
        pass

    def _bits(self, n):
        """
        Convert an integer number to a binary string. Uses the built-in "bin()" method.
        :param n: Number.
        :return: Binary string
        """
        return bin(int(n))[2:]

    def gen_a_instruction(self, address_value):
        """
        Generates an A-Instruction from a specified address_value.
        :param address_value: Value of address in decimal.
        :return: A-Instruction in binary (String).
        """
        return '0' + self._bits(address_value).zfill(15)

    def gen_c_instruction(self, dest, comp, jump):
        """
        Generates an A-Instruction from a specified address_value.
        :param dest: 'dest' part of the instruction (string).
        :param comp: 'comp' part of the instruction (string).
        :param jump: 'jmp' part of the instruction (string).
        :return: C-Instruction in binary (string).
        """
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)

    def dest(self, d):
        """
        Generates the corresponding binary code for the given 'dest' instruction part.
        """
        return self._bits(self._dest_codes.index(d)).zfill(3)

    def comp(self, c):
        """
        Generates the corresponding binary code for the given 'comp' instruction part.
        """
        return self._comp_codes[c]

    def jump(self, j):
        """
        Generates the corresponding binary code for the given 'jmp' instruction part.
        """
        return self._bits(self._jump_codes.index(j)).zfill(3)

