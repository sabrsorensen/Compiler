
import sys
import re
import logging
from Scanner import Token

class Parser(object):


    def __init__(self, tokens):
        self.parsed = ''
        self.cur_token = self.tokens.next()
        self.index = len(tokens)
        self.tokens = iter(tokens)

    ############### Utility Functions ###############

    def error(self):
        logging.error("Couldn't match: %s" % self.t_lexeme())

    def t_type(self):
        """
        So that we don't have to call the line below
        every time we need a current token type
        """
        return self.cur_token.token_type

    def t_lexeme(self):
        """
        Same as above - just a wrapper to make code
        more elegant
        """
        return self.cur_token.token_value

    def match(self, lexeme):
        self.cur_token = self.tokens.next()
        logging.info("Matched '%s'" % lexeme)
        return False


    ############### Rule handling functions ###############


    def system_goal(self):
        """
        Expanding
        System Goal -> Program $
        """
        if self.t_type() == 'MP_PROGRAM':
            self.program()
            self.match('MP_EOF') # ?
        else:
            self.error()

    def program(self):
        """
        Expanding
        Program -> ProgramHeading ";" Block "."
        """
        if self.t_type() == 'MP_PROGRAM':
            self.program_heading()
            self.match('MP_SCOLON')
            self.block()
            self.match('.')
        else:
            self.error()

    def program_heading(self):
        """
        Expanding
        "program" Identifier
        """
        if self.t_type() == 'MP_PROGRAM':
            self.match('program')
            self.program_identifier()
        else:
            self.error()

    def program_identifier(self):
        """
        Expanding
        ProgramIdentifier -> Identifier
        """
        pass

    def block(self):
        """
        Expanding
        Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
        """
        if self.t_type() == ('MP_VAR' or 'MP_PROCEDURE' or 'MP_BEGIN' or 'MP_FUNCTION'):
            self.variable_declaration_part()
            self.procedure_function_declaration_part()
            self.statement_part()
        else:
            self.error()

    def variable_declaration_part(self):
        """
        Expanding
        VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
                                -> e
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.variable_declaration()
            self.match(';')
            self.variable_declaration_tail()
        elif self.t_type() == ('MP_BEGIN' or 'MP_FUNCTION' or 'MP_PROCEDURE'):
            self.epsilon()
        else:
            self.error()

    def epsilon(self):
        """
        Branch went to epsilon - pass
        """
        pass

    def variable_declaration_tail(self):
        """
        Expanding
        VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail
                                -> e
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.variable_declaration()
            self.match(';')
            self.variable_declaration_tail()
        elif self.t_type() == ('MP_BEGIN' or 'MP_FUNCTION' or 'MP_PROCEDURE'):
            self.epsilon()
        else:
            self.error()

    def variable_declaration(self):
        return

    def procedure_function_declaration_part(self):
        return

    def statement_part(self):
        return

    def identifier(self):
        pass


