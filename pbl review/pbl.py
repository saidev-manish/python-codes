# Simple Python Program - Basic Calculator (Module 1)
# Now with multiplication, square and square root

import math   # for square root

FIRST = "Enter first number: "
SECOND = "Enter second number: "

while True:
    print("\n====== Simple Calculator ======")
    print("1. Convert Celsius to Fahrenheit")
    print("2. Swap Two Numbers")
    print("3. Addition of Two Numbers")
    print("4. Subtraction of Two Numbers")
    print("5. Division and Modulo Division")
    print("6. Multiplication of Two Numbers")   # NEW
    print("7. Square of a Number")              # NEW
    print("8. Square Root of a Number")         # NEW
    print("9. Exit")

    choice = int(input("Enter your choice (1-9): "))

    # 1. Temperature conversion
    if choice == 1:
        c = float(input("Enter temperature in Celsius: "))
        f = (c * 9/5) + 32
        print(c, "°C =", f, "°F")

    # 2. Swap numbers
    elif choice == 2:
        a = int(input(FIRST))
        b = int(input(SECOND))
        print("Before swapping: a =", a, ", b =", b)
        a, b = b, a   # swapping without 3rd variable
        print("After swapping: a =", a, ", b =", b)

    # 3. Addition
    elif choice == 3:
        a = float(input(FIRST))
        b = float(input(SECOND))
        print("Addition =", a + b)

    # 4. Subtraction
    elif choice == 4:
        a = float(input(FIRST))
        b = float(input(SECOND))
        print("Subtraction =", a - b)

    # 5. Division and Modulo
    elif choice == 5:
        a = int(input(FIRST))
        b = int(input(SECOND))
        if b != 0:
            print("Division =", a / b)
            print("Modulo Division =", a % b)
        else:
            print("Division by zero is not allowed!")

    # 6. Multiplication
    elif choice == 6:
        a = float(input(FIRST))
        b = float(input(SECOND))
        print("Multiplication =", a * b)

    # 7. Square
    elif choice == 7:
        a = float(input("Enter a number: "))
        print("Square =", a * a)

    # 8. Square Root
    elif choice == 8:
        a = float(input("Enter a number: "))
        if a >= 0:
            print("Square Root =", math.sqrt(a))
        else:
            print("Square root of negative number is not possible!")

    # 9. Exit
    elif choice == 9:
        print("Exiting... Thank you!")
        break

    else:
        print("Invalid choice! Try again.")
