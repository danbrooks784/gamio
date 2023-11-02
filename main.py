"""
CP1404 - Guessing Game for review and refactor
Some of this is "good" code, but some things are intentionally poor
This is for a code review and refactoring exercise
"""
import math
import random

DEFAULT_LOW = 1
DEFAULT_HIGH = 10


def main():
    """Menu-driven guessing game with option to change high limit."""
    low = DEFAULT_LOW
    high = DEFAULT_HIGH
    number_of_games = 0
    print("Welcome to the guessing game")
    choice = input("(P)lay, (S)et limit, (H)igh scores, (Q)uit: ").upper()
    while choice != "Q":
        if choice == "P":
            number_of_guesses = play_game(low, high)
            if is_good_score(number_of_guesses, high - low + 1):
                print("Good guessing!")
            save_choice = input("Do you want to save your score? (y/N) ")
            if save_choice.upper() == "Y":
                save_score(number_of_guesses, low, high)
            else:
                print("Fine then.")
            number_of_games += 1
        elif choice == "S":
            high = set_limit(low)
        elif choice == "H":
            scores = load_scores()
            display_high_scores(scores)
        else:
            print("Invalid choice")
        choice = input("(P)lay, (S)et limit, (H)igh scores, (Q)uit: ").upper()
    print(f"Thanks for playing ({number_of_games} times)!")


def save_score(number_of_guesses, low, high):
    """Save score to scores.txt with range"""
    with open("scores.txt", "a", encoding='utf-8') as out_file:
        # Score format is number of guesses | range of values
        print(f"{number_of_guesses}|{high - low + 1}", file=out_file)


def play_game(low, high):
    """Play guessing game using current low and high values."""
    secret = random.randint(low, high)
    number_of_guesses = 1
    guess = get_valid_number(f"Guess a number between {low} and {high}: ")
    while guess != secret:
        number_of_guesses += 1
        if guess < secret:
            print("Higher")
        else:
            print("Lower")
        guess = get_valid_number(f"Guess a number between {low} and {high}: ")
    print(f"You got it in {number_of_guesses} guesses.")
    return number_of_guesses


def set_limit(low):
    """Set high limit to new value from user input."""
    print("Set new limit")
    new_high = get_valid_number(f"Enter a new high value, above {low}: ")
    while new_high <= low:
        print("Higher!")
        new_high = get_valid_number(f"Enter a new high value, above {low}: ")
    return new_high


def get_valid_number(prompt):
    """Get a valid number input."""
    is_valid = False
    while not is_valid:
        try:
            number = int(input(prompt))
            is_valid = True
        except ValueError:
            print("Invalid number")
    return number  # PyCharm raises an error but number will always be valid


def is_good_score(number_of_guesses, range_):
    """Determine if a score is good."""
    return number_of_guesses <= math.ceil(math.log2(range_))


def load_scores():
    """Load scores text file."""
    scores = []
    with open("scores.txt", "r", encoding='utf-8') as in_file:
        for line in in_file:
            line = line.split("|")
            scores.append((int(line[0]), int(line[1])))
    return scores


def display_high_scores(scores):
    """Sort scores in ascending order and print them."""
    scores.sort()
    for score in scores:
        marker = "!" if is_good_score(score[0], score[1]) else ""
        print(f"{score[0]} ({score[1]}) {marker}")


main()
