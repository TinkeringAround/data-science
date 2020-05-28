# Excercises RAJ - ES5 - Excercise 1
# Write a program to guess a number in between0 and 100! Hence the computer invents the number and the user = you tries to guess it!

# Static Messages & Declarations
promptMessage <- "Enter a value > 100 to quit or any number (100 > n > 0) to guess: "
successMessage <- "You guessed correctly. Finally, this guessing game is over."
higherMessage <- "My number is higher than the number you entered."
lowerMessage <- "My number is lower than the number you entered."
exitMessage <- "Press any Key to Exit."

printSeparator <- function() {
  cat("", sep="\n\n\n")
}

# Clear Console
cat(rep("\n", 50))

# Starting Messages
print("---------------------------------------------------------------------------------------------")
print("Hi, I am the Computer. I generate a random number between 0 and 100. You have to guess it.")
print("I now have generated a number. Start the guessing game!!")
printSeparator()

# Initialize Game
number <- sample(1:100, 1)
gameCancelled <- FALSE

# Game Loop
repeat {   
  guess <- as.integer(readline(prompt=promptMessage));

  if (guess > 100) {
      gameCancelled <- TRUE
      break
  }

  if (guess == number) {
    print(successMessage);
    printSeparator()
    break
  } else if (number > guess) {
     print(higherMessage)
  } else if (number < guess) {
     print(lowerMessage)
  }

  printSeparator()
}

# Hold if not cancelled to prevent instant quit after win
if (!gameCancelled) {
    readline(prompt=exitMessage)
}

quit()