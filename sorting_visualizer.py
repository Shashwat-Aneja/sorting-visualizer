import time


def clear_console():
    print("\033[2J\033[H", end="")


def print_array(arr, message="Sorting..."):
    clear_console()
    print(message)
    for value in arr:
        print("#" * value)
    time.sleep(0.2)


def render_step(arr, message, enabled):
    if enabled:
        print_array(arr, message=message)


def bubble_sort(arr, visualize=True):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            render_step(arr, f"Bubble Sort (i={i}, j={j})", visualize)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
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


def main():
    arr = [5, 3, 8, 6, 2, 7, 4, 1]
    algorithms = {
        "1": ("Bubble Sort", bubble_sort),
        "2": ("Insertion Sort", insertion_sort),
        "3": ("Selection Sort", selection_sort),
    }

    print("Sorting Algorithm Visualizer")
    print("Choose an algorithm:")
    for key, (name, _) in algorithms.items():
        print(f"{key}. {name}")

    choice = input("Enter choice: ")
    if choice not in algorithms:
        print("Invalid choice. Please run the program again and select 1, 2, or 3.")
        return

    algo_name, algo_func = algorithms[choice]
    print(f"\nRunning {algo_name}...")
    time.sleep(1)

    sorted_arr = algo_func(arr.copy())

    clear_console()
    print(f"{algo_name} Completed 🎉")
    print("Final Array:")
    print(sorted_arr)


if __name__ == "__main__":
    main()
