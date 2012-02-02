import re

class Scanner():

    def __init__(self):
        self.contents = []

    def open_file(self, input_file):
        f = open(input_file)

    def get_token(self):
        for line in self.contents:
            print line
            re.sub(r'\s', '', line)
            print line





s = Scanner()
s.open_file('C:\Users\Anna\Documents\Code\Aptana\workspace\Compiler\sample.txt')
s.get_token()