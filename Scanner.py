import re
import os
import sys
from user import f

log = logging.getLogger()
ch  = logging.StreamHandler()
log.addHandler(ch)
log.setLevel(logging.DEBUG)

class Scanner():


    def __init__(self, in_file=None):
        self.file = in_file
        self.column
        self.line
        self.symbols = ['\.',',','(',')','=','>','<',':','+','-','*','\w','\d','\'','{','}']
        self.tokens = []
        self.keywords = {'and':'MP_AND','begin':'MP_BEGIN','div':'MP_DIV','do':'MP_DO',
                         'downto':'MP_DOWNTO','else':'MP_ELSE','end':'MP_END','fixed':'MP_FIXED',
                         'float':'MP_FLOAT','for':'MP_FOR','function':'MP_FUNCTION','if':'MP_IF',
                         'integer':'MP_INTEGER','mod':'MP_MOD','not':'MP_NOT','or':'MP_OR',
                         'procedure':'MP_PROCEDURE','program':'MP_PROGRAM','read':'MP_READ',
                         'repeat':'MP_REPEAT','then':'MP_THEN','to':'MP_TO','until':'MP_UNTIL',
                         'var':'MP_VAR','while':'MP_WHILE','write':'MP_WRITE'}

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
            }
        
    def open_file(self, input_file):
        self.file = open(input_file)

    def create_token(self, token_type, token_line, token_column, token_name ):
        s = Token(token_type,token_line,token_column, token_name)
        tokens.append(s)

    def get_token(self):
        #cur = self.file.read(1)
        cur = 'a'
        while cur is not '':
            for pattern, f_name in self.sym_dict.items():
                result = re.match(pattern, cur)
                # print 'blah'
                logging.debug('Result: %s' % result)
                if result.group(0):
                    cur = getattr(self, self.sym_dict.get(pattern, 't_error'))(result.group(0))
                    break



    def get_lexeme(self):
        pass
    def get_line(self):
        return self.line
    def get_column(self):
        return self.column
    def err_invalid_token(self):
        pass



    '''
    Distributor Sub-Methods
    Functions take as input the last character read.
    Then perform whatever is necessary to determine if the given token and subsequent characters give a valid token
    If a valid token is found, instantiate a new token object and append to list of tokens
    If no valid token is found, call err_invalid_token()
        This kills the scanner
    Pre-condition: file object points at character after last read
    Post-condition: file object points at character 2 after the end of last complete token

    e.g. input is "...dog+cat=hamster ..."
    distributor gets to 'd', and file object is now pointing at 'o'
    so distributor passes 'd' to t_id_key(), t_id_key() finds 'dog', creates a token, and adds it to list
    t_id_key() passes '+' back to the distributor, and file object now points at 'c'
    '''
    def t_period(self, in_char):
        token_type = 'MP_PERIOD'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_comma(self, in_char):
        token_type = 'MP_COMMA'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_semicolon(self, in_char):
        token_type = 'MP_SCOLON'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_l_paren(self, in_char):
        token_type = 'MP_LPAREN'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_r_paren(self, in_char):
        token_type = 'MP_RPAREN'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_eq(self, in_char):
        token_type = 'MP_EQUAL'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_plus(self, in_char):
        token_type = 'MP_PLUS'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_minus(self, in_char):
        token_type = 'MP_MINUS'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_mul(self, in_char):
        token_type = 'MP_TIMES'
        line = self.get_line()
        column = self.get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
        #Complex sub-methods, can have different types of tokens created
    def t_gt(self, in_char):
        pass
    def t_lt(self, in_char):
        pass
    def t_colon(self, in_char):
        pass
    def t_id_key(self, in_char):
        logging.debug('Yay! it is a letter: %s' % in_char)
        return ''
        pass
    def t_num(self, in_char):
        pass
    def t_string(self, in_char):
        pass
    def t_l_comment(self, in_char):
        pass
    def t_r_comment(self, in_char):
        pass

    def scanner_read_char(self):
        self.cur = self.file.read(1)
        if cur is '\n':
            self.line += 1
            self.column = 0
        if cur is not '\n':
            self.column += 1
        return self.cur


class Token(object):
    def __init__(self, token_type, line, column, token_value):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.token_value = token_value
    def __repr__(self):
        return "%16s %6s %4s %s\n" % (self.token_type, self.line, self.column, self.token_value)

s = Scanner()
s.open_file(r'.\sample.txt')
s.get_token()
