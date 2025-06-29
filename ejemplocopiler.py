# === MiniLang Compiler ===

import re

# --------------------------------------
# 1. Analisis lexico
# --------------------------------------

token_specification = [
    ('NUMBER',   r'\d+'),
    ('LET',      r'let'),
    ('PRINT',    r'print'),
    ('IDENT',    r'[a-zA-Z_]\w*'),
    ('ASSIGN',   r'='),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('TIMES',    r'\*'),
    ('DIVIDE',   r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)


def tokenize(code):
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', int(value)))
        elif kind in {'LET', 'PRINT', 'ASSIGN', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'}:
            tokens.append((kind, value))
        elif kind == 'IDENT':
            tokens.append(('IDENT', value))
        elif kind == 'NEWLINE':
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r}')
    return tokens

# --------------------------------------
# 2. Analisis sintactico
# --------------------------------------
#
#   <program>       ::= <statement> { <statement> }
#
#   <statement>     ::= "LET" <identifier> "ASSIGN" <expression>
#                   | "PRINT" "LPAREN" <expression> "RPAREN"
#
#   <expression>    ::= <term> { ("PLUS" | "MINUS") <term> }
#
#   <term>          ::= <factor> { ("TIMES" | "DIVIDE") <factor> }
#
#   <factor>        ::= "NUMBER"
#                 | "IDENT"
#                 | "LPAREN" <expression> "RPAREN"
#    
# --------------------------------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type=None):
        token = self.tokens[self.pos]
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f'Expected {expected_type}, got {token[0]}')
        self.pos += 1
        return token

    def parse(self):
        stmts = []
        while self.pos < len(self.tokens):
            stmts.append(self.statement())
        return stmts

    def statement(self):
        if self.tokens[self.pos][0] == 'LET':
            self.consume('LET')
            name = self.consume('IDENT')[1]
            self.consume('ASSIGN')
            expr = self.expression()
            return ('assign', name, expr)
        elif self.tokens[self.pos][0] == 'PRINT':
            self.consume('PRINT')
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return ('print', expr)
        else:
            raise SyntaxError('Invalid statement')

    def expression(self):
        left = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            op = self.consume()[0]
            right = self.term()
            left = (op.lower(), left, right)
        return left

    def term(self):
        left = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('TIMES', 'DIVIDE'):
            op = self.consume()[0]
            right = self.factor()
            left = (op.lower(), left, right)
        return left

    def factor(self):
        token = self.tokens[self.pos]
        if token[0] == 'NUMBER':
            return ('number', self.consume('NUMBER')[1])
        elif token[0] == 'IDENT':
            return ('var', self.consume('IDENT')[1])
        elif token[0] == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError('Invalid factor')

# --------------------------------------
# 3. Generacion de codigo
# --------------------------------------

def generate_python(ast):
    output = []
    for node in ast:
        output.append(gen_stmt(node))
    return '\n'.join(output)

def gen_stmt(node):
    if node[0] == 'assign':
        return f"{node[1]} = {gen_expr(node[2])}"
    elif node[0] == 'print':
        return f"print({gen_expr(node[1])})"

def gen_expr(expr):
    if expr[0] == 'number':
        return str(expr[1])
    elif expr[0] == 'var':
        return expr[1]
    elif expr[0] in {'plus', 'minus', 'times', 'divide'}:
        op = {'plus': '+', 'minus': '-', 'times': '*', 'divide': '/'}[expr[0]]
        return f"({gen_expr(expr[1])} {op} {gen_expr(expr[2])})"

# --------------------------------------
# Codigo principal
# --------------------------------------

def compile_minilang(code):
    tokens = tokenize(code)
    print("\nTokens:")
    print(tokens)


    print("\nAST")
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)
    py_code = generate_python(ast)
    return py_code

if __name__ == '__main__':

    example_code = \
    """
    let x = 5
    let y = 10
    print(x + y * 2)
    """
    compiled = compile_minilang(example_code)
    print("\nConversion a python:\n")
    print(compiled)
    print("\n--- Ejecucion ---")
    exec(compiled)
