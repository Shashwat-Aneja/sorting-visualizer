import os
import tempfile
import argparse
import re
from pathlib import Path
import sys
import json
import math
from contextvars import ContextVar
import time

MAX_BAR_WIDTH = 40
FRAME_DELAY = ContextVar("frame_delay", default=0.2)
FRAME_BUDGET = ContextVar("frame_budget", default=None)


def animation_delay(raw):
    value = float(raw)
    if not math.isfinite(value) or value < 0 or value > 10:
        raise argparse.ArgumentTypeError("Delay must be a finite number from 0 to 10 seconds")
    return value


def parse_values(raw):
    tokens = raw.split(",")
    if not tokens or any(not token.strip() for token in tokens):
        raise ValueError("provide comma-separated integers without empty values")
    try:
        return [int(token.strip()) for token in tokens]
    except ValueError as exc:
        raise ValueError("values must be comma-separated integers") from exc


def clear_console():
    print("\033[2J\033[H", end="")


def print_array(arr, message="Sorting..."):
    clear_console()
    print(message)
    max_magnitude = max((abs(value) for value in arr), default=0)
    for value in arr:
        magnitude = abs(value)
        width = 0 if max_magnitude == 0 else (magnitude * MAX_BAR_WIDTH) // max_magnitude
        if magnitude and width == 0:
            width = 1
        bar = "#" * width
        print(f"{value:>5} | {bar}")
    time.sleep(FRAME_DELAY.get())


def render_step(arr, message, enabled):
    if enabled:
        remaining = FRAME_BUDGET.get()
        if remaining is not None:
            if remaining <= 0:
                return
            FRAME_BUDGET.set(remaining - 1)
        print_array(arr, message=message)


def _less(left, right, reverse):
    return left > right if reverse else left < right


def shell_sort(arr, visualize=True, reverse=False):
    """Sort in place by gapped insertion using a halving gap sequence."""
    gap = len(arr) // 2
    while gap:
        for index in range(gap, len(arr)):
            value = arr[index]
            current = index
            while current >= gap and _less(value, arr[current - gap], reverse):
                arr[current] = arr[current - gap]
                current -= gap
                render_step(arr, f"Shell Sort (gap={gap})", visualize)
            arr[current] = value
        gap //= 2
    return arr


def bubble_sort(arr, visualize=True, reverse=False):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            render_step(arr, f"Bubble Sort (i={i}, j={j})", visualize)
            if _less(arr[j + 1], arr[j], reverse):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(arr, visualize=True, reverse=False):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        render_step(arr, f"Insertion Sort (i={i})", visualize)
        while j >= 0 and _less(key, arr[j], reverse):
            arr[j + 1] = arr[j]
            j -= 1
            render_step(arr, "Insertion Sort", visualize)
        arr[j + 1] = key
    return arr


def selection_sort(arr, visualize=True, reverse=False):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            render_step(arr, f"Selection Sort (i={i}, j={j})", visualize)
            if _less(arr[j], arr[min_idx], reverse):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(arr, visualize=True, reverse=False):
    """Sort values in place using merge sort and return the same list."""
    def sort(values):
        if len(values) <= 1:
            return values

        middle = len(values) // 2
        left = sort(values[:middle])
        right = sort(values[middle:])
        merged = []
        left_index = right_index = 0

        while left_index < len(left) and right_index < len(right):
            if not _less(right[right_index], left[left_index], reverse):
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1

        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        render_step(merged, "Merge Sort (merge)", visualize)
        return merged

    arr[:] = sort(arr)
    return arr


