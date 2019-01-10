import time
import csv
import sys
import requests

def deliver_joke(prompt, punchline):
    print(prompt)
    time.sleep(2)
    print(punchline)

get_user_input = lambda: input("Input (next/quit): ")

def read_input():
    user_input = get_user_input()
    while user_input not in ("next", "quit"):
        print("I don't understand")
        user_input = get_user_input()
    return user_input == "next"

def read_jokes_from_csv(csv_filename):
    with open(csv_filename) as csv_file:
        return list(csv.reader(csv_file))

def get_reddit_posts():
    return (
        requests
            .get("https://www.reddit.com/r/dadjokes.json",
                 headers={'User-agent': "my_jokebot"})
            .json()
            ['data']
            ['children']
    )

def filter_posts(posts_iterable):
    yield from filter(lambda post: (post['data']['title']
                                       .startswith(("Why ", "What ", "How "))
                                    and not post['data']['over_18']
                                   ),
                      posts_iterable)

def get_list_of_jokes(posts_iterable):
    return [(post['data']['title'], post['data']['selftext'])
            for post in posts_iterable]


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Too many command-line arguments")
    else:
        try:
            jokes = (
                read_jokes_from_csv(sys.argv[1]) if len(sys.argv) == 2
                else get_list_of_jokes(filter_posts(get_reddit_posts()))
            )
            for prompt, punchline in jokes:
                if read_input():
                    deliver_joke(prompt, punchline)
                else:
                    break
        except FileNotFoundError:
            print("Joke file not found")
