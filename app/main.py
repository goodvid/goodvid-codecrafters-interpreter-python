import sys
#todo fix why index of '\n' isnt working. its just seeking to the end of the file if theres a comment

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
        #print(i, len(file_contents))
        update = 1
        c = file_contents[i]
        d = file_contents[i : i + 2]
        

        if c == ' ' or c == '\t' or c == '\n':
          pass
        elif d == '//':
          if ("\n" in file_contents[i: ]):
            #print("HELLO",file_contents.index('\n', i) )
            i = file_contents.index('\n', i) # should be go to that index, not jump by that many
            #print(update)
          else:
            i = len(file_contents)
          
        elif d in double_tokens:
          print(double_tokens[d] + ' ' + d + ' null')
          update += 1
        elif c in single_tokens:
          print(single_tokens[c] + ' ' + c + ' null')
        else:
          line_number = file_contents.count("\n", 0, i) + 1
          print(f'[line {line_number}] Error: Unexpected character: {c}', file=sys.stderr)
          isError = True
        i += update

      
    print('EOF  null')
    if isError:
      exit(65)
    
    exit(0)

          
    
if __name__ == "__main__":
    main()
