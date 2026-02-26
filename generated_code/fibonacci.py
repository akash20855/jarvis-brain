def fibonacci(n: int, raise_if_invalid=True) -> int:
    """Fibonacci sequence generator.

    Args:
        n (int): Position in the Fibonacci sequence to return.
        raise_if_invalid (bool, optional): Raise a ValueError if `n` is less than or equal to 0. Defaults to True.

    Returns:
        int: The requested Fibonacci number.

    Raises:
        ValueError: If `n` is less than or equal to 0 and raise_if_invalid is True.
    """
    if n <= 0 and raise_if_invalid:
        raise ValueError("Fibonacci position must be greater than 0.")

    if n == 1 or n == 2:
        return n - 1 if n == 1 else 1

    a, b = 1, 1
    for _ in range(2, n):
        a, b = b, a + b

    return b