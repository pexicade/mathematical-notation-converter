"""This is a utitlity script containg functions that convert between different Notations"""

from __future__ import annotations
import re

from stack import Stack

OPERATORS = ['+', '-', '*', '/', '^']
PRECEDENECE = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
FUNCTIONS = ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']

def extract_infix(text: str) -> list:
    tokens = []
    #use regex to replace all whitespaces with ''
    text = re.sub('\s+', '', text)
    n = len(text)
    i = 0
    operators = OPERATORS+['(',')']
    on = False
    p = 0 #number of opening parentheses
    while(i<n):
        for functions in FUNCTIONS:
            if text[i:i+len(functions)] == functions:
                tokens.append(functions)
                tokens.append('[') #function call start
                i += len(functions)+1
                on = True
                break
        t = text[i]
        if t in operators:
            aded = False
            if on:
                if t == ')':
                    p -= 1
                    if p == -1:
                        on = False
                        p = 0
                        tokens.append(']') #function call end
                        aded = True
                elif t == '(':
                    p += 1
            if not aded:
                tokens.append(t)

        elif t.isalnum(): #if it is a number or an alphabet then we need to extract the whole thing
            j = i+1
            while j<n and text[j].isalnum():
                j += 1
            tokens.append(text[i:j]) 
            i = j-1
        i += 1
    return tokens

def extract_pre_post(text: str) -> list:
    tokens = []
    #Just replace all whitespaces with a single space(' ') so that we can then split the string by space
    text = re.sub('\s+', ' ', text)
    text = text.split(' ')
    for t in text:
        if len(t)>1:
            tokens.extend(extract_infix(t))
        else:
            tokens.append(t)
    return tokens

def extract_tokens(text: str,notation: str) -> list:
    """we need to extract all tokens from given text
    example:
    input: 'A   -2*(B +3C)' , output: ['A', '-2', '*', '(', 'B', '+', '3C', ')'] #infix notation
    input: '36+ (C- dx)^1', output: ['36', '+', '(', 'C', '-', 'dx', ')', '^', '1'] #infix notation
    input: '/ + A B - Cx D', output: ['/', '+', 'A', 'B', '-', 'Cx', 'D'] #prefix notation
    input: 'A B + Cx d - / 48 *', output: ['A', 'B', '+', 'Cx', 'd', '-', '/', '48', '*'] #postfix notation
    input: 'A B + CD e - *' output: ['A', 'B', '+', 'CD', 'e', '-', '*'] #postfix notation
    """
    if notation.lower() == 'infix':
        return extract_infix(text)
    else:
        return extract_pre_post(text)

