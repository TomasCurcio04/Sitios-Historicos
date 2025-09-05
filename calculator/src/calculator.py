from calculator.src import operations


def calculate(operation, a, b):#realiza la operacion segun su operador
    if operation == "+":
        return operations.add(a,b)
    elif operation == "-":
        return operations.subtract(a,b)
    elif operation == "*":
        return operations.multiply(a,b)
    elif operation == "/":
        return operations.divide(a,b)
    else:
        return "Invalid operation"