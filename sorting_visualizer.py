import time
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_array(arr, message="Sorting..."):
    clear_console()
    print(message)
    for value in arr:
        print("#" * value)
    time.sleep(0.2)


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            print_array(arr, message=f"Bubble Sort (i={i}, j={j})")
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        print_array(arr, message=f"Insertion Sort (i={i})")
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            print_array(arr)
        arr[j + 1] = key
    return arr


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            print_array(arr, message=f"Selection Sort (i={i}, j={j})")
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
    algo_name, algo_func = algorithms.get(choice, ("Bubble Sort", bubble_sort))

    print(f"\nRunning {algo_name}...")
    time.sleep(1)

    sorted_arr = algo_func(arr.copy())

    clear_console()
    print(f"{algo_name} Completed 🎉")
    print("Final Array:")
    print(sorted_arr)


if __name__ == "__main__":
    main()
