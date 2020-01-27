from dataclasses import dataclass


@dataclass
class Symbol:
    name: str

@dataclass
class VarSymbol(Symbol):
    varType: str

@dataclass
class ConstSymbol(Symbol):
    value: str

@dataclass
class ProcSymbol(Symbol):
    params: []

class ScopedSymbolTable:
    def __init__(self, name, outScope = None):
        self.name = name
        self.outScope = outScope
        self.symbols = {}
    
    def insert(self, symbol):
        self.symbols[symbol.name] = symbol
    
    def search(self, name, curOnly = False):
        symbol = self.symbols.get(name)

        if symbol is not None:
            return symbol
        if curOnly:
            return symbol
        if self.outScope is not None:
            return self.outScope.search(name)