# CMSC 14200 Course Project

Team members:
- QA: Evelyn Wang (egwang)
- Bot: Vivian Chang (vchang5)
- GUI: Paulina DePaulo (pdepaulo)

## Improvements

### Game Logic
Grading comment: Issue with Constructor. See code comment(s)

Comment: [Code Quality] This if statement doesn't properly check if a point is out of bounds. As it is, only one of the x or y need to be in bounds for the ValueError to be dodged. Which means i can have a starting position at (-100, 0) which would be counted as in bounds here. 

Furthermore, we received a comment suggesting that we make an additional helper function.

Comment: I would highly recommend making this check a helper function, ie: a method that takes in a (row, col) coordinate pair and returns whether or not it is on the board.

