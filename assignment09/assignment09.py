import random
def green_letter(letter):
    return '\033[92m' + letter + '\033[0m'


def yellow_letter(letter):
    return '\033[93m' + letter + '\033[0m'

def generate_word_list():
    words = open("words.txt", "r")
    word_list = []
    for line in words.readlines():
        line = line.strip()
        word_list.append(line)
    words.close()
    return word_list

def get_guess(word_list):
    guess = False
    while guess != True:
        word = input("Enter a guess: ")
        if word in word_list:
            guess = True
        else:
            guess = False
    return word

def pick_word(word_list):
    word = random.randint(0,len(word_list))
    word = word_list[word]
    return word

def is_game_over(word, guesses):
    if word in guesses:
        return True
    elif len(guesses) == 6:
        return True
    else:
        return False

def display_board(word, guesses):
    colorguess = ''
    if len(guesses) >= 1:
        guess = guesses[len(guesses) - 1]
        for letters in range(len(word)):
            if guess[letters] in word:
                if word[letters] == guess[letters]:
                    colorguess = colorguess + green_letter(guess[letters])
                elif guess[letters] in word:
                    if guess[letters] in colorguess:
                        if guess[letters] in word[word.find(guess[letters]) + 1:len(word)] and guess[letters] in guess[guess.find(guess[letters]):len(guess)]:
                            colorguess = colorguess + yellow_letter(guess[letters])
                        else:
                            colorguess = colorguess + guess[letters]
                    else:
                        colorguess = colorguess + yellow_letter(guess[letters])
            else:
                colorguess = colorguess + guess[letters]
        guesses.remove(guesses[len(guesses) -1])
        guesses.append(colorguess)
    print('+-----+')
    for x in range(len(guesses)):
        print('|' + guesses[x] + '|')
    for y in range(6 - len(guesses)):
        print('|     |')
    print('+-----+')

def play_pyrdle():
    print('PYRDLE')
    wordList = generate_word_list()
    word = pick_word(wordList)
    guesses = []
    isgameover = False
    while isgameover != True:
        display_board(word, guesses)
        guesses.append(get_guess(wordList))
        isgameover = is_game_over(word, guesses)
    display_board(word, guesses)
    if word in guesses:
        print('YOU WIN')
    else:
        print("The word was:" + word)
        print("YOU LOSE")