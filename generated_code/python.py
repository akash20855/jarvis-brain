def fibonacci(n):
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

def main():
    try:
        num = int(input("Enter the number of Fibonacci numbers to calculate (>= 0): "))
        if num < 0:
            raise ValueError("Number must be greater than or equal to 0.")
        fib_numbers = fibonacci(num)
        print(f"Fibonacci numbers for the first {num} terms are:")
        print(fib_numbers)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()