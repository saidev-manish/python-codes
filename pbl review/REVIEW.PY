while True:
    print("\n====== Simple Utility Calculator ======")
    print("1. Convert Celsius to Fahrenheit")
    print("2. Swap Two Numbers")
    print("3. Addition of Two Numbers")
    print("4. Subtraction of Two Numbers")
    print("5. Division")
    print("6. Modulo Division")
    print("7. Exit")
    print("8. Calculate SGPA")
    print("9. Calculate CGPA")

    try:
        choice = int(input("Enter your choice (1-9): "))
    except ValueError:
        print("❌ Please enter a valid number (1-9).")
        continue

    # 1. Temperature conversion
    if choice == 1:
        c = float(input("Enter temperature in Celsius: "))
        f = (c * 9/5) + 32
        print(f"{c}°C = {f:.2f}°F")

    # 2. Swap numbers
    elif choice == 2:
        a = float(input("Enter first value: "))
        b = float(input("Enter second value: "))
        print(f"Before swapping: a = {a}, b = {b}")
        a, b = b, a
        print(f"After swapping: a = {a}, b = {b}")

    # 3. Addition
    elif choice == 3:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print(f"Addition = {a + b}")

    # 4. Subtraction
    elif choice == 4:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        print(f"Subtraction = {a - b}")

    # 5. Division
    elif choice == 5:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        if b != 0:
            print(f"Division = {a / b}")
        else:
            print("❌ Division by zero is not allowed!")

    # 6. Modulo Division
    elif choice == 6:
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        if b != 0:
            print(f"Modulo Division = {a % b}")
        else:
            print("❌ Division by zero is not allowed!")

    # 7. Exit
    elif choice == 7:
        print("👋 Thank you for using the calculator. Goodbye!")
        break

    # 8. SGPA Calculation
    elif choice == 8:
        grade_points = {
            "O": 10.0,
            "A+": 9.0,
            "A": 8.0,
            "B+": 7.0,
            "B": 6.0,
            "C": 5.0,
            "F": 0.0
        }

        n = int(input("Enter number of subjects in this semester: "))
        total_credits = 0
        total_points = 0

        for i in range(1, n + 1):
            credit = float(input(f"Enter credits for subject {i}: "))
            grade = input(f"Enter letter grade for subject {i} (O, A+, A, B+, B, C, F): ").upper()

            if grade in grade_points:
                grade_point = grade_points[grade]
            else:
                print("❌ Invalid grade entered! Defaulting to 0.")
                grade_point = 0.0

            total_credits += credit
            total_points += credit * grade_point

        sgpa = total_points / total_credits if total_credits != 0 else 0
        print(f"✅ Your SGPA for {n} subjects = {sgpa:.2f}")

    # 9. CGPA Calculation
    elif choice == 9:
        semesters = int(input("Enter number of semesters completed: "))
        total_sgpa = 0

        for i in range(1, semesters + 1):
            sgpa = float(input(f"Enter SGPA of semester {i}: "))
            total_sgpa += sgpa

        cgpa = total_sgpa / semesters if semesters != 0 else 0
        print(f"✅ Your CGPA after {semesters} semesters = {cgpa:.2f}")

    else:
        print("❌ Invalid choice! Try again.")