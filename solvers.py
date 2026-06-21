from collections import deque
from dataclasses import dataclass
from typing import Callable

from arc_utils import Grid, Task, copy_grid, empty_grid, grids_equal


SolverFunction = Callable[[Grid], Grid | None]


@dataclass(frozen=True)
class Solver:
    name: str
    description: str
    solve: SolverFunction


def solve_mask_intersection(grid: Grid) -> Grid | None:
    """Task 0520fde7: combine two masks split by a vertical separator."""
    height = len(grid)
    width = len(grid[0]) if height else 0
    if width < 3 or width % 2 == 0:
        return None

    middle = width // 2
    if any(row[middle] != 5 for row in grid):
        return None

    left_width = middle
    right_start = middle + 1
    if width - right_start != left_width:
        return None

    output = empty_grid(height, left_width)
    for row in range(height):
        for col in range(left_width):
            if grid[row][col] == 1 and grid[row][right_start + col] == 1:
                output[row][col] = 2
    return output


def solve_template_expansion(grid: Grid) -> Grid | None:
    """Task 007bbfb7: copy the input pattern into blocks selected by non-zero cells."""
    height = len(grid)
    width = len(grid[0]) if height else 0
    if height == 0 or width == 0:
        return None

    output = empty_grid(height * height, width * width)
    for block_row in range(height):
        for block_col in range(width):
            if grid[block_row][block_col] == 0:
                continue
            for row in range(height):
                for col in range(width):
                    output[block_row * height + row][block_col * width + col] = grid[row][col]
    return output


def solve_enclosed_zero_fill(grid: Grid) -> Grid | None:
    """Task 00d62c1b: fill zero regions that are fully enclosed by non-zero pixels."""
    height = len(grid)
    width = len(grid[0]) if height else 0
    if height == 0 or width == 0:
        return None

    outside = [[False for _ in range(width)] for _ in range(height)]
    queue: deque[tuple[int, int]] = deque()

    def mark_if_background(row: int, col: int) -> None:
        if grid[row][col] == 0 and not outside[row][col]:
            outside[row][col] = True
            queue.append((row, col))

    for row in range(height):
        mark_if_background(row, 0)
        mark_if_background(row, width - 1)
    for col in range(width):
        mark_if_background(0, col)
        mark_if_background(height - 1, col)

    while queue:
        row, col = queue.popleft()
        for d_row, d_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + d_row
            next_col = col + d_col
            if 0 <= next_row < height and 0 <= next_col < width:
                mark_if_background(next_row, next_col)

    output = copy_grid(grid)
    changed = False
    for row in range(height):
        for col in range(width):
            if grid[row][col] == 0 and not outside[row][col]:
                output[row][col] = 4
                changed = True

    return output if changed else None


SOLVERS = [
    Solver(
        name="mask_intersection",
        description="Two equal masks are separated by color 5; their overlap is marked with color 2.",
        solve=solve_mask_intersection,
    ),
    Solver(
        name="template_expansion",
        description="Every non-zero cell selects a block where the whole input pattern is copied.",
        solve=solve_template_expansion,
    ),
    Solver(
        name="enclosed_zero_fill",
        description="Zero cells unreachable from the border are enclosed regions and are filled with color 4.",
        solve=solve_enclosed_zero_fill,
    ),
]


def solver_matches_task(solver: Solver, task: Task) -> bool:
    for example in task["train"]:
        predicted = solver.solve(example["input"])
        if predicted is None or not grids_equal(predicted, example["output"]):
            return False
    return True


def select_solver(task: Task) -> Solver | None:
    for solver in SOLVERS:
        if solver_matches_task(solver, task):
            return solver
    return None
