from Scanner import Scanner
import sys

def main():
    input_file = sys.argv[1]
    #input_file = "program1.mp"
    output_file = open('token_file.txt', 'w')

    s = Scanner()
    s.open_file(input_file)
    s.get_token()
    for token in s.tokens:
        #tokens to standard out
        print "%s" % token
        #tokens to file
        output_file.write('%s\n' % token)

    output_file.close()

main()