import random

number = random.randint(1, 10)

guess = int(input("Guess a number from 1 to 10: "))

if guess == number:
    print("Correct")
else:
    print(f"Wrong! The number was {number}")