import time
import csv
import sys

def deliver_joke(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline)
    
def read_input():
    user_input = input("Input: ")
    while user_input not in ("next", "quit"):
        print("I don't understand")
        user_input = input("Input: ")
    return user_input == "next"

def read_jokes(csv_filename):
    with open(csv_filename) as csv_file:
        return list(csv.reader(csv_file))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No joke file given")
    elif len(sys.argv) > 2:
        print("Too many command-line arguments")
    else:
        try:
            jokes = read_jokes(sys.argv[1])
            for prompt, punchline in jokes:
                if read_input():
                    deliver_joke(prompt, punchline)
                else:
                    break
        except FileNotFoundError:
            print("Joke file not found")
