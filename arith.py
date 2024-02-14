import re
import sys
import json
from collections import namedtuple

Token = namedtuple('Token', 'kind lexeme pos')

################################# Parser code ################################

def parse(text):
    toks = tokenize(text)
    toksIndex = 0
    tok = toks[toksIndex]
    toksIndex += 1

    def program(asts):
        # Handling leading newlines
        if peek('\n'):
            while peek('\n'):
                consume('\n')
            return program(asts)
        # Handling end of file
        elif peek('EOF'):
            return asts
        else:
            # Parsing data literals
            d = data_literal()
            asts.append(d)
            return program(asts)

    def data_literal():
        if peek('['):
            return list_literal()
        elif peek('{'):
            return tuple_literal()
        elif peek('%'):
            return map_literal()
        else:
            return primitive_literal()

    # Function to parse list literals
    def list_literal():
        consume('[')
        if peek(']'):
            consume(']')
            return {"%k": "list", "%v": []}
        else:
            items = []
            items.append(data_literal())
            while peek(','):
                consume(',')
                items.append(data_literal())
            consume(']')
            return {"%k": "list", "%v": items}

    # Function to parse tuple literals
    def tuple_literal():
        consume('{')
        items = []
        if not peek('}'):
            items.append(data_literal())
            while peek(','):
                consume(',')
                items.append(data_literal())
        consume('}')
        return {"%k": "tuple", "%v": items}

    # Function to parse map literals
    def map_literal():
        consume('%')
        consume('{')
        pairs = []
        while not peek('}'):
            pairs.append(key_value())
            if not peek(','):
                break
            consume(',')
        consume('}')  # Consume the closing '}'
        return {"%k": "map", "%v": pairs}


    # Function to parse key-value pairs in map literals
    def key_value():
        if peek(':') or peek('ATOM'):
            k = key()
        else:
            k = data_literal()
        
        if peek('=>'):
            consume('=>')
            v = data_literal()
        else:
            v = data_literal()
            
        return [k, v]

    # Function to parse keys in map literals
    def key():
        if peek(':'):
            consume(':')
            key_value = tok.lexeme
            return {"%k": "atom", "%v": key_value}
        elif peek('ATOM'):
            key_value = convert_format(tok.lexeme)
            consume('ATOM')
            return {"%k": "atom", "%v": key_value}
    
    def convert_format(input_string):
        if input_string.endswith(':'):
            return f':{input_string[:-1]}'
        else:
            return input_string

    # Function to parse primitive literals
    def primitive_literal():
        if peek('INT'):
            v = int(tok.lexeme.replace("_", ""))
            consume('INT')
            return {"%k": "int", "%v": v}
        elif peek('ATOM'):
            v = tok.lexeme
            consume('ATOM')
            return {"%k": "atom", "%v": v}
        elif peek('BOOL'):
            v = True if tok.lexeme == 'true' else False
            consume('BOOL')
            return {"%k": "bool", "%v": v}
        else:
            error('primitive literal', text)

    # Function to check if the next token matches the expected kind
    def peek(kind):
        nonlocal tok
        return tok.kind == kind

    # Function to consume the next token if it matches the expected kind
    def consume(kind):
        nonlocal tok, toks, toksIndex
        if peek(kind):
            tok = toks[toksIndex]
            toksIndex += 1
        else:
            error(kind, text)

    # Function to handle parsing errors
    def error(kind, text):
        nonlocal tok
        pos = tok.pos
        if pos >= len(text) or text[pos] == '\n':
            pos -= 1
        lineBegin = text.rfind('\n', 0, pos)
        if lineBegin < 0:
            lineBegin = 0
        lineEnd = text.find('\n', pos)
        if lineEnd < 0:
            lineEnd = len(text)
        line = text[lineBegin:lineEnd]
        print(f"error: expecting '{kind}' but got '{tok.kind}'", file=sys.stderr)
        print(line, file=sys.stderr)
        nSpace = pos - lineBegin if pos >= lineBegin else 0
        print('^'.rjust(nSpace + 1), file=sys.stderr)
        sys.exit(1)

    # List to hold parsed ASTs
    asts = []
    # Starting parsing the program
    program(asts)
    if tok.kind != 'EOF':
        error('EOF', text)
    return asts

################################# Lexer Code #################################

# Regular expressions for tokenizing
SKIP_RE = re.compile(r'(( |\t|\n)|\#.*)+')
INT_RE = re.compile(r'-?\d+(?:_\d+)*')
ATOM_RE = re.compile(r':[a-zA-Z0-9_]\w*|\b[a-zA-Z0-9_]\w*:')
BOOL_RE = re.compile(r'\b(true|false)\b')
COMMENT_RE = re.compile(r'\#.+(?=\n|$)')

# Function to tokenize the input text
def tokenize(text, pos=0):
    toks = []
    while pos < len(text):
        m = SKIP_RE.match(text, pos)
        if m:
            pos += len(m.group())
            continue

        if pos >= len(text):
            break

        if m := INT_RE.match(text, pos):
            tok = Token('INT', m.group(), pos)
        elif m := ATOM_RE.match(text, pos):
            tok = Token('ATOM', m.group(), pos)
        elif m := BOOL_RE.match(text, pos):
            tok = Token('BOOL', m.group(), pos)
        elif text[pos] == '=' and text[pos+1] == '>':
            tok = Token('=>', '=>', pos)
            pos += 2
        elif m := COMMENT_RE.match(text, pos):
            pos += len(m.group())
            continue  # Skip comments
        else:
            tok = Token(text[pos], text[pos], pos)
            pos += 1

        if m:
            pos += len(m.group())

        toks.append(tok)

    toks.append(Token('EOF', '<EOF>', pos))
    return toks


################################## Driver Code #################################

# Main function to execute the parser
def main():
    
    text=sys.stdin.read()
    
    asts = parse(text)
    print(json.dumps(asts, separators=(',', ': '), indent=2))  # proper JSON format with indentation

if __name__ == "__main__":
    main()
