import os
import requests
from colorama import init, Back
from graphics import *

# Constants
WELCOME_MESSAGE = "Welcome to NODle"
PLAYER_INSTRUCTIONS = ""
GUESS_MESSAGE = ""
ALLOWED_GUESSES = 6
WORD_LENGTH = 5
WORD_LANGUAGE = "en"

init()
clear_screen = lambda: os.system('clear')

def start_game():
    """Keeps one current game running until the answer is correct or the user runs out of guesses"""
    clear_screen()
    correct_guess = False
    guessed_words_list = []
    word_attempts = 0

    while not correct_guess and word_attempts < ALLOWED_GUESSES:
        key = win.getKey()
        if key == "Return":
            box.setText('')
            entered_word = inputBox.getText()
            if is_valid_user_guess(entered_word):
                inputBox.setText('')
                guessed_word = [i for i in entered_word]
                correct_guess, state_list = check_user_guess(guessed_word)
                guessed_words_list.append([guessed_word, state_list])
                show_grid_graphic(guessed_words_list, win)
                word_attempts += 1
            else:
                box.setText(f'"{entered_word}" is not a valid word. Try again!')

    # user did not guess correct
    if not correct_guess:
        t = Text(Point((1 + WORD_LENGTH) * 35 + 10, 500), f"😢 Sorry...\nThe correct word was: {''.join(generated_word).upper()}")
        t.setSize(20)
        t.setFill("black")
        t.draw(win)

    # The user guessed correct
    else:
        t = Text(Point(250, 500), '')
        t.setText(f"🎉 CONGRATS! You guessed correctly!\n The word was: {''.join(generated_word).upper()}")
        t.setSize(20)
        t.setFill('white')
        t.setTextColor('red')
        t.draw(win)

    return word_attempts, correct_guess

def generate_word(length, language):
    """Fetches a random word using an API"""
    query_params = {'lang': language, 'length': length}

    try:
        response = requests.get("https://random-word-api.herokuapp.com/word", params=query_params)
        response.raise_for_status()
        word = response.json()[0]
        return [letter.lower() for letter in word]
    except requests.RequestException as e:
        print(f"Error fetching word: {e}")
        return []

def replay_game():
    """Ask user if they want to play again. Returns boolan value"""
    m = Text(Point(250,580), 'Press y to play again and n to stop playing and show stats')
    m.setSize(12)
    m.setFill('white')
    m.setTextColor('black')
    m.draw(win)
    
    while True:
        key = win.getKey().lower()
        if key == 'y':
            return True
        elif key == 'n':
            return False

def get_user_guess(WORD_LENGTH: int):
    """Gets input from user and checks if the word is valid"""
    valid_word = False

    while not valid_word:
        guessed_word = input(f'Guess a {WORD_LENGTH} letter word: ')
        if is_valid_user_guess(guessed_word):
            valid_word = True
        else:
            print('\nThat is not a valid word\n')
    return [i for i in guessed_word]

def is_valid_user_guess(guessed_word):
    """Checks that it is only letters"""
    return guessed_word.isalpha() and len(guessed_word) == len(generated_word)

def check_user_guess(guessed_word):
    """Checks the correctness of the users guess and returns a list of each letters state"""
    state_list = []

    if guessed_word == generated_word:
        return True, [2] * WORD_LENGTH
    else:
        temp_generated_word = generated_word.copy()
        temp_guessed_word = guessed_word.copy()
        for i in range(len(temp_guessed_word)):
            #state_list.append(is_in_word(guessed_word[i], i))
            if temp_guessed_word[i] == temp_generated_word[i]:
                state_list.append(2)
                temp_generated_word[i] = " "
                temp_guessed_word[i] = " "
            else:
                state_list.append(0)

        for i in range(len(temp_guessed_word)):
            if temp_guessed_word[i] in temp_generated_word and not temp_guessed_word[i] == " ":
                state_list[i] = 1
                temp_generated_word.remove(temp_guessed_word[i])
        return False, state_list

def is_in_word(letter, position):
    """Old function to check a letters stati in word"""
    if letter in generated_word:
        if generated_word[position] == letter:
            return 2 # letter in word, in correct position
        else:
            return 1 # letter in word, wrong position
    else:
        return 0 # letter not in word

def show_grid(guessed_words_list):
    """Old depricated function to show guesses in the terminal"""
    clear_screen()

    for word in guessed_words_list:
        string_output = ""
        for index in range(len(word[0])):
            if word[1][index] == 2: # letter in word, in correct position
                string_output += Back.GREEN + word[0][index].lower() + Back.RESET
            elif word[1][index] == 1: # letter in word, wrong position
                string_output += Back.YELLOW + word[0][index].lower() + Back.RESET
            else: # letter not in word
                string_output += Back.BLACK + word[0][index].lower() + Back.RESET
        print(string_output)

