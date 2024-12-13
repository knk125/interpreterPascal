INTEGER,PLUS,EOF = 'INTEGER','PLUS','EOF','EMPTY'

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
    
    def error(self):
        raise Exception('Error parsing input')
    
    def get_next_token(self):

        text = self.text

        # If we are at the end of the text return end-of-file token
        if self.pos > len(text) - 1:
            return Token(EOF,None)
        
        # Get the character at a position and assign a value
        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos +=1
            return token
        
        
        

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    

    def expr(self):
        self.current_token = self.get_next_token()
        
        left = []
        right = []
        
        while self.current_token.type == INTEGER :
            
            left.append(self.current_token.value)
            self.eat(INTEGER)
 

        op = self.current_token
        self.eat(PLUS)
        
        while self.current_token.type == INTEGER:
            right.append(self.current_token.value)
            self.eat(INTEGER)

    
        left_int = 0  
        right_int = 0
        
        for i in range(len(left)-1,0-1, -1):
            left_int += left[i]*pow(10,len(left)-1-i)

        for i in range(len(right)-1,0-1,-1):
            right_int += right[i]*pow(10,len(right)-1-i)

        result = left_int + right_int

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
