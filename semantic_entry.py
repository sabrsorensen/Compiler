__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

class SemanticEntry(object):

    def __init__(self):
        #instead of empty, do my_sem_entry.semantic_record_stack
        self.depth = 0
        self.cur_record = None
        self.semantic_record_stack = []


    def put(self, record):
        if self.cur_record:
            self.semantic_record_stack.insert(0,self.cur_record)
        self.cur_record = record
        self.depth += 1

    def back_out(self):
        if self.semantic_record_stack:
            self.cur_record = self.semantic_record_stack.pop()
        else:
            self.cur_record = None
        self.depth -= 1

    def __repr__(self):
        return "%s %s" % (self.cur_record, self.semantic_record_stack)