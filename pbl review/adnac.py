import math

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

def square():
    x = float(input("Enter a number: "))
    print(f"Square = {x ** 2}")

def squareroot():
    x = float(input("Enter a number: "))
    print(f"Square root = {math.sqrt(x)}")

def trigonometric():
    angle = float(input("Enter angle in radians: "))
    print(f"sin({angle}) = {math.sin(angle)}")
    print(f"cos({angle}) = {math.cos(angle)}")
    print(f"tan({angle}) = {math.tan(angle)}")

def exponential():
    x = float(input("Enter power for e^x: "))
    print(f"e^{x} = {math.exp(x)}")

def logarithmic():
    x = float(input("Enter a number: "))
    print(f"log({x}) = {math.log(x)}")

def power():
    x = float(input("Enter base: "))
    y = float(input("Enter exponent: "))
    print(f"{x}^{y} = {x ** y}")

def factorial():
    x = int(input("Enter a number: "))
    print(f"Factorial of {x} = {math.factorial(x)}")

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
    s = sum(int(d)**len(str(n)) for d in str(n))
    if s == n:
        print(f"{n} is an Armstrong number")
    else:
        print(f"{n} is not an Armstrong number")

def temperature():
    print("1. C → F")
    print("2. F → C")
    print("3. C → K")
    print("4. K → C")
    choice = int(input("Choose: "))
    t = float(input("Enter temperature: "))
    if choice == 1:
        print(f"{t}°C = {(t*9/5)+32}°F")
    elif choice == 2:
        print(f"{t}°F = {((t-32)*5/9)}°C")
    elif choice == 3:
        print(f"{t}°C = {t+273.15}K")
    elif choice == 4:
        print(f"{t}K = {t-273.15}°C")
    else:
        print("Invalid choice")

def main():
    print("|======= Simple Scientific Calculator =======|")
    while True:
        print("""
1. Addition
2. Subtraction
3. Multiplication
4. Division
5. Square
6. Square Root
7. Trigonometric (sin, cos, tan)
8. Exponential (e^x)
9. Logarithmic (ln)
10. Power (x^y)
11. Factorial
12. Prime Number Check
13. Armstrong Number Check
14. Temperature Conversion
0. Exit
""")
        choice = int(input("Enter your choice: "))

        if choice == 0:
            print("Exiting... Goodbye!")
            break
        elif choice == 1:
            addition()
        elif choice == 2:
            subtraction()
        elif choice == 3:
            multiplication()
        elif choice == 4:
            division()
        elif choice == 5:
            square()
        elif choice == 6:
            squareroot()
        elif choice == 7:
            trigonometric()
        elif choice == 8:
            exponential()
        elif choice == 9:
            logarithmic()
        elif choice == 10:
            power()
        elif choice == 11:
            factorial()
        elif choice == 12:
            prime()
        elif choice == 13:
            armstrong()
        elif choice == 14:
            temperature()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
