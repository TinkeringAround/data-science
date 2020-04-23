# Modules & Declarations
import numpy as np
import random
import requests
from os import system, name


class HangmanGame:
    # Example API for Testing Purpose, Did not want to build one myself so I used the first free I found
    API_URL = "https://random-word-api.herokuapp.com/word?number=1&swear=0"
    gameIsBeaten = False
    lives = 15
    round = 0
    word = ""
    maskedWord = ""
    enteredKeys = np.array([])
    PREDEFINED_WORDS = ["extraordinary", "communication",
                        "membership", "psychologist"]  # Default Words when Example API

    # Starting the Game
    def start(self):
        self.clearConsole()
        print("-> Welcome to a simple Hangman Game! <-")
        self.printNewLine()
        self.word = self.getRandomWordFromApi()

        if len(self.word) == 0:
            self.word = self.getRandomPredefinedWord(self.PREDEFINED_WORDS)

        self.maskedWord = self.generateMaskFromWord(self.word)
        self.enterGameLoop()

    # Print Functions
    def printNewLine(self):
        print("\n")

    def clearConsole(self):
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def printWall(self, minus):
        spaces = ""
        length = 8 - minus
        index = 0
        while index < length:
            spaces += " "
            index += 1

        return spaces + "|"

    def printHangMan(self, lives):
        # Line 5
        if lives <= 4:
            print("   __________")

        # Line 4
        if lives <= 5 and lives > 3:
            print("   |")
        elif lives <= 3:
            print("   |" + self.printWall(0))

        # Line 3
        if lives == 7:
            print("  ( ")
        elif lives <= 6 and lives > 2:
            print("  ( )")
        elif lives <= 2:
            print("  ( " + ")" + self.printWall(1))

        # Line 2
        if lives == 12:
            print("   |")
        elif lives == 11:
            print("  -|")
        elif lives == 10:
            print(" --|")
        elif lives == 9:
            print(" --|-")
        elif lives <= 8 and lives > 1:
            print(" --|--")
        elif lives <= 1:
            print(" --|--" + self.printWall(2))

        # Line 1
        if lives == 14:
            print("  /")
        elif lives <= 13 and lives > 0:
            print("  /" + " \\")
        elif lives <= 0:
            print("  /" + " \\" + self.printWall(1))

    # Fetch Random Word from API
    def getRandomWordFromApi(self):
        try:
            r = requests.get(self.API_URL)
            if r.status_code == 200 and len(r.json()) > 0:
                return str(r.json()[0])
            else:
                return ""
        except:
            return ""

    # Get Random Word when REST API is not working
    def getRandomPredefinedWord(self, words):
        if isinstance(words, list):
            return words[random.randint(0, len(words) - 1)]
        else:
            return ""

    # Generate Masked Word
    def generateMaskFromWord(self, word):
        mask = ""
        for x in word:
            mask += "_"
        return mask

    # Main Game Loop
    def enterGameLoop(self):
        while self.gameIsBeaten or self.lives > 0:
            self.round += 1
            if self.round > 1:
                self.clearConsole()

            self.showGameOutput()
            input = self.waitForInput()

            # Enter '1' to QUIT the Game
            if self.isQuitGameKey(input):
                break

            # Enter whole Word
            if len(input) > 1:
                if self.compareWords(self.word, input):
                    self.gameIsBeaten = True
                    break
                else:
                    self.lives -= 2

            # Enter single Character
            lowerCaseInput = input.lower()
            if len(lowerCaseInput) == 1 and not np.isin(lowerCaseInput, self.enteredKeys):
                self.enteredKeys = np.append(self.enteredKeys, lowerCaseInput)

                if self.wordContainsCharacter(self.word, lowerCaseInput):
                    self.maskedWord = self.updateMaskedWord(
                        self.word, self.maskedWord, lowerCaseInput)
                    if self.compareWords(self.word, self.maskedWord):
                        self.gameIsBeaten = True
                        break
                else:
                    self.lives -= 1

        # End Screen
        self.showWordAndQuit()

    # Show Current Game Stats
    def showGameOutput(self):
        print("########## ROUND " +
              str(self.round) + " ##########")
        print("# Lives:         " + str(self.lives))
        print("# Entered Keys:  " +
              self.concatArrayElementsToString(self.enteredKeys))
        self.printHangMan(self.lives)
        self.printNewLine()
        print(self.maskedWord)
        self.printNewLine()

    # Check if Player wants to Quit
    def isQuitGameKey(self, character):
        if character == "1":
            return True

    # Quit Message and End Screen
    def showWordAndQuit(self):
        self.clearConsole()
        if self.gameIsBeaten:
            print("########## YOU WON! ##########")
        else:
            print("########## GAME OVER ##########")
            self.printHangMan(0)
            self.printNewLine()

        print("The Word to solve: " + self.word)
        print("You entered the following Keys: " +
              self.concatArrayElementsToString(self.enteredKeys))
        print("Thanks for playing this simple Hangman Game!")
        self.printNewLine()

    # Wait for User Input
    def waitForInput(self):
        return input("Type in a Character or '1' to QUIT: ")

    def concatArrayElementsToString(self, array):
        return "; ".join(array)

    # Check if a String contains a character
    def wordContainsCharacter(self, word, character):
        index = word.find(character)
        return index >= 0

    # Update Masked Word => Replace _ with character on correct indices
    def updateMaskedWord(self, originalWord, maskedWord, character):
        newMaskedWord = list(maskedWord)
        indexList = self.getAllCharacterIndexInWord(originalWord, character)

        for index in indexList:
            newMaskedWord[index] = character

        return "".join(newMaskedWord)

    # Get all Indices of character in a word
    def getAllCharacterIndexInWord(self, word, character):
        indexList = np.int_([])
        wordLength = len(word)
        index = 0

        while index < wordLength:
            if word[index] == character:
                indexList = np.append(indexList, int(index))
            index += 1

        return indexList

    # Check if two Strings are the same (ignoring capitals)
    def compareWords(self, word1, word2):
        return word1.lower() == word2.lower()


# Initialization & Game Loop
playGame = True
while playGame:
    hangmanGame = HangmanGame()
    hangmanGame.start()

    inputKey = input("Press 1 to RESTART or Any Other Key to QUIT: ")
    if not inputKey == "1":
        playGame = False
