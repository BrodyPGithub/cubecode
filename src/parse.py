from ply import lex, yacc

tokens = (
   'GDTOKEN',
   'DECIMAL',
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'INEQUALITY',
   'EQUALITY',
   'EQUALS',
   'TUPLE',
   'LBRACKET',
   'RBRACKET',
   'LCBRACKET',
   'RCBRACKET',
   'COMMENT',
   'STRING',
   'VARLINK',
   'NAME',
)

# Define the GDTOKEN first to prioritize its matching
t_GDTOKEN = r'(\d+[gcib]|\?[gcib])'

# Define other tokens afterwards
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_INEQUALITY = r'\!\='
t_EQUALITY = r'\=\='
t_EQUALS = r'\='
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_LCBRACKET  = r'\{'
t_RCBRACKET  = r'\}'
t_COMMENT = r'\/\/.*'
t_NAME = r'[a-zA-Z][a-zA-Z0-9]*'
t_DECIMAL = r'[.]'

# A regular expression rule with some action code

def t_TUPLE(t):
    r'[\(](.*[,]*)*[\)]'
    # Extracting the inner part of the tuple
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARLINK(t):
    r'\.[a-z]+'
    t.value = t.value[1:]
    return t

def t_STRING(t):
    r'\'(.*?)\'|"(.*?)"'
    t.value = t.value[1:-1]  # Remove the quotes from the value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Example data to tokenize
data = '''
print("fanum rizz" + 10g + 10c.value)
3+1
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

# Parsing rules
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)