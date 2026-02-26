Here's a simple command-line calculator in Python with basic arithmetic operations (addition, subtraction, multiplication, division) and some error handling:

```python
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

def main():
    print("Select operation: \n1 - Add\n2 - Subtract\n3 - Multiply\n4 - Divide")

    while True:
        choice = input("Enter your choice (1/2/3/4): ")

        try:
            choice = int(choice)
            if 1 <= choice <= 4:
                break
            else:
                print("Invalid input. Please enter a valid number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number between 1 and 4.")

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == 1:
        result = add(num1, num2)
    elif choice == 2:
        result = subtract(num1, num2)
    elif choice == 3:
        result = multiply(num1, num2)
    elif choice == 4:
        try:
            result = divide(num1, num2)
        except ValueError as e:
            print(e)
            return

    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```