import sys

# three pronged : left, operator, right
# two pronged: operator, right
# literal: number, string or true, false, nil
# group: (group expression)

class three_pronged:
    def __init__(self, oper_type, oper, left, right):
        self.oper_type = oper_type
        self.oper = oper
        self.left = left
        self.right = right
    def __str__(self):
        return f'({self.oper} {self.left} {self.right})'

class two_pronged:
    def __init__(self, oper, right):
        self.oper = oper
        self.right = right
    def __str__(self):
        return f'({self.oper} {self.right})'

class literal:
    def __init__(self, literal):
        self.literal = literal
    def __str__(self):
        return f'{self.literal}'

class group:
    def __init__(self, expr):
        self.expr = expr
    def __str__(self):
        return f'(group {self.expr})'
#todo, add line number to token as 4th value
# you have to make all the types of parsing a class, or else you are cooked for evaluation
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
final_expr = None
isError = False
   
def match(token: str): #we know what curr token is, just need what its matching against
   global curr_token
   
   if curr_token >= len(tokens):
      return False
   
   
   if token == 'equality':
      
      if tokens[curr_token][1] in ['!=', '==']:
         curr_token += 1
         return True
      return False
   if token == 'compare':
      
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
      to_check = tokens[curr_token][0] 
      
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
   output = is_equality()
   
   return output

def missing(token: str, line_number: int):
   global isError
   print(f'[line {line_number}] Error at \'{token}\': Expect expression', file=sys.stderr)
   isError = True

def is_equality():
   left = is_comp()
   while (match('equality')):
      operator = tokens[curr_token - 1][1]
      right = is_comp()
      
      if not right:
         missing(tokens[curr_token - 1][1], tokens[curr_token - 1][3])
         return
      left = three_pronged(oper_type='equality', oper=operator, left=left, right=right)
   return left

def is_comp():
   left = is_term()
   while(match('compare')):
      operator = tokens[curr_token - 1][1]
      right = is_term()
      if not right:
         missing(tokens[curr_token - 1][1], tokens[curr_token - 1][3])
         return
      left = three_pronged(oper_type='compare', oper=operator, left=left, right=right)
   return left

def is_term():
   left = is_factor()

   while(match('term')):
      operator = tokens[curr_token - 1][1]
      right = is_factor()
      if not right:
         missing(tokens[curr_token - 1][1], tokens[curr_token - 1][3])
         return
      left = three_pronged(oper_type='term', oper=operator, left=left, right=right)
   return left

def is_factor():
   left = is_unary()
   while (match('factor')):
      operator = tokens[curr_token - 1][1]
     
      right = is_unary()
      if not right:
         missing(tokens[curr_token - 1][1], tokens[curr_token - 1][3])
         return
      
      left = three_pronged(oper_type='factor', oper=operator, left=left, right=right)
   return left

def is_unary():
   if (match('unary')):
      
      operator = tokens[curr_token - 1][1]
      right = is_unary()
      if not right:
         missing(tokens[curr_token - 1][1], tokens[curr_token - 1][3])
         return
     
      return two_pronged(oper=operator, right=right)
   else:
      return is_prim()
   
def is_prim():
   check = match('primary')
   if hasattr(check, "__len__"):
   
      if (check[0] and check[1] in ['TRUE','FALSE', 'NIL']):
         return literal(check[1].lower())
      if (check[0] and check[1] in ['NUMBER', 'STRING'] ):
       
         return literal(tokens[curr_token - 1][2])
   
   if match('paren'):
      
      expr = expression()
      
      if match('paren'):
         #return '(group ' + str(expr) + ')'
         return group(expr=expr)
      else:
         missing('(', 1)
      

def tokenize(file_contents):
    global isError
    i = 0
    
    isError = False
    while i < (len(file_contents)):
        
        
        update = 1
        c = file_contents[i]
        d = file_contents[i : i + 2]

        line_number = file_contents.count("\n", 0, i) + 1
        

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
          tokens.append(['STRING', f'\"{string}\"', string, line_number])
        
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
          tokens.append(['NUMBER', value, number, line_number])
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
             tokens.append([ident.upper(), ident, 'null', line_number])
          else:
            tokens.append(['IDENTIFIER', ident, 'null', line_number])
            #print(f'IDENTIFIER {ident} null')
        
        

        elif d in double_tokens:
          #print(double_tokens[d] + ' ' + d + ' null')
          tokens.append([double_tokens[d], d, 'null', line_number])
          update += 1
        elif c in single_tokens:
          #print(single_tokens[c] + ' ' + c + ' null')
          tokens.append([single_tokens[c], c, 'null', line_number])
        else:
          line_number = file_contents.count("\n", 0, i) + 1
          print(f'[line {line_number}] Error: Unexpected character: {c}', file=sys.stderr)
          isError = True
        i += update

    #tokens.append(['EOF','', 'null']) 
    #print('EOF  null')  
   
def parse():
   global final_expr
   final_expr = expression()
   
   return final_expr

def evaluate(expr):
   def remove_trailing_zeros(num):
         if num == 0:
            return 0
         if '.' not in str(num):
            return num 
    # Convert to string and strip trailing zeros and the decimal point if needed
         num_str = str(num).rstrip('0').rstrip('.')
         
         # Check if the number is an integer after removing the trailing zeros
         if '.' not in num_str:
            return int(num_str)
         else:
            return float(num_str)
      

   if isinstance(expr, three_pronged):
      left = evaluate(expr.left)
      right = evaluate(expr.right)
      oper = expr.oper
      
      if expr.oper_type == 'factor':
         if oper == '*':
            return left * right
         if oper == '/':
            return remove_trailing_zeros(left   / right)
      
      if expr.oper_type == 'term':
         if oper == '+':
            if type(left) == str and type(right) == str:
               return left + right
            return remove_trailing_zeros(left + right)
         if oper == '-':
            return remove_trailing_zeros(left - right)

      if expr.oper_type == 'compare':
         if oper == '>':
            return str(left > right).lower()
         if oper == '<':
            return str(left < right).lower()
         if oper == '>=':
            return str(left >= right).lower()
         if oper == '<=':
            return str(left <= right).lower()
   if isinstance(expr, two_pronged):
      right = evaluate(expr.right)
      if expr.oper == '-':
         if not isinstance(right, str):
            return -1 * right
      if expr.oper == '!':
         if right == 'true':
            return 'false'
         if right in ['false', 'nil']:
            return 'true'
         return str(not right).lower()
   
   if isinstance(expr, literal): 
      
      
      if isinstance(expr.literal, str): 
         return expr.literal
      return remove_trailing_zeros(expr.literal)
   if isinstance(expr, group):
      #print('ee', expr.expr)
      return evaluate(expr.expr)
   
def main():
    
    
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 1:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in set(['tokenize', 'parse', 'evaluate']):
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    
    

    tokenize(file_contents)
    

    
    
    if command == 'tokenize':
      for token in tokens:
            print(token[0],  token[1],  token[2])
      print('EOF  null')
      if isError:
         exit(65)
      exit(0)
    
    parse()
    
    if command == "parse":
      if final_expr: print(final_expr)
      if isError:
         exit(65)
      exit(0)
    
    if command == 'evaluate':
       print(evaluate(final_expr) )
    
    if isError:
       exit(65)
    exit(0)
       
    

          
    
if __name__ == "__main__":
    main()
