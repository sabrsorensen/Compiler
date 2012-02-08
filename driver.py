from Scanner import Scanner
import sys

def main():
    input_file = sys.argv[1]
    output_file = open('token_file.txt')

    s = Scanner()
    s.open_file(input_file)
    s.get_token()
    print s.tokens

main()