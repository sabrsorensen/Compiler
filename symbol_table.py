from semantic_record import *

class SymbolTable(object):

    def __init__(self, name):
        self.name = name
        self.sem_records = []

