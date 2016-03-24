#!/usr/local/bin/python3


class SymbolTable(dict):
    """
    Symbol Table is a basically a dictionary, which is referred to in the book as a hash-table store. It is used to store
    and resolve Symbols (labels and variables) and their associated addresses.
    """
    def __init__(self):
        super().__init__()
        self.update({
            'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
            'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
            'SCREEN': 0x4000, 'KBD': 0x6000
        })

    def contains(self, symbol):
        return symbol in self

    def add_entry(self, symbol, address):
        self[symbol] = address

    def get_address(self, symbol):
        return self[symbol]

