import random

number = random.randint (1,10)

guess = int(input("Guess a number between 1 and 10: "))

if guess == 7:
    print("Correct!")
else:
    print("Wrong! The number was 7", number)