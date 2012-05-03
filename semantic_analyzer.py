import logging
import traceback
from symbol_table import SymbolTable

__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

class SemanticAnalyzer():
    output = ''#output string

    def __init__(self, st_in):
        self.sym_table = st_in

    def gen_add_sp(self, size):
        #
        self.output += "add sp #" + size + " sp\n"

    def gen_ass_statement(self,id_rec, expr_rec):
        # todo add type matching back in, commented for testing
        '''
        if id_rec.type != expr_rec.type:
            #invalid type match
            logging.error("Type match error!")
            exit(0)
        '''
        temp = self.sym_table.find(id_rec.lexeme)
        if temp:
            trans_rec = temp.cur_record
        else:
            traceback.print_stack()
            print "Failed to find semantic entry."
            exit(0)
        self.output += "pop " + str(trans_rec.offset) + "(d" + str(trans_rec.depth) + ")\n"
    #Stub methods from here down.
    def process_id(self, id_rec):
        pass
    def gen_push_id(self, id_rec, rec_out):
        #Type checking
        if id_rec.type != 'Integer':
            traceback.print_stack()
            print "Type match error!"
            exit(0)
        temp = self.sym_table.find(id_rec.lexeme)
        if temp:
            trans_rec = temp.cur_record
        else:
            traceback.print_stack()
            print "Failed to find semantic entry."
            exit(0)
        self.output += "push" + str(trans_rec.offset) + "(d" + str(trans_rec.depth) + ")\n"
    def gen_push_int(self, int_rec_in):
        self.output += "push #" + str(int_rec_in.lexeme) + "\n"
    def gen_begin(self):
        self.output += 'mov d0 0(sp)\nmov sp d0\n'
    def gen_end(self):
        self.output += 'hlt\n'
    def gen_arithmetic(self,left_operand, operator, right_operator, rec_out):
        pass
    def to_file(self, file_name):
        pass
    def write_IR(self):
        print self.output
    def gen_write(self, expr_rec):
        self.output += 'wrts\n'
    def gen_read(self, read_param_rec):
        if self.sym_table.find(read_param_rec.lexeme) is not None:
            read_param_rec = self.sym_table.find(read_param_rec.lexeme).cur_record
            self.output += 'read ' + str(read_param_rec.offset) + '(d' + str(read_param_rec.depth) + ')\n'
        else:
            logging.error("Variable " + read_param_rec.lexeme + " referenced before declaration.\n")
            exit(-1)
    """
    Possible additional "if" handling.
    """