const calculator = {
  // Operators supported by the calculator
  operators: {
    '+': (a, b) => a + b,
    '-': (a, b) => a - b,
    '*': (a, b) => a * b,
    '/': (a, b) => (a / b).toFixed(8), // Use toFixed() for floating point operations to ensure precision
  },

  display: document.querySelector('.display'),

  clearDisplay() {
    this.display.textContent = '0';
  },

  appendToDisplay(number) {
    if (this.display.textContent === '0') {
      this.display.textContent = number;
    } else {
      this.display.textContent += number;
    }
  },

  calculateResult() {
    try {
      const input = this.display.textContent;
      const currentNumber = parseFloat(input);
      if (isNaN(currentNumber)) throw new Error('Invalid input');

      // Store the previous result to enable chaining operations
      this.previousResult = currentNumber;

      // Split the input into an array of operands and operators
      const regex = /([0-9]+|[\+\-\*\/\.])+/g;
      const match = input.match(regex);

      let result = parseFloat(match[0]);

      for (let i = 1; i < match.length; i++) {
        const operator = match[i];
        result = this.operators[operator](result, parseFloat(match[i + 1]));
        i++;
      }

      // Set the display to the calculated result
      this.display.textContent = result;
    } catch (error) {
      alert(`Error: ${error.message}`);
      this.clearDisplay();
    }
  },
};

// Event listeners for number buttons and operators
document.querySelectorAll('button').forEach((button) => {
  button.addEventListener('click', () => {
    const value = button.textContent;
    if (value >= 0 && value <= 9) {
      calculator.appendToDisplay(value);
    } else if (['+', '-', '*', '/'].includes(value)) {
      calculator.calculateResult();
      calculator.appendToDisplay(value);
    } else if (value === 'C') {
      calculator.clearDisplay();
    } else if (value === '=') {
      calculator.calculateResult();
    }
  });
});