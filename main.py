from pathlib import Path

from arc_utils import grid_shape, grid_to_text, grids_equal, has_expected_output, load_task
from solvers import select_solver


TASK_DIR = Path("data/selected_tasks")


def run_task(path: Path) -> bool:
    task = load_task(path)
    solver = select_solver(task)

    print("=" * 72)
    print(f"Task: {path.stem}")
    if solver is None:
        print("Selected solver: none")
        return False

    print(f"Selected solver: {solver.name}")
    print(f"Rule: {solver.description}")
    print(f"Train examples matched: {len(task['train'])}/{len(task['train'])}")

    all_tests_ok = True
    for index, example in enumerate(task["test"], start=1):
        prediction = solver.solve(example["input"])
        input_shape = grid_shape(example["input"])
        output_shape = grid_shape(prediction or [])

        print(f"\nTest #{index}")
        print(f"Input shape: {input_shape[0]}x{input_shape[1]}")
        print(grid_to_text(example["input"]))
        print(f"\nPredicted output shape: {output_shape[0]}x{output_shape[1]}")
        print(grid_to_text(prediction or []))

        if has_expected_output(example):
            ok = grids_equal(prediction or [], example["output"])
            all_tests_ok = all_tests_ok and ok
            print(f"\nExpected output available: yes")
            print(f"Match: {'YES' if ok else 'NO'}")
        else:
            print("\nExpected output available: no")

    return all_tests_ok


def main() -> None:
    task_paths = sorted(TASK_DIR.glob("*.json"))
    if not task_paths:
        raise SystemExit(f"No ARC tasks found in {TASK_DIR}")

    results = [run_task(path) for path in task_paths]
    print("=" * 72)
    print(f"Summary: {sum(results)}/{len(results)} tasks passed all available tests.")


if __name__ == "__main__":
    main()
