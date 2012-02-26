import inspect
import sys
import re
import logging
from Scanner import Token

class Parser(object):


    def __init__(self, tokens):
        self.index = len(tokens)
        self.tokens = iter(tokens)
        self.cur_token = self.tokens.next()

    ############### Utility Functions ###############

    def error(self):
        logging.error("Couldn't match: %s in %s()" % (self.t_lexeme(),
                                                      inspect.stack()[2][3]))

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
        Expanding Rule 1:
        System Goal -> Program $
        """
        if self.t_type() == 'MP_PROGRAM':
            self.program()
            self.match('MP_EOF') # ?
        else:
            self.error()

    def program(self):
        """
        Expanding Rule 2:
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
        Expanding Rule 3:
        "program" Identifier
        """
        if self.t_type() == 'MP_PROGRAM':
            self.match('program')
            self.program_identifier()
        else:
            self.error()

    def block(self):
        """
        Expanding Rule 4:
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
        Expanding Rules 5, 6:
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
        Expanding Rules 7, 8:
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
        """
        Expanding Rule 9:
        VariableDeclaration -> IdentifierList ":" Type
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.identifier_list()
            self.match(';')
            self.type()
        else:
            self.error()

    def type(self):
        """
        Expanding Rules 10, 11:
        Type -> "Integer"
             -> "Float"
        """
        if self.t_type() == 'MP_FLOAT':
            self.match('float')
        elif self.t_type() == 'MP_INTEGER':
            self.match('integer')
        else:
            self.error()

    def procedure_function_declaration_part(self):
        """
        Expanding Rules 12, 13, 14:
        ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
                                            -> FunctionDeclaration ProcedureAndFunctionDeclarationPart
                                            -> epsilon
        """
        if self.t_type() == 'MP_PROCEDURE':
            self.procedure_declaration()
            self.procedure_and_function_declaration_part()
        elif self.t_type() == 'MP_FUNCTION':
            self.function_declaration()
            self.procedure_and_function_declaration_part()
        elif self.t_type() == 'MP_BEGIN':
            self.epsilon()
        else:
            self.error()

    def procedure_declaration(self):
        """
        Expanding Rule 15:
        ProcedureDeclaration -> ProcedureHeading ";" Block ";"
        """
        if self.t_type() == 'MP_PROCEDURE':
            self.procedure_heading()
            self.match(';')
            self.block()
            self.match(';')
        else:
            self.error()


    def function_declaration(self):
        """
        Expanding Rule 16:
        FunctionDeclaration -> FunctionHeading ";" Block ";"
        """
        if self.t_type() == 'MP_FUNCTION':
            self.function_heading()
            self.match(';')
            self.block()
            self.match(';')
        else:
            self.error()

    def procedure_heading(self):
        """
        Expanding Rule 17:
        ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
        """
        if self.t_type() == 'MP_PROCEDURE':
            self.match('procedure')
            self.procedure_identifier()
            self.optional_formal_parameter_list()
        else:
            self.error()

    def function_heading(self):
        """
        Expanding Rule 18:
        FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
        """
        if self.t_type() == 'MP_FUNCTION':
            self.match('function')
            self.function_identifier()
            self.optional_formal_parameter_list()
            self.match(':')
            self.type()
        else:
            self.error()

    def statement_part(self):
        return


    def program_identifier(self):
        """
        Expanding Rule 56:
        ProgramIdentifier -> Identifier
        """
        pass

    def identifier(self):
        pass


