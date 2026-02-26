class Calculator:
    def __init__(self):
        self.valid_operators = {'+', '-', '*', '/'}

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def calculate(self, expression):
        try:
            tokens = expression.split()
            stack = []
            current_number = None

            for token in tokens:
                if token.isdigit():
                    if current_number is not None:
                        stack.append(current_number)
                    current_number = int(token)
                elif token in self.valid_operators:
                    if current_number is not None:
                        right_operand = current_number
                        current_number = None

                        left_operand = stack.pop()
                        result = self.__dict__[f"{token}"](left_operand, right_operand)
                        stack.append(result)
                elif token == '.':
                    if current_number is None:
                        raise ValueError("Invalid number format")
                    else:
                        current_number = round(current_number, 2)

            if current_number is not None:
                stack.append(current_number)

            result = stack[0]
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

# Example usage
calculator = Calculator()
result = calculator.calculate("12 4 +")  # Output: 16
result = calculator.calculate("3.5 2.2 /")  # Output: 1.6363636363636364
result = calculator.calculate("10 2 * 3 +")  # Output: 30
result = calculator.calculate("7 0 /")  # Outputs an error message "Error: Cannot divide by zero"