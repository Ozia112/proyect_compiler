# === Compilador del Lenguaje Tan ===
# Basado en numeracion maya (base 20)

import re

# --------------------------------------
# 1. Analisis Lexico
# --------------------------------------

# Funcion para convertir numeros mayas a decimal
def maya_to_decimal(maya_num):
    """
    Convierte un numero maya a decimal
    . = 1
    | = 5
    0 = 0
    , = separador de bloques (multiplos de 20)
    """
    # Eliminar espacios
    maya_num = maya_num.strip()
    
    # Si es solo 0, retornar 0
    if maya_num == '0':
        return 0
    
    # Dividir por bloques usando comas
    blocks = maya_num.split(',')
    
    total = 0
    power = len(blocks) - 1
    
    for block in blocks:
        block = block.strip()
        block_value = 0
        
        # Contar puntos y barras
        dots = block.count('.')
        bars = block.count('|')
        zeros = block.count('0')
        
        # Si hay un 0 en el bloque, el valor es 0
        if zeros > 0:
            block_value = 0
        else:
            # Primero van los puntos, luego las barras
            block_value = dots + (bars * 5)
        
        # Multiplicar por la potencia de 20 correspondiente
        total += block_value * (20 ** power)
        power -= 1
    
    return total

# Especificacion de tokens
token_specification = [
    ('MAYA_NUM', r'(?:[.|]+\s*|0)(?:\s*,\s*(?:[.|]+\s*|0))*'),  # Numeros mayas
    ('XIIB',     r'xiib'),                                      # let
    ('TSIIBIL',  r'tsiibil'),                                   # print
    ('KEET',     r'keet'),                                      # =
    ('IDENT',    r'[a-zA-Z_]\w*'),                             # Identificadores
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('TIMES',    r'\*'),
    ('DIVIDE',   r'/'),
    ('LPAREN',   r'\['),                                        # Usando [ en lugar de (
    ('RPAREN',   r'\]'),                                        # Usando ] en lugar de )
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
        
        if kind == 'MAYA_NUM':
            decimal_value = maya_to_decimal(value)
            tokens.append(('NUMBER', decimal_value))
        elif kind in {'XIIB', 'TSIIBIL', 'KEET', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'}:
            tokens.append((kind, value))
        elif kind == 'IDENT':
            # No tokenizar palabras reservadas como identificadores
            if value not in ['xiib', 'tsiibil', 'keet']:
                tokens.append(('IDENT', value))
        elif kind in ('NEWLINE', 'SKIP'):
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Caracter inesperado {value!r}')
    
    return tokens

# --------------------------------------
# 2. Analisis Sintactico
# --------------------------------------
# Gramatica:
#   <program>       ::= <statement> { <statement> }
#   <statement>     ::= "xiib" <identifier> "keet" <expression>
#                   |   "tsiibil" "[" <expression> "]"
#   <expression>    ::= <term> { ("+" | "-") <term> }
#   <term>          ::= <factor> { ("*" | "/") <factor> }
#   <factor>        ::= NUMBER | IDENT | "[" <expression> "]"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type=None):
        if self.pos >= len(self.tokens):
            if expected_type == 'RPAREN':
                raise SyntaxError('Se esperaba cerrar expresion con ]')
            elif expected_type == 'LPAREN':
                raise SyntaxError('Se esperaba abrir expresion con [')
            else:
                raise SyntaxError('Final inesperado del programa')
        token = self.tokens[self.pos]
        if expected_type and token[0] != expected_type:
            if expected_type == 'RPAREN':
                raise SyntaxError(f'Falta cerrar ] (se obtuvo {token[0]})')
            elif expected_type == 'LPAREN':
                raise SyntaxError(f'Falta abrir [ (se obtuvo {token[0]})')
            else:
                raise SyntaxError(f'Se esperaba {expected_type}, se obtuvo {token[0]}')
        self.pos += 1
        return token

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def parse(self):
        stmts = []
        while self.pos < len(self.tokens):
            stmts.append(self.statement())
        return stmts

    def statement(self):
        if self.peek() and self.peek()[0] == 'XIIB':
            # xiib <identifier> keet <expression>
            self.consume('XIIB')
            name = self.consume('IDENT')[1]
            self.consume('KEET')
            expr = self.expression()
            return ('assign', name, expr)
        elif self.peek() and self.peek()[0] == 'TSIIBIL':
            # tsiibil [ <expression> ]
            self.consume('TSIIBIL')
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return ('print', expr)
        else:
            raise SyntaxError(f'Declaracion invalida: {self.peek()}')

    def expression(self):
        left = self.term()
        while self.peek() and self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[0]
            right = self.term()
            left = (op.lower(), left, right)
        return left

    def term(self):
        left = self.factor()
        while self.peek() and self.peek()[0] in ('TIMES', 'DIVIDE'):
            op = self.consume()[0]
            right = self.factor()
            left = (op.lower(), left, right)
        return left

    def factor(self):
        token = self.peek()
        if not token:
            raise SyntaxError('Se esperaba un factor')
            
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
            raise SyntaxError(f'Factor invalido: {token}')

# --------------------------------------
# 3. Generacion de Codigo
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
# Funcion Principal del Compilador
# --------------------------------------

def compile_tan(code):
    print("=== COMPILADOR DEL LENGUAJE TAN ===\n")
    print("Codigo fuente:")
    print(code)
    
    try:
        # Analisis lexico
        tokens = tokenize(code)
        print("\nTokens generados:")
        for token in tokens:
            print(f"  {token}")
        
        # Analisis sintactico
        parser = Parser(tokens)
        ast = parser.parse()
        print("\nArbol Sintactico Abstracto (AST):")
        for node in ast:
            print(f"  {node}")
        
        # Generacion de codigo
        py_code = generate_python(ast)
        print("\nCodigo Python generado:")
        print(py_code)
        
        return py_code
        
    except Exception as e:
        print(f"\nError durante la compilacion: {e}")
        return None

