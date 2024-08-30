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