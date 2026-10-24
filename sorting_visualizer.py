import argparse
import time


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
    for value in arr:
        bar = "#" * abs(value)
        print(f"{value:>5} | {bar}")
    time.sleep(0.2)


def render_step(arr, message, enabled):
    if enabled:
        print_array(arr, message=message)


def bubble_sort(arr, visualize=True):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            render_step(arr, f"Bubble Sort (i={i}, j={j})", visualize)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(arr, visualize=True):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        render_step(arr, f"Insertion Sort (i={i})", visualize)
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            render_step(arr, "Insertion Sort", visualize)
        arr[j + 1] = key
    return arr


def selection_sort(arr, visualize=True):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            render_step(arr, f"Selection Sort (i={i}, j={j})", visualize)
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(arr, visualize=True):
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
            if left[left_index] <= right[right_index]:
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


def quick_sort(arr, visualize=True):
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
                if arr[current] < pivot:
                    arr[lower], arr[current] = arr[current], arr[lower]
                    lower += 1
                    current += 1
                elif arr[current] > pivot:
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


def main(argv=None):
    parser = argparse.ArgumentParser(description="Visualize sorting algorithms in the terminal")
    parser.add_argument("--values", type=parse_values, default=[5, 3, 8, 6, 2, 7, 4, 1], help="Comma-separated integers to sort")
    parser.add_argument("--no-visualization", action="store_true", help="Sort and print the result without animation")
    args = parser.parse_args(argv)
    arr = args.values
    algorithms = {
        "1": ("Bubble Sort", bubble_sort),
        "2": ("Insertion Sort", insertion_sort),
        "3": ("Selection Sort", selection_sort),
        "4": ("Merge Sort", merge_sort),
        "5": ("Quick Sort", quick_sort),
    }

    print("Sorting Algorithm Visualizer")
    print("Choose an algorithm:")
    for key, (name, _) in algorithms.items():
        print(f"{key}. {name}")

    choice = input("Enter choice: ")
    if choice not in algorithms:
        print("Invalid choice. Please run the program again and select 1, 2, 3, 4, or 5.")
        return

    algo_name, algo_func = algorithms[choice]
    print(f"\nRunning {algo_name}...")
    time.sleep(1)

    sorted_arr = algo_func(arr.copy(), visualize=not args.no_visualization)

    clear_console()
    print(f"{algo_name} Completed 🎉")
    print("Final Array:")
    print(sorted_arr)


if __name__ == "__main__":
    main()
