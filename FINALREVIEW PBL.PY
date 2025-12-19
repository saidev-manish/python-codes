import math

# ==============================
# SIMPLE + SCIENTIFIC CALCULATOR
# ==============================

def addition():
    x = float(input("Enter first number: "))
    y = float(input("Enter second number: "))
    print(f"Sum = {x + y}")

def subtraction():
    x = float(input("Enter first number: "))
    y = float(input("Enter second number: "))
    print(f"Difference = {x - y}")

def multiplication():
    x = float(input("Enter first number: "))
    y = float(input("Enter second number: "))
    print(f"Product = {x * y}")

def division():
    x = float(input("Enter numerator: "))
    y = float(input("Enter denominator: "))
    if y != 0:
        print(f"Quotient = {x / y}")
        print(f"Remainder = {x % y}")
    else:
        print("Error: Division by zero")

def modulo():
    x = int(input("Enter first number: "))
    y = int(input("Enter second number: "))
    if y != 0:
        print(f"Modulo Division = {x % y}")
    else:
        print("Division by zero is not allowed!")

def swap():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    print(f"Before swapping: a = {a}, b = {b}")
    a, b = b, a
    print(f"After swapping: a = {a}, b = {b}")

def square():
    x = float(input("Enter a number: "))
    print(f"Square = {x ** 2}")

def squareroot():
    x = float(input("Enter a number: "))
    if x >= 0:
        print(f"Square root = {math.sqrt(x)}")
    else:
        print("Error: Cannot take square root of a negative number")

def logarithmic():
    x = float(input("Enter a number: "))
    if x > 0:
        print(f"log({x}) = {math.log(x)}")
    else:
        print("Error: Logarithm undefined for non-positive values")

def power():
    x = float(input("Enter base: "))
    y = float(input("Enter exponent: "))
    print(f"{x}^{y} = {x ** y}")

def factorial():
    x = int(input("Enter a number: "))
    if x >= 0:
        print(f"Factorial of {x} = {math.factorial(x)}")
    else:
        print("Error: Factorial undefined for negative numbers")

def prime():
    n = int(input("Enter a number: "))
    if n > 1:
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                print(f"{n} is not prime")
                return
        print(f"{n} is prime")
    else:
        print(f"{n} is not prime")

def armstrong():
    n = int(input("Enter a number: "))
    s = sum(int(d) ** len(str(n)) for d in str(n))
    if s == n:
        print(f"{n} is an Armstrong number")
    else:
        print(f"{n} is not an Armstrong number")

def temperature():
    print("""
Temperature Conversion Options:
1. Celsius → Fahrenheit
2. Fahrenheit → Celsius
3. Celsius → Kelvin
4. Kelvin → Celsius
""")
    choice = int(input("Choose: "))
    t = float(input("Enter temperature: "))

    if choice == 1:
        print(f"{t}°C = {(t * 9/5) + 32}°F")
    elif choice == 2:
        print(f"{t}°F = {(t - 32) * 5/9}°C")
    elif choice == 3:
        print(f"{t}°C = {t + 273.15}K")
    elif choice == 4:
        print(f"{t}K = {t - 273.15}°C")
    else:
        print("Invalid choice")

def sgpa_calculation():
    grade_points = {
        "O": 10.0, "10": 10.0,
        "A+": 9.0, "9": 9.0,
        "A": 8.0, "8": 8.0,
        "B+": 7.0, "7": 7.0,
        "B": 6.0, "6": 6.0,
        "C": 5.0, "5": 5.0,
        "F": 0.0, "0": 0.0
    }

    n = int(input("Enter number of subjects in this semester: "))
    total_credits = 0
    total_points = 0

    for i in range(1, n + 1):
        credit = float(input(f"Enter credits for subject-{i}: "))
        grade = input("Enter grade (O/A+/A/B+/B/C/F): ").upper()

        if grade in grade_points:
            grade_point = grade_points[grade]
        else:
            print("❌ Invalid grade entered! Defaulting to 0.")
            grade_point = 0.0

        total_credits += credit
        total_points += credit * grade_point

    sgpa = total_points / total_credits if total_credits != 0 else 0
    print(f"✅ Your SGPA = {sgpa:.2f}")

def cgpa_calculation():
    semesters = int(input("Enter number of semesters completed: "))
    total_sgpa = 0

    for i in range(1, semesters + 1):
        sgpa = float(input(f"Enter SGPA of semester {i}: "))
        total_sgpa += sgpa

    cgpa = total_sgpa / semesters if semesters != 0 else 0
    print(f"✅ Your CGPA = {cgpa:.2f}")


# ==============================
# MAIN PROGRAM
# ==============================

def main():
    print("|======= Ultimate Utility & Scientific Calculator =======|")
    while True:
        print("""
=============== MENU ===============
1.  Addition
2.  Subtraction
3.  Multiplication
4.  Division
5.  Modulo Division
6.  Swap Two Numbers
7.  Square
8.  Square Root
9.  Power (x^y)
10. Factorial
11. Logarithmic (ln)
12. Prime Number Check
13. Armstrong Number Check
14. Temperature Conversion
15. SGPA Calculation
16. CGPA Calculation
0.  Exit
====================================
""")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if choice == 0:
            print("Exiting... Goodbye!")
            break
        elif choice == 1: addition()
        elif choice == 2: subtraction()
        elif choice == 3: multiplication()
        elif choice == 4: division()
        elif choice == 5: modulo()
        elif choice == 6: swap()
        elif choice == 7: square()
        elif choice == 8: squareroot()
        elif choice == 9: power()
        elif choice == 10: factorial()
        elif choice == 11: logarithmic()
        elif choice == 12: prime()
        elif choice == 13: armstrong()
        elif choice == 14: temperature()
        elif choice == 15: sgpa_calculation()
        elif choice == 16: cgpa_calculation()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
