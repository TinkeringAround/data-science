# Excercises RAJ - ES5 - Excercise 2
# Analyse the esoph dataset. Can you derive some useful statements from it? Use data() to see all available datasets.

# Install Packages
#install.packages("skimr")
#install.packages("devtools")

# Imports
library(stats)
library(skimr)
library(devtools)
library(graphics) # for mosaicplot

# Declarations
printSeparator <- function() {
    cat("", sep="\n\n\n")
    print("---------------------------------------------------------------------------------------------")
    cat("", sep="\n\n\n")
}

# Clear Console
cat(rep("\n", 50))
printSeparator()

# Plain Dataset
print("Dataset:")
print(esoph)

printSeparator()

# Dataset Summary with Mean and Median Values
print("Summary of the esoph Dataset:")
print(summary(esoph))

printSeparator()

# Use Skim to Analyze Dataset
print("Analyze Dataset with skim:")
print(skim(esoph))

printSeparator()

#####################################################################################################
## Example Code copied from - https://stat.ethz.ch/R-manual/R-patched/library/datasets/html/esoph.html

## effects of alcohol, tobacco and interaction, age-adjusted
model1 <- glm(cbind(ncases, ncontrols) ~ agegp + tobgp * alcgp,
              data = esoph, family = binomial())
print(anova(model1))

printSeparator()

## Try a linear effect of alcohol and tobacco
model2 <- glm(cbind(ncases, ncontrols) ~ agegp + unclass(tobgp)
                                         + unclass(alcgp),
              data = esoph, family = binomial())
print(summary(model2))

printSeparator()

## Re-arrange data for a mosaic plot
ttt <- table(esoph$agegp, esoph$alcgp, esoph$tobgp)
o <- with(esoph, order(tobgp, alcgp, agegp))
ttt[ttt == 1] <- esoph$ncases[o]
tt1 <- table(esoph$agegp, esoph$alcgp, esoph$tobgp)
tt1[tt1 == 1] <- esoph$ncontrols[o]
tt <- array(c(ttt, tt1), c(dim(ttt),2),
            c(dimnames(ttt), list(c("Cancer", "control"))))
mosaicplot(tt, main = "esoph data set", color = TRUE)

# Finish
readline("Press any Key to exit.")
quit()