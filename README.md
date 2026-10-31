# CityNet Optimizer - Smart City Network & Resource Planner
Mini Project : Design and Analysis of Algorithms (DAA)
## Author
# Name: Aditya Mangalam
# UID: 26MCC20078
# Chandigarh University
# Assigned By: Rajan Saluja (E15748)
## Project structure
```
CityNet_Optimizer/
├── citynet.py          Desktop app (Python + Tkinter)
├── Open_Web_Version.bat  Double-click: opens the web version in Chrome (Windows)
├── open_web.sh         Same for Mac / Linux
├── README.md
└── web/                Web app (HTML + CSS + JavaScript)
    ├── index.html      Page layout
    ├── style.css       Styling (dark/light theme, responsive)
    ├── algorithms.js   All algorithms (Dijkstra, Kruskal, Prim, Knapsack, Huffman, sorts)
    └── app.js          User interface and animations
```

## How to run
* **`python citynet.py`** opens the project **directly in Google Chrome** (no Tkinter window).
  If Chrome is not installed it uses your default browser.
* Or just double-click **`Open_Web_Version.bat`** (Windows) / run `sh open_web.sh` (Mac / Linux).
* Optional: `python citynet.py --desktop` shows the old Tkinter desktop window.
* Keep the `web` folder next to `citynet.py`. No internet or server is needed.

## Algorithms (syllabus mapping)
| Module              | Algorithm                  | Unit   | Complexity        |
|---------------------|----------------------------|--------|-------------------|
| Emergency Route     | Dijkstra                   | Unit 2 | O((V+E) log V)    |
| Fibre Network       | Kruskal and Prim (MST)     | Unit 2 | O(E log V)        |
| Relief Loading      | Fractional Knapsack        | Unit 2 | O(n log n)        |
| Message Compressor  | Huffman coding             | Unit 2 | O(n log n)        |
| Sorting Benchmark   | Bubble / Merge / Quick     | Unit 1 | O(n²) / O(n log n)|

## What is new in this version
* **Huffman module:** the letters are now listed in **ascending order of their frequency**
  (ties are broken alphabetically) in the log, the frequency bar chart and the code table.
  Space is shown as the symbol `␣` (web) or `_` (desktop).
* **New web interface:** sidebar navigation, light/dark theme, animation speed slider,
  step log, responsive layout for small screens.
* **Dijkstra:** click cities on the map to choose start/destination, swap button, moving ambulance.
* **Knapsack:** live capacity slider with animated truck loading.
* **Huffman:** sample messages, Enter key to compress, frequency bar chart, bit-stream and decode check.
* **Benchmark:** larger input sizes and a clean line chart.
