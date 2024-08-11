import sys
#todo fix why index of '\n' isnt working. its just seeking to the end of the file if theres a comment

def find_line_end(file, start):
  if '\n' in file[start: ]:
    return file.index('\n', start)
  return len(file)
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
            #print("HELLO",find_line_end(file_contents, i) )
            i = find_line_end(file_contents, i) # should be go to that index, not jump by that many
            #print(update)
          else:
            i = len(file_contents)
        elif c == '\"':
          start = i + 1
          line_end = find_line_end(file_contents, i)
          
          if '\"' in file_contents[start : line_end]:
             end = file_contents.index('\"', start, line_end)
          else:
             i = line_end
             line_number = file_contents.count("\n", 0, i) + 1
             print(f"[line {line_number}] Error: Unterminated string.", file=sys.stderr)
             isError = True
             continue

          string = ""

          while start < end :
            string += file_contents[start]
            start += 1
          i = end
          
          print(f'STRING \"{string}\" {string}')
        
        elif c.isdigit():
           # keep going until its not a number no more (also include , .)
          number = ""
          
          start = i

          mods = 0

          
          
          #print(f'NUMBER {number} {number} {start}')
          while (start < len(file_contents) and ((file_contents[start].isdigit() or file_contents[start] == '.'))):
             if (file_contents[start] == '.'):
                mods += 1
             if mods > 1:
                i = start - 1
                break
             number += file_contents[start]
             start += 1
          
          if number[-1] == '.':
             number = number[:-1]
             start -= 1
          value = number
          number = float(number)

          
          print(f'NUMBER {value} {number}')
          i = start - 1
            
          
        elif c.isalpha() or c == '_':
          start = i
          ident = ""
          
          while (start < len(file_contents) and file_contents[start] != ' '):
            #print(start)
            ident += file_contents[start]
            start += 1
          i = start - 1
          print(f'IDENTIFIER {ident} null')
        
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
