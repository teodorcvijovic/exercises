# Use covered topics to build yourself a simple python script which:
# ● Parses input numbers A and B and an operator +, -, *, /
# ● Puts together an expression A {operator} B and outputs it's result
# ● Handle bad input (strings, booleans, etc..) and display a proper error message
# ● Run the script in dedicated virtual environment

# function that returns a tuple in format (OPERAND, OPERATOR, OPERAND)
def parse(str):
    OPERATORS = '+-*/'
    a, b, op = None, None, None

    try:
        for OP in OPERATORS:
            expr = str.split(OP)
            if len(expr) == 2:
                a = float(expr[0])
                b = float(expr[1])
                op = OP
                break

    except Exception:
        print('Error: Input expression is not valid. Both operands should be numbers.')
        exit(1)

    if len(expr) != 2:
        print('Error: Input expression is not valid. Operator is not supported.')
        exit(2)

    return a, op, b


# expression evaluation, arguments should be passed in format (OPERAND, OPERATOR, OPERAND)
def eval_expr(a, op, b):
    match op:
        case '+':
            return a + b
        case '-':
            return a - b
        case '*':
            return a * b
        case '/':
            return a / b


def calculate():
    input_str = input('Input should be an expression in the following format: OPERAND OPERATOR OPERAND\nExpression: ').replace(' ', '')
    a, op, b = parse(input_str)
    result = eval_expr(a, op, b)
    print(f'{a} {op} {b} = {result}')


if __name__ == '__main__':
    while True:
        calculate()

