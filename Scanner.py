import re

class Scanner():

    def __init__(self, in_file):
        self.file = in_file
        self.symbols = ['.', ',', '(', ')', '=', '+', '-', '*']
        self.hash =

    def open_file(self, input_file):
        self.file = open(input_file)

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

    #distributor sub-methods
    def t_period(self):
        pass
    def t_comma(self):
        pass
    def t_semicolon(self):
        pass
    def t_l_paren(self):
        pass
    def t_r_paren(self):
        pass
    def t_eq(self):
        pass
    def t_gt(self):
        pass
    def t_lt(self):
        pass
    def t_colon(self):
        pass
    def t_plus(self):
        pass
    def t_minus(self):
        pass
    def t_mul(self):
        pass
    def t_id_key(self):
        pass
    def t_num(self):
        pass
    def t_string(self):
        pass
    def t_l_comment(self):
        pass
    def t_r_comment(self):
        pass




s = Scanner()
s.open_file('C:\Users\Anna\Documents\Code\Aptana\workspace\Compiler\sample.txt')
s.get_token()