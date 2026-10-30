# CityNet Optimizer
### Smart City Network & Resource Planner

**Author:** Aditya Mangalam  
**UID:** 26MCC20078  
**University:** Chandigarh University  
**Subject:** Design and Analysis of Algorithms (DAA)  
**Subject Code:** 26CAP-612  
**Academic Year:** 2026–2027  
**Project Guide:** Mr. Rajan Saluja

---

## Overview

CityNet Optimizer is a Python desktop application that demonstrates how classical algorithms can solve practical smart-city planning problems. It models ten cities across Punjab and Chandigarh as a weighted graph and provides visual demonstrations of routing, network design, relief-resource allocation, message compression, and sorting performance.

The application uses **Python and Tkinter** to provide an interactive graphical interface.

## Features

- **Emergency Route Planner:** Uses Dijkstra's algorithm to find the shortest route between two cities.
- **Fibre Network Planner:** Uses Kruskal's and Prim's algorithms to construct a minimum spanning tree.
- **Relief Loading:** Uses Fractional Knapsack to maximise the value of relief goods within a truck's capacity.
- **Message Compressor:** Uses Huffman Coding to compress emergency messages.
- **Sorting Benchmark:** Compares Bubble Sort, Merge Sort, and Quick Sort.
- **Algorithm Visualisation:** Displays the network, routes, spanning trees, and step-by-step results.

## Algorithms and Time Complexity

| Algorithm | Application | Time Complexity |
|---|---|---|
| Dijkstra's Algorithm | Shortest route | `O((V + E) log V)` |
| Kruskal's Algorithm | Minimum spanning tree | `O(E log E)` |
| Prim's Algorithm | Minimum spanning tree | `O(E log V)` |
| Fractional Knapsack | Resource allocation | `O(n log n)` |
| Huffman Coding | Message compression | `O(n log n)` |
| Merge Sort | Sorting benchmark | `O(n log n)` |
| Quick Sort | Sorting benchmark | `O(n log n)` average |
| Bubble Sort | Sorting benchmark | `O(n²)` |

Here, `V` is the number of vertices, `E` is the number of edges, and `n` is the input size.

## Technology Stack

- **Programming Language:** Python 3.8 or higher
- **GUI Framework:** Tkinter and ttk
- **Libraries:** `heapq`, `random`, `time`
- **IDE:** Python IDLE or Visual Studio Code
- **Operating Systems:** Windows, Linux, and macOS with compatible Python/Tk support

The project uses Python standard-library modules; no third-party packages are listed as required in the project report.

## Installation and Execution

### Prerequisites

Install Python 3.8 or higher and ensure that Tkinter is available.

### Run the application

1. Place `citynet.py` in your project folder.
2. Open a terminal in that folder.
3. Execute:

```bash
python citynet.py
```

Alternatively, open `citynet.py` in Python IDLE and press **F5**.

## How to Use

1. Launch the application.
2. Select a module from the navigation menu.
3. Enter the required inputs or select the desired options.
4. Run the algorithm.
5. Observe the visualisation, step-by-step log, and final result.

## Sample Results

The project report records the following results:

- **Ludhiana to Amritsar:** 142 km via Jalandhar.
- **Bathinda to Chandigarh:** 155 km via Patiala.
- **Minimum spanning tree:** 564 km using both Kruskal's and Prim's algorithms.
- **Fractional Knapsack:** Maximum reported priority value of 890 for a 120 kg truck.
- **Huffman Coding:** Message compressed from 168 bits to 79 bits.
- **Sorting Benchmark:** Compares the measured performance of Bubble Sort, Merge Sort, and Quick Sort.

*Note: The road distances are approximate demonstration values, not official real-time distances.*

## Project Structure

```text
CityNet-Optimizer/
├── citynet.py
└── README.md
```

## Testing

The project report describes the following validation checks:

- Verify shortest-route results for the selected city pairs.
- Confirm that Kruskal's and Prim's algorithms produce the same minimum spanning tree cost.
- Validate the Fractional Knapsack result for a capacity of 120 kg.
- Check that Huffman decoding reproduces the original message.
- Compare sorting results with Python's built-in `sorted()` function.

## Future Enhancements

- Integrate real-time maps and road distances.
- Allow users to add cities and roads dynamically.
- Implement Floyd–Warshall for all-pairs shortest paths.
- Add delivery-tour optimisation and graph-colouring problems.
- Improve visualisation and testing capabilities.

## References

1. Anany Levitin, *Introduction to the Design and Analysis of Algorithms*, 3rd Edition.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th Edition.
3. Ellis Horowitz, Sartaj Sahni, and Sanguthevar Rajasekaran, *Fundamentals of Computer Algorithms*, 2nd Edition.
4. [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
5. [Python heapq Documentation](https://docs.python.org/3/library/heapq.html)

---

**Developed by Aditya Mangalam**  
**UID:** 26MCC20078  
**Chandigarh University**
