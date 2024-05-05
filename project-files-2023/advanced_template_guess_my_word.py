

#!/usr/bin/env python3
"""Guess-My-Word is a game where the player has to guess a word. 
Author: Sahan Fernando
Company: words-r-cool
Copyright: April 2024

"""
# Your code must use PEP8
# Your code must be compatible with Python 3.1x
# You cannot use any libraries outside the python standard library without the explicit permission of your lecturer.

# This code uses terms and symbols adopted from the following source:
# See https://github.com/3b1b/videos/blob/68ca9cfa8cf5a41c965b2015ec8aa5f2aa288f26/_2022/wordle/simulations.py#L104

import random
from os import path

#MISS = 0  # _-.: letter not found ⬜
#MISPLACED = 1  # O, ?: letter in wrong place 🟨
#EXACT = 2  # X, +: right letter, right place 🟩

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = 'word-bank/all_words.txt'
TARGET_WORDS = 'word-bank/target_words.txt'

GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
WHITE = '\033[00m'
GREY = '\033[90m'
WIPE = '\033c'
WIPE_LINE = '\033[K'
UP_LINE ='\033[F'
MENU_LINE = '\033[3H'

TITLE = f'{WIPE}{GREEN}-- W O R D L E --{WHITE}\n'

# def all_index(list, element):
#     return [i for i in range(len(list)) if list[i] == element]

def game_frame(guesses):
    print(f"{TITLE}")
    for x in range(MAX_ATTEMPTS):
        try:
            print("   "+guesses[x])
        except:
            print("   "+f" {GREY}▢{WHITE}"*5)


def play(user_name):
    guesses = []
    """Code that controls the interactive game play"""
    #clear the screen & print title
    game_frame(guesses)
    # select a word of the day:
    word_of_the_day = get_target_word()
    # build a list of valid words (words that can be entered in the UI):
    valid_words = get_valid_words()
    # do the following in an iteration construct
    i = 0
    while True:
        i += 1
        print(" ")
        guess = ask_for_guess(valid_words)
        if not guess in ["exit", "help"]:
            score = score_guess(guess, word_of_the_day)
            guesses.append(format_score(guess, score))
            #print frame
            game_frame(guesses)
            if is_correct(score):
                print(f"\nCongratulations, you guessed the word in {i} attempts")
                break
        if guess == "exit" or i >= MAX_ATTEMPTS:
            print(f"\nThe word was: {GREEN}{word_of_the_day}{WHITE} \nBetter luck next time!")
            break
        elif guess == "help":
            i -= 1
            help()
            game_frame(guesses)
    # end iteration
    log_game(word_of_the_day, guesses, user_name)
    if input("Play again? (y/n): ").lower() in ["y", "yes"]:
        return True
    else:
        return False


def log_game(word, guesses, user_name):
    with open(f"USERDATA/{user_name}.txt", "a") as file:
        file.write(f"\n{word}")
        listg = []
        for letter in guesses:
            listg.append(letter[6::7])
        file.write(str(listg))


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is
    Examples:
    >>> is_correct((1,1,1,1,1))
    False
    >>> is_correct((2,2,2,2,1))
    False
    >>> is_correct((0,0,0,0,0))
    False
    >>> is_correct((2,2,2,2,2))
    True"""
    if score == ((2,)*WORD_LENGTH):
        return True
    return False


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words.
    Note to test that the file is read correctly, use:
    >>> get_valid_words()[0]
    'aahed'
    >>> get_valid_words()[-1]
    'zymic'
    >>> get_valid_words()[10:15]
    ['abamp', 'aband', 'abase', 'abash', 'abask']

    """
    # read words from files and return a list containing all words that can be entered as guesses
    return open(file_path,"r").read().split("\n")


def get_target_word(file_path=TARGET_WORDS, seed=None):
    """Picks a random word from a file of words

    Args:
        file_path (str): the path to the file containing the words

    Returns:
        str: a random word from the file

    How do you test that a random word chooser is choosing the correct words??
    Discuss in class!
    >>> get_target_word()
    'aback'
    >>> get_target_word()
    'zonal'
    """
    # read words from a file and return a random word (word of the day)
    with open(file_path,"r") as file:
        words = file.read().splitlines()
    return random.choice(words)


def ask_for_guess(valid_words):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
    """
    while True:
        print(f"{GREY}guess 'help' for more info. 'exit' to give up{WHITE}")
        word = input("guess: ")
        if word.lower() in valid_words or word == "exit" or word == "help":
            break
        elif len(word) != 5:
            print('\033[1A\x1b[2K'*3 + f"{RED}#Invalid: word must be 5 letters{WHITE}")
        else:
            print('\033[1A\x1b[2K'*3 + f"{RED}#Invalid: {word} isn't a word{WHITE}")
    return word.lower()


def score_guess(guess, target_word):
    # """given two strings of equal length, returns a tuple of ints representing the score of the guess
    # against the target word (MISS, MISPLACED, or EXACT)
    # Here are some example (will run as doctest):

    # >>> score_guess('hello', 'hello')
    # (2, 2, 2, 2, 2)
    # >>> score_guess('drain', 'float')
    # (0, 0, 1, 0, 0)
    # >>> score_guess('hello', 'spams')
    # (0, 0, 0, 0, 0)

    # Try and pass the first few tests in the doctest before passing these tests.
    # >>> score_guess('gauge', 'range')
    # (0, 2, 0, 2, 2)
    # >>> score_guess('melee', 'erect')
    # (0, 1, 0, 1, 0)
    # >>> score_guess('array', 'spray')
    # (0, 0, 2, 2, 2)
    # >>> score_guess('train', 'tenor')
    # (2, 1, 0, 0, 1)
    # >>> score_guess('aaaaa', 'ababa')
    # (2, 0, 2, 0, 2)
    # >>> score_guess('caaac', 'ababa')
    # (0, 1, 2, 1, 0)
    # >>> score_guess('array', 'spraa')
    # (1, 0, 2, 2, 0)
    #     """


    # You must use this convention as test automation will be validating your scorer
    score = [0] * WORD_LENGTH
    for base_index in range(WORD_LENGTH):
        if guess[base_index] == target_word[base_index]:
            score[base_index] = 2
    
    for base_index in range(WORD_LENGTH):
        if score[base_index] == 0:
            for letter_index in range(WORD_LENGTH):
                if (guess[base_index] == target_word[letter_index] 
                    and score[letter_index] != 2 
                    and [*guess[0:base_index]].count(guess[base_index]) < [*target_word].count(guess[base_index])):
                    
                    score[base_index] = 1


    #     target_work_area = list(target_word)
    # guess_work_area = list(guess)
    # score = [0] * WORD_LENGTH
    # for base_index in range(WORD_LENGTH):
    #     if guess[base_index] == target_word[base_index]:
    #         score[base_index] = 2
    #         target_work_area[base_index] = None
    #         guess_work_area[base_index] = None
    
    # for i, g in enumerate(guess_work_area):
    #     if g and g in target_work_area:
    #         score[i] = 1
    #         target_work_area.remove(g)


    # make variable score, append a zero for length of the word
    # iterate over the length of the word
        # if letter in guess and target word match at the given position
            # set the score to 2 at that position
    # iterate over the length of the word
        # if the score is 0 at that position
            #iterate for length of the word
                # if the letter in guess in the first iteration = the letter in the target word in the second iteration, and the score at the second iteration is not 2, and there are fewer number of the letter at position of fisrt iteration in the guess from the start of the word to place in second iteration than there are total of that letter in the target word.
                    #set the score to 1 at the position of the first iteration.

    # LEGACY
    # for base_index in range(WORD_LENGTH):
    #     if guess[base_index] == target_word[base_index]:
    #         # print("match at:", base_index)
    #         score[base_index] = 2
    #         # set a 1 with letter to 0 if :
    #         for i in range(base_index):
    #             #if i is 1 and letter is same and guess letter count < target letter count:
    #             if score[i] == 1 and guess[i] == guess[base_index] and [*guess[0:base_index]].count(guess[base_index]) < [*target_word[0:base_index]].count(guess[base_index]):
    #                 print(base_index, guess[base_index], [*guess[0:base_index]].count(guess[base_index]), [*target_word[0:base_index]].count(guess[base_index]))
    #                 score[i] = 0
            
    #     else:
    #         #score 1 if guess letter count < target letter count
    #         if guess[base_index] in target_word and [*guess[0:base_index]].count(guess[base_index]) < [*target_word].count(guess[base_index]):
    #             score[base_index] = 1
    return tuple(score)


def help():
    """Provides help for the game"""
    print(f"{TITLE}")
    print("Guess the 5 letter word\nIf a letter is in the correct position it will be \033[32mgreen\033[0m\nIf a letter is in the word it will be \033[33myellow\033[0m\nIf the ltter is not in the word it will be \033[97mwhite\033[0m\nUse this information to guess the right word")
    input("Enter anything to return to game: ")


def format_score(guess, score):
    """Formats a guess with a given score as output to the terminal.
    The following is an example output (you can change it to meet your own creative ideas, 
    but be sure to update these examples)
    >>> print(format_score('hello', (0,0,0,0,0)))
    H E L L O
    _ _ _ _ _
    >>> print(format_score('hello', (0,0,0,1,1)))
    H E L L O
    _ _ _ ? ?
    >>> print(format_score('hello', (1,0,0,2,1)))
    H E L L O
    ? _ _ + ?
    >>> print(format_score('hello', (2,2,2,2,2)))
    H E L L O
    + + + + +"""
    word_return = ""
    for i in range(WORD_LENGTH):
        if score[i] == 2:
            word_return += f"{GREEN} {guess[i]}"
        elif score[i] == 1:
            word_return += f"{YELLOW} {guess[i]}"
        else:
            word_return += f"{WHITE} {guess[i]}"
    word_return += WHITE
    return word_return


