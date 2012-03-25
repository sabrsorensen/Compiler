
class SemanticRecord(object):

    def __init__(self, lexeme, type, param_mode, param_type, kind):
        self.type = type
        self.lexeme = lexeme
        self.param_mode = param_mode
        self.param_type = param_type
        self.kind = kind
