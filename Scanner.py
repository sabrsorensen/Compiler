import re
from user import f


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

    def open_file(self, input_file):
        self.file = open(input_file)

    def create_token(self, token_type, token_line, token_column, token_name ):
        s = Token(token_type,token_line,token_column, token_name)
        tokens.append(s)

    def get_token(self):
        cur = self.file.read(1)
        val = 0
        for pattern in t_dict:
            result = re.match(pattern, cur)
            if result.group(0):
                val = t_dict.index(pattern)


        

        re.sub(r'\s', '', line)
        print line


    def get_lexeme(self):
        pass
    def get_line(self):
        pass
    def get_column(self):
        pass
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
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_comma(self, in_char):
        token_type = 'MP_COMMA'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_semicolon(self, in_char):
        token_type = 'MP_SCOLON'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_l_paren(self, in_char):
        token_type = 'MP_LPAREN'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_r_paren(self, in_char):
        token_type = 'MP_RPAREN'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_eq(self, in_char):
        token_type = 'MP_EQUAL'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_plus(self, in_char):
        token_type = 'MP_PLUS'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_minus(self, in_char):
        token_type = 'MP_MINUS'
        line = get_line()
        column = get_column()
        token = in_char
        self.create_token(token_type, line, column, token)
        cur_char = f.read(1)
        return cur_char
    def t_mul(self, in_char):
        token_type = 'MP_TIMES'
        line = get_line()
        column = get_column()
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


class Token(object):
    def __init__(self, token_type, line, column, token_value):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.token_value = token_value
    def __repr__(self):
        return "%16s %6s %4s %s" % (self.token_type, self.line, self.column, self.token_value)

s = Scanner()
s.open_file(r'.\sample.txt')
s.get_token()

