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

    def error(self, expected=None):
        logging.error("Couldn't match: %s in %s()" % (self.t_lexeme(),
                                                      inspect.stack()[2][3]))
        logging.error('Expected tokens: %s' % expected)

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

    def procedure_and_function_declaration_part(self):
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

    def optional_formal_parameter_list(self):
        """
        Expanding Rules 19, 20:
        OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                                    -> epsilon
        """
        if self.t_type() == 'MP_LPAREN':
            self.match('(')
            self.formal_parameter_section()
            self.formal_parameter_section_tail()
            self.match(')')
        elif self.t_type() == ('MP_FLOAT' or 'MP_INTEGER' or 'MP_SCOLON'):
            self.epsilon()
        else:
            self.error()

    def formal_parameter_section_tail(self):
        """
        Expanding Rules 21, 22:
        FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
                                   -> epsilon
        """
        if self.t_type() == 'MP_SCOLON':
            self.match(';')
            self.formal_parameter_section()
            self.formal_parameter_section_tail()
        elif self.t_type() == ('MP_RPAREN'):
            self.epsilon()
        else:
            self.error()

    def formal_parameter_section(self):
        """
        Expanding Rules 23, 24:
        FormalParameterSection -> ValueParameterSection
                               -> VariableParameterSection
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.value_parameter_section()
        elif self.t_type() == 'MP_VAR':
            self.variable_parameter_section()
        else:
            self.error()

    def value_parameter_section(self):
        """
        Expanding Rule 25:
        ValueParameterSection -> IdentifierList ":" Type
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.identifier_list()
            self.match(':')
            self.type()
        else:
            self.error()


    def variable_parameter_section(self):
        """
        Expanding Rule 26:
        VariableParameterSection -> "var" IdentifierList ":" Type
        """
        if self.t_type() == 'MP_VAR':
            self.identifier_list()
            self.match(':')
            self.type()
        else:
            self.error()


    def statement_part(self):
        """
        Expanding Rule 27:
        StatementPart -> CompoundStatement
        """
        if self.t_type() == 'MP_BEGIN':
            self.compound_statement()
        else:
            self.error()


    def compound_statement(self):
        """
        Expanding Rule 28:
        CompoundStatement -> "begin" StatementSequence "end"
        """
        if self.t_type() == 'MP_BEGIN':
            self.match('begin')
            self.statement_sequence()
            self.match('end')
        else:
            self.error()

    def statement_sequence(self):
        """
        Expanding Rule 29:
        StatementSequence -> Statement StatementTail
        """
        if self.t_type() == ('MP_BEGIN' or 'MP_END' or 'MP_READ'
                             or 'MP_WRITE' or 'MP_IF' or 'MP_WHILE'
                             or 'MP_REPEAT' or 'MP_FOR' or 'MP_IDENTIFIER'):
            self.statement()
            self.statement_tail()
        else:
            self.error()

    def statement_tail(self):
        """
        Expanding Rules 30, 31 :
        StatementTail -> ";" Statement StatementTail
                      -> epsilon
        """
        if self.t_type() == 'MP_SCOLON':
            self.match(';')
            self.statement()
            self.statement_tail()
        elif self.t_type() == ('MP_END' or 'MP_UNTIL'):
            self.epsilon()
        else:
            self.error()
    def statement(self):
        """
        Expanding Rule 32 - 41 :
        Statement -> EmptyStatement
                  -> CompoundStatement
                  -> ReadStatement
                  -> WriteStatement
                  -> AssignmentStatement
                  -> IfStatement
                  -> WhileStatement
                  > RepeatStatement
                  -> ForStatement
                  -> ProcedureStatement
        """
        if self.t_type() == 'MP_END':
            self.empty_statement()
        #TODO resolve conflict
