__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

import logging

class SemanticRecord(object):

    def __init__(self):
        self.type = ''
        self.lexeme = ''
        self.param_mode = ''
        self.kind = ''
        self.size = 0
        self.offset = None
        self.label1 = ''
        self.label2 = ''
        self.loop_label = ''
        self.depth = None
        self.negative = 0

    def __repr__(self):
        return "[%7s |%7s |%7s |%7s |%7s |%7s ]" %   (self.lexeme, self.kind,
                                                    self.type, self.size,
                                                    self.offset, self.depth)

    def set_size(self, type):
        """
        Setting the size of the entry based on its type
        """
        if type.lower() in ['integer', 'boolean']:
            self.size = 1
        elif  type.lower() == 'float':
            self.size = 2
        else:
            logging.error('Unknown type: %s' % type)

        # @Sam, @Keith: hey, what about string literal? Char?





















