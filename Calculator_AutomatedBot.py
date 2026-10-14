import re

def ai_calculator(question):
    question = question.lower()

    # Percentage
    match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)", question)
    if match:
        percentage = float(match.group(1))
        number = float(match.group(2))
        return percentage / 100 * number

    # Addition
    match = re.search(r"add\s+(\d+(?:\.\d+)?)\s+(?:and|to)\s+(\d+(?:\.\d+)?)", question)
    if match:
        return float(match.group(1)) + float(match.group(2))

    return "I don't understand that calculation yet."

while True:
    question = input("AI Calculator: ")
    if question.lower() == "exit":
        break
    result = ai_calculator(question)
    print("Answer: ", result)