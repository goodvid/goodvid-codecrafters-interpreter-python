import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 1:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    
    single_tokens = {'/': 'SLASH','<':'LESS', '>': 'GREATER','!': 'BANG', '=': 'EQUAL', ';': 'SEMICOLON','-': 'MINUS','{' : 'LEFT_BRACE', '}': 'RIGHT_BRACE','(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', '*': 'STAR', '.': 'DOT', ',': 'COMMA', '+': 'PLUS'}
    double_tokens = {'==':'EQUAL_EQUAL', '!=': 'BANG_EQUAL','<=':'LESS_EQUAL', '>=':'GREATER_EQUAL'}
    #
    isError = False
    i = 0
    while i < (len(file_contents)):
        update = 1
        c = file_contents[i]
        d = file_contents[i : i + 2]
        

        if c == ' ' or c == '\t':
          if c == '\t':
             print('hey')
          pass
        elif d == '//':
          if ('\n' in file_contents[i: ]):
            update += file_contents.index('\n', i)
          else:
            update += len(file_contents)
          
        elif d in double_tokens:
          print(double_tokens[d] + ' ' + d + ' null')
          update += 1
        elif c in single_tokens:
          print(single_tokens[c] + ' ' + c + ' null')
        else:
          line_number = file_contents.count("\n", 0, file_contents.find(c)) + 1
          print(f'[line {line_number}] Error: Unexpected character: {c}!', file=sys.stderr)
          isError = True
        i += update

      # for i in range(len(line)):
      #   c = line[i]
      #   print(line[i], i)
        # if line[i : i + 2] == "==":
        #   print("EQUAL_EQUAL == null")
        # elif c in single_tokens:
        #   print(single_tokens[c] + ' ' + c + ' null')
        # else:
        #   print(f'[line {i + 1}] Error: Unexpected character: {c}', file=sys.stderr)
        #   isError = True
    print('EOF  null')
    if isError:
      exit(65)
    
    exit(0)

          
    
if __name__ == "__main__":
    main()
