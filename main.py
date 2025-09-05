from calculator.src import calculate

if __name__ == "__main__":
    num = float(input("Enter a number: "))
    operation = input("Enter an operation (+, -, *, /): ")
    other_num = float(input("Enter another number: "))
    result = calculate(operation, num, other_num)
    print(result)