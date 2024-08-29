import sys
#todo abstract string, number and identifier
#make a class for token and then add tokens to list
def find_line_end(file, start):
  if '\n' in file[start: ]:
    return file.index('\n', start)
  return len(file)
tokens = []
single_tokens = {'/': 'SLASH','<':'LESS', '>': 'GREATER','!': 'BANG', '=': 'EQUAL', ';': 'SEMICOLON','-': 'MINUS','{' : 'LEFT_BRACE', '}': 'RIGHT_BRACE','(': 'LEFT_PAREN', ')': 'RIGHT_PAREN', '*': 'STAR', '.': 'DOT', ',': 'COMMA', '+': 'PLUS'}
double_tokens = {'==':'EQUAL_EQUAL', '!=': 'BANG_EQUAL','<=':'LESS_EQUAL', '>=':'GREATER_EQUAL'}
identifiers = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]
file_contents = []
curr_token = 0  

def tokenize(file_contents):
    i = 0
    
    isError = False
    while i < (len(file_contents)):
        
        
        update = 1
        c = file_contents[i]
        d = file_contents[i : i + 2]
        

        if c == ' ' or c == '\t' or c == '\n':
          pass
        
        elif d == '//':
          if ("\n" in file_contents[i: ]):
            
            i = find_line_end(file_contents, i) # should be go to that index, not jump by that many
            
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
          
          #print(f'STRING \"{string}\" {string}')
          tokens.append(['STRING', f'\"{string}\"', string])
        
        elif c.isdigit():
           # keep going until its not a number no more (also include , .)
          number = ""
          
          start = i

          mods = 0

          
          
          
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

          
          #print(f'NUMBER {value} {number}')
          tokens.append(['NUMBER', value, number])
          i = start - 1
            
          
        elif c.isalpha() or c == '_':
          start = i
          ident = ""
          
          while (start < len(file_contents) and (file_contents[start].isalnum() or file_contents[start] == '_')):
            
            ident += file_contents[start]
            start += 1
          i = start - 1
          if ident in set(identifiers):
             #print(f'{ident.upper()} {ident} null')
             tokens.append([ident.upper(), ident, 'null'])
          else:
            tokens.append(['IDENTIFIER', ident, 'null'])
            #print(f'IDENTIFIER {ident} null')
        
        

        elif d in double_tokens:
          #print(double_tokens[d] + ' ' + d + ' null')
          tokens.append([double_tokens[d], d, 'null'])
          update += 1
        elif c in single_tokens:
          #print(single_tokens[c] + ' ' + c + ' null')
          tokens.append([single_tokens[c], c, 'null'])
        else:
          line_number = file_contents.count("\n", 0, i) + 1
          print(f'[line {line_number}] Error: Unexpected character: {c}', file=sys.stderr)
          isError = True
        i += update

    #tokens.append(['EOF','', 'null']) 
    #print('EOF  null')
    
    
    return isError




def match(token: str): #we know what curr token is, just need what its matching against
   global curr_token
   
   if curr_token >= len(tokens):
      return False
   
   
   if token == 'equality':
      
      if tokens[curr_token][1] in ['!=', '==']:
         curr_token += 1
         return True
      return False
   if token == 'comparison':
      
      if tokens[curr_token][1] in ['>=', '<=','>','<']:
         curr_token += 1
         return True
      return False
   if token == 'term':
      
      if tokens[curr_token][1] in ['+', '-']:
         curr_token += 1
         return True
      return False
   if token == 'factor':
      #curr_token += 1
      if tokens[curr_token][1] in ['/','*']:
         curr_token += 1
         return True
      return False
   if token == 'unary':
      #curr_token += 1
      
      if tokens[curr_token ][1] in ['!', '-']:
         curr_token += 1
         return True
      return False
   if token == 'primary':
      
      #curr_token += 1
      to_check = tokens[curr_token ][0] 
      
      if to_check in ['NUMBER','STRING','TRUE','FALSE','NIL']: #bc lazy, non consistent token check
         curr_token += 1
         return [True, to_check]
      return [False, []]
   if token == 'paren':
      #curr_token += 1
      if tokens[curr_token][1] in ['(',')']:
         curr_token += 1
         return True
      return False
   return False
def expression():
   return is_equality()

def is_equality():
   left = is_comp()
   while (match('equality')):
      operator = tokens[curr_token - 1][0]
      right = is_comp()
      left = [left, operator, right]
   return left

def is_comp():
   left = is_term()
   while(match('compare')):
      operator = tokens[curr_token - 1][0]
      right = is_term()
      left = [left, operator, right]
   return left

def is_term():
   left = is_factor()
   while(match('term')):
      operator = tokens[curr_token - 1][1]
      right = is_term()
      left = '('+operator+ ' ' + str(left) + ' ' + str(right) + ')'
   return left

def is_factor():
   left = is_unary()
   while (match('factor')):
      operator = tokens[curr_token - 1][1]
      right = is_unary()
      #left = [left, operator, right]
      left = '('+operator+ ' ' + str(left) + ' ' + str(right) + ')'
   return left

def is_unary():
   if (match('unary')):
      
      operator = tokens[curr_token - 1][1]
      right = is_unary()
      return '(' + operator + ' ' +   str(right) + ')'
   else:
      return is_prim()
   
def is_prim():
   check = match('primary')
   #curr_token -= 1
   
   if (check[0] and check[1] in ['TRUE','FALSE', 'NIL']):
      return check[1].lower()
   if (check[0] and check[1] in ['NUMBER', 'STRING'] ):
      return tokens[curr_token - 1][2]
   
   if match('paren'):
      
      expr = expression()
      if match('paren'):
         return '(group ' + str(expr) + ')'
   
   
def parse():
   
   return expression()
  #  while i < len(tokens):
  #     token = tokens[i]

  #     if token[0] == 'LEFT_PAREN':
  #        stack = ['(']
  #        start = i + 1
  #        content = ['(group' ]
  #        while (start < len(tokens)):
  #           content.append(tokens[start][2])
  #           if tokens[start][0] == 'LEFT_PAREN':
  #              stack.append('LEFT_PAREN')
  #           elif tokens[start][0] == 'RIGHT_PAREN':
  #              stack.pop()
  #           start += 1
  #        if stack:
  #           print("Error: Unmatched parentheses.", stack)
  #        else:
  #           print(' '.join(content))
  #        i = start
  #     if token[1] in identifiers:
  #           print(token[1])#.lower())22
  #         #dd
  #     if token[0] == 'NUMBER':
  #            print(token[2])
          
  #     if token[0] == 'STRING':
  #            print(token[2])
  #     i += 1
def main():
    
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 1:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in set(['tokenize', 'parse']):
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    
    

    isError = tokenize(file_contents)

    if command == "parse":
       print(parse())
    
    if command == 'tokenize':
      for token in tokens:
            print(token[0],  token[1],  token[2])
      print('EOF  null')
    
    if isError:
       exit(65)
    exit(0)
       
    

          
    
if __name__ == "__main__":
    main()