def quick_sort(arr, visualize=True, reverse=False):
    """Sort in place using iterative three-way quicksort.

    Three-way partitioning handles duplicate-heavy inputs efficiently, while an
    explicit stack avoids Python recursion-depth failures on large inputs.
    """
    if len(arr) < 2:
        return arr

    pending = [(0, len(arr) - 1)]
    while pending:
        low, high = pending.pop()
        while low < high:
            pivot = arr[(low + high) // 2]
            lower, current, upper = low, low, high

            while current <= upper:
                render_step(arr, f"Quick Sort (pivot={pivot})", visualize)
                if _less(arr[current], pivot, reverse):
                    arr[lower], arr[current] = arr[current], arr[lower]
                    lower += 1
                    current += 1
                elif _less(pivot, arr[current], reverse):
                    arr[current], arr[upper] = arr[upper], arr[current]
                    upper -= 1
                else:
                    current += 1

            left = (low, lower - 1)
            right = (upper + 1, high)
            left_size = left[1] - left[0]
            right_size = right[1] - right[0]

            # Process the smaller partition immediately to bound stack growth.
            if left_size < right_size:
                if right[0] < right[1]:
                    pending.append(right)
                low, high = left
            else:
                if left[0] < left[1]:
                    pending.append(left)
                low, high = right

    return arr


def heap_sort(arr, visualize=True, reverse=False):
    """Sort in place with O(n log n) work and constant auxiliary storage."""
    def sift(root, end):
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and _less(arr[child], arr[child + 1], reverse):
                child += 1
            if not _less(arr[root], arr[child], reverse):
                return
            arr[root], arr[child] = arr[child], arr[root]
            render_step(arr, "Heap Sort (sift)", visualize)
            root = child
    for root in range(len(arr) // 2 - 1, -1, -1):
        sift(root, len(arr))
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        render_step(arr, "Heap Sort (extract)", visualize)
        sift(0, end)
    return arr


def export_sorted_json(payload, destination, source=None):
    destination = Path(destination).expanduser().resolve()
    if source is not None:
        source = Path(source).expanduser().resolve()
        if destination == source or (destination.exists() and destination.samefile(source)):
            raise ValueError("Sorted output must differ from the input values file.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, allow_nan=False)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def _main(argv=None):
    parser = argparse.ArgumentParser(description="Visualize sorting algorithms in the terminal")
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--values", type=parse_values, default=[5, 3, 8, 6, 2, 7, 4, 1], help="Comma-separated integers to sort")
    inputs.add_argument("--values-file", help="Read comma- or whitespace-separated integers from a UTF-8 file")
    parser.add_argument("--no-visualization", action="store_true", help="Sort and print the result without animation")
    parser.add_argument(
        "--algorithm",
        choices=("bubble", "insertion", "selection", "merge", "quick", "heap", "shell"),
        help="Run an algorithm directly without prompting (useful for scripts)",
    )
    parser.add_argument("--delay", type=animation_delay, default=0.2, help="Animation frame delay in seconds (0–10)")
    parser.add_argument("--json", action="store_true", help="Print only machine-readable output; requires --algorithm and disables animation")
    parser.add_argument("--descending", action="store_true", help="Sort highest-to-lowest with the selected algorithm")
    parser.add_argument("--output", help="Atomically save sorted JSON; implies unattended JSON mode and requires --algorithm")
    parser.add_argument("--max-frames", type=int, help="Maximum animated frames while allowing the sort to finish; zero disables animation")
    args = parser.parse_args(argv)
    if args.max_frames is not None and args.max_frames < 0:
        parser.error("--max-frames must be non-negative")
    if args.values_file is not None:
        try:
            text = Path(args.values_file).expanduser().read_text(encoding="utf-8").strip()
            args.values = parse_values(",".join(re.split(r"[,\s]+", text)))
        except (OSError, ValueError) as exc:
            parser.error(f"Could not read integer input: {exc}")
    if args.json or args.output:
        if args.algorithm is None:
            parser.error("--json requires --algorithm")
        functions = {"bubble": bubble_sort, "insertion": insertion_sort, "selection": selection_sort, "merge": merge_sort, "quick": quick_sort, "heap": heap_sort, "shell": shell_sort}
        result = functions[args.algorithm](args.values.copy(), visualize=False, reverse=args.descending)
        payload = {"algorithm": args.algorithm, "values": result}
        if args.output:
            try:
                export_sorted_json(payload, args.output, args.values_file)
            except (OSError, ValueError) as exc:
                parser.error(str(exc))
        print(json.dumps(payload))
        return 0
    arr = args.values
    algorithms = {
        "1": ("Bubble Sort", bubble_sort),
        "2": ("Insertion Sort", insertion_sort),
        "3": ("Selection Sort", selection_sort),
        "4": ("Merge Sort", merge_sort),
        "5": ("Quick Sort", quick_sort),
        "6": ("Heap Sort", heap_sort),
        "7": ("Shell Sort", shell_sort),
    }

    visualize = not args.no_visualization and args.max_frames != 0
    print("Sorting Algorithm Visualizer")
    if args.algorithm is None:
        print("Choose an algorithm:")
        for key, (name, _) in algorithms.items():
            print(f"{key}. {name}")
        try:
            choice = input("Enter choice: ").strip()
        except EOFError:
            print("No algorithm selected. Use --algorithm for non-interactive runs.")
            return 2
    else:
        choice = {
            "bubble": "1",
            "insertion": "2",
            "selection": "3",
            "merge": "4",
            "quick": "5",
            "heap": "6",
            "shell": "7",
        }[args.algorithm]

    if choice not in algorithms:
        print("Invalid choice. Please run the program again and select 1, 2, 3, 4, 5, 6, or 7.")
        return 2

    algo_name, algo_func = algorithms[choice]
    print(f"\nRunning {algo_name}...")
    if visualize:
        time.sleep(1)

    token = FRAME_DELAY.set(args.delay)
    budget_token = FRAME_BUDGET.set(args.max_frames)
    try:
        sorted_arr = algo_func(arr.copy(), visualize=visualize, reverse=args.descending)
    finally:
        FRAME_DELAY.reset(token)
        FRAME_BUDGET.reset(budget_token)

    if visualize:
        clear_console()
    print(f"{algo_name} Completed 🎉")
    print("Final Array:")
    print(sorted_arr)
    return 0


def main(argv=None):
    try:
        return _main(argv)
    except KeyboardInterrupt:
        print("Sorting interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

