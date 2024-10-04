from re import compile

from utils.logger import setup_logger

TOKEN_TYPES = [
    ('ARROW', r'->'),
    ('KEYWORD', r'\b(func|return|const|var|int|float|string|void)\b'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('OPERATOR', r'[+\-*/=]'),
    ('SYMBOL', r'[(){}:;,>]'),
    ('STRING', r'"[^"]*"'),
    ('WHITESPACE', r'\s+')
]


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

        self.__logger = setup_logger(__class__.__name__)

    def tokenize(self):
        tokens = []

        while self.position < len(self.code):
            match = None
            for token_type, regex in TOKEN_TYPES:
                pattern = compile(regex)
                match = pattern.match(self.code, self.position)
                if match:
                    value = match.group(0)

                    self.__logger.debug(f'Position: {self.position}, Code: {
                                        self.code[self.position]}, CODEX: {self.code}, MATCH: {value}')

                    if token_type != 'WHITESPACE':
                        tokens.append((token_type, value))
                    self.position = match.end()
                    break
            if not match:
                raise Exception(f'Invalid syntax at position {
                                self.position}: "{self.code[self.position]}"')

        return tokens


code = 'func add(a: int, b: int) -> int { return a + b; }'

lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
