
__author__ = 'logiasin'
import sys
import re

class Parser:

    def __init__(self):
        #### Regular Expressions out the wazoo. Yes, that is typically where they come from ####
        self.ProgramRE = r'%s;%s.' % (self.ProgramHeadingRE, self.BlockRE)
        self.ProgramHeadingRE = r'program %s' % (self.IdentifierRE)
        self.BlockRE = r'%s %s %s' % (self.VariableDecPartRE, self.ProcedureFuncDecPartRE, self.StatementPartRE)
        self.VariableDecPartRE = r'(var (%s;)+)?' % (self.VariableDecRE)
        self.ProcedureFuncDecPartRE = r'((%s | %s);)*' % (self.ProcedureDecRE, self.FunctionDecRE)
        self.StatementPartRE = r'%s' % (self.CompountStatementRE)
        self.VariableDecRE = r'%s:%s' % (self.IdentifierListRE, self.TypeRE)
        self.TypeRE = r'(Integer)|(Float)'
        self.ProcedureDecRE = r'%s;%s' % (self.ProcedureHeadingRE, self.BlockRE)
        self.FunctionDecRE = r'%s;%s' % (self.FunctionHeadingRE, self.BlockRE)
        self.ProcedureHeadingRE = r'(procedure) %s (%s)?' % (self.IdentifierRE,self.FormalParameterListRE)
        self.FunctionHeadingRE = r'(function) %s (%s)? : %s' % (self.IdentifierRE,self.FormalParameterListRE,self.TypeRE)
        self.FormalParameterListRE = r'\( %s (;%s)* \)' % (self.FormalParameterSectionRE, self.FormalParameterSectionRE)
        self.FormalParameterSectionRE = r'(%s|%s)' % (self.ValueParameterSectionRE, self.VariableParameterSectionRE)
        self.ValueParameterSectionRE = r'%s:%s' % (self.IdentifierListRE, self.TypeRE)
        self.VariableParameterSectionRE = r'var %s:%s' % (self.IdentifierListRE,self.TypeRE)
        self.CompoundStatementRE = r'begin %s end' % (self.StatementSequenceRE)
        self.StatementSequenceRE = r'%s (;%s)*' % (self.StatementRE,self.StatementRE)
        self.StatementRE = r'(%s|%s)' % (self.SimpleStatementRE,self.StructuredStatementRE)
        self.SimpleStatementRE = r'(%s|%s|%s|%s|%s)' % (self.EmptyStatementRE,self.ReadStatementRE,self.WriteStatementRE,self.AssignmentStatementRE,self.ProcedureStatementRE)
        self.StructuredStatementRE = r'(%s|%s|%s)' % (self.CompoundStatementRE, self.ConditionalStatementRE,self.RepetitiveStatementRE)
        self.ConditionalStatementRE = r'%s' % (self.IfStatementRE)
        self.RepetitiveStatementRE = r'(%s|%s|%s)' % (self.WhileStatementRE,self.RepeatStatementRE,self.ForStatementRE)
        self.EmptyStatementRE = r''
        self.ReadStatementRE = r'read %s' % (self.ReadParameterListRE)
        self.WriteStatementRE = r'write %s' % (self.WriteParameterListRE)
        self.AssignmentStatementRE = r'(%s | %s):=%s' % (self.VariableRE, self.FunctionIdentifierRE,self.ExpressionRE)
        self.LetterRE = r'[a-zA-Z]'
        self.DigitRE = r'[0-9]'
        self.DigitSequenceRE = r'[0-9]+'
        self.UnderRE = r'_'
        self.SignRE = r'[-+]'
        self.UnsignedIntegerRE = r'%s' % DigitSequenceRE

"""
StructuredStatement                 = CompoundStatement | ConditionalStatement | RepetitiveStatement
ConditionalStatement                = IfStatement
RepetitiveStatement                 = WhileStatement | RepeatStatement | ForStatement
EmptyStatement                      =
ReadStatement                       = "read" ReadParameterList
WriteStatement                      = "write" WriteParameterList
AssignmentStatement                 = ( Variable | FunctionIdentifier ) ":=" Expression
ProcedureStatement                  = ProcedureIdentifier [ ActualParameterList ]
IfStatement                         = "if" BooleanExpression "then" Statement [ "else" Statement ]
RepeatStatement                     = "repeat" StatementSequence "until" BooleanExpression
WhileStatement                      = "while" BooleanExpression "do" Statement
ForStatement                        = "for" ControlVariable ":=" InitialValue ( "to" | "downto" ) FinalValue "do" Statement
ControlVariable                     = VariableIdentifier
InitialValue                        = OrdinalExpression
FinalValue                          = OrdinalExpression
Expression                          = SimpleExpression [ RelationalOperator SimpleExpression ]
SimpleExpression                    = [ Sign ] Term { AddingOperator Term }
Term                                = Factor { MultiplyingOperator Factor }
Factor                              = UnsignedInteger | Variable | FunctionDesignator | "not" Factor | "(" Expression ")"
RelationalOperator                  = "=" | "<" | ">" | "<=" | ">=" | "<>"
AddingOperator                      = "+" | "-" | "or"
MultiplyingOperator                 = "*" | "div" | "mod" | "and"
FunctionDesignator                  = FunctionIdentifier [ ActualParameterList ]
Variable                            = VariableIdentifier
ActualParameterList                 = "(" ActualParameter { "," ActualParameter } ")"
ActualParameter                     = Expression
ReadParameterList                   = "(" ReadParameter { "," ReadParameter } ")"
ReadParameter                       = Variable
WriteParameterList                  = "(" WriteParameter { "," WriteParameter } ")"
WriteParameter                      = Expression
BooleanExpression                   = OrdinalExpression
OrdinalExpression                   = Expression
VariableIdentifier                  = Identifier
ProcedureIdentifier                 = Identifier
FunctionIdentifier                  = Identifier
IdentifierList                      = Identifier { "," Identifier }
Identifier                          = ??
##UnsignedInteger                     = DigitSequence
##Sign                                = "+" | "-"
##Under                               = "_"
##DigitSequence                       = Digit { Digit }
##Letter                              = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
                                     |"n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
                                     |"A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
                                     |"N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
##Digit                               = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
"""