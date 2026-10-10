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
