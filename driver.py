__authors__ = 'Sam Sorensen', 'Keith Smith', 'Anna Andriyanova'
__date__ = 'Spring 2012'

from Scanner import Scanner
from Parser import Parser
import sys

def main():
    input_file = sys.argv[1]
#    output_file = open('token_file.txt', 'w')

    s = Scanner()
    s.open_file(input_file)
    s.get_token()
    p = Parser(s.tokens)
    print p.system_goal()

#    for token in s.tokens:
#        #tokens to standard out
#        print "%s" % token
#        #tokens to file
#        output_file.write('%s\n' % token)
#
#    output_file.close()

main()