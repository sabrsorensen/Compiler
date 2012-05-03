import logging
import traceback

__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

class SemanticAnalyzer():
    output = ''#output string

    def __init__(self, st_in):
        self.sym_table = st_in
        self.cur_label = 0

    def gen_label(self):
        label = self.cur_label
        self.cur_label += 1
        return label

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
        if self.sym_table.find(id_rec.lexeme):
            id_rec.type = self.sym_table.find(id_rec.lexeme).cur_record.type
        else:
            logging.error("Variable " + id_rec.lexeme + " referenced before declaration.\n")
            exit(0)
        #Type checking
        if id_rec.type != 'integer' and id_rec.type != 'Integer':
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
        self.output += "push " + str(trans_rec.offset) + "(d" + str(trans_rec.depth) + ")\n"
    def gen_push_int(self, int_rec_in):
        if int_rec_in.negative:
            self.output += "push #-" + str(int_rec_in.lexeme) + "\n"
        else:
            self.output += "push #" + str(int_rec_in.lexeme) + "\n"
    def gen_begin(self):
        self.output += 'mov d0 0(sp)\nmov sp d0\n'
    def gen_end(self):
        self.output += 'hlt\n'
    def gen_arithmetic(self,left_operand, operator, right_operand, rec_out):
        #Type check:
        if left_operand.type != right_operand.type:
            print "Type mismatch. " + str(left_operand.lexeme) + " not same type as " + str(right_operand.lexeme)
        if operator.lexeme == '+':
            self.output += "adds\n"
        elif operator.lexeme == '-':
            self.output += "subs\n"
        elif operator.lexeme == '*':
            self.output += "muls\n"
        elif operator.lexeme == 'div':
            self.output += "divs\n"
        elif operator.lexeme == 'mod':
            pass
        elif operator.lexeme == 'or':
            pass
        elif operator.lexeme == 'and':
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
            self.output += 'rd ' + str(read_param_rec.offset) + '(d' + str(read_param_rec.depth) + ')\n'
        else:
            logging.error("Variable " + read_param_rec.lexeme + " referenced before declaration.\n")
            exit(-1)
    """
    Possible additional "if" handling.
    """
    def begin_if(self, if_rec):
        if_rec.label1 = self.gen_label()
        if_rec.label2 = self.gen_label()
        if if_rec.lexeme == 'eq':
            self.output += "bne " + "-1(sp) "  + "sp" + ' L' + str(if_rec.label1) +'\n'
        elif if_rec.lexeme == 'lt':
            self.output += "bgt " + "-1(sp) "  + "sp" + ' L' + str(if_rec.label1) +'\n'
            self.output += "beq " + "-2(sp) "  + "-1(sp)" + ' L' + str(if_rec.label1) +'\n'
        elif if_rec.lexeme == 'gt':
            self.output += "blt " + "-1(sp) "  + "sp" + ' L' + str(if_rec.label1) +'\n'
            self.output += "beq " + "-2(sp) "  + "-1(sp)" + ' L' + str(if_rec.label1) +'\n'
        elif if_rec.lexeme == 'lte':
            self.output += "bgt " + "-1(sp) "  + "sp" + ' L' + str(if_rec.label1) +'\n'
        elif if_rec.lexeme == 'gte':
            self.output += "blt " + "-1(sp) "  + "sp" + ' L' + str(if_rec.label1) +'\n'
        elif if_rec.lexeme == 'ne':
            self.output += "beq " + "-1(sp) "  + "sp" + ' L' + str(if_rec.label1) +'\n'

    def end_if(self, if_rec):
        self.output += 'L'+ str(if_rec.label2) + ':\n'

    def opt_else(self, if_rec):
        self.output += 'br L' + str(if_rec.label2) + '\n'
        self.output += 'L' + str(if_rec.label1) + ':\n'

    def begin_repeat(self, rep_rec):
        rep_rec.label1 = self.gen_label()
        self.output += 'L' + str(rep_rec.label1) + ':\n'

    def end_repeat(self, rep_rec):
        if rep_rec.lexeme == 'eq':
            self.output += "bne " + "-1(sp) "  + "sp" + ' L' + str(rep_rec.label1) +'\n'
        elif rep_rec.lexeme == 'lt':
            self.output += "bgt " + "-1(sp) "  + "sp" + ' L' + str(rep_rec.label1) +'\n'
            self.output += "beq " + "-2(sp) "  + "-1(sp)" + ' L' + str(rep_rec.label1) +'\n'
        elif rep_rec.lexeme == 'gt':
            self.output += "blt " + "-1(sp) "  + "sp" + ' L' + str(rep_rec.label1) +'\n'
            self.output += "beq " + "-2(sp) "  + "-1(sp)" + ' L' + str(rep_rec.label1) +'\n'
        elif rep_rec.lexeme == 'lte':
            self.output += "bgt " + "-1(sp) "  + "sp" + ' L' + str(rep_rec.label1) +'\n'
        elif rep_rec.lexeme == 'gte':
            self.output += "blt " + "-1(sp) "  + "sp" + ' L' + str(rep_rec.label1) +'\n'
        elif rep_rec.lexeme == 'ne':
            self.output += "beq " + "-1(sp) "  + "sp" + ' L' + str(rep_rec.label1) +'\n'

    def begin_while(self, while_rec):
        while_rec.label1 = self.gen_label()
        while_rec.label2 = self.gen_label()

    def gen_while(self, while_rec, expr_rec):
        self.output += "l" + str(while_rec.label1) + ":\n"
        if expr_rec.lexeme == 'eq':
            self.output += "bne -1(sp) sp l" + str(while_rec.label2) + "\n"
        elif expr_rec.lexeme == 'lt':
            self.output += "bge -1(sp) sp l" + str(while_rec.label2) + "\n"
        elif expr_rec.lexeme == 'lte':
            self.output += "bgt -1(sp) sp l" + str(while_rec.label2) + "\n"
        elif expr_rec.lexeme == 'gt':
            self.output += "ble -1(sp) sp l" + str(while_rec.label2) + "\n"
        elif expr_rec.lexeme == 'gte':
            self.output += "blt -1(sp) sp l" + str(while_rec.label2) + "\n"
        elif expr_rec.lexeme == 'ne':
            self.output += "beq -1(sp) sp l" + str(while_rec.label2) + "\n"

    def end_while(self, while_rec):
        self.output += "br l" + str(while_rec.label1) + "\n"
        self.output += "l" + str(while_rec.label2) + ":\n"

    def begin_for(self, for_rec):
        for_rec.label1 = self.gen_label()
        for_rec.label2 = self.gen_label()

    def gen_for(self, for_rec):
        self.gen_while(for_rec, for_rec)

    def end_for(self,for_rec, control_var_rec, final_rec):
        self.gen_push_id(control_var_rec, None)
        if for_rec.lexeme == 'lte':
            self.output += "push #1\nadds\n"
        elif for_rec.lexeme == 'gte':
            self.output += "push #1\nsubs\n"
        temp = self.sym_table.find(control_var_rec.lexeme).cur_record
        self.output += "pop " + str(temp.offset) + "(d" + str(temp.depth) + ")\n"
        self.gen_push_id(control_var_rec, None)
        if self.sym_table.find(final_rec.lexeme):
            self.gen_push_id(final_rec, None)
        else:
            self.gen_push_int(final_rec)

        self.output += "br l" + str(for_rec.label1) + "\n"
        self.output += "l" + str(for_rec.label2) + ":\n"
