import logging
from symbol_table import SymbolTable

__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

class SemanticAnalyzer():
    output = ''#output string

    def __init__(self):
        self.sym_table = None

    def gen_add_sp(self, size):
        #
        self.output += "add sp #" + size + " sp\n"

    def gen_ass_statement(self,id_rec, expr_rec):
        #
        if id_rec.type != expr_rec.type:
            #invalid type match
            logging.error("Type match error!")
            exit(0)
        self.output += "; Oh hey, we're assigning stuff to " + id_rec.lexeme
        trans_rec = self.sym_table.find(id_rec.lexeme).cur_rec #is cur_rec right?
        self.output += "pop " + trans_rec.offset + "(d" + trans_rec.depth + ")\n"

    #Stub methods from here down.
    def process_id(self, id_rec):
        return
    def gen_push_id(self, id_rec, rec_out):
        if id_rec.type != "Integer":
            logging.error("lol, type error.")
            return False
        trans_rec = self.sym_table.find(id_rec.lexeme).cur_rec #is cur_rec right?
        self.output += "push " + trans_rec.offset + "(d" + trans_rec.depth + ")\n"
        return True

    def gen_push_int(self, int_rec_in):
        self.output += "push #"+ int_rec_in.lexeme + "\n"
    def gen_begin(self):
        self.output += "push d0\nmov sp d0\n"
    def gen_end(self):
        self.output += "hlt\n"
    def gen_arithmetic(self,left_operand, operator, right_operator, rec_out):
        pass
    def to_file(self, file_name):
        try:
            output_file = open('a.out','w')
            output_file.write(self.output)
            output_file.close()
        except IOError as (errno, strerror):
            logging.error("I/O error(%s): %s" % errno,strerror)

    """
    Possible additional "if" handling.
    """