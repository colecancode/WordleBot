import re

#word list
words = open("Wordle Answers.txt", "r").readlines()

#instructions
print('''
                      ---Wordle Solver---
Input your guess, as well as the result using letters or boxes.

⬛ or "B" - Incorrect letter & position
🟩 or "Y" - Correct letter, incorrect position
🟨 or "G" - Correct letter & position

The format is as follows:

GUESS            OR        GUESS
⬛⬛🟨🟩⬛                BBGYB

''')

def SortWords(c = [], wp = [], i = []):
    #input
    guess = list(input("Guess:  ").lower())
    result = list(input("Result: ").lower())

    #search for compatable words
    correct = c
    wrongPlace = wp
    incorrect = i

    for i in range(0, 5):
        r = result[i]
        g = guess[i]
        if r == "🟨" or r == "g":
            correct.append([g, i])
            
    for i in range(0, 5):
        r = result[i]
        g = guess[i]
        if r == "🟩" or r == "y":
            wrongPlace.append([g, i])
        elif r  == "⬛" or r == "b":
            bool = False
            for letter in correct:
                if letter[0] == g:
                    wrongPlace.append([g, i])
                    bool = True
            for letter in wrongPlace:
                    if letter[0] == g:
                        bool = True
            if bool == False:
                incorrect.append(g)
    
    potentialWords = []

    for word in words:
        valid = True
        for letter in incorrect:
            if letter in word:
                valid = False
        for letter in wrongPlace:
            if letter[0] in word:
                if word[letter[1]] == letter[0]:
                    valid = False
            else:
                valid = False
        for letter in correct:
            if word[letter[1]] != letter[0]:
                valid = False
        if valid:
            potentialWords.append(word)

    #print
    print("\n\n")
    if len(potentialWords) == 0:
        print("No possible words, try again")
    for word in potentialWords:
        print(word[:-1])
    print("\n\n")

    SortWords(correct, wrongPlace, incorrect)

SortWords()
