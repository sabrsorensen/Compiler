from semantic_record import semantic_record

class semantic_entry(object):

    def __init__(self):
        self.empty = True;
        self.depth
        self.current_record = self.semantic_record()
        self.semantic_record_stack


    def put(self, record):
        if self.empty:
            self.empty = False
        if self.current_record is not None:
            semantic_record_stack.insert(0,self.current_record)

        self.current_record = record
        self.depth += 1

    def back_out(self):
        if semantic_record is not None:
            if len(self.semantic_record_stack) >= 1:
                self.current_record = self.semantic_record_stack.pop()
            if len(self.semantic_record_stack) == 0:
                self.semantic_record_stack = None
        else:
            self.current_record = None
            self.empty = True

    def get_current_record(self):
        return self.current_record

    def is_empty(self):
        return self.empty

    def get_depth(self):
        return self.depth

    def to_string(self):
        self.output.append(self.current_record)
        if self.semantic_record_stack is not None:
            for sem_record in semantic_record_stack:
                self.output.append(sem_record)
                self.output.append(" ")

        self.output.append('\n')
        return output
