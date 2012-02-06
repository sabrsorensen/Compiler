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
        fixed_lit_pattern = r'^([0-9])+(\.)([0-9])+$'
        integer_lit_pattern = r'^([0-9])+$'
        float_lit_pattern = r'^[0-9]+(\.[0-9]+)?[eE][+-]?([0-9])+$'
        string_lit_pattern = r'^\'(\'\'|[^\'\n])*\'$'
        self.file = None
        self.column = 0
        self.line = 0
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
            r'\t ': 't_white_space',
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
                break
            next = self.scanner_read_char()


    def scanner_read_char(self):
        cur = self.file.read(1)
        if cur == '\n':     #If we see new line, increment line counter and reset column
            self.line += 1
            self.column = 0
        else:               #if not new line, increment column counter
            self.column += 1
        return cur

    def get_lexeme(self):
        pass

    def get_line(self):
        return self.line

    def get_column(self):
        return self.column

    def err_invalid_token(self):
        pass



#    Distributor Sub-Methods
#    Functions take as input the last character read.
#    Then perform whatever is necessary to determine if the given token and subsequent characters give a valid token
#    If a valid token is found, instantiate a new token object and append to list of tokens
#    If no valid token is found, call err_invalid_token()
#        This kills the scanner
#    Pre-condition: file object points at character after last read
#    Post-condition: file object points at character 2 after the end of last complete token
#
#    e.g. input is "...dog+cat=hamster ..."
#    distributor gets to 'd', and file object is now pointing at 'o'
#    so distributor passes 'd' to t_id_key(), t_id_key() finds 'dog', creates a token, and adds it to list
#    t_id_key() passes '+' back to the distributor, and file object now points at 'c'

    def t_white_space(self, in_char):
        return

    def t_period(self, in_char):
        token_type = 'MP_PERIOD'
        self.create_token(token_type, self.get_line(),
                            self.get_column(), in_char)

    def t_comma(self, in_char):
        token_type = 'MP_COMMA'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_semicolon(self, in_char):
        token_type = 'MP_SCOLON'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_l_paren(self, in_char):
        token_type = 'MP_LPAREN'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_r_paren(self, in_char):
        token_type = 'MP_RPAREN'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_eq(self, in_char):
        token_type = 'MP_EQUAL'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_plus(self, in_char):
        token_type = 'MP_PLUS'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_minus(self, in_char):
        token_type = 'MP_MINUS'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    def t_mul(self, in_char):
        token_type = 'MP_TIMES'
        self.create_token(token_type, self.get_line(),
            self.get_column(), in_char)

    #Complex sub-methods, can have different types of tokens created

    def t_gt(self, in_char):
        pass

    def t_lt(self, in_char):
        pass

    def t_colon(self, in_char):
        pass

    def t_id_key(self, in_char):
        logging.debug('In t_id_key')
        final_lexeme = in_char
        temp = in_char
        result = re.match(self.id_pattern, temp)
        while result:
            final_lexeme = temp
            next = self.scanner_read_char()
            logging.debug('Next token: %s' % next)
            temp += next
            result = re.match(self.id_pattern, temp)

        # popped out of the while loop - means we got our id
        # first, rewind
        logging.debug('Temp after id is formed: %s' % temp)
        self.file.seek(-1, 1)

        # check if the id we have is a keyword

        for lexeme, token in self.keywords.items():
            if final_lexeme == lexeme:
                self.create_token(token, self.get_line(),
                                    self.get_column(), final_lexeme)
                return

        # we have an identifier
        token_type = 'MP_IDENTIFIER'
        self.create_token(token_type, self.get_line(),
                            self.get_column(), final_lexeme)

    def t_num(self, in_char):
        pass

    def t_string(self, in_char):
        pass

    def t_l_comment(self, in_char):
        next = ''
        while next != '}':
            next = self.scanner_read_char()

    def t_r_comment(self, in_char):
        pass



class Token(object):

    def __init__(self, token_type, line, column, token_value):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.token_value = token_value

    def __repr__(self):
        return "%16s %6s %4s %s\n" % (self.token_type, self.line, self.column, self.token_value)
