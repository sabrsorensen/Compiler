__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import logging
from semantic_record import SemanticRecord
from semantic_entry import SemanticEntry

class SymbolTable(object):

    def __init__(self):
        self.name = ''
        self.cur_depth = 0
        self.context_attributes_stack = []
        self.cur_context_attributes = None
        self.sym_table = {}

    def create(self): #subtables
        self.cur_context_attributes = ContextAttrs()
        self.cur_depth += 1

    def create_root(self): #Root table
        self.cur_context_attributes = ContextAttrs()

    def destroy(self):
        self.cur_lexeme = ''
        for lexeme in self.cur_context_attributes.context_lexemes:
            self.cur_entry = self.find(lexeme)
            if self.cur_entry:
                self.cur_entry.back_out()
                if self.cur_entry.semantic_record_stack is None:
                    del self.sym_table[lexeme]

    def insert(self, record):
        self.cur_context_attributes.context_lexemes.append(record.lexeme)
        record.offset = self.cur_depth
        self.cur_depth += record.size
        self.existing_entry = self.find(record.lexeme)
        if self.existing_entry is None:
            self.new_entry = SemanticEntry()
            record.depth = 0
            self.new_entry.put(record)
            self.sym_table[record.lexeme] = self.new_entry
        else:
            record.depth = self.existing_entry.depth
            self.existing_entry.put(record)

    def find(self, lexeme):
         return self.sym_table.get(lexeme, None)

    def __repr__(self):
        return self.sym_table


class ContextAttrs(object):

    def __init__(self):
        self.context_lexemes = []
        self.nesting_level = 1
        self.cur_offset = None
        # note: no need for size; len(ex.context_lexemes) works.
