# kakuro-solver-csp
The canonical Kakuro puzzle is played in a grid of filled and barred cells, "black" and "white" respectively. Puzzles are usually 16×16 in size, although these dimensions can vary widely. Apart from the top row and leftmost column which are entirely black, the grid is divided into "entries"—lines of white cells—by the black cells. The black cells contain a diagonal slash from upper-left to lower-right and a number in one or both halves, such that each horizontal entry has a number in the black half-cell to its immediate left and each vertical entry has a number in the black half-cell immediately above it. These numbers, borrowing crossword terminology, are commonly called "clues".

The objective of the puzzle is to insert a digit from 1 to 9 inclusive into each white cell so that the sum of the numbers in each entry matches the clue associated with it and that no digit is duplicated in any entry.


![image](https://user-images.githubusercontent.com/75631297/180121510-0a3bde63-7950-4f61-8ab0-fbdfe75ae9a9.png)
![image](https://user-images.githubusercontent.com/75631297/180121550-4e7476e9-1d6c-4bd5-a626-070ec8d0cb77.png)

## Results

![Screenshot from 2022-07-21 08-42-10](https://user-images.githubusercontent.com/75631297/180122053-b1a242fc-7fb9-4ab7-83b4-be3e566a5d5c.png)

Count BS - No.of backtrack calls in generic backtracking search with AC-3 applied before to reduce domain.

Count MAC - No.of backtrack calls in backtracking search with Maintaining Arc Consistency after each variable assignment.

Time BS - Time taken in seconds for generic backtracking search.

Time MAC - Time taken in seconds for backtracking search with Maintaining arc consistency.

## Formulating the puzzle as general CSP:

In kakuro we have row and column constraints where a sum is
given and a certain number of variables should sum up to the given
constraint and the value of variables should be distinct. (All diff
constraint)
Domain - to satisfy the sum constraint the variables can take values
from 1 to 9
Example:
Say the row sum constraint for some row is 7 and the number
of variables whose sum needs to be 7 is 3. Say, x1,x2,x3 are the
three variables. The first constraint on them is x1+x2+x3 = 7. The
second constraint is x1!=x2 and x2!=x3 and x1!=x3. The domain of
these variables can be from 1 to 9

## N-ary to binary constraint conversion:

From the above example we have constraints as x1+x2+x3=7
and all of x1,x2,x3 should be distinct. But it is a N-ary constraint as
all three variables are involved in the constraint , here N = 3.
To make it into a binary constraint we can generate all possible
permutations of three values which satisfies the given constraints.
For above example , one such permutation is 1,2,4. So the binary
constraints are (x1,1,x2,2) , (x2,2,x3,4) , (x1,1,x3,4) which is of the
form (var1,value1,var2,value2) which means there is a possible
permutation in which var1 can take value1 and var2 can take
value2. Here both sum and all diff constraints are maintained.
These constraints are stored in a dictionary. Neighbours of each
variable are also stored in a dictionary. In the above example
neighbours of x1 are x2 and x3, neighbours of x2 are x1 and x3 and
neighbours of x3 are x1 and x2.

## Node consistency:

For each variable domain of that variable is min(9,sum) ,
where sum is the sum constraint of that variable.

## Arc consistency:

Standard AC-3 algorithm is applied , initially all arcs are put in
the queue. It is used to reduce the domain. If we consider the arc
Xi,Xj then for some value in domain of Xi if there is no value which
satisfies the csp is in Xj then the value is removed from domain for
Xi.

## Generic Backtracking search:

First an unassigned variable is taken and for each value in the
domain of that variable if the value is consistent with assigned
variables then we assign this value to this variable and backtracking
search is called again with this assignment. If assignment of some
variable leads to Failure then we backtrack from there by removing
that assignment to that variable and then trying the next value for
that variable.

## Backtracking search with MAC:

It is same as generic backtracking search but additionally
when we assign some value to a variable we call the AC-3
algorithm in which the queue initially has the arcs (Xj,Xi) for all Xj
which is unassigned neighbour of Xi. Xi is the variable to which
value was assigned. AC-3 returns false when after some
assignment of value to a variable, some of its neighbour’s domain
becomes empty. When AC-3 returns false the assignment is not
possible so we backtrack.
