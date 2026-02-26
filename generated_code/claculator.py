def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def calculator():
    print("Calculator")
    print("Operations available are +, -, *, and /")

    while True:
        try:
            num1 = float(input("\nEnter first number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    operation = ""
    while operation not in ["+", "-", "*", "/"]:
        operation = input(f"Enter operation (+, -, *, /): ")

    while True:
        try:
            num2 = float(input("\nEnter second number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    if operation == "+":
        result = add(num1, num2)
    elif operation == "-":
        result = subtract(num1, num2)
    elif operation == "*":
        result = multiply(num1, num2)
    elif operation == "/":
        result = divide(num1, num2)

    print(f"\nResult: {result}")

if __name__ == "__main__":
    calculator()