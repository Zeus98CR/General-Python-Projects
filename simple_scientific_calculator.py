import math

def show_menu():
    print("\n===== Scientific Calculator =====")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power (x^y)")
    print("6. Square Root")
    print("7. Sine")
    print("8. Cosine")
    print("9. Tangent")
    print("10. Logarithm (log10)")
    print("11. Natural Log (ln)")
    print("12. Factorial")
    print("0. Exit")
    print("================================")

def calculator():
    while True:
        show_menu()
        choice = input("Enter your choice (0-12): ")

        if choice == "0":
            print("Thank you for using the calculator. Goodbye!")
            break

        elif choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print("Result:", num1 + num2)

        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print("Result:", num1 - num2)

        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print("Result:", num1 * num2)

        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            if num2 == 0:
                print("Error: Cannot divide by zero!")
            else:
                print("Result:", num1 / num2)

        elif choice == "5":
            base = float(input("Enter base: "))
            exponent = float(input("Enter exponent: "))
            print("Result:", base ** exponent)

        elif choice == "6":
            num = float(input("Enter number: "))
            if num < 0:
                print("Error: Cannot calculate square root of negative number!")
            else:
                print("Result:", math.sqrt(num))

        elif choice == "7":
            angle = float(input("Enter angle in degrees: "))
            print("Result:", math.sin(math.radians(angle)))

        elif choice == "8":
            angle = float(input("Enter angle in degrees: "))
            print("Result:", math.cos(math.radians(angle)))

        elif choice == "9":
            angle = float(input("Enter angle in degrees: "))
            print("Result:", math.tan(math.radians(angle)))

        elif choice == "10":
            num = float(input("Enter number: "))
            if num <= 0:
                print("Error: Logarithm only works with positive numbers!")
            else:
                print("Result:", math.log10(num))

        elif choice == "11":
            num = float(input("Enter number: "))
            if num <= 0:
                print("Error: Natural log only works with positive numbers!")
            else:
                print("Result:", math.log(num))

        elif choice == "12":
            num = int(input("Enter a non-negative integer: "))
            if num < 0:
                print("Error: Factorial only works with non-negative integers!")
            else:
                print("Result:", math.factorial(num))

        else:
            print("Invalid choice! Please try again.")

# Start the program
calculator()