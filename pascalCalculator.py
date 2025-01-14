INTEGER,PLUS,EOF,EMPTY,MINUS, MULTI, DIV = 'INTEGER','PLUS','EOF','EMPTY','MINUS','MULTI','DIV'

class Token(object):

    def __init__(self,type,value):

        # The token type: INTEGER, PLUS or EOF
        self.type = type

        # The token value: 0,..,9,+ or None
        self.value = value

    def __str__(self):

        return 'Token{{type},{value}}'.format(
            type = self.type,
            value = repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self,text):
        
        # Client starting input
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]
    
    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        #get the curent_char variable
        self.pos += 1
        if self.pos> len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        # return a multidigit integer
        result=''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            elif self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            elif self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            elif self.current_char == '*':
                self.advance()
                return Token(MULTI, '*')
            elif self.current_char == '/':
                self.advance()
                return Token (DIV, '/')

            self.error()

        return Token(EOF, None)


    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    

    def expr(self):
        
        
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)
        while(self.current_char is not None):

            # we expect the current token to be either a '+' or '-'
            op = self.current_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            elif op.type == MULTI:
                self.eat(MULTI)
            elif op.type == DIV:
                self.eat(DIV)

            # we expect the current token to be an integer
            right = self.current_token
            self.eat(INTEGER)

            if op.type == PLUS:
                result = left.value + right.value
            elif op.type == MINUS:
                result = left.value - right.value
            elif op.type == MULTI:
                result = left.value*right.value
            elif op.type == DIV:
                result = left.value/right.value

            left.value = result
   
        return result

        
def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