def show_grid_graphic(guessed_words_list, win):
    """Updates the window with every current guess"""
    letter_size = 20
    rec_size = 60
    letter_offset = rec_size/2
    y = 10
    for word in guessed_words_list:
        x = rec_size + 10
        for index in range(len(word[0])):
            r = Rectangle(Point(x, y), Point(x + rec_size, y + rec_size))

            if word[1][index] == 2: # letter in word, in correct position
                r.setFill("green") 
            elif word[1][index] == 1: # letter in word, wrong position
                r.setFill("yellow")
            else: # letter not in word
                r.setFill("grey")

            t = Text(Point(x + letter_offset, y + letter_offset), word[0][index].upper())
            t.setSize(letter_size)
            t.setStyle("bold")
            t.setFill("White")
            r.draw(win)
            t.draw(win)
            x += rec_size + 10
        y += rec_size + 20

def show_stats():
    """Old depricated terminal based stats function"""
    total_games = len(user_stats)

    if total_games == 0:
        print("No games played.")
        return

    number_of_wins = sum(guess[1] for guess in user_stats)
    win_percentage = (number_of_wins / total_games) * 100

    print(f"Number of games played: {total_games}")
    print(f"Win percentage: {win_percentage:.2f}%")

    print("Guess distribution: ")
    for i in range(1, 7):
        number_of_times = sum(1 for guess in user_stats if guess[0] == i and guess[1])
        print(f"{i}: {number_of_times}")

def show_stats_graphic():
    """Creates anew window with statistics of your current streak of games"""
    stats_win = GraphWin("Stats", 400, 500)
    x = 50
    y = 30

    number_of_games = len(user_stats)
    number_of_wins = len([guess for guess in user_stats if guess[1] == True])
    win_percentage = int(100 * number_of_wins / number_of_games)
    stats_lst = [number_of_games, number_of_wins, win_percentage]

    for i in stats_lst:
        t = Text(Point(x , y), str(i))
        t.setSize(30)
        t.setStyle("bold")
        t.draw(stats_win)
        x += 90

    x = 50
    y += 30
    str_lst = ["Played", "Wins", "Win %"]

    for string in str_lst:
        t = Text(Point(x , y), string)
        t.setSize(18)
        t.draw(stats_win)
        x += 90

    x = 120
    y += 50
    t = Text(Point(x , y), "Guess Distribution")
    t.setStyle("bold")
    t.setSize(18)
    t.draw(stats_win)
    x = 50

    for i in range(1, 7):
        number_of_times = len([guess for guess in user_stats if guess[0] == i and guess[1] == True])
        y += 30
        t = Text(Point(x, y), f"{i}: {number_of_times}")
        t.setSize(15)
        t.draw(stats_win)

    while True:
        try:
            stats_win.getMouse()
            stats_win.close()
        except GraphicsError:
            break

def show_instructions():
    """Creates a window for information on how to play"""
    x_window = 700
    y_window = 500
    win = GraphWin("How to play", x_window, y_window)
    string_list = [("How To Play", 30), ("Guess the word in 6 tries", 20), ("Each guess must be a valid 5 letter word", 20),\
                ("The color of the tiles will change to show clues about your guess", 20), ("Example: The correct word is TRAIN", 24),\
                    ("T and R is in the correct spot", 20), ("I is in the word but in the wrong spot", 20), ("C and K are not in the word", 20)]
    x = x_window / 2
    y = 10

    for string, size in string_list:
        y += size
        t = Text(Point(x, y), string)
        t.setTextColor("white")
        t.setSize(size)
        t.draw(win)
        y += size

    example_guess = [["T", "R", "I", "C", "K"], [2, 2, 1, 0, 0]]
    rec_size = 60
    letter_offset = rec_size/2
    letter_size = 20
    x -= 3 * rec_size

    for index in range(len(example_guess[0])):
        r = Rectangle(Point(x, y), Point(x + rec_size, y + rec_size))

        if example_guess[1][index] == 2: # letter in word, in correct position
            r.setFill("green")
        elif example_guess[1][index] == 1: # letter in word, wrong position
            r.setFill("yellow")
        else: # letter not in word
            r.setFill("grey")

        t = Text(Point(x + letter_offset, y + letter_offset), example_guess[0][index].upper())
        t.setSize(letter_size)
        t.setStyle("bold")
        t.setFill("White")
        r.draw(win)
        t.draw(win)
        x += rec_size + 10

    while True:
        try:
            win.getMouse()
            win.close()
        except GraphicsError:
            break

if __name__ == '__main__':
    user_stats = []
    game_on = True
    show_instructions()

    while game_on:
        win = GraphWin("Nodle", (2 + WORD_LENGTH) * 70, 700)
        win.setBackground("lightblue")

        # User input box
        inputBox = Entry(Point(250,650), 5)
        inputBox.setSize(36)
        inputBox.setTextColor('black')
        inputBox.draw(win)

        # Error message display
        box = Text(Point(250,550), '')
        box.setSize(22)
        box.setFill('white')
        box.setTextColor('black')
        box.draw(win)

        # game message
        message = Text(Point(245, 740), "Let's play a game of NODLE. Guess a 5 letter word!")
        message.setSize(20)
        message.setFill('white')
        message.setTextColor('red')
        message.draw(win)

        generated_word = generate_word(WORD_LENGTH, WORD_LANGUAGE)
        word_attempts, correct_guess = start_game()
        user_stats.append((word_attempts, correct_guess))
        game_on = replay_game()
        win.close()

    show_stats_graphic()