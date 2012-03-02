import inspect
import logging

class Parser(object):


    def __init__(self, tokens):
        self.index = len(tokens)
        self.tokens = iter(tokens)
        self.cur_token = self.tokens.next()     #Default token holder
        self.next_token = self.tokens.next()    #LL2 lookahead token holder for when needed

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

    def match(self, lexeme):
        self.cur_token = self.next_token
        try:
            self.next_token = self.tokens.next()
        except StopIteration:
            pass
        logging.info("Matched '%s' in %s()" % (lexeme, inspect.stack()[1][3]))
        return False


    ############### Rule handling functions ###############


    def system_goal(self):
        """
        Expanding Rule 1:
        System Goal -> Program $
        """
        if self.t_type() == 'MP_PROGRAM':
            self.program()
            if self.t_type() == 'MP_EOF':
                self.match('EOF')
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
            self.program_heading()
            self.match(';')
            self.block()
            self.match('.')
        else:
            self.error('MP_PROGRAM')

    def program_heading(self):
        """
        Expanding Rule 3:
        "program" Identifier
        """
        if self.t_type() == 'MP_PROGRAM':
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
            self.match('var')
            self.variable_declaration()
            self.match(';')
            self.variable_declaration_tail()
        elif self.t_type() in eps_list:
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
        eps_list = ['MP_BEGIN', 'MP_FUNCTION', 'MP_PRODCEDURE']
        if self.t_type() == 'MP_IDENTIFIER':
            self.variable_declaration()
            self.match(';')
            self.variable_declaration_tail()
        elif self.t_type() in eps_list:
            self.epsilon()
        else:
            self.error(eps_list.append('MP_IDENTIFIER'))

    def variable_declaration(self):
        """
        Expanding Rule 9:
        VariableDeclaration -> IdentifierList ":" Type
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.identifier_list()
            self.match(':')
            self.type()
        else:
            self.error('MP_IDENTIFIER')

    def type(self):
        """
        Expanding Rules 10, 11:
        Type -> "Integer"
             -> "Float"
        """
        accepted_list = ['MP_FLOAT', 'MP_INTEGER']
        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

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
            self.error(['MP_PROCEDURE', 'MP_FUNCTION', 'MP_BEGIN'])

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
            self.error('MP_PROCEDURE')


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
            self.error('MP_FUNCTION')

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
            self.error('MP_PROCEDURE')

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
            self.error('MP_FUNCTION')

    def optional_formal_parameter_list(self):
        """
        Expanding Rules 19, 20:
        OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
                                    -> epsilon
        """
        eps_list = ['MP_FLOAT', 'MP_INTEGER', 'MP_SCOLON']
        if self.t_type() == 'MP_LPAREN':
            self.match('(')
            self.formal_parameter_section()
            self.formal_parameter_section_tail()
            self.match(')')
        elif self.t_type() in eps_list:
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
            self.match(';')
            self.formal_parameter_section()
            self.formal_parameter_section_tail()
        elif self.t_type() == 'MP_RPAREN':
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
            self.value_parameter_section()
        elif self.t_type() == 'MP_VAR':
            self.variable_parameter_section()
        else:
            self.error(['MP_IDENTIFIER', 'MP_VAR'])

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
            self.error('MP_IDENTIFIER')


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
            self.error('MP_VAR')


    def statement_part(self):
        """
        Expanding Rule 27:
        StatementPart -> CompoundStatement
        """
        if self.t_type() == 'MP_BEGIN':
            self.compound_statement()
        else:
            self.error('MP_BEGIN')


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
            self.match(';')
            self.statement()
            self.statement_tail()
        elif self.t_type() in eps_list:
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
            self.empty_statement()
        elif self.t_type() == 'MP_BEGIN':
            self.compound_statement()
        elif self.t_type() == 'MP_READ':
            self.read_statement()
        elif self.t_type() == 'MP_WRITE':
            self.write_statement()
        elif self.t_type() == 'MP_IDENTIFIER':
            procedure_list = ['MP_END', 'MP_SCOLON', 'MP_LPAREN']
            procedure_list_2 = ['MP_COLON', 'MP_ASSIGN']
            if self.next_token.token_type in procedure_list:
                self.procedure_statement()
            elif self.next_token.token_type in procedure_list_2:
                self.assignment_statement()
            else:
                self.error(['MP_END', 'MP_SCOLON', 'MP_LPAREN', 'MP_COLON', 'MP_ASSIGN'])
        elif self.t_type() == 'MP_IF':
            self.if_statement()
        elif self.t_type() == 'MP_WHILE':
            self.while_statement()
        elif self.t_type() == 'MP_REPEAT':
            self.repeat_statement()
        elif self.t_type() == 'MP_FOR':
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
            self.epsilon()
        else:
            self.error(accepted_list)

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
            self.error('MP_READ')

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
            self.error(['MP_COMMA', 'MP_RPAREN'])

    def read_parameter(self):
        """
        Expanding Rule 46 :
        ReadParameter -> VariableIdentifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.variable_identifier()
        else:
            self.error('MP_IDENTIFIER')

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
            self.error('MP_WRITE')

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
            self.error(['MP_COMMA', 'MP_PAREN'])


    def write_parameter(self):
        """
        Expanding Rule 50 :
        WriteParameter -> OrdinalExpression
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
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
            self.match('else')
            self.statement()
        elif self.t_type() in eps_list:
            self.epsilon()
        else:
            self.error(eps_list.extend('MP_ELSE'))

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

    def while_statement(self):
        """
        Expanding Rule 57:
        WhileStatement -> "while" BooleanExpression "do" Statement
        """
        if self.t_type() == 'MP_WHILE':
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
            self.ordinal_expression()
        else:
            self.error(accepted_list)

    def step_value(self):
        """
        Expanding Rules 61, 62 :
        StepValue -> "to"
                  -> "downto"
        """
        accepted_list = ['MP_TO', 'MP_DOWNTO']
        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

    def final_value(self):
        """
        Expanding Rule 63:
        FinalValue -> OrdinalExpression
        """
        accepted_list = ['MP_LPAREN','MP_PLUS','MP_MINUS','MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']
        if self.t_type() in accepted_list:
            self.ordinal_expression()
        else:
            self.error(accepted_list)


    def procedure_statement(self):
        """
        Expanding Rule 64:
        ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
        """
        if self.t_type() == 'MP_IDENTIFIER':
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
            self.match('(')
            self.actual_parameter()
            self.actual_parameter_tail()
            self.match(')')
        elif self.t_type() in eps_list:
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
            self.match(',')
            self.actual_parameter()
            self.actual_parameter_tail()
        elif self.t_type() == 'MP_RPAREN':
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
            self.relational_operator()
            self.simple_expression()
        elif self.t_type() in eps_list:
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
        accepted_list = ['MP_LTHAN', 'MP_LEQUAL', 'MP_GTHAN',
                         'MP_GEQUAL', 'MP_EQUAL', 'MP_NEQUAL']
        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

    def simple_expression(self):
        """
        Expanding Rule 79 :
        SimpleExpression -> OptionalSign Term TermTail
        """
        accepted_list = ['MP_LPAREN', 'MP_PLUS', 'MP_MINUS',
                         'MP_IDENTIFIER', 'MP_INTEGER', 'MP_NOT']

        if self.t_type() in accepted_list:
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
            #self.optional_sign()
            self.adding_operator()
            self.term()
            self.term_tail()
        elif self.t_type() in eps_list:
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
        accepted_list = ['MP_PLUS','MP_MINUS']
        eps_list = ['MP_IDENTIFIER', 'MP_INTEGER','MP_NOT']

        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        elif self.t_type() in eps_list:
            self.epsilon()
        else:
            self.error(accepted_list.extend(eps_list))

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
            self.multiplying_operator()
            self.factor()
            self.factor_tail()
        elif self.t_type() in eps_list:
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
        accepted_list = ['MP_TIMES', 'MP_DIV', 'MP_MOD', 'MP_AND']

        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

    def factor(self):
        """
        Expanding Rule 95,96,97,98,99:
        Factor -> UnsignedInteger
        Factor -> VariableIdentifier
        Factor -> "not" Factor
        Factor -> "(" Expression ")"
        Factor -> FunctionIdentifier OptionalActualParameterList
        """
        accepted_list = ['MP_INTEGER', 'MP_IDENTIFIER', 'MP_NOT', 'MP_LPAREN']
        if self.t_type() in accepted_list:
            self.match(self.t_lexeme())
        else:
            self.error(accepted_list)

    def program_identifier(self):
        """
        Expanding Rule 100:
        ProgramIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.match(self.t_lexeme())
        else:
            self.error('MP_IDENTIFIER')

    def variable_identifier(self):
        """
        Expanding Rule 101:
        VariableIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.match(self.t_lexeme())
        else:
            self.error('MP_IDENTIFIER')

    def procedure_identifier(self):
        """
        Expanding Rule 102:
        ProcedureIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.match(self.t_lexeme())
        else:
            self.error('MP_IDENTIFIER')

    def function_identifier(self):
        """
        Expanding Rule 103:
        ProgramIdentifier -> Identifier
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.match(self.t_lexeme())
        else:
            self.error('MP_IDENTIFIER')

    def boolean_expression(self):
        """
        Expanding Rule 104:
        BooleanIdentifier -> Identifier
        """
        accepted_list = ['MP_IDENTIFIER', 'MP_PLUS', 'MP_MINUS', 'MP_IDENTIFIER', 'MP_INTEGER', 'MP_NOT']

        if self.t_type() in accepted_list:
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
            self.expression()
        else:
            self.error(accepted_list)

    def identifier_list(self):
        """
        Expanding Rule 106:
        IdentifierList -> Identifier IdentifierTail
        """
        if self.t_type() == 'MP_IDENTIFIER':
            self.identifier()
            self.identifier_tail()
        else:
            self.error()

    def identifier_tail(self):
        """
        Expanding Rule 107,108:
        IdentifierTail -> "," Identifier IdentifierTail
        IdentifierTail -> ?
        """
        if self.t_type() == 'MP_COMMA':
            self.match(',')
            self.identifier()
            self.identifier_tail()
        elif self.t_type() == 'MP_COLON':
            self.epsilon()
        else:
            self.error(['MP_COMMMA', 'MP_COLON'])

    def identifier(self):
        self.match(self.t_lexeme())

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

