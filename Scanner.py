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
        #### Regular Expressions ####
        self.id_pattern =  r'(^(_|[a-zA-Z])[_a-zA-Z0-9]*$)'
        #Matches any number, or partial number still being scanned
        self.generic_num_pattern = r'^([0-9]+(\.?([0-9]+)?)([eE])?([-+])?([0-9]+)?)+$'
        self.integer_lit_pattern = r'^([0-9])+$'
        self.fixed_lit_pattern = r'^([0-9])+(\.)([0-9])+$'
        self.float_lit_pattern = r'^[0-9]+(\.[0-9]+)?[eE][+-]?([0-9])+$'
        self.string_lit_pattern = r'^\'(\'\'|[^\'\n])*\'$'

        self.file = None
        self.column = 0         #current column indicator, accessible by all methods
        self.line = 1           #current column indicator, accessible by all methods
        self.no_errors = True   #binary flag used by distributor to tell if an error token has been produced
                                #modified by err_invalid_token()
        self.tokens = []        #list of generated tokens

        #keyword ==> <keyword token> lookup dictionary
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

        #input char type ==> method dictionary
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

    def err_invalid_token(self, token_type, token_line, token_column, lexeme_char):
        s = Token(token_type, token_line, token_column, lexeme_char)
        self.tokens.append(s)
        self.no_errors = False

    def get_token(self):
        next = self.scanner_read_char()
        while len(next) is not 0 and self.no_errors:
            bad_char = True
            for pattern, f_name in self.sym_dict.items():
                result = re.match(pattern, next)
                if result:
                    #invalid character found
                    getattr(self, self.sym_dict.get(pattern, 't_error'))(result.group(0))
                    bad_char = False
            if bad_char and next != '\n':
                #invalid character found
                self.err_invalid_token("MP_ERROR",self.column, self.line, next)
                logging.error('Scanning error: Input char: %s is not a valid character in the language.' % (next))
            next = self.scanner_read_char()
        #add end of file token
        self.create_token("MP_EOF", self.get_line(),
                          self.get_column(len(' ')), '')

    ######### helper functions ############
    def scanner_read_char(self):
        cur = self.file.read(1)
        line_msg = ''
        if cur == '\n':                 #If we see new line, increment line counter and reset column
            line_msg = ', and found new line.'
            self.line += 1
            self.column = 0
        elif cur == '\r':
            self.column = 1
            cur = self.file.read(1)
        else:
            self.column += 1            #if not new line, increment column counter
            #logging.debug('Column Incremented! %s' % self.column)
        temp_cur = cur
        if temp_cur == '\n':
            temp_cur = '\\n'
        logging.debug('Char is: %2s current line: %s current col: %s%s' % (temp_cur, self.line, self.column, line_msg))
        line_msg = ''
        return cur

    #Back the file pointer up, can't back up past beginning of line
    def rewind(self):
        self.file.seek(-2, 1)
        cur = self.scanner_read_char()
        if cur == '\n':
            self.line -= 1
        self.column -= 2
        if self.column < 0:
            self.column = 1

    def get_lexeme(self):
        pass

    #return current file pointer line
    def get_line(self):
        return self.line

    #return current file pointer column
    def get_column(self, token_length):
        return self.column - token_length + 1

    ############## FSAs ###################

    def t_white_space(self, in_char):
        if in_char == '\t':
            self.column = self.column + 4 - (self.column % 4)
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
            logging.error('Scanning Error: Partial number type found, but incomplete token.')
            self.err_invalid_token("MP_ERROR",self.get_line(), self.get_column(len(lexeme)), lexeme)

    def t_string(self, in_char):
        lexeme = in_char
        cur_col = self.get_column(len(lexeme))
        cur_line = self.get_line()
        new_char = in_char
        go = True
        #scanning string
        while go:
            new_char = self.scanner_read_char()
            lexeme += new_char
            #found potential end of string
            if new_char == '\'':
                go = False
                cur_col = self.get_column(len(lexeme))
                new_char = self.scanner_read_char()
                #check for ''
                if new_char == '\'':
                    lexeme += new_char
                    go = True
            elif new_char == "\n":
                lexeme = lexeme[0:-1] + '\\n'
                go = False
        self.rewind()
        if re.match(self.string_lit_pattern,lexeme):
            # strip quotes from a string literal
            lexeme = lexeme.strip('\'')
            self.create_token("MP_STRING_LIT", cur_line,
                cur_col, lexeme)
        else:
            if new_char == '\n':
                logging.debug("Run on string beginning at line: %s, col: %s" % (cur_line,cur_col))
                self.err_invalid_token("MP_RUN_STRING",cur_line,
                    cur_col, lexeme)
            else:
                logging.debug("Scanning error: invalid string match")
                self.err_invalid_token("MP_ERROR",cur_line,
                    cur_col, lexeme)

    def t_l_comment(self, in_char):
        lexeme = in_char
        cur_col = self.get_column(len(lexeme))
        cur_line = self.get_line()
        go = True
        while go:
            next = self.scanner_read_char()
            lexeme += next
            if next == '}':
                go = False
            elif next == '':
                go = False
                logging.error('Reached end of file while parsing. Run on comment beginning at line: %s, col: %s' % (cur_line,cur_col))
                self.err_invalid_token("MP_RUN_COMMENT",cur_line,
                    cur_col, '{')

    def t_r_comment(self, in_char):
        logging.error('Found a stray right comment.')
        self.err_invalid_token("MP_ERROR",self.get_line(),
            self.get_column(1), '}')


class Token(object):
    """This class is used to create token objects for the token file"""

    def __init__(self, token_type, line, column, token_value):
        self.token_type = token_type
        self.line = line
        self.column = column
        self.token_value = token_value

    #how Token objects are represented in string format
    #TOKEN_ID        COL   LINE  LEXEME
    def __repr__(self):
        return "%s %s  %s  %s" % (self.token_type.ljust(16, ' '),
                                      str(self.line).ljust(4, ' '),
                                      str(self.column).ljust(4, ' '),
                                      self.token_value)
