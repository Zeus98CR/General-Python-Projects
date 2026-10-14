num1 = float(input("20: "))
operator = input("+: ")
num2 = float(input("15: "))

if operator == "+":
    print(num1 + num2)

elif operator == "-":
    print(num1 - num2)

elif operator == "/":
    if num2 != 0:
        print(num1 / num2)
    else:
        print("You can't divide by zero!")

else:
    print("Invalid operator")