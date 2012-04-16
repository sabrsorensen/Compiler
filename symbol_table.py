__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'


from semantic_entry import SemanticEntry
from semantic_record import SemanticRecord
from collections import OrderedDict

class SymbolTable(object):

    def __init__(self, parent):
        self.parent_table = parent
        self.name = ''
        self.cur_depth = 0
        self.context_attributes_stack = []
        self.cur_context_attributes = None
        self.sym_table = OrderedDict()
        self.record = SemanticRecord()

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
        self.record = record
        self.cur_context_attributes.context_lexemes.append(self.record.lexeme)
        self.record.offset = self.cur_depth
        self.cur_depth += self.record.size
        self.existing_entry = self.find(self.record.lexeme)
        if self.existing_entry is None:
            self.new_entry = SemanticEntry()
            self.record.depth = 0
            self.new_entry.put(self.record)
            self.sym_table[self.record.lexeme] = self.new_entry
        else:
            self.record.depth = self.existing_entry.depth
            self.existing_entry.put(self.record)

    def find(self, lexeme):
         return self.sym_table.get(lexeme, None)

    def __repr__(self):
        output = "\n[%s | %s | %s | %s | %s | %s]" %   ("lexeme", "kind",
                                                      "type", "size",
                                                      "offset", "depth")
        for k,v in self.sym_table.items():
            output = output + '\n' + v.cur_record.__repr__()
        return output


class ContextAttrs(object):

    def __init__(self):
        self.context_lexemes = []
        self.nesting_level = 1
        self.cur_offset = None
        # note: no need for size; len(ex.context_lexemes) works.
