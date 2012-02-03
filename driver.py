from Scanner import Scanner
import sys

def main():
    input_file = sys.argv[1]
    s = Scanner()
    s.open_file(input_file)
    s.get_token()

main()