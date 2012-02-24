
import sys
import re
import logging
from Scanner import Scanner
from Scanner import Token

class Parser(object):


    def __init__(self, tokens):
        self.parsed = ''
        self.cur_token = ''
        self.index = len(tokens)
        self.tokens = iter(tokens)

    def error(self):
        pass

    def lookahead(self):
        if self.tokens.next().token_type == 'MP_EOF':
            logging.info('Done Parsing.')
            exit()
        else:
            self.cur_token = self.tokens.next()

    def match(self, token):
        return self.cur_token.token_type == token

    def system_goal(self): #Someone message Sam and let him know if this is what the stubs should be looking like
        self.lookahead()
        if self.match('MP_PROGRAM'):
            self.program()
            self.lookahead()
        else:
            self.error()

        if self.match('$'):
            logging.info('Matched end of program')
        else:
            self.error()

    def program(self):
        """ Expanding -----Program = ProgramHeading ";" Block "."-----"""
        self.program_heading()

        self.lookahead()
        if self.match('MP_SCOLON'):
            logging.info('Matched a Semicolon.')
            self.lookahead()
        else:
            self.error()

        self.block()

        self.lookahead()
        if self.match('MP_PERIOD'):
            logging.info('Matched a period.')
        else:
            self.error()

    def program_heading(self):
        """"Expanding -----"program" Identifier-----"""
        if self.match('MP_PROGRAM'):
            logging.info('Matched %s' % self.cur_token.lexeme)
            self.lookahead()
        else:
            self.error()

        self.identifier()

    def block(self):

        if self.match('MP_VAR'):
            self.lookahead()
            self.variable_declaration_part()
            self.lookahead()
        if self.match('MP_PROCEDURE'):
            self.lookahead()
            self.procedure_function_declaration_part()
            self.lookahead()
        if self.match('MP_BEGIN'):
            self.lookahead()
            self.statement_part()
        else:
            self.error()

    def variable_declaration_part(self):
        if self.match('MP_IDENTIFIER'):
            self.variable_declaration()
            self.lookahead()
        else:
            self.error()
        if self.match('MP_SCOLON'):
                self.lookahead()
                if self.match('MP_IDENTIFIER'):
                    self.variable_declaration_tail()
                else:
                    return
        else:
            self.error()

    def variable_declaration_tail(self): ##Sam's confused on this one
        self.variable_declaration()
        self.lookahead()

        if self.match('MP_SCOLON'):
            self.lookahead()
            if self.match('MP_IDENTIFIER'):
                self.variable_declaration_tail()
            else:
                return
        else:
            self.error()

    def variable_declaration(self):
        return

    def procedure_function_declaration_part(self):
        return
    def statement_part(self):
        return
    def identifier(self):
        if self.match('MP_IDENTIFIER'):
            logging.info('Matched an identifier.')
            self.lookahead()
