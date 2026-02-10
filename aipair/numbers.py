"""Utilities for working with integers: primality and perfect-number checks.

Functions
- isprime(number): Return True if number is prime.
- isperfect(number): Return True if number is a perfect number.
"""


def isprime(number: int) -> bool:
    """Return True if `number` is a prime integer.

    Args:
        number: Integer to test for primality.

    Returns:
        True if `number` is prime, False otherwise.

    Examples:
        >>> isprime(2)
        True
        >>> isprime(15)
        False
    """
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


def isperfect(number: int) -> bool:
    """Return True if `number` is a perfect number.

    A perfect number equals the sum of its proper positive divisors
    (excluding the number itself).

    Args:
        number: Integer to test; numbers less than 1 are not perfect.

    Returns:
        True if `number` is perfect, False otherwise.

    Examples:
        >>> isperfect(6)
        True
        >>> isperfect(28)
        True
        >>> isperfect(10)
        False
    """
    if number < 1:
        return False
    sum_of_divisors = sum(i for i in range(
        1, number // 2 + 1) if number % i == 0)
    return sum_of_divisors == number