#        elif self.t_type() == 'MP_BEGIN':
#            self.compound_statement()
        elif self.t_type() == 'MP_READ':
            self.read_statement()
        elif self.t_type() == 'MP_WRITE':
            self.write_statement()
        elif self.t_type() == 'MP_IDENTIFIER':
            self.assignment_statement()
        elif self.t_type() == 'MP_IF':
            self.if_statement()
        elif self.t_type() == 'MP_WHILE':
            self.while_statement()
        elif self.t_type() == 'MP_REPEAT':
            self.repeat_statement()
        elif self.t_type() == 'MP_FOR':
            self.for_statement()
        elif self.t_type() == 'MP_IDENTIFIER': # need to resolve ambiguity
            self.procedure_statement()
        else:
            self.error()

    def empty_statement(self):
        """
        Expanding Rule 42:
        EmptyStatement -> epsilon
        """
        if self.t_type() == ('MP_SCOLON' or 'MP_ELSE' or 'MP_END' or 'MP_UNTIL'):
            self.epsilon()
        else:
            self.error()

    def read_statement(self):
        """
        Expanding Rule 43:
        ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
        """
        if self.t_type() == 'MP_READ':
            self.match('read')
            self.match('(')
            self.read_parameter()
            self.read_parameter_tail()
            self.match(')')
        else:
            self.error()

    def read_parameter_tail(self):
        """
        Expanding Rules 44, 45 :
        ReadParameterTail -> "," ReadParameter ReadParameterTail
                          -> epsilon
        """
        if self.t_type() == 'MP_COMMA':
            self.match(',')
            self.read_parameter()
            self.read_parameter_tail()
        elif self.t_type() == 'MP_RPAREN':
            self.epsilon()
        else:
            self.error()

    def read_parameter(self):
        """
        Expanding Rule 46 :
        ReadParameter -> VariableIdentifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.variable_identifier()
        else:
            self.error()

    def write_statement(self):
        """
        Expanding Rule 47:
        WriteStatement -> "write" "(" WriteParameter WriteParameterTail ")"
        """
        if self.t_type() == 'MP_WRITE':
            self.match('write')
            self.match('(')
            self.write_parameter()
            self.write_parameter_tail()
            self.match(')')
        else:
            self.error()

    def write_parameter_tail(self):
        """
        Expanding Rules 48, 49 :
        WriteParameterTail -> "," WriteParameter WriteParameterTail
                           -> epsilon
        """
        if self.t_type() == 'MP_COMMA':
            self.match(',')
            self.write_parameter()
            self.write_parameter_tail()
        elif self.t_type() == 'MP_RPAREN':
            self.epsilon()
        else:
            self.error()


    def write_parameter(self):
        """
        Expanding Rule 50 :
        WriteParameter -> OrdinalExpression
        """
        if self.t_type() == ('MP_PLUS' or 'MP_MINUS' or 'MP_INTEGER'
                             or 'MP_NOT' or 'MP_LPAREN' or 'MP_IDENTIFIER'):
            self.ordinal_expression()
        else:
            self.error(['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT'])

    def assignment_statement(self):
        """
        Expanding Rules 51, 52:
        AssignmentStatement -> VariableIdentifier ":=" Expression
                            -> FunctionIdentifier ":=" Expression
        """
        # the conflict here should be considered resolved, because in the end
        #both those guys lead to identifier
        if self.t_type() == 'MP_IDENTIFIER':
            self.variable_identifier()
        else:
            self.error('MP_IDENTIFIER')


    def if_statement(self):
        """
        Expanding Rule 53:
        IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
        """
        if self.t_type() == 'MP_IF':
            self.match('if')
            self.boolean_expression()
            self.match('then')
            self.statement()
            self.optional_else_part()
        else:
            self.error('MP_IF')

    def optional_else_part(self):
        """
        Expanding Rule 54:
        OptionalElsePart -> "else" Statement
        """
        if self.t_type() == 'MP_ELSE':
            self.match('else')
            self.statement()
        elif self.t_type() == ('MP_SCOLON' or 'MP_END' or 'MP_UNTIL'):
            self.epsilon()
        else:
            self.error(['MP_ELSE', 'MP_SCOLON', 'MP_END', 'MP_UNTIL'])

    def repeat_statement(self):
        """
        Expanding Rule 56:
        RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
        """
        if self.t_type() == 'MP_REPEAT':
            self.match('repeat')
            self.statement_sequence()
            self.match('until')
            self.boolean_expression()
        else:
            self.error('MP_REPEAT')
            
    def program_identifier(self):
        """
        Expanding Rule 56:
        ProgramIdentifier -> Identifier
        """
        pass

    def identifier(self):
        pass




    def fun_template(self):
        """
        Expanding Rule :

        """
        if self.t_type() == '':
            pass
        elif self.t_type() == '':
            pass
        else:
            self.error()

