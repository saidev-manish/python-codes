# Simple Python Program - simple Calculator (Module 1)

def save_result(result):
    with open("results.txt", "a") as file:# open file in append mode
        file.write(result + "\n")  # write result and move to next line

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
        result = f"Answer is = {f} °F"
        print(result)
        save_result(result)

    # 2. Swap numbers
    elif choice == 2:
        a = int(input("Enter first value : "))
        b = int(input("Enter second value : "))
        result = f"Before swapping: a = {a}, b = {b} | After swapping: a = {b}, b = {a}"
        print(result)
        save_result(result)

    # 3. Addition
    elif choice == 3:
        a = float(input("Enter a number: "))
        b = float(input("Enter b number: "))
        result = f"Addition = {a + b}"
        print(result)
        save_result(result)

    # 4. Subtraction
    elif choice == 4:
        a = float(input("Enter a number: "))
        b = float(input("Enter b number: "))
        result = f"Subtraction = {a - b}"
        print(result)
        save_result(result)

    # 5. Division
    elif choice == 5:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        if b != 0:
            result = f"Division = {a / b}"
            print(result)
            save_result(result)
        else:
            result = "Division by zero is not allowed!"
            print(result)
            save_result(result)

    # 6. Modulo Division
    elif choice == 6:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        if b != 0:
            result = f"Modulo Division = {a % b}"
            print(result)
            save_result(result)
        else:
            result = "Division by zero is not allowed!"
            print(result)
            save_result(result)

    # 7. Exit
    elif choice == 7:
        print("Exit")
        break

    else:
        print("Invalid choice! Try again.")
