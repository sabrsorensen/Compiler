from Scanner import Scanner
import sys

def main():
    input_file = sys.argv[1]
#    to rewind one character back
#    f = open(input_file)
#    print f.read(1)
#    print f.read(1)
#    print f.seek(-1, 1)
#    print f.read(1)

    s = Scanner()
    s.open_file(input_file)
    s.get_token()
    print s.tokens

main()