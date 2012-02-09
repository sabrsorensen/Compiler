import re
import os
import sys
import logging
#from user import f

log = logging.getLogger()
ch  = logging.StreamHandler()
log.addHandler(ch)
log.setLevel(logging.DEBUG)

class Scanner():
    
    def __init__(self):
        self.id_pattern =  r'(^(_|[a-zA-Z])[_a-zA-Z0-9]*$)'
        self.symbols = ['.', ',', ';', '(', ')', '=', '>', '<', '+', '-', '*', ':']
        #self.generic_num_pattern = r'^([0-9]+([\.][0-9]+([eE]([+-])?[0-9]+)?)?)+$'
        self.generic_num_pattern = r'^([0-9]+(\.?([0-9]+)?)([eE])?([-+])?([0-9]+)?)+$'
        self.integer_lit_pattern = r'^([0-9])+$'
        self.fixed_lit_pattern = r'^([0-9])+(\.)([0-9])+$'
        self.float_lit_pattern = r'^[0-9]+(\.[0-9]+)?[eE][+-]?([0-9])+$'
        self.string_lit_pattern = r'^\'(\'\'|[^\'\n])*\'$'
        self.file = None
        self.column = 1
        self.line = 1
        self.tokens = []
        self.keywords = {'and':'MP_AND',
                         'begin':'MP_BEGIN',
                         'div':'MP_DIV',
                         'do':'MP_DO',
                         'downto':'MP_DOWNTO',
                         'else':'MP_ELSE',
                         'end':'MP_END',
                         'fixed':'MP_FIXED',
                         'float':'MP_FLOAT',
                         'for':'MP_FOR',
                         'function':'MP_FUNCTION',
                         'if':'MP_IF',
                         'integer':'MP_INTEGER',
                         'mod':'MP_MOD',
                         'not':'MP_NOT',
                         'or':'MP_OR',
                         'procedure':'MP_PROCEDURE',
                         'program':'MP_PROGRAM',
                         'read':'MP_READ',
                         'repeat':'MP_REPEAT',
                         'then':'MP_THEN',
                         'to':'MP_TO',
                         'until':'MP_UNTIL',
                         'var':'MP_VAR',
                         'while':'MP_WHILE',
                         'write':'MP_WRITE'}

        self.sym_dict = {
                        r'\.': 't_period',
                        r',': 't_comma',
                        r'\(': 't_l_paren',
                        r'\)': 't_r_paren',
                        r'=': 't_eq',
                        r'>': 't_gt',
                        r'<': 't_lt',
                        r':': 't_colon',
                        r'\+': 't_plus',
                        r'-': 't_minus',
                        r'\*': 't_mul',
                        r'[a-zA-Z]': 't_id_key', # unfortunately, \w matches all alphanumeric characters and underscore
                        r'\d': 't_num',
                        r'\'': 't_string',
                        r'{': 't_l_comment',
                        r'}': 't_r_comment',
                        r'_': 't_id_key',
                        r';': 't_semicolon',
                        r'\t| ': 't_white_space',
            }
        
    def open_file(self, input_file):
        self.file = open(input_file)

    def create_token(self, token_type, token_line, token_column, token_name ):
        s = Token(token_type,token_line,token_column, token_name)
        self.tokens.append(s)

    def get_token(self):
        next = self.scanner_read_char()
        while len(next) is not 0:
            for pattern, f_name in self.sym_dict.items():
                result = re.match(pattern, next)
                if result:
                    getattr(self, self.sym_dict.get(pattern, 't_error'))(result.group(0))

            next = self.scanner_read_char()

    ######### helper functions ############
    def scanner_read_char(self):
        logging.debug('Scanner Read Char is called')
        cur = self.file.read(1)
        if cur == '\n':                 #If we see new line, increment line counter and reset column
            self.line += 1
            self.column = 1
            cur = self.file.read(1)
        elif cur == '\r'  :
            self.column = 1
            cur = self.file.read(1)
        else:
            self.column += 1            #if not new line, increment column counter
        logging.debug('Char is: %s' % cur)
        return cur

    def rewind(self):
        self.file.seek(-1, 1)
        self.column -= 1
        if self.column < 0:
            self.column = 0

    def get_lexeme(self):
        pass

    def get_line(self):
        return self.line

    def get_column(self, token_length):
        self.column -=1
        return self.column - token_length

    def err_invalid_token(self):
        pass

    ############## FSAs ###################

    def t_white_space(self, in_char):
        return

    def t_period(self, in_char):
        token_type = 'MP_PERIOD'
        self.create_token(token_type, self.get_line(),
                            self.get_column(len(in_char)), in_char)

    def t_comma(self, in_char):
        token_type = 'MP_COMMA'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_semicolon(self, in_char):
        token_type = 'MP_SCOLON'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_l_paren(self, in_char):
        token_type = 'MP_LPAREN'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_r_paren(self, in_char):
        token_type = 'MP_RPAREN'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_eq(self, in_char):
        token_type = 'MP_EQUAL'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_plus(self, in_char):
        token_type = 'MP_PLUS'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_minus(self, in_char):
        token_type = 'MP_MINUS'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    def t_mul(self, in_char):
        token_type = 'MP_TIMES'
        self.create_token(token_type, self.get_line(),
            self.get_column(len(in_char)), in_char)

    #Complex sub-methods, can have different types of tokens created

    def t_gt(self, in_char):
        lexeme = in_char
        token = 'MP_GTHAN'
        next = self.scanner_read_char()
        if next == '=':
            lexeme = in_char + next
            token = 'MP_GEQUAL'
            self.create_token(token, self.get_line(),
                self.get_column(len(in_char)), lexeme)
            return
        else:
            self.rewind()
            self.create_token(token, self.get_line(),
                                self.get_column(len(in_char)), lexeme)

    def t_lt(self, in_char):
        lexeme = in_char
        token = 'MP_LTHAN'
        next = self.scanner_read_char()
        if next == '=':
            lexeme = in_char + next
            token = 'MP_LEQUAL'
            self.create_token(token, self.get_line(),
                self.get_column(len(in_char)), lexeme)
            return
        elif next == '>':
            lexeme = in_char + next
            token = 'MP_NEQUAL'
            self.create_token(token, self.get_line(),
                self.get_column(len(in_char)), lexeme)
            return
        else:
            self.rewind()
            self.create_token(token, self.get_line(),
                self.get_column(len(in_char)), lexeme)

    def t_colon(self, in_char):
        lexeme = in_char
        token = 'MP_COLON'
        next = self.scanner_read_char()
        if next == '=':
            lexeme = in_char + next
            token = 'MP_ASSIGN'
            self.create_token(token, self.get_line(),
                self.get_column(len(in_char)), lexeme)
            return
        else:
            self.rewind()
            self.create_token(token, self.get_line(),
                self.get_column(len(in_char)), lexeme)

    def t_id_key(self, in_char):
        final_lexeme = in_char
        temp = in_char
        result = re.match(self.id_pattern, temp)
        while result:
            final_lexeme = temp
            next = self.scanner_read_char()
            temp += next
            result = re.match(self.id_pattern, temp)

        # popped out of the while loop - means we got our id
        # first, rewind
        self.rewind()

        # check if the id we have is a keyword
        for lexeme, token in self.keywords.items():
            if final_lexeme == lexeme:
                self.create_token(token, self.get_line(),
                                    self.get_column(len(final_lexeme)), final_lexeme)
                return

        # we have an identifier
        token_type = 'MP_IDENTIFIER'
        self.create_token(token_type, self.get_line(),
                            self.get_column(len(final_lexeme)), final_lexeme)

    def t_num(self, in_char):
        lexeme = in_char
        #generic_num_pattern matches integers, fixed, and float
        while re.match(self.generic_num_pattern, lexeme):
            lexeme += self.scanner_read_char()
        lexeme = lexeme[0:-1]
        self.rewind()
        #find out what kind of number was found
        if re.match(self.float_lit_pattern, lexeme):
            self.create_token("MP_FLOAT_LIT", self.get_line(),
                                self.get_column(len(lexeme)),lexeme)
            return
        elif re.match(self.fixed_lit_pattern, lexeme):
            self.create_token("MP_FIXED_LIT", self.get_line(),
                                self.get_column(len(lexeme)), lexeme)
            return
        elif re.match(self.integer_lit_pattern, lexeme):
            self.create_token("MP_INTEGER_LIT", self.get_line(),
                                self.get_column(len(lexeme)), lexeme)
        else:
            #invalid token found
            pass

    def t_string(self, in_char):
        lexeme = in_char
        new_char = ''
        while  new_char != '\'':
            new_char = self.scanner_read_char()
            lexeme += new_char
        new_char = self.scanner_read_char()
        if new_char == '\'':
            lexeme += new_char
            new_char = ''
            while new_char != '\'':
                new_char = self.scanner_read_char()
                lexeme += new_char
        else:
            self.rewind()
        if re.match(self.string_lit_pattern,lexeme):
            self.create_token("MP_STRING_LIT", self.get_line(),
                self.get_column(len(lexeme)), lexeme)
        else:
            #invalid token found
            pass

    def t_l_comment(self, in_char):
        next = ''
        while next != '}':
            next = self.scanner_read_char()

    def t_r_comment(self, in_char):
        pass



class Token(object):
    """This class is used to create token objects for the token file"""

    def __init__(self, token_type, line, column, token_value):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.token_value = token_value

    def __repr__(self):
        return "%16s %6s %4s   %s\n" % (self.token_type, self.line, self.column, self.token_value)
