from Scanner import Scanner
import sys

def main():
    input_file = sys.argv[1]
    #input_file = "program1.mp"
    output_file = open('token_file.txt', 'w')

    s = Scanner()
    s.open_file(input_file)
    s.get_token()
    print s.tokens

    for token_line in s.tokens:
        output_file.write("%s" % token_line)
main()