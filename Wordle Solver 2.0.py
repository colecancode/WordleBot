import re
import pyautogui as pg
import time
import sys

# print(sys.getrecursionlimit())
sys.setrecursionlimit(10000000)

# word list
words = open("Wordle Answers.txt", "r").readlines()


def newGame():
    def findNewWord(g, r, c=[], wp=[], i=[]):

        # search for compatible words
        if wp is None:
            wp = []
        guess = g
        result = r
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
            elif r == "⬛" or r == "b":
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
                potentialWords.append(word[:-1])
        return findBestWord(potentialWords)

    def findBestWord(words):
        scores = {}
        letterFrequency = open('Letter Frequency.txt', 'r').read().splitlines()
        for word in words:
            letterCount = {}
            scores[word] = 0
            for letter in word:
                if letter in letterCount.keys():
                    letterCount[letter] += 1
                else:
                    letterCount[letter] = 1
                scores[word] -= letterFrequency.index(letter)
            for value in letterCount.values():
                if value >= 2:
                    scores[word] += value * 10
        scores = sorted(scores.items(), key=lambda x: x[1])
        bestWord = scores[0]
        return bestWord[0]

    def getColor(row, index, img):
        spacing = row[2] / 5
        x = row[0] + spacing * index - 15
        y = row[1] + 5
        pg.moveTo((x, y))
        color = img.getpixel((x, y))
        match color:
            case (120, 124, 126):
                return "b"
            case (201, 180, 88):
                return "y"
            case (106, 170, 100):
                return "g"

    def newRow(prior):
        return (prior[0], prior[1] + 70, prior[2], prior[3])

    def restart():
        time.sleep(2)
        # button = pg.locateCenterOnScreen('Button.png')
        # if button != None:
        #    pg.click(button)
        # else:
        pg.click(x=835, y=720)
        newGame()

    def executeGuess(guess, rowIndex=0, reset=False):
        pg.write(guess, interval=.05)
        pg.hotkey("enter")

        time.sleep(2)

        bool = True
        while bool:
            sc = pg.screenshot()

            result = [getColor(rows[rowIndex], 1, sc),
                      getColor(rows[rowIndex], 2, sc),
                      getColor(rows[rowIndex], 3, sc),
                      getColor(rows[rowIndex], 4, sc),
                      getColor(rows[rowIndex], 5, sc)]

            if "b" in result or "y" in result:
                if rowIndex >= 5:
                    bool = False
                    restart()
                    return
                newGuess = findNewWord(guess, result)
                executeGuess(newGuess, rowIndex + 1)
            else:
                bool = False
                restart()
                return

    # pg.PAUSE = .5

    time.sleep(1)

    rows = [pg.locateOnScreen('Blank Row.png')]
    for i in range(0, 5):
        rows.append(newRow(rows[i]))

    executeGuess("tears")


newGame()

# Gray - (120, 124, 126)
# Yellow - (201, 180, 88)
# Green - (106, 170, 100)
