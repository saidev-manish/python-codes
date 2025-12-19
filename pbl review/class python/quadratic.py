import math as np
import sys

try:
    a=float(input("Enter first integer: "))
    b=float(input("Enter second integer: "))
    c=float(input("Enter a float number: "))
except ValueError:
    print("Invalid input: please enter numeric values.")
    sys.exit(1)