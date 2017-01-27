# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In a unit, when there are 2 boxes, both permit exactly same 2 values, then un-permit those 2 values on other boxes in the same unit.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Add 2 diagonal unit to unit list

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.

## Algorithm used here

### Sudoku to N-Rook problems

Instead of the reduction method provided by Udacity Lesson, here use another algorithm.

In a 9x9 Sudoku grid, there is X and Y dimension
Lets add a Z dimension to the grid (length=9), which means "permitted value".
So we have 9x9x9 boolean grid represent the Sudoku data.
In fact, the 9x9x9 grid can be converted to the "values" dict, and vice versa.

In each XY / XZ / YZ planes in the 3D boolean table,
there are no two "True" value exist in the same row or same col.
That is "N-Rooks problem"  ("something like N-Queens but the pieces are rook").
Solving those N-Rooks problem would finally solve the Sudoku game.

Other than the XY / XZ / YZ planes, there are 3 special cases to handle.

Case 1: Square units

To solve the square units, we transform the 9 unit into 9 N-Rook problems. (w_transform)

Case 2: Sub group exclusion

In following example:

    234 567 ...
    AAA BBB CCC
    AAA BBB CCC

We can assume that A must contains a 1, and B must contains a 1.
So C must NOT contains a 1.

In the Z-plane which z=1, the boolean value should be viewed as:

    000 000 111
    111 111 111
    111 111 111

Now we merge 3 boxes horizontally by "or" operator, the boolean value become:

    001
    111
    111

Than we can solve this 3x3 N-rooks problems, to mark all z=1 in C boxes to be false.
That is implemented as v_transform

Case 3: Diagonal unit

To solve the diagonal units, we transform the 2 unit into 2 N-Rook problems. (pick_diag)

### N-rook problem

Case 1: 3x3 N-rook problem example:

    001
    111
    111

Obviously, we can mark the r2c3 and r3c3 value to false.
The table will become:

    001
    110
    110

Case 2: 4x4 N-rook problem example:

    0011
    0011
    1111
    1111

In r1 and r2, there should be 1 in c3 and c4, so r3c3, r3c4, r4c3, r4c4 should be false.

    0011
    0011
    1100
    1100

Case 1 is level-1 reduction, as the reduction is start from data in 1 row.
Case 2 is level-2 reduction, as the reduction is start from data in 2 row.

In 9x9 N-rook problem
For level-1 reduction, we check the board 9 times.
For level-2 reduction, we check the board 9C2 = 36 times.
For level-3 reduction, we check the board 9C3 = 84 times.
For level-4 reduction, we check the board 9C4 = 126 times.

In order to speed up the calculation,
We should avoid using high level reduction, unless all lower reduction are not working.


### N-Rook and known Sudoku reduction strategies

Nearly all Sudoku reduction strategies can be transformed to N-rook problem.
(In fact, all reduction strategies I know can be transformed,
I say "nearly" just because other strategies may exist.)

Compare with http://www.sudokudragon.com/sudokustrategy.htm

* Only choice rule: XZ / YZ / WZ plane, level 1
* Single possibility rule: XZ / YZ / WZ plane, level 1
* Only square rule: XY plane, level 1
* Two out of three rule: level 1
* Sub-group exclusion rule: descripted above, level 1
* Hidden Twin exclusion rule: level 2 
* Naked Twin exclusion rule: level 2
* General permutation rule: the n-rook problem
* X-Wing and Swordfish: level 3

If N-rooks method not work, we need to do trial and error, which means searching.
