
__author__ = 'logiasin' # Sam took all the credit :P
                        # that was all PyCharm, it grabbed my username :P
import sys
import re
import logging
from Scanner import Scanner

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

    def program(self):
        """ Expanding -----Program = ProgramHeading ";" Block "."-----"""
        self.lookahead()

        self.program_heading()

        if self.match('MP_SCOLON'):
            logging.info('Matched a Semicolon.')
            self.lookahead()
        else:
            self.error()

        self.block()

        if self.match('MP_PERIOD'):
            logging.info('Matched a period.')
            self.lookahead()


    def program_heading(self):
        """"Expanding -----"program" Identifier-----"""
        if self.match('MP_PROGRAM'):
            logging.info('Matched %s' % self.cur_token.lexeme)
            self.lookahead()
        else:
            self.error()

        self.identifier()

    def block(self):
        variable_declaration_part()
        procedure_function_declaration_part()
        statement_part()

#    def variable_declaration_part(self):
#        if lookahead() is 'var':
#            self.parsed += 'var'
#            #This needs more looping!
#            variable_declaration()
#            self.parsed += ';'
#
#    def procedure_and_function_declaration_part(self):
#        #broken switch statement, don't know how to do it in Python
#
#        switch (lookahead())
#        {
#            case blah1:
#                procedure_declaration()
#                break
#            case blah2:
#                function_declaration()
#                break()
#            case others:
#                error()
#        }
#        self.parsed += ';'


    def variable_declaration(self):
        identifier_list()
        self.parsed += ':'
        type()

    def identifier(self):
        if self.match('MP_IDENTIFIER'):
            logging.info('Matched an identifier.')
            self.lookahead()
