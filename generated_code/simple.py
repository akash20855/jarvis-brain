import sys

def main():
    try:
        print("Hello, World!")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()