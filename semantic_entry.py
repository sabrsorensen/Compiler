__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

# according to PEP, class names are written in CamelBack notation
# My mistake. Should we rename the filenames as well?
class SemanticEntry(object):

    def __init__(self):
        #instead of empty, do my_sem_entry.semantic_record_stack
        self.depth = 0
        self.cur_record = None
        self.semantic_record_stack = []


    def put(self, record):
        self.semantic_record_stack.append(record)
        self.cur_record = record
        self.depth += 1

    def back_out(self):
        if self.semantic_record_stack:
            self.cur_record = self.semantic_record_stack.pop()
        else:
            self.cur_record = None
        self.depth -= 1

    # We don't really need the following three functions, python instance variables are public by default.
    # Can I pull them out then, along with to_string?
#    def get_current_record(self):
#        return self.current_record
#
#    def is_empty(self):
#        return self.empty
#
#    def get_depth(self):
#        return self.depth

    # Sam, remember __repr__ ? :)
    # Hmm, nifty function.
    def __repr__(self):
        return "%s %s" % (self.cur_record, self.semantic_record_stack)

#    def to_string(self):
#        self.output.append(self.current_record)
#        if self.semantic_record_stack is not None:
#            for sem_record in semantic_record_stack:
#                self.output.append(sem_record)
#                self.output.append(" ")
#
#        self.output.append('\n')
#        return output
