from Scanner import Scanner
import sys

def main():
    input_file = sys.argv[1]
    output_file = open('token_file.txt', 'w')

    s = Scanner()
    s.open_file(input_file)
    s.get_token()
    for token in s.tokens:
        output_file.write('%s' % token)
    print s.tokens

    output_file.close()

main()