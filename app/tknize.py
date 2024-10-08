import sys
from enum import Enum



def find_line_end(file, start):
  if '\n' in file[start: ]:
    return file.index('\n', start)
  return len(file)
def tokenize(file_contents):
    i = 0
    single_tokens = {'/': 'SLASH','<':'LESS', '>': 'GREATER','!': 'BANG', '=': 'EQUAL', ';': 'SEMICOLON','-': 'MINUS','{' : 'LEFT_BRACE', '}': 'RIGHT_BRACE','(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', '*': 'STAR', '.': 'DOT', ',': 'COMMA', '+': 'PLUS'}
    double_tokens = {'==':'EQUAL_EQUAL', '!=': 'BANG_EQUAL','<=':'LESS_EQUAL', '>=':'GREATER_EQUAL'}
    isError = False
    i = 0
    tokens = []
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
          tokens.append(['STRING', string, string])
        
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
          tokens.append(['NUMBER', value, number])
          i = start - 1
            
          
        elif c.isalpha() or c == '_':
          start = i
          ident = ""
          
          while (start < len(file_contents) and (file_contents[start].isalnum() or file_contents[start] == '_')):
            #print(start)
            ident += file_contents[start]
            start += 1
          i = start - 1
          if ident in set(["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]):
             print(f'{ident.upper()} {ident} null')
             tokens.append([ident.upper(), ident, 'null'])
          else:
            tokens.append(['IDENTIFIER, ident, null'])
            print(f'IDENTIFIER {ident} null')
        
        

        elif d in double_tokens:
          print(double_tokens[d] + ' ' + d + ' null')
          tokens.append([double_tokens[d], d, 'null'])
          update += 1
        elif c in single_tokens:
          print(single_tokens[c] + ' ' + c + ' null')
          tokens.append([single_tokens[c], c, 'null'])
        else:
          line_number = file_contents.count("\n", 0, i) + 1
          print(f'[line {line_number}] Error: Unexpected character: {c}', file=sys.stderr)
          isError = True
        i += update

      
    print('EOF  null')
    if isError:
      exit(65)
    
    return tokens