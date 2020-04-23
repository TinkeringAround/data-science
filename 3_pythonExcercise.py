# Modules
import numpy as np
import random
import requests
from os import system, name


class HangmanGame:
    # Example API for Testing Purpose, Did not want to build one myself so I used the first free I found
    API_URL = "https://random-word-api.herokuapp.com/word?number=1&swear=0"
    gameIsBeaten = False
    lives = 16
    round = 0
    word = ""
    maskedWord = ""
    enteredKeys = np.array([])
    PREDEFINED_WORDS = ["extraordinary", "communication",
                        "membership", "psychologist"]  # Default Words when Example API

    # Starting Game
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

    def getRandomWordFromApi(self):
        try:
            r = requests.get(self.API_URL)
            if r.status_code == 200 and len(r.json()) > 0:
                return str(r.json()[0])
            else:
                return ""
        except:
            return ""

    def getRandomPredefinedWord(self, words):
        if isinstance(words, list):
            return words[random.randint(0, len(words) - 1)]
        else:
            return ""

    def generateMaskFromWord(self, word):
        mask = ""
        for x in word:
            mask += "_"
        return mask

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

    def showGameOutput(self):
        print("########## ROUND " +
              str(self.round) + " ##########")
        print("# Lives:         " + str(self.lives))
        print("# Entered Keys:  " +
              self.concatArrayElementsToString(self.enteredKeys))  # TODO: Add Hangman Man
        self.printNewLine()
        print(self.maskedWord)
        self.printNewLine()

    def isQuitGameKey(self, character):
        if character == "1":
            return True

    def showWordAndQuit(self):
        self.clearConsole()
        if self.gameIsBeaten:
            print("########## YOU WON! ##########")
        else:
            print("########## GAME OVER ##########")

        print("The Word to solve: " + self.word)
        print("You entered the following Keys: " +
              self.concatArrayElementsToString(self.enteredKeys))
        print("Thanks for playing this simple Hangman Game!")
        self.printNewLine()

    def waitForInput(self):
        return input("Type in a Character or '1' to QUIT: ")

    def concatArrayElementsToString(self, array):
        result = ""
        for element in array:
            result += element + "; "
        return result

    def wordContainsCharacter(self, word, character):
        index = word.find(character)
        return index >= 0

    def updateMaskedWord(self, originalWord, maskedWord, character):
        newMaskedWord = list(maskedWord)
        indexList = self.getAllCharacterIndexInWord(originalWord, character)

        for index in indexList:
            newMaskedWord[index] = character

        return "".join(newMaskedWord)

    def getAllCharacterIndexInWord(self, word, character):
        indexList = np.int_([])
        wordLength = len(word)
        index = 0

        while index < wordLength:
            if word[index] == character:
                indexList = np.append(indexList, int(index))
            index += 1

        return indexList

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
