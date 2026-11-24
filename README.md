# Sorting Algorithm Visualizer (CLI)
A simple and interactive Python program that visualizes sorting algorithms directly in the terminal using step-by-step animation.

This project demonstrates core algorithmic thinking, clean Python coding, and basic visualization without external libraries.

---

## 📊 Supported Algorithms
- Bubble Sort
- Insertion Sort
- Selection Sort

(QuickSort & MergeSort can be added later)

---

## ▶ How It Works
Numbers are displayed as bars (`#` symbols). As the sorting algorithm progresses, the bars rearrange in each step, making sorting easy to understand. Bubble Sort stops early when a full pass makes no swaps, so already-sorted inputs do not perform unnecessary passes.

Example:
```
### ###### ##### ### >> ### ##### ###### ###
```

---

## 🚀 Usage

### 1. Clone repo
```bash
git clone https://github.com/<your-username>/sorting-visualizer
cd sorting-visualizer
```

### 2. Run
```bash
python sorting_visualizer.py
```

Sort your own comma-separated values:

```bash
python sorting_visualizer.py --values 9,3,7,1
```

Skip the animation when you only need the sorted result:

```bash
python sorting_visualizer.py --values 9,3,7,1 --no-visualization
```

---

## 🔧 Requirements
- Python 3.7+
- No external libraries needed

---

## 📎 File Structure
```
sorting-visualizer/
│
├── sorting_visualizer.py
├── tests/
│   └── test_sorting_visualizer.py
└── README.md
```

---

## 🎯 Future Enhancements
- Add QuickSort and MergeSort
- Add time complexity comparison
- Optional graphical version (matplotlib)

---

## 🧠 Educational Use
This project is great for:
- Students learning sorting algorithms
- Demonstrating algorithm logic
- Technical interviews practice

---

Built by **Shashwat Aneja**


## Run tests

Install pytest, then run the test suite from the repository root:

```bash
python -m pip install pytest
python -m pytest -q
```

The tests cover all three algorithms, empty and single-item lists, duplicate values, and Bubble Sort's early-exit behavior.


Use `--delay 0.05` to control animation speed (0–10 seconds per frame). The choice is scoped to the run; `--no-visualization` continues to skip all animation delays.

`--algorithm quick --json` emits only a JSON object with the selected algorithm and sorted values. JSON mode never prompts, clears the terminal or sleeps.

`--descending` runs the chosen algorithm highest-to-lowest, including its intermediate animation. The programmatic sort functions accept `reverse=True` and still mutate and return the same list.

Heap sort is available as menu option 6 or `--algorithm heap`. It supports animation, JSON output and descending comparisons, with O(n log n) work and constant auxiliary storage.

`--values-file values.txt` reads comma- or whitespace-separated integers from UTF-8 text, avoiding command-line length limits. It is mutually exclusive with `--values` and supports every algorithm and output mode. The file is read without modification.

Shell sort is available as interactive option 7 or `--algorithm shell`, including JSON and descending workflows. It uses gapped insertion with halving gaps, sorts the original list in place, and does not promise stable ordering of equal records.

`--algorithm heap --values-file values.txt --output sorted.json` atomically saves sorted JSON and prints the same JSON without animation. An input file or its hard-link alias cannot be used as output. Failed replacement preserves prior output and removes temporary files.