def create_user_file():
    while True:
        print(f"{TITLE}{GREEN} - C R E A T E -\n{GREY}\nEnter nothing to login{WHITE}\n\nPassword: ", end = "\r")
        user_name = input(f"{UP_LINE}Username: {YELLOW}")
        if path.isfile(f"USERDATA/{user_name}.txt"):
            input(f"{UP_LINE}{UP_LINE}{UP_LINE}{WIPE_LINE}{RED}That username is already taken!\n{WIPE_LINE}{GREY}Enter to continue\n{WHITE}Username: {RED}{user_name}{WHITE}\n{WHITE}Password: {WHITE}\n")
            continue
        elif user_name == "":
            break
        else:
            password = input(f"{UP_LINE}{UP_LINE}{WIPE_LINE}{GREY}Enter nothing to redo username\n{WHITE}Username: {GREEN}{user_name}{WHITE}\nPassword: {YELLOW}")
            if password == "":
                continue
            else:
                with open(f"USERDATA/{user_name}.txt", "x") as user_file:
                    user_file.write(password)
                    input(f"{UP_LINE}{UP_LINE}{UP_LINE}{UP_LINE}{WIPE_LINE}{GREEN}Profile created!\n{WIPE_LINE}{GREY}Enter to continue\n{WHITE}Username: {GREEN}{user_name}{WHITE}\n{WIPE_LINE}Password: {GREEN}{password}{WHITE}\n")
                break


def login():
    while True:
        print(f"{TITLE}{GREEN}  - L O G I N -\n\n{GREY}Enter nothing to create new profile{WHITE}\n\nPassword: ", end = "")
        user_name = input(f"{UP_LINE}Username: {YELLOW}")
        if user_name == "":
            create_user_file()
        else:
            try:
                with open(f"USERDATA/{user_name}.txt", "r") as user_file:
                    guess = input(f"{MENU_LINE}{WIPE_LINE}\n{WIPE_LINE}{GREY}Enter nothing to go back\n{WHITE}Username: {GREEN}{user_name}{WHITE} \nPassword: {YELLOW}")
                    if guess == "":
                        continue
                    password = user_file.readline().rstrip('\n')
                    filecontent = user_file.readlines()
                    if guess == password:
                        print(f"{WIPE}{TITLE}{GREEN}  - S T A T S -\n{WHITE}Welcome {GREEN}{user_name}\n\n{YELLOW}calculating statistics...{WHITE}", end = "\r")
                        try:

                            stats = [len(filecontent), 0, 0, 0, 0, 0]
                            for game in filecontent:
                                listg = game[7:-3].split("', '")
                                if game[:5] in listg:
                                    stats[1] += 1
                                    stats[3] += (1+MAX_ATTEMPTS-len(listg))*10
                                else:
                                    if len(listg)<6:
                                        stats[5] += 1
                            stats[2] = (stats[1]/stats[0])*100
                            stats[4] = (stats[3]/stats[0])

                            input(f"{UP_LINE}{WIPE_LINE}{GREY}Enter to start!\n{WIPE_LINE}{WHITE}Games played: {stats[0]}\n{WIPE_LINE}Games won: {stats[1]}\n{WIPE_LINE}Success rate: {stats[2]}\n{WIPE_LINE}Total score: {stats[3]}\n{WIPE_LINE}AVG score: {stats[4]}\n{WIPE_LINE}Gave up: {stats[5]}\n")
                        except:
                            input(f"{MENU_LINE}{WIPE_LINE}{RED}We ran into a problem calculating your statistics!{WHITE}")
                            continue
                        return user_name
                    else:
                        input(f"{MENU_LINE}{WIPE_LINE}{RED}Password incorrect!{GREY}\n{WIPE_LINE}Enter to continue\n{WHITE}Username: {RED}{user_name}\n{WHITE}Password: {RED}{guess}{WHITE}\n")
            except:
                input(f"{MENU_LINE}{WIPE_LINE}{RED}This user does not exist!\n{WIPE_LINE}{GREY}Enter to continue\n{WIPE_LINE}{WHITE}Username: {RED}{user_name}\n{WHITE}Password:\n")
                continue


def main(test=False):
    while True:
        user_name = login()
        if test:
            import doctest
            #return doctest.testmod()
            doctest.run_docstring_examples(score_guess, globals())
        while play(user_name):
            pass
        if input("login to another user?\n").lower() not in ["y", "yes"]:
            break
    print("Have a good day!")


if __name__ == '__main__':
    print(main(test=True))