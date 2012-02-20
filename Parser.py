
__author__ = 'logiasin' # Sam took all the credit :P
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







        #### Regular Expressions out the wazoo. Yes, that is typically where they come from ####
#        self.ProgramRE = r'%s;%s.' % (self.ProgramHeadingRE, self.BlockRE)
#        self.ProgramHeadingRE = r'program %s' % (self.IdentifierRE)
#        self.BlockRE = r'%s %s %s' % (self.VariableDecPartRE, self.ProcedureFuncDecPartRE, self.StatementPartRE)
#        self.VariableDecPartRE = r'(var (%s;)+)?' % (self.VariableDecRE)
#        self.ProcedureFuncDecPartRE = r'((%s | %s);)*' % (self.ProcedureDecRE, self.FunctionDecRE)
#        self.StatementPartRE = r'%s' % (self.CompountStatementRE)
#        self.VariableDecRE = r'%s:%s' % (self.IdentifierListRE, self.TypeRE)
#        self.TypeRE = r'(Integer)|(Float)'
#        self.ProcedureDecRE = r'%s;%s' % (self.ProcedureHeadingRE, self.BlockRE)
#        self.FunctionDecRE = r'%s;%s' % (self.FunctionHeadingRE, self.BlockRE)
#        self.ProcedureHeadingRE = r'(procedure) %s (%s)?' % (self.IdentifierRE,self.FormalParameterListRE)
#        self.FunctionHeadingRE = r'(function) %s (%s)? : %s' % (self.IdentifierRE,self.FormalParameterListRE,self.TypeRE)
#        self.FormalParameterListRE = r'\( %s (;%s)* \)' % (self.FormalParameterSectionRE, self.FormalParameterSectionRE)
#        self.FormalParameterSectionRE = r'(%s|%s)' % (self.ValueParameterSectionRE, self.VariableParameterSectionRE)
#        self.ValueParameterSectionRE = r'%s:%s' % (self.IdentifierListRE, self.TypeRE)
#        self.VariableParameterSectionRE = r'var %s:%s' % (self.IdentifierListRE,self.TypeRE)
#        self.CompoundStatementRE = r'begin %s end' % (self.StatementSequenceRE)
#        self.StatementSequenceRE = r'%s (;%s)*' % (self.StatementRE,self.StatementRE)
#        self.StatementRE = r'(%s|%s)' % (self.SimpleStatementRE,self.StructuredStatementRE)
#        self.SimpleStatementRE = r'(%s|%s|%s|%s|%s)' % (self.EmptyStatementRE,self.ReadStatementRE,self.WriteStatementRE,self.AssignmentStatementRE,self.ProcedureStatementRE)
#        self.StructuredStatementRE = r'(%s|%s|%s)' % (self.CompoundStatementRE, self.ConditionalStatementRE,self.RepetitiveStatementRE)
#        self.ConditionalStatementRE = r'%s' % (self.IfStatementRE)
#        self.RepetitiveStatementRE = r'(%s|%s|%s)' % (self.WhileStatementRE,self.RepeatStatementRE,self.ForStatementRE)
#        self.EmptyStatementRE = r''
#        self.ReadStatementRE = r'read %s' % (self.ReadParameterListRE)
#        self.WriteStatementRE = r'write %s' % (self.WriteParameterListRE)
#        self.AssignmentStatementRE = r'(%s|%s):=%s' % (self.VariableRE, self.FunctionIdentifierRE,self.ExpressionRE)
#        self.ProcedureStatementRE = r'%s(%s)?' % (self.ProcedureIdentifierRE,self.ActualParameterListRE)
#        self.IfStatementRE = r'if %s then %s (else %s)?' % (self.BooleanExpressionRE, self.StatementRE, self.StatementRE)
#        self.RepeatStatementRE = r'repeat %s until %s' % (self.StatementSequenceRE,self.BooleanExpressionRE)
#        self.WhileStatementRE = r'while %s do %s' % (self.BooleanExpressionRE, self.StatementRE)
#        self.ForStatementRE = r'for %s := %s (to|downto) %s do %s' % (self.ControlVariableRE,self.InitialValueRE, self.FinalValueRE, self.StatementRE)
#        self.ControlVariableRE = r'%s' % self.VariableIdentifierRE
#        self.InitialValueRE = r'%s' % self.OrdinalExpressionRE
#        self.FinalValueRE = r'%s' % self.OrdinalExpressionRE
#        self.ExpressionRE = r'%s (%s %s)?' % (self.SimpleExpressionRE, self.RelationalOperatorRE, self.SimpleExpressionRE)
#        self.SimpleExpressionRE = r'(%s)? %s (%s %s)*' % (self.SignRE, self.TermRE, self.AddingOperatorRE, self.TermRE)
#        self.TermRE = r'%s (%s %s)*' % (self.FactorRE, self.MultiplyingOperatorRE, self.FactorRE)
#        self.FactorRE = r'(%s|%s|%s|not %s|(%s))'
#        self.RelationalOperatorRE = r'(=|<|>|<=|>=|<>)'
#        self.AddingOperatorRE = r'(+|-|or)'
#        self.MultiplyingOperatorRE = r'(\*|div|mod|and)'
#        self.FunctionalDesignatorRE = r'%s (%s)?' % (self.FunctionIdentifierRE,self.ActualParamaterListRE)
#        self.VariableRE = r'%s' % self.VariableIdentifierRE
#        self.ActualParameterListRE = r'\(%s(,%s)*\)' % (self.ActualParameterRE,self.ActualParameterRE)
#        self.ActualParameterRE = r'%s' % self.ExpressionRE
#
#        self.LetterRE = r'[a-zA-Z]'
#        self.DigitRE = r'[0-9]'
#        self.DigitSequenceRE = r'[0-9]+'
#        self.UnderRE = r'_'
#        self.SignRE = r'[-+]'
#        self.UnsignedIntegerRE = r'%s' % DigitSequenceRE

#Variable                            = VariableIdentifier
#ActualParameterList                 = "(" ActualParameter { "," ActualParameter } ")"
#ActualParameter                     = Expression
#ReadParameterList                   = "(" ReadParameter { "," ReadParameter } ")"
#ReadParameter                       = Variable
#WriteParameterList                  = "(" WriteParameter { "," WriteParameter } ")"
#WriteParameter                      = Expression
#BooleanExpression                   = OrdinalExpression
#OrdinalExpression                   = Expression
#VariableIdentifier                  = Identifier
#ProcedureIdentifier                 = Identifier
#FunctionIdentifier                  = Identifier
#IdentifierList                      = Identifier { "," Identifier }
#Identifier                          = ??
###UnsignedInteger                     = DigitSequence
###Sign                                = "+" | "-"
###Under                               = "_"
###DigitSequence                       = Digit { Digit }
###Letter                              = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
#                                     |"n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
#                                     |"A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
#                                     |"N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
###Digit                               = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"