# Names 
- Patricia Bivol
- Jaden Towey 
- Anthony Ilchev 

# Programming Assignment 3 (PA3): Sudoku via SAT

In this assignment you will use the SAT solver from PA2 to solve $9\times 9$ Sudoku puzzles.

Work in groups of 2-4 people. Comment and document your code thoroughly.

## Files

Implement your solution in:

```text
sudoku_solver.py
```

Your `sudoku_solver.py` must use a SAT solver. You may copy your PA2
implementation into:

```text
sat_solver.py
```

## Required Functions

Implement:

```python
def sudoku_encode(grid):
    ...

def solve(grid):
    ...
```

Input:

- `grid`: a list of 9 lists, each containing 9 integers
- `0` means an empty cell
- values `1` through `9` are given

Output:

- if the Sudoku puzzle is solvable, return a solved `9 x 9` grid
- if it is unsolvable, return `None`

## SAT Encoding

Use Boolean variables of the form:

```text
cell (row, column) contains digit d
```

A common integer encoding is:

```python
varnum(row, col, digit) = 100 * row + 10 * col + digit
```

where `row`, `col`, and `digit` are in `{1, ..., 9}`.

Your CNF encoding should enforce:

1. Every cell contains at least one digit.
2. Every cell contains at most one digit.
3. Every digit appears in every row.
4. Every digit appears in every column.
5. Every digit appears in every `3 x 3` box.
6. The given digits from the input grid are respected.

Then call your SAT solver from PA2 on the resulting clauses. For the encoding, see also the corresponding [exercise](https://hackmd.io/@jweinberger/SkBvxPcCbg).

## Examples

Several test cases are typical:

- a standard solvable Sudoku,
- a sparse solvable Sudoku,
- grids with contradictions that should return `None`.

Your solutions will be tested on the given as well as possibly on additional puzzles. The tests only check for solvable/unsolvable, not for a concrete solution.

You can run the solver file directly from the shell:

```bash
python3 sudoku_solver.py "[
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]"
```

A solution here would be:
```
[5, 3, 4, 6, 7, 8, 9, 1, 2]
[6, 7, 2, 1, 9, 5, 3, 4, 8]
[1, 9, 8, 3, 4, 2, 5, 6, 7]
[8, 5, 9, 7, 6, 1, 4, 2, 3]
[4, 2, 6, 8, 5, 3, 7, 9, 1]
[7, 1, 3, 9, 2, 4, 8, 5, 6]
[9, 6, 1, 5, 3, 7, 2, 8, 4]
[2, 8, 7, 4, 1, 9, 6, 3, 5]
[3, 4, 5, 2, 8, 6, 1, 7, 9]
```

However, e.g., the following is unsolvable:

```
[
    [5, 1, 6, 8, 4, 9, 7, 3, 2],
    [3, 0, 7, 6, 0, 5, 0, 0, 0],
    [8, 0, 9, 7, 0, 0, 0, 6, 5],
    [1, 3, 5, 0, 6, 0, 9, 0, 7],
    [4, 7, 2, 5, 9, 1, 0, 0, 6],
    [9, 6, 8, 3, 7, 0, 0, 5, 0],
    [2, 5, 3, 1, 8, 6, 0, 7, 4],
    [6, 8, 4, 2, 0, 7, 5, 0, 0],
    [7, 9, 1, 0, 5, 0, 6, 0, 8],
]
```

## Grading (15 points)

Grading breakdown:

- **9 points**: tests pass
- **2 points**: output contract and CLI usage
- **2 point**: maintaining directory and file structure
- **2 point**: code quality (readable implementation, clear variable naming, no hard-coding)

## Run Checks

From the `pa3` directory, run:

```bash
python3 tests/test_pa3.py --solution sudoku_solver.py
```