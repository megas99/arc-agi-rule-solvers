import json
from pathlib import Path
from typing import Any

Grid = list[list[int]]
Task = dict[str, list[dict[str, Grid]]]


def load_task(path: Path) -> Task:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def grid_shape(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0]) if grid else 0


def empty_grid(height: int, width: int, value: int = 0) -> Grid:
    return [[value for _ in range(width)] for _ in range(height)]


def copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]


def grid_to_text(grid: Grid) -> str:
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def grids_equal(left: Grid, right: Grid) -> bool:
    return left == right


def has_expected_output(example: dict[str, Any]) -> bool:
    return "output" in example
