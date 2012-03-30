__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import logging

class SymbolTable(object):

    def __init__(self, name, depth):
        self.name = name
        self.depth = depth
        self.sem_records = []


class ContextAttrs(object):

    def __init__(self):
        self.context_lexemes = []
        self.nesting_level = 1
        self.cur_offset = None
        # note: no need for size; len(ex.context_lexemes) works.

