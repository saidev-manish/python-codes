# Simple Python Program - simple Calculator (Module 1)

while True:
    print("\n====== Simple Utility Calculator ======")
    print("1. Convert Celsius to Fahrenheit")
    print("2. Swap Two Numbers")
    print("3. Addition of Two Numbers")
    print("4. Subtraction of Two Numbers")
    print("5. Division ")
    print("6. Modulo Division")
    print("7. Exit")

    choice = int(input("Enter your choice (1-7): "))

    # 1. Temperature conversion
    if choice == 1:
        c = float(input("Enter temperature in Celsius: "))
        f = (c * 9/5) + 32
        print("answer is =", f, "°F")

    # 2. Swap numbers
    elif choice == 2:
        a = int(input("Enter first value : "))
        b = int(input("Enter second value : "))
        print("Before swapping: a =", a, ", b =", b)
        a, b = b, a   # swapping without 3rd variable
        print("After swapping: a =", a, ", b =", b)

    # 3. Addition
    elif choice == 3:
        a = float(input("Enter a number: "))
        b = float(input("Enter b number: "))
        print("Addition =", a + b)

    # 4. Subtraction
    elif choice == 4:
        a = float(input("Enter a number: "))
        b = float(input("Enter b number: "))
        print("Subtraction =", a - b)

    # 5. Division and Modulo
    elif choice == 5:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        if b != 0:
            print("Division =", a / b)
           
        else:
            print("Division by zero is not allowed!")

    # 6. Modulo Division
    elif choice == 6:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        if b != 0:
            print("Modulo Division =", a % b)
        else:
            print("Division by zero is not allowed!")

    # 7. Exit
    elif choice == 7:
        print("Exit")
        break

    else:
        print("Invalid choice! Try again.")