def infix_to_postfix(infix: list) -> str:
    """convert infix to postfix notation"""
    if infix[0]=='-':
        infix = ['-'] + check_validation(infix[1:], 'infix')
    else:
        infix = check_validation(infix, 'infix')
    postfix = []
    steps = [] #elemnts are tuple that contain stack and postfix at each step
    stack = Stack()
    last_token = unary = ''
    op = ('(','*','/','^')
    for token in infix:
        if token in FUNCTIONS:
            if unary:
                token += unary
                unary = ''
            stack.push(token)
        elif type(token) == list:
            res = infix_to_postfix(token)
            postfix.extend(res.split(' '))
            postfix.append(stack.pop())
        elif token in OPERATORS:
            if token == '-' and (not last_token or last_token in op):
                unary = '?'
                last_token = token
                continue
            top_element = stack.peek()
            while top_element and top_element != '(' and PRECEDENECE[token] <= PRECEDENECE[top_element]:
                postfix.append(top_element)
                stack.pop()
                top_element = stack.peek()
            stack.push(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while stack.peek() != '(':
                postfix.append(stack.pop())
            stack.pop()
        else:
            if unary:
                token = token + unary
                unary = ''
            postfix.append(token)
        last_token = token
        steps.append((' '.join(stack), ' '.join(postfix)))
    while stack.peek():
        postfix.append(stack.pop())
        steps.append((' '.join(stack), ' '.join(postfix)))
    print('\n'.join([f'{x[0]} || {x[1]}' for x in steps]))
    return ' '.join(postfix)

def postfix_to_infix(postfix: list) -> str:
    """convert postfix to infix notation"""
    check_validation(postfix, 'postfix')
    stack = Stack()
    for token in postfix:
        if token in OPERATORS:
            a = stack.pop()
            b = stack.pop()
            stack.push('(' + b + token + a + ')')
        else:
            stack.push(token)
    return stack.pop()

def prefix_to_infix(prefix: list) -> str:
    """convert prefix to infix notation"""
    check_validation(prefix, 'prefix')
    stack = Stack()
    prefix = prefix[::-1]
    for token in prefix:
        if token in OPERATORS:
            a = stack.pop()
            b = stack.pop()
            stack.push('(' + a + token + b + ')')
        else:
            stack.push(token)
    return stack.pop()

def infix_to_prefix(infix: list) -> str:
    """convert infix to prefix notation"""
    check_validation(infix, 'infix')
    stack = Stack()
    infix = infix[::-1]#() 
    prefix = []
    for token in infix:
        if token in OPERATORS:
            top_element = stack.peek()
            while top_element and top_element != ')' and PRECEDENECE[token] <= PRECEDENECE[top_element]:
                prefix.append(top_element)
                stack.pop()
                top_element = stack.peek()
            stack.push(token)
        elif token == '(':
            while stack.peek() != ')':
                prefix.append(stack.pop())
            stack.pop()
        elif token == ')':
            stack.push(token)
        else:
            prefix.append(token)
            
    while stack.peek():
        prefix.append(stack.pop())
    return ' '.join(prefix[::-1])

def prefix_to_postfix(prefix: list) -> str:
    """convert prefix to postfix notation"""
    check_validation(prefix, 'prefix')
    stack = Stack()
    prefix = prefix[::-1]
    for token in prefix:
        if token in OPERATORS:
            a = stack.pop()
            b = stack.pop()
            stack.push(a + ' ' + b + ' ' + token)
        else:
            stack.push(token)
    return stack.pop()

def postfix_to_prefix(postfix: list) -> str:
    """convert postfix to prefix notation"""
    check_validation(postfix, 'postfix')
    stack = Stack()
    for token in postfix:
        if token in OPERATORS:
            a = stack.pop()
            b = stack.pop()
            stack.push(token + ' ' + b + ' ' + a)
        else:
            stack.push(token)
    return stack.pop()

def check_validation(expression: list[str]|tuple, src: str):
    check_type_validation(expression,src)
    chack_chars_validation(expression,src)
    check_start_end_validation(expression,src)
    x = 1
    p = 0
    exp = []
    on = False
    last_token = ''
    op = ('(', '[','*','/','^')
    for token in expression:
        if token in OPERATORS:
            if src=='infix':
                if last_token and last_token not in op:
                    x += 1
            else:
                x += 1
        elif token.isalnum():
            if not token in FUNCTIONS: 
                x -= 1
        elif token == '(':
            p += 1
        elif token == ')':
            p -= 1
        elif token == '[':
            on = True
            exp.append([])
        elif token == ']':
            on = False
            exp[-1] = exp[-1][1:]
            continue
        if on:
            exp[-1].append(token)
        else:
            exp.append(token)
        last_token = token
        
    if x> 0:
            raise ValueError(f"Invalid expression. Missing {x} operands")
    elif x < 0:
            raise ValueError(f"Invalid expression. Missing {abs(x)} operators")
    if p > 0:
            raise ValueError(f"Invalid expression. Missing {p} right parentheses")
    elif p < 0:
            raise ValueError(f"Invalid expression. Missing {abs(p)} left parentheses")
    return exp

def check_type_validation(expression: list|tuple, src: str) -> bool:
    if type(expression) not in (list,tuple):
        raise TypeError(f"{src.title()} expression must be of type list or tuple")

def chack_chars_validation(expression: list|tuple, src:str) -> bool:
    if src == 'infix':
        for c,token in enumerate(expression):
            if not is_char_allowed(token,['(',')','[',']']):
                raise ValueError(f"{src.title()} expression must only contain alphabet, digits, operators and parentheses\n{token} found in index {c}")
    else:
        for c,token in enumerate(expression):
            if not is_char_allowed(token):
                raise ValueError(f"{src.title()} expression must only contain alphabet, digits and operators\n{token} found in index {c}")

def is_char_allowed(txt: str, especial_case: list = None) ->bool:
    if txt.isalnum() or txt in OPERATORS:
        return True
    if especial_case and txt in especial_case:
        return True
    return False

def check_start_end_validation(expression: list|tuple, src: str) -> bool:
    if src == 'prefix':
        if expression[0] not in OPERATORS:
            raise ValueError('Prefix should start with an operator')
        if expression[-1] in OPERATORS:
            raise ValueError('Prefix should Not end with an operator')
    elif src=='postfix':
        if expression[0] in OPERATORS:
            raise ValueError('Postfix should Not start with an operator')
        if expression[-1] not in OPERATORS:
            raise ValueError('Postfix should end with an operator')
    else:
        if expression[0] in OPERATORS:
            raise ValueError('Infix should Not start with an operator')
        if expression[-1] in OPERATORS:
            raise ValueError('Infix should Not end with an operator')

converters = {'infix_to_postfix': infix_to_postfix,'postfix_to_infix': postfix_to_infix,'prefix_to_infix': prefix_to_infix,
            'infix_to_prefix': infix_to_prefix,'prefix_to_postfix': prefix_to_postfix,'postfix_to_prefix': postfix_to_prefix}
