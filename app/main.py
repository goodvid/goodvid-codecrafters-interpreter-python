import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # read per line, then read per token
    single_tokens = {';': 'SEMICOLON','-': 'MINUS','{' : 'LEFT_BRACE', '}': 'RIGHT_BRACE','(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', '*': 'STAR', '.': 'DOT', ',': 'COMMA', '+': 'PLUS'}
    isError = False
    for line in file_contents:
      for i, c in enumerate(line):
        if c in single_tokens:
          print(single_tokens[c] + ' ' + c + ' null')
        else:
          print(f'[line {i + 1}] Error: Unexpected character: {c}', file=sys.stderr)
          isError = True
    print('EOF  null')
    if isError:
      exit(65)
    
    exit(1)

          
    
if __name__ == "__main__":
    main()
