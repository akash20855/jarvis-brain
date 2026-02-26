"""
Simple Calculator Module for JARVIS
Provides basic arithmetic operations with history tracking.
"""


class Calculator:
    """A simple calculator class for performing basic arithmetic operations."""
    
    def __init__(self):
        """Initialize the calculator with empty history."""
        self.history = []
        self.last_result = None
    
    def add(self, num1, num2):
        """
        Add two numbers.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: The sum
        """
        try:
            result = num1 + num2
            entry = f"Added {num1} and {num2} = {result}"
            self.history.append(entry)
            self.last_result = result
            return result
        except (TypeError, ValueError) as e:
            return f"Error in addition: Invalid input"
    
    def subtract(self, num1, num2):
        """
        Subtract two numbers.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: The difference
        """
        result = num1 - num2
        entry = f"Subtracted {num2} from {num1} = {result}"
        self.history.append(entry)
        self.last_result = result
        return result
    
    def multiply(self, num1, num2):
        """
        Multiply two numbers.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: The product
        """
        result = num1 * num2
        entry = f"Multiplied {num1} and {num2} = {result}"
        self.history.append(entry)
        self.last_result = result
        return result
    
    def divide(self, num1, num2):
        """
        Divide two numbers.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: The quotient
            
        Raises:
            ZeroDivisionError: If attempting to divide by zero
        """
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = num1 / num2
        entry = f"Divided {num1} by {num2} = {result}"
        self.history.append(entry)
        self.last_result = result
        return result
    
    def power(self, base, exponent):
        """
        Raise a number to a power.
        
        Args:
            base (float): Base number
            exponent (float): Exponent
            
        Returns:
            float: The result
        """
        result = base ** exponent
        entry = f"{base} to the power of {exponent} = {result}"
        self.history.append(entry)
        self.last_result = result
        return result
    
    def square_root(self, num):
        """
        Calculate square root.
        
        Args:
            num (float): Number
            
        Returns:
            float: The square root
            
        Raises:
            ValueError: If number is negative
        """
        if num < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = num ** 0.5
        entry = f"Square root of {num} = {result}"
        self.history.append(entry)
        self.last_result = result
        return result
    
    def calculate(self, operation, num1, num2=None):
        """
        Perform a calculation based on operation string.
        
        Args:
            operation (str): Operation ('add', 'subtract', 'multiply', 'divide')
            num1 (float): First number
            num2 (float): Second number (optional for some operations)
            
        Returns:
            float or str: The result or error message
        """
        try:
            op = operation.lower().strip()
            
            if op in ["add", "plus", "+"]:
                return self.add(num1, num2)
            elif op in ["subtract", "minus", "-"]:
                return self.subtract(num1, num2)
            elif op in ["multiply", "times", "*", "x"]:
                return self.multiply(num1, num2)
            elif op in ["divide", "divided", "/"]:
                return self.divide(num1, num2)
            elif op in ["power", "^", "**", "pow"]:
                return self.power(num1, num2)
            elif op in ["sqrt", "square root"]:
                return self.square_root(num1)
            else:
                return f"Unknown operation: {operation}. Try: add, subtract, multiply, divide, power, sqrt"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_history(self):
        """
        Get calculation history.
        
        Returns:
            list: List of all calculations
        """
        return self.history.copy()
    
    def get_last_result(self):
        """
        Get the last calculation result.
        
        Returns:
            float or None: Last result or None if no calculations performed
        """
        return self.last_result
    
    def clear_history(self):
        """Clear calculation history."""
        self.history = []
        self.last_result = None
    
    def format_history(self):
        """
        Format history as a readable string.
        
        Returns:
            str: Formatted history
        """
        if not self.history:
            return "No calculations yet."
        return "\n".join(self.history)


def demo():
    """Demonstrate calculator functionality."""
    calc = Calculator()
    
    print("=== JARVIS Calculator Demo ===\n")
    
    # Perform some calculations
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 2 = {calc.subtract(10, 2)}")
    print(f"4 * 6 = {calc.multiply(4, 6)}")
    print(f"12 / 3 = {calc.divide(12, 3)}")
    print(f"2^8 = {calc.power(2, 8)}")
    print(f"√16 = {calc.square_root(16)}")
    
    print("\n=== Calculation History ===")
    print(calc.format_history())
    
    print(f"\nLast Result: {calc.get_last_result()}")


if __name__ == "__main__":
    demo()
