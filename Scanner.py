import re

class Scanner():

    keywords = {'and':'MP_AND','begin':'MP_BEGIN','div':'MP_DIV','do':'MP_DO',
                'downto':'MP_DOWNTO','else':'MP_ELSE','end':'MP_END','fixed':'MP_FIXED',
                'float':'MP_FLOAT','for':'MP_FOR','function':'MP_FUNCTION','if':'MP_IF',
                'integer':'MP_INTEGER','mod':'MP_MOD','not':'MP_NOT','or':'MP_OR',
                'procedure':'MP_PROCEDURE','program':'MP_PROGRAM','read':'MP_READ',
                'repeat':'MP_REPEAT','then':'MP_THEN','to':'MP_TO','until':'MP_UNTIL',
                'var':'MP_VAR','while':'MP_WHILE','write':'MP_WRITE'}
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