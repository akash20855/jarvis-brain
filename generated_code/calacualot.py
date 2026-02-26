def calculate(operation, num1, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                raise ValueError("Cannot divide by zero")
        else:
            raise ValueError(f"Invalid operation. Supported operations are '+', '-', '*', '/'.")

        return result
    except ValueError as e:
        print(e)
        return None

def main():
    while True:
        num1 = input("Enter first number: ")
        num2 = input("Enter second number: ")
        operation = input("Enter operation (+, -, *, /): ")

        result = calculate(operation, num1, num2)
        if result is not None:
            print(f"Result: {result}")
            break

if __name__ == "__main__":
    main()