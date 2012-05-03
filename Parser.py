import inspect
import logging

from symbol_table import SymbolTable
from semantic_analyzer import SemanticAnalyzer
from semantic_record import SemanticRecord

log = logging.getLogger()
ch  = logging.StreamHandler()
#log.setLevel(logging.DEBUG)
log.setLevel(logging.ERROR)

class Parser(object):

    def __init__(self, tokens):
        self.index = len(tokens)
        self.tokens = iter(tokens)
        self.cur_token = self.tokens.next()     #Default token holder
        self.next_token = self.tokens.next()    #LL2 lookahead token holder for when needed
        self.cur_symbol_table = None
        self.root_table = SymbolTable(None)
        self.sem_analyzer = SemanticAnalyzer(self.root_table)
        self.program_name = ''
        self.cur_proc_name = ''
        self.cur_func_name = ''

    ############### Utility Functions ###############

    def error(self, expected=None):
        logging.error("Couldn't match: \"%s\" in %s(). Received %s" % (self.t_lexeme(),
                                                      inspect.stack()[1][3],self.t_type()))
        logging.error('Expected tokens: %s' % expected)
        logging.error("Three level parse tree (stack) trace, most recent call last.\n\t^ %s()\n\t^ %s()\n\t> %s()" % (inspect.stack()[3][3],
                                                                                                                  inspect.stack()[2][3],
                                                                                                                  inspect.stack()[1][3]))
        exit()

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

    @classmethod
    def print_tree(cls, level):
        """
        A method for printing where we are at in parse tree
        In case future assignments will require more complexity
        """
        logging.debug(level)

    def match(self, lexeme):
        self.cur_token = self.next_token
        try:
            self.next_token = self.tokens.next()
        except StopIteration:
            pass
        logging.info("Matched '%s' in %s()" % (lexeme, inspect.stack()[1][3]))
        return False

    def print_symbol_table(self, type, table):
        level = log.getEffectiveLevel()
        log.setLevel(logging.DEBUG)
        logging.debug(type + " Symbol Table " + table.name + table.__repr__() + '\n')
        log.setLevel(level)


    ############### Rule handling functions ###############


    def system_goal(self):
        """
        Expanding Rule 1:
        System Goal -> Program $
        """
        if self.t_type() == 'MP_PROGRAM':
            Parser.print_tree('1')
            self.program()
            if self.t_type() == 'MP_EOF':
                self.match('EOF')
                self.print_symbol_table("Program",self.root_table)
                self.sem_analyzer.write_IR()
                return "The input program parses!"
            exit()
        else:
            self.error('MP_PROGRAM')

    def program(self):
        """
        Expanding Rule 2:
        Program -> ProgramHeading ";" Block "."
        """
        if self.t_type() == 'MP_PROGRAM':
            Parser.print_tree('2')
            self.program_heading()
            self.match(';')
            self.root_table.create_root()
            self.root_table.name = self.program_name
            self.cur_symbol_table = self.root_table
            self.sem_analyzer.sym_table = self.cur_symbol_table
            self.sem_analyzer.gen_begin()
            self.block()
            self.sem_analyzer.gen_end()
            self.match('.')
        else:
            self.error('MP_PROGRAM')

    def program_heading(self):
        """
        Expanding Rule 3:
        "program" Identifier
        """
        if self.t_type() == 'MP_PROGRAM':
            Parser.print_tree('3')
            self.match('program')
            self.program_identifier()
        else:
            self.error('MP_PROGRAM')

    def block(self):
        """
        Expanding Rule 4:
        Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
        """
        accepted_list = ['MP_VAR', 'MP_PROCEDURE', 'MP_BEGIN', 'MP_FUNCTION']
        if self.t_type() in accepted_list:
            Parser.print_tree('4')
            self.variable_declaration_part()
            self.procedure_and_function_declaration_part()
            self.statement_part()
        else:
            self.error(accepted_list)

    def variable_declaration_part(self):
        """
        Expanding Rules 5, 6:
        VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
                                -> e
        """
        eps_list = ['MP_BEGIN', 'MP_FUNCTION', 'MP_PROCEDURE']
        if self.t_type() == 'MP_VAR':
            Parser.print_tree('5')
            self.match('var')
            self.variable_declaration()
            self.match(';')
            self.variable_declaration_tail()
        elif self.t_type() in eps_list:
            Parser.print_tree('6')
            self.epsilon()
        else:
            self.error(eps_list.append('MP_VAR'))

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
        eps_list = ['MP_BEGIN', 'MP_FUNCTION', 'MP_PROCEDURE']
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('7')
            self.variable_declaration()
            self.match(';')
            self.variable_declaration_tail()
        elif self.t_type() in eps_list:
            Parser.print_tree('8')
            self.epsilon()
        else:
            self.error(eps_list.append('MP_IDENTIFIER'))

    def variable_declaration(self):
        """
        Expanding Rule 9:
        VariableDeclaration -> IdentifierList ":" Type
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('9')
            var_list = self.identifier_list([])
            self.match(':')
            type = self.type()
            #iterate through the list of vars
            for var in var_list:
                record = SemanticRecord()
                record.type = type
                record.lexeme = var
                record.set_size(type)
                record.kind = "var"
                record.depth = self.cur_symbol_table.cur_depth
                self.cur_symbol_table.insert(record)
        else:
            self.error('MP_IDENTIFIER')

    def type(self):
        """
        Expanding Rules 10, 11:
        Type -> "Integer"
             -> "Float"
        """
        lexeme = ''
        if self.t_type() == 'MP_FLOAT':
            Parser.print_tree('11')
            lexeme = self.t_lexeme()
            self.match(lexeme)
        elif self.t_type() == 'MP_INTEGER':
            Parser.print_tree('10')
            lexeme = self.t_lexeme()
            self.match(lexeme)
        else:
            self.error(['MP_FLOAT', 'MP_INTEGER'])
        return lexeme
    def procedure_and_function_declaration_part(self):
        """
        Expanding Rules 12, 13, 14:
        ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
                                            -> FunctionDeclaration ProcedureAndFunctionDeclarationPart
                                            -> epsilon
        """
        if self.t_type() == 'MP_PROCEDURE':
            Parser.print_tree('12')
            self.procedure_declaration()
            self.procedure_and_function_declaration_part()
        elif self.t_type() == 'MP_FUNCTION':
            Parser.print_tree('13')
            self.function_declaration()
            self.procedure_and_function_declaration_part()
        elif self.t_type() == 'MP_BEGIN':
            Parser.print_tree('14')
            self.epsilon()
        else:
            self.error(['MP_PROCEDURE', 'MP_FUNCTION', 'MP_BEGIN'])

    def procedure_declaration(self):
        """
        Expanding Rule 15:
        ProcedureDeclaration -> ProcedureHeading ";" Block ";"
        """
        if self.t_type() == 'MP_PROCEDURE':
            old_proc_name = self.cur_proc_name
            proc_sym_table = SymbolTable(self.cur_symbol_table)
            proc_sym_table.create()
            self.cur_symbol_table = proc_sym_table
            self.sem_analyzer.sym_table = self.cur_symbol_table
            Parser.print_tree('15')
            self.procedure_heading()
            proc_sym_table.name = self.cur_proc_name
            self.match(';')
            self.block()
            self.match(';')
            self.print_symbol_table("Procedure", proc_sym_table)
            self.cur_symbol_table = self.cur_symbol_table.parent_table
            self.cur_proc_name = old_proc_name
            proc_sym_table.destroy()
        else:
            self.error('MP_PROCEDURE')


    def function_declaration(self):
        """
        Expanding Rule 16:
        FunctionDeclaration -> FunctionHeading ";" Block ";"
        """
        if self.t_type() == 'MP_FUNCTION':
            old_func_name = self.cur_func_name
            func_sym_table = SymbolTable(self.cur_symbol_table)
            func_sym_table.create()
            self.cur_symbol_table = func_sym_table
            self.sem_analyzer.sym_table = self.cur_symbol_table
            Parser.print_tree('16')
            self.function_heading()
            func_sym_table.name = self.cur_func_name
            self.match(';')
            self.block()
            self.match(';')
            self.print_symbol_table("Function",func_sym_table)
            self.cur_func_name = old_func_name
            self.cur_symbol_table = self.cur_symbol_table.parent_table
            func_sym_table.destroy()
        else:
            self.error('MP_FUNCTION')

    def procedure_heading(self):
        """
        Expanding Rule 17:
        ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
        """
        if self.t_type() == 'MP_PROCEDURE':
            Parser.print_tree('17')
            self.match('procedure')
            self.procedure_identifier()
            self.optional_formal_parameter_list()
        else:
            self.error('MP_PROCEDURE')

    def function_heading(self):
        """
        Expanding Rule 18:
        FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
        """
        if self.t_type() == 'MP_FUNCTION':
            Parser.print_tree('18')
            self.match('function')
            self.function_identifier()
            self.optional_formal_parameter_list()
            self.match(':')
            type = self.type()
        else:
            self.error('MP_FUNCTION')

    def optional_formal_parameter_list(self):
        """
        Expanding Rules 19, 20:
        OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                                    -> epsilon
        """
        eps_list = ['MP_FLOAT', 'MP_INTEGER', 'MP_SCOLON']
        if self.t_type() == 'MP_LPAREN':
            Parser.print_tree('19')
            self.match('(')
            self.formal_parameter_section()
            self.formal_parameter_section_tail()
            self.match(')')
        elif self.t_type() in eps_list:
            Parser.print_tree('20')
            self.epsilon()
        else:
            self.error(eps_list.append('MP_LPAREN'))

    def formal_parameter_section_tail(self):
        """
        Expanding Rules 21, 22:
        FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
                                   -> epsilon
        """
        if self.t_type() == 'MP_SCOLON':
            Parser.print_tree('21')
            self.match(';')
            self.formal_parameter_section()
            self.formal_parameter_section_tail()
        elif self.t_type() == 'MP_RPAREN':
            Parser.print_tree('22')
            self.epsilon()
        else:
            self.error(['MP_SCOLON', 'MP_RPAREN'])

    def formal_parameter_section(self):
        """
        Expanding Rules 23, 24:
        FormalParameterSection -> ValueParameterSection
                               -> VariableParameterSection
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('23')
            self.value_parameter_section()
        elif self.t_type() == 'MP_VAR':
            Parser.print_tree('24')
            self.variable_parameter_section()
        else:
            self.error(['MP_IDENTIFIER', 'MP_VAR'])

    def value_parameter_section(self):
        """
        Expanding Rule 25:
        ValueParameterSection -> IdentifierList ":" Type
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('25')
            val_param_list = self.identifier_list([])
            self.match(':')
            type = self.type()
            for var in val_param_list:
                record = SemanticRecord()
                record.type = type
                record.lexeme = var
                record.set_size(type)
                record.kind = "var"
                record.depth = self.cur_symbol_table.cur_depth
                self.cur_symbol_table.insert(record)
        else:
            self.error('MP_IDENTIFIER')


    def variable_parameter_section(self):
        """
        Expanding Rule 26:
        VariableParameterSection -> "var" IdentifierList ":" Type
        """
        if self.t_type() == 'MP_VAR':
            Parser.print_tree('26')
            self.match(self.t_type())
            var_param_list = self.identifier_list([])
            self.match(':')
            type = self.type()
            #iterate through the list of vars
            for var in var_param_list:
                record = SemanticRecord()
                record.type = type
                record.lexeme = var
                record.set_size(type)
                record.kind = "var"
                record.depth = self.cur_symbol_table.cur_depth
                self.cur_symbol_table.insert(record)
        else:
            self.error('MP_VAR')


    def statement_part(self):
        """
        Expanding Rule 27:
        StatementPart -> CompoundStatement
        """
        if self.t_type() == 'MP_BEGIN':
            Parser.print_tree('27')
            self.compound_statement()
        else:
            self.error('MP_BEGIN')


    def compound_statement(self):
        """
        Expanding Rule 28:
        CompoundStatement -> "begin" StatementSequence "end"
        """
        if self.t_type() == 'MP_BEGIN':
            Parser.print_tree('28')
            self.match('begin')
            self.statement_sequence()
            self.match('end')
        else:
            self.error('MP_BEGIN')

    def statement_sequence(self):
        """
        Expanding Rule 29:
        StatementSequence -> Statement StatementTail
        """
        accepted_list = ['MP_BEGIN', 'MP_END', 'MP_READ',
                         'MP_WRITE', 'MP_IF', 'MP_WHILE',
                         'MP_REPEAT', 'MP_FOR', 'MP_IDENTIFIER']
        if self.t_type() in accepted_list:
            Parser.print_tree('29')
            self.statement()
            self.statement_tail()
        else:
            self.error(accepted_list)

    def statement_tail(self):
        """
        Expanding Rules 30, 31 :
        StatementTail -> ";" Statement StatementTail
                      -> epsilon
        """
        eps_list = [ 'MP_END', 'MP_UNTIL']
        if self.t_type() == 'MP_SCOLON':
            Parser.print_tree('30')
            self.match(';')
            self.statement()
            self.statement_tail()
        elif self.t_type() in eps_list:
            Parser.print_tree('31')
            self.epsilon()
        else:
            self.error(eps_list.append('MP_SCOLON'))

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
                  -> RepeatStatement
                  -> ForStatement
                  -> ProcedureStatement
        """
        if self.t_type() == 'MP_END':
            Parser.print_tree('32')
            self.empty_statement()
        elif self.t_type() == 'MP_BEGIN':
            Parser.print_tree('33')
            self.compound_statement()
        elif self.t_type() == 'MP_READ':
            Parser.print_tree('34')
            self.read_statement()
        elif self.t_type() == 'MP_WRITE':
            Parser.print_tree('35')
            self.write_statement()
        elif self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('36')
            procedure_list = ['MP_END', 'MP_SCOLON', 'MP_LPAREN']
            procedure_list_2 = ['MP_COLON', 'MP_ASSIGN']
            if self.next_token.token_type in procedure_list:
                self.procedure_statement()
            elif self.next_token.token_type in procedure_list_2:
                self.assignment_statement()
            else:
                self.error(['MP_END', 'MP_SCOLON', 'MP_LPAREN', 'MP_COLON', 'MP_ASSIGN'])
        elif self.t_type() == 'MP_IF':
            Parser.print_tree('37')
            self.if_statement()
        elif self.t_type() == 'MP_WHILE':
            Parser.print_tree('38')
            self.while_statement()
        elif self.t_type() == 'MP_REPEAT':
            Parser.print_tree('39')
            self.repeat_statement()
        elif self.t_type() == 'MP_FOR':
            Parser.print_tree('40')
            self.for_statement()
        else:
            self.error(['MP_END', 'MP_BEGIN', 'MP_WRITE', 'MP_IDENTIFIER',
                        'MP_IF', 'MP_WHILE', 'MP_REPEAT', 'MP_FOR'])

    def empty_statement(self):
        """
        Expanding Rule 42:
        EmptyStatement -> epsilon
        """
        accepted_list = ['MP_SCOLON', 'MP_ELSE', 'MP_END', 'MP_UNTIL']
        if self.t_type() in accepted_list:
            Parser.print_tree('42')
            self.epsilon()
        else:
            self.error(accepted_list)

    def read_statement(self):
        """
        Expanding Rule 43:
        ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
        """
        if self.t_type() == 'MP_READ':
            Parser.print_tree('43')
            self.match('read')
            self.match('(')
            self.read_parameter()
            self.read_parameter_tail()
            self.match(')')
        else:
            self.error('MP_READ')

    def read_parameter_tail(self):
        """
        Expanding Rules 44, 45 :
        ReadParameterTail -> "," ReadParameter ReadParameterTail
                          -> epsilon
        """
        if self.t_type() == 'MP_COMMA':
            Parser.print_tree('44')
            self.match(',')
            self.read_parameter()
            self.read_parameter_tail()
        elif self.t_type() == 'MP_RPAREN':
            Parser.print_tree('45')
            self.epsilon()
        else:
            self.error(['MP_COMMA', 'MP_RPAREN'])

    def read_parameter(self):
        """
        Expanding Rule 46 :
        ReadParameter -> VariableIdentifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('46')
            self.variable_identifier()
        else:
            self.error('MP_IDENTIFIER')

    def write_statement(self): #AAA
        """
        Expanding Rule 47:
        WriteStatement -> "write" "(" WriteParameter WriteParameterTail ")"
        """
        write_param_rec = SemanticRecord()
        if self.t_type() == 'MP_WRITE':
            Parser.print_tree('47')
            self.match('write')
            self.match('(')
            self.write_parameter() # this is an expression
            self.write_parameter_tail() # this too is an expression of some sort
            self.match(')')
            # todo: handle combining the two returns from param and param_tail, push on the stack
            self.sem_analyzer.gen_write(write_param_rec)
        else:
            self.error('MP_WRITE')

    def write_parameter_tail(self):
        """
        Expanding Rules 48, 49 :
        WriteParameterTail -> "," WriteParameter WriteParameterTail
                           -> epsilon
        """
        if self.t_type() == 'MP_COMMA':
            Parser.print_tree('48')
            self.match(',')
            self.write_parameter()
            self.write_parameter_tail()
        elif self.t_type() == 'MP_RPAREN':
            Parser.print_tree('49')
            self.epsilon()
        else:
            self.error(['MP_COMMA', 'MP_PAREN'])


    def write_parameter(self):
        """
        Expanding Rule 50 :
        WriteParameter -> OrdinalExpression
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
            Parser.print_tree('50')
            self.ordinal_expression()
        else:
            self.error(accepted_list)

    def assignment_statement(self):
        """
        Expanding Rules 51, 52:
        AssignmentStatement -> VariableIdentifier ":=" Expression
                            -> FunctionIdentifier ":=" Expression
        """
        # the conflict here should be considered resolved, because in the end
        #both those guys lead to identifier
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('51')
            self.variable_identifier()
            self.match(':=')
            self.expression()
        else:
            self.error('MP_IDENTIFIER')


    def if_statement(self):
        """
        Expanding Rule 53:
        IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
        """
        if self.t_type() == 'MP_IF':
            Parser.print_tree('53')
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
        eps_list = ['MP_SCOLON', 'MP_END', 'MP_UNTIL']
        if self.t_type() == 'MP_ELSE':
            Parser.print_tree('54')
            self.match('else')
            self.statement()
        elif self.t_type() in eps_list:
            Parser.print_tree('55')
            self.epsilon()
        else:
            self.error(eps_list.extend('MP_ELSE'))

    def repeat_statement(self):
        """
        Expanding Rule 56:
        RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
        """
        if self.t_type() == 'MP_REPEAT':
            Parser.print_tree('56')
            self.match('repeat')
            self.statement_sequence()
            self.match('until')
            self.boolean_expression()
        else:
            self.error('MP_REPEAT')

    def while_statement(self):
        """
        Expanding Rule 57:
        WhileStatement -> "while" BooleanExpression "do" Statement
        """
        if self.t_type() == 'MP_WHILE':
            Parser.print_tree('57')
            self.match('while')
            self.boolean_expression()
            self.match('do')
            self.statement()
        else:
            self.error('MP_WHILE')


    def for_statement(self):
        """
        Expanding Rule 58:
        ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
        """
        if self.t_type() == 'MP_FOR':
            Parser.print_tree('58')
            self.match('for')
            self.control_variable()
            self.match(':=')
            self.initial_value()
            self.step_value()
            self.final_value()
            self.match('do')
            self.statement()
        else:
            self.error('MP_FOR')

    def control_variable(self):
        """
        Expanding Rule 59:
        ControlVariable -> VariableIdentifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('59')
            self.variable_identifier()
        else:
            self.error('MP_IDENTIFIER')

    def initial_value(self):
        """
        Expanding Rule 60:
        InitialValue -> OrdinalExpression
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
            Parser.print_tree('60')
            self.ordinal_expression()
        else:
            self.error(accepted_list)

    def step_value(self):
        """
        Expanding Rules 61, 62 :
        StepValue -> "to"
                  -> "downto"
        """
        if self.t_type() == 'MP_TO':
            Parser.print_tree('61')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_DOWNTO':
            Parser.print_tree('62')
            self.match(self.t_lexeme())
        else:
            self.error(['MP_TO', 'MP_DOWNTO'])

    def final_value(self):
        """
        Expanding Rule 63:
        FinalValue -> OrdinalExpression
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
            Parser.print_tree('63')
            self.ordinal_expression()
        else:
            self.error(accepted_list)


    def procedure_statement(self):
        """
        Expanding Rule 64:
        ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('64')
            self.procedure_identifier()
            self.optional_actual_parameter_list()
        else:
            self.error('MP_IDENTIFIER')

    def optional_actual_parameter_list(self):
        """
        Expanding Rules 65, 66 :
        OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"
        """
        eps_list = ['MP_TIMES', 'MP_RPAREN', 'MP_PLUS',
                    'MP_COMMA', 'MP_MINUS', 'MP_SCOLON',
                    'MP_LTHAN', 'MP_LEQUAL', 'MP_GTHAN',
                    'MP_GEQUAL', 'MP_EQUAL', 'MP_NEQUAL',
                    'MP_AND', 'MP_DIV', 'MP_DO',
                    'MP_DOWNTO', 'MP_ELSE', 'MP_END',
                    'MP_MOD', 'MP_OR', 'MP_THEN',
                    'MP_TO', 'MP_UNTIL']

        if self.t_type() == 'MP_LPAREN':
            Parser.print_tree('65')
            self.match('(')
            self.actual_parameter()
            self.actual_parameter_tail()
            self.match(')')
        elif self.t_type() in eps_list:
            Parser.print_tree('66')
            self.epsilon()
        else:
            self.error(eps_list.append('MP_LPAREN'))

    def actual_parameter_tail(self):
        """
        Expanding Rules 67, 68:
        ActualParameterTail -> "," ActualParameter ActualParameterTail
                            -> epsilon
        """
        if self.t_type() == 'MP_COMMA':
            Parser.print_tree('67')
            self.match(',')
            self.actual_parameter()
            self.actual_parameter_tail()
        elif self.t_type() == 'MP_RPAREN':
            Parser.print_tree('68')
            self.epsilon()
        else:
            self.error(['MP_COMMA', 'MP_RPAREN'])

    def actual_parameter(self):
        """
        Expanding Rule 69:
        ActualParameter -> OrdinalExpression
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
            Parser.print_tree('69')
            self.ordinal_expression()
        else:
            self.error(accepted_list)

    def expression(self):
        """
        Expanding Rule 70 :
        Expression -> SimpleExpression OptionalRelationalPart
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
            Parser.print_tree('70')
            self.simple_expression()
            self.optional_relational_part()
        else:
            self.error(accepted_list)

    def optional_relational_part(self):
        """
        Expanding Rule 71, 72:
        OptionalRelationalPart -> RelationalOperator SimpleExpression
                               -> epsilon
        """
        accepted_list = ['MP_LTHAN', 'MP_LEQUAL', 'MP_GTHAN',
                         'MP_GEQUAL', 'MP_EQUAL', 'MP_NEQUAL']
        eps_list = ['MP_RPAREN', 'MP_COMMA', 'MP_SCOLON',
                    'MP_DO', 'MP_DOWNTO', 'MP_ELSE',
                    'MP_END', 'MP_THEN', 'MP_TO', 'MP_UNTIL']

        if self.t_type() in accepted_list:
            Parser.print_tree('71')
            self.relational_operator()
            self.simple_expression()
        elif self.t_type() in eps_list:
            Parser.print_tree('72')
            self.epsilon()
        else:
            self.error(accepted_list.extend(eps_list))

    def relational_operator(self):
        """
        Expanding Rules 73 - 78:
        RelationalOperator  -> "="
                            -> "<"
                            -> ">"
                            -> "<="
                            -> ">="
                            -> "<>"
        """
        if self.t_type() == 'MP_EQUAL':
            Parser.print_tree('73')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_LTHAN':
            Parser.print_tree('74')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_GTHAN':
            Parser.print_tree('75')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_LEQUAL':
            Parser.print_tree('76')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_GEQUAL':
            Parser.print_tree('77')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_NEQUAL':
            Parser.print_tree('78')
        else:
            self.error(['MP_EQUAL', 'MP_LTHAN', 'MP_GTHAN',
                        'MP_LEQUAL', 'MP_GEQUAL', 'MP_NEQUAL'])

    def simple_expression(self):
        """
        Expanding Rule 79 :
        SimpleExpression -> OptionalSign Term TermTail
        """
        accepted_list = ['MP_LPAREN', 'MP_PLUS', 'MP_MINUS',
                         'MP_IDENTIFIER', 'MP_INTEGER', 'MP_NOT']

        if self.t_type() in accepted_list:
            Parser.print_tree('79')
            self.optional_sign()
            self.term()
            self.term_tail()
        else:
            self.error(accepted_list)

    def term_tail(self):
        """
        Expanding Rule 80,81 :
        TermTail -> AddingOperator Term TermTail
        TermTail -> ?
        """
        eps_list = ['MP_RPAREN', 'MP_COMMA', 'MP_SCOLON',
                         'MP_LTHAN', 'MP_LEQUAL', 'MP_NEQUAL',
                         'MP_EQUAL', 'MP_GTHAN', 'MP_GEQUAL',
                         'MP_DO', 'MP_DOWNTO', 'MP_ELSE',
                         'MP_TO', 'MP_UNTIL']
        accepted_list = ['MP_PLUS', 'MP_MINUS']

        if self.t_type() in accepted_list:
            Parser.print_tree('80')
            #self.optional_sign()
            self.adding_operator()
            self.term()
            self.term_tail()
        elif self.t_type() in eps_list:
            Parser.print_tree('81')
            self.epsilon()
        else:
            self.error(accepted_list.extend(eps_list))

    def optional_sign(self):
        """
        Expanding Rule 82,83,84:
        OptionalSign -> "+"
        OptionalSign -> "-"
        OptionalSign -> ?
        """
        eps_list = ['MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']

        if self.t_type() == 'MP_PLUS':
            Parser.print_tree('82')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_MINUS':
            Parser.print_tree('83')
            self.match(self.t_lexeme())
        elif self.t_type() in eps_list:
            Parser.print_tree('84')
            self.epsilon()
        else:
            self.error(eps_list.extend(['MP_PLUS','MP_MINUS']))

    def adding_operator(self):
        """
        Expanding Rule 85,86,87:
        AddingOperator -> "+"
        AddingOperator -> "-"
        AddingOperator -> "or"
        """
        accepted_list = ['MP_PLUS','MP_MINUS','MP_OR']

        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

    def term(self):
        """
        Expanding Rule 88:
        Term -> Factor FactorTail
        """
        accepted_list = ['MP_LPAREN', 'MP_IDENTIFIER', 'MP_INTEGER', 'MP_NOT']
        if self.t_type() in accepted_list:
            Parser.print_tree('88')
            self.factor()
            self.factor_tail()
        else:
            self.error(accepted_list)

    def factor_tail(self):
        """
        Expanding Rule 89,90:
        FactorTail -> MultiplyingOperator Factor FactorTail
        FactorTail -> ?
        """
        accepted_list = ['MP_TIMES', 'MP_AND',
                         'MP_DIV', 'MP_MOD']

        eps_list = ['MP_RPAREN', 'MP_PLUS', 'MP_COMMA',
                    'MP_MINUS', 'MP_SCOLON', 'MP_LTHAN',
                    'MP_LEQUAL', 'MP_NEQUAL', 'MP_EQUAL',
                    'MP_GTHAN', 'MP_GEQUAL', 'MP_DO',
                    'MP_DOWNTO', 'MP_ELSE', 'MP_END',
                    'MP_OR,', 'MP_THEN', 'MP_TO',
                    'MP_UNTIL']

        if self.t_type() in accepted_list:
            Parser.print_tree('89')
            self.multiplying_operator()
            self.factor()
            self.factor_tail()
        elif self.t_type() in eps_list:
            Parser.print_tree('90')
            self.epsilon()
        else:
            self.error(accepted_list.extend(eps_list))

    def multiplying_operator(self):
        """
        Expanding Rule 91,92,93,94:
        MultiplyingOperator -> "*"
        MultiplyingOperator -> "div"
        MultiplyingOperator -> "mod"
        MultiplyingOperator -> "and"
        """
        if self.t_type() == 'MP_TIMES':
            Parser.print_tree('91')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_DIV':
            Parser.print_tree('92')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_MOD':
            Parser.print_tree('93')
            self.match(self.t_lexeme())
        elif self.t_type() == 'MP_AND':
            Parser.print_tree('94')
            self.match(self.t_lexeme())
        else:
            self.error(['MP_TIMES', 'MP_DIV', 'MP_MOD', 'MP_AND'])

    def factor(self, sem_rec=None): #AAA
        """
        Expanding Rule 95,96,97,98,99:
        Factor -> UnsignedInteger
        Factor -> VariableIdentifier
        Factor -> "not" Factor
        Factor -> "(" Expression ")"
        Factor -> FunctionIdentifier OptionalActualParameterList
        """
        if self.t_type() == 'MP_INTEGER':
            Parser.print_tree('95')
            self.match(self.t_lexeme())
            self.sem_analyzer.gen_push_int(sem_rec)
        elif self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('96')
            self.match(self.t_lexeme())
            self.sem_analyzer.gen_push_id(sem_rec, SemanticRecord())
        elif self.t_type() == 'MP_NOT':
            Parser.print_tree('97')
            self.match(self.t_lexeme())
            self.factor(SemanticRecord())
        elif self.t_type() == 'MP_LPAREN':
            Parser.print_tree('98')
            self.match(self.t_lexeme())
            self.expression(SemanticRecord()) #AAA
            if self.t_type() == 'MP_RPAREN':
                self.match(self.t_lexeme())
            else:
                self.error('MP_RPAREN')
        else:
            self.error(['MP_INTEGER', 'MP_IDENTIFIER', 'MP_NOT', 'MP_LPAREN'])
        return sem_rec

    def program_identifier(self):
        """
        Expanding Rule 100:
        ProgramIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('100')
            self.program_name = self.t_lexeme()
            self.match(self.program_name)
        else:
            self.error('MP_IDENTIFIER')

    def variable_identifier(self):
        """
        Expanding Rule 101:
        VariableIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('101')
            self.match(self.t_lexeme())
        else:
            self.error('MP_IDENTIFIER')

    def procedure_identifier(self):
        """
        Expanding Rule 102:
        ProcedureIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('102')
            self.cur_proc_name = self.t_lexeme()
            self.match(self.cur_proc_name)
        else:
            self.error('MP_IDENTIFIER')

    def function_identifier(self):
        """
        Expanding Rule 103:
        ProgramIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('103')
            self.cur_func_name = self.t_lexeme()
            self.match(self.cur_func_name)
        else:
            self.error('MP_IDENTIFIER')

    def boolean_expression(self):
        """
        Expanding Rule 104:
        BooleanExpression -> Expression
        """
        accepted_list = ['MP_LPAREN', 'MP_PLUS', 'MP_MINUS',
                         'MP_IDENTIFIER', 'MP_INTEGER', 'MP_NOT']

        if self.t_type() in accepted_list:
            Parser.print_tree('104')
            self.match(self.t_lexeme())
            self.expression()
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

    def ordinal_expression(self):
        """
        Expanding Rule 105:
        OrdinalExpression -> Expression
        """
        accepted_list = ['MP_LPAREN', 'MP_PLUS', 'MP_MINUS',
                         'MP_IDENTIFIER', 'MP_INTEGER', 'MP_NOT']

        if self.t_type() in accepted_list:
            Parser.print_tree('105')
            self.expression()
        else:
            self.error(accepted_list)

    def identifier_list(self, id_list):
        """
        Expanding Rule 106:
        IdentifierList -> Identifier IdentifierTail
        """
        if self.t_type() == 'MP_IDENTIFIER':
            Parser.print_tree('106')
            id_list.append(self.identifier())
            self.identifier_tail(id_list)
        else:
            self.error()
        return id_list

    def identifier_tail(self, id_list):
        """
        Expanding Rule 107,108:
        IdentifierTail -> "," Identifier IdentifierTail
        IdentifierTail -> ?
        """
        if self.t_type() == 'MP_COMMA':
            Parser.print_tree('107')
            self.match(',')
            id_list.append(self.identifier())
            self.identifier_tail(id_list)
        elif self.t_type() == 'MP_COLON':
            Parser.print_tree('108')
            self.epsilon()
        else:
            self.error(['MP_COMMMA', 'MP_COLON'])
        return id_list

    def identifier(self):
        id = self.t_lexeme()
        self.match(id)
        return id


