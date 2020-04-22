# Modules
import random

# Declarations


class HangmanGame:
    gameIsBeaten = False
    lives = 3
    word = ""
    maskedWord = ""
    enteredKeys = []
    PREDEFINED_WORDS = ["Teleskopgabel", "Wochenplaner",
                        "Elefantenrennen"]  # Add More Words for less Duplications

    def start(self):
        print("-> Welcome to a simple Hangman Game! <-")
        self.word = self.getRandomPredefinedWord(self.PREDEFINED_WORDS)
        self.maskedWord = self.generateMaskFromWord(self.word)
        self.startGameLoop()

    def printNewLine(self):
        print("\n")

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

    def startGameLoop(self):
        while self.gameIsBeaten or self.lives > 0:
            self.showGameOutput()
            input = self.waitForInput()
            if self.isQuitGameKey(input):
                self.showWordAndQuit()
                break
            else:
                # TODO: Compare and Update Masked
                print("TODO: Compare and Update")

    def showGameOutput(self):
        self.printNewLine()
        print("############## ROUND " +
              str(len(self.enteredKeys) + 1) + " ##############")
        print("# Lives: " + str(self.lives))
        self.printNewLine()
        print("Hangman Word and Characters already entered: " + self.maskedWord +
              " " + self.concatArrayElementsToString(self.enteredKeys))

    def isQuitGameKey(self, character):
        if character == "1":
            return True

    def showWordAndQuit(self):
        print("The Word was: " + self.word)
        print("You entered the following Keys: " +
              self.concatArrayElementsToString(self.enteredKeys))
        print("Thanks for playing this simple Hangman Game!")

    def waitForInput(self):
        return input("Type Character or '1' to QUIT: ")

    def concatArrayElementsToString(self, array):
        result = ""
        for element in array:
            result += element + ";"
        return result


# Initialization
hangmanGame = HangmanGame()
hangmanGame.start()
