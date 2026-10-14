import math

MAX_FACTORIAL_INPUT = 1000

def show_menu():
    print("\n=== Scientific Calculator ===")
    print("1.  Addition (+)")
    print("2.  Subtraction (-)")
    print("3.  Multiplication (*)")
    print("4.  Division (/)")
    print("5.  Power (x^y)")
    print("6.  Square Root (sqrt)")
    print("7.  Sine (sin)")
    print("8.  Cosine (cos)")
    print("9.  Tangent (tan)")
    print("10. Logarithm (log10)")
    print("11. Natural Log (ln)")
    print("12. Factorial (!)")
    print("0.  Exit")
    print("============================")

def get_number(prompt="Enter a number: "):
    while True:
        try:
            number = float(input(prompt))
            if not math.isfinite(number):
                print("Invalid input. Please enter a finite number.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a number.")

def scientific_calculator():
    while True:
        show_menu()
        choice = input("Choose an option (0-12): ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":  # Addition
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result: {a} + {b} = {a + b}")

        elif choice == "2":  # Subtraction
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result: {a} - {b} = {a - b}")

        elif choice == "3":  # Multiplication
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            print(f"Result: {a} * {b} = {a * b}")

        elif choice == "4":  # Division
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            if b == 0:
                print("Error: Cannot divide by zero!")
            else:
                print(f"Result: {a} / {b} = {a / b}")

        elif choice == "5":  # Power
            a = get_number("Enter base: ")
            b = get_number("Enter exponent: ")
            try:
                print(f"Result: {a}^{b} = {a ** b}")
            except (OverflowError, ValueError):
                print("Error: That power calculation is outside the supported range.")

        elif choice == "6":  # Square Root
            a = get_number("Enter number: ")
            if a < 0:
                print("Error: Cannot take square root of a negative number!")
            else:
                print(f"Result: sqrt({a}) = {math.sqrt(a)}")

        elif choice == "7":  # Sine
            a = get_number("Enter angle in degrees: ")
            radians = math.radians(a)
            print(f"Result: sin({a}) = {math.sin(radians)}")

        elif choice == "8":  # Cosine
            a = get_number("Enter angle in degrees: ")
            radians = math.radians(a)
            print(f"Result: cos({a}) = {math.cos(radians)}")

        elif choice == "9":  # Tangent
            a = get_number("Enter angle in degrees: ")
            radians = math.radians(a)
            if math.isclose(math.cos(radians), 0.0, abs_tol=1e-12):
                print("Error: Tangent is undefined at this angle.")
            else:
                print(f"Result: tan({a}) = {math.tan(radians)}")

        elif choice == "10":  # Log base 10
            a = get_number("Enter number: ")
            if a <= 0:
                print("Error: Logarithm is only defined for positive numbers!")
            else:
                print(f"Result: log10({a}) = {math.log10(a)}")

        elif choice == "11":  # Natural log
            a = get_number("Enter number: ")
            if a <= 0:
                print("Error: Natural log is only defined for positive numbers!")
            else:
                print(f"Result: ln({a}) = {math.log(a)}")

        elif choice == "12":  # Factorial
            a = get_number("Enter a non-negative integer: ")
            if a < 0 or a != int(a):
                print("Error: Factorial is only defined for non-negative integers!")
            elif a > MAX_FACTORIAL_INPUT:
                print(f"Error: Please enter a value no larger than {MAX_FACTORIAL_INPUT}.")
            else:
                print(f"Result: {int(a)}! = {math.factorial(int(a))}")

        else:
            print("Invalid choice. Please select a number from 0 to 12.")

if __name__ == "__main__":
    scientific_calculator()