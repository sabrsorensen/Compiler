__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import logging
from semantic_record import SemanticRecord
from symbol_table import ContextAttrs
from semantic_entry import SemanticEntry


class SymbolTable(object):

    def __init__(self, name, depth):
        self.name = name
        self.cur_depth = depth
        self.sem_records = [] #Do we need this?
        self.context_attributes_stack = []
        self.cur_context_attributes
        self.sym_table = {}

    def create(self, newRecord): #subtables
        self.cur_context_attributes = ContextAttrs()
        self.cur_depth += 1

    def create(self): #Root table
        self.cur_context_attributes = ContextAttrs()

    def destroy(self):
        self.cur_lexeme = ''


    def insert(self, record):
        self.cur_context_attributes.context_lexemes.append(record.lexeme, record.size)
        record.offset = self.cur_depth
        self.cur_depth += record.size
        self.existing_entry = self.find(record.lexeme)
        if existing_entry == None:
            self.new_entry = SemanticEntry()
            record.depth = 0
            self.new_entry.put(record)
            self.sym_table[record.lexeme] = self.new_entry
        else:
            record.depth = existing_entry.depth
            existing_entry.put(record)

    def find(self, lexeme):
        return sym_table[lexeme]

    def __repr__(self):
        return "%s" % self.sym_table


class ContextAttrs(object):

    def __init__(self):
        self.context_lexemes = []
        self.nesting_level = 1
        self.cur_offset = None
        # note: no need for size; len(ex.context_lexemes) works.
