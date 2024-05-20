# CMSC 14200 Course Project

Team members:
- QA: Evelyn Wang (egwang)
- Bot: Vivian Chang (vchang5)
- GUI: Paulina DePaulo (pdepaulo)

## Improvements

### Game Logic

Grading comment: Issue with Constructor. See code comment(s)

Comment: [Code Quality] This if statement doesn't properly check if a point is out of bounds. As it is, only one of the x or y need to be in bounds for the ValueError to be dodged. Which means i can have a starting position at (-100, 0) which would be counted as in bounds here. 
I would highly recommend making this check a helper function, ie: a method that takes in a (row, col) coordinate pair and returns whether or not it is on the board.

Improvement: We fixed the code in blokus.py so that it would check that both the x and y coordinate were within the board, rather than checking that either of them were within the board. We also followed the grader's suggestion and made this check a method, called valid_coordinate() in line 197.
Furthermore, we changed one of the tests within test_exceptions_init() in test_blokus.py to check that the code will raise an error when one coordinate is on the board but the other isn't (line 338).

### Tests

Code Quality: Areas for improvement
Grading comment: Missing docstrings for new functions/methods

Comment: [Code Quality] Please add docstrings for your tests to communicate what the test is trying to test.
For example, describing how this test is meant to test all 4 ValueErrors upon construction.

Improvement: I added docstrings describing the purpose of each test for each test based on the requirements listed in Milestone 1 and 2 for the QA portion
