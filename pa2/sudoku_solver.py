"""PA3 starter: solve Sudoku puzzles using SAT."""

from __future__ import annotations

import ast
import sys

from sat_solver import sat_solve


def varnum(row, col, digit):
    """Encode (row, col, digit) as one positive SAT variable.

    row, col, and digit are all 1-based numbers in {1, ..., 9}.
    """
    return 100 * row + 10 * col + digit


def exactly_one(literals):
    """Return CNF clauses expressing that exactly one literal is true."""
    clauses = [list(literals)]

    # At most one: for every pair, not both can be true.
    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            clauses.append([-literals[i], -literals[j]])

    return clauses


def sudoku_encode(grid):
    clauses = []

    # Every cell must contain exactly one digit
    for r in range(1, 10):
        for c in range(1, 10):
            possibilities = [varnum(r, c, n) for n in range(1, 10)]
            clauses.extend(exactly_one(possibilities))

    # Every digit appears once per row
    for r in range(1, 10):
        for n in range(1, 10):
            row_values = [varnum(r, c, n) for c in range(1, 10)]
            clauses.extend(exactly_one(row_values))

    # Every digit appears once per column
    for c in range(1, 10):
        for n in range(1, 10):
            col_values = [varnum(r, c, n) for r in range(1, 10)]
            clauses.extend(exactly_one(col_values))

    # Every digit appears once in each 3x3 box
    for box_r in range(3):
        for box_c in range(3):
            for n in range(1, 10):
                block_values = [
                    varnum(3 * box_r + dr, 3 * box_c + dc, n)
                    for dr in range(1, 4)
                    for dc in range(1, 4)
                ]
                clauses.extend(exactly_one(block_values))

    # Add fixed puzzle values
    for r in range(1, 10):
        for c in range(1, 10):
            value = grid[r - 1][c - 1]
            if value != 0:
                clauses.append([varnum(r, c, value)])

    return clauses


def decode_solution(assignment):
    """Convert a satisfying SAT assignment back into a Sudoku grid."""
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(1, 10):
        for col in range(1, 10):
            for digit in range(1, 10):
                if assignment.get(varnum(row, col, digit)) is True:
                    grid[row - 1][col - 1] = digit
                    break
    return grid


def solve(grid):
    """Return a solved Sudoku grid, or None if the puzzle is unsolvable."""
    clauses = sudoku_encode(grid)

    assignment = sat_solve(clauses, {})

    if assignment is None:
        return None

    return decode_solution(assignment)


def print_result(solution):
    """Print the Sudoku result using the assignment handout format."""
    print(f'solvable: {str(solution is not None).lower()}')
    if solution is None:
        print('solution: None')
        return

    print('solution:')
    for row in solution:
        print(row)


def main():
    """Run the Sudoku solver from the command line on one grid."""
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    grid = ast.literal_eval(raw)
    print_result(solve(grid))


if __name__ == '__main__':
    main()