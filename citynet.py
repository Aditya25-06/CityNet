"""
CityNet Optimizer  -  Smart City Network & Resource Planner
Mini Project : Design and Analysis of Algorithms (DAA)

Algorithms used (from the syllabus)
  1. Dijkstra's Algorithm      (Unit 2 - Shortest paths)        -> Emergency route finder
  2. Kruskal's Algorithm       (Unit 2 - Minimum cost spanning)  -> Optical-fibre network
  3. Prim's Algorithm          (Unit 2 - Minimum cost spanning)  -> Optical-fibre network
  4. Fractional Knapsack       (Unit 2 - Greedy method)          -> Relief-truck loading
  5. Huffman Coding            (Unit 2 - Optimal tree problem)   -> Emergency message compressor
  6. Merge / Quick / Bubble sort (Unit 1 - Sorting)              -> Sorting benchmark

Run :  python citynet.py        (only the Python standard library is needed)
"""
import heapq
import random
import time
import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------------------
#  DATA  (Punjab road network - distances are approximate, in km)
# ----------------------------------------------------------------------------
CITIES = {            # name : (x, y, population in lakh - approximate)
    "Amritsar":   (110, 80, 11.3),
    "Jalandhar":  (225, 165, 8.7),
    "Hoshiarpur": (345, 135, 1.7),
    "Chandigarh": (500, 105, 10.6),
    "Ferozepur":  (90, 290, 1.1),
    "Moga":       (205, 300, 1.6),
    "Ludhiana":   (330, 265, 16.2),
    "Patiala":    (490, 295, 4.5),
    "Sangrur":    (385, 385, 0.9),
    "Bathinda":   (210, 435, 2.9),
}
ROADS = [
    ("Amritsar", "Jalandhar", 80), ("Amritsar", "Ferozepur", 115),
    ("Jalandhar", "Hoshiarpur", 40), ("Jalandhar", "Ludhiana", 62),
    ("Jalandhar", "Moga", 85), ("Hoshiarpur", "Chandigarh", 100),
    ("Ludhiana", "Chandigarh", 100), ("Ludhiana", "Moga", 62),
    ("Ludhiana", "Patiala", 110), ("Ludhiana", "Sangrur", 80),
    ("Moga", "Ferozepur", 45), ("Moga", "Bathinda", 80),
    ("Patiala", "Chandigarh", 65), ("Patiala", "Sangrur", 50),
    ("Sangrur", "Bathinda", 90), ("Patiala", "Bathinda", 90),
    ("Ferozepur", "Bathinda", 120),
]
RELIEF_ITEMS = [      # name, weight (kg), priority value
    ("Medicines", 10, 300), ("Food packets", 40, 280), ("Tents", 60, 240),
    ("Blankets", 30, 150), ("Water cans", 50, 100), ("Generators", 80, 320),
]

# colour palette
BG, PANEL, CARD = "#0b1220", "#111a2e", "#16223b"
TXT, MUTED = "#e5edf9", "#8da2c0"
BLUE, GREEN, AMBER, RED, PURPLE, CYAN = ("#38bdf8", "#22c55e", "#f59e0b",
                                         "#ef4444", "#a78bfa", "#22d3ee")


# ----------------------------------------------------------------------------
#  ALGORITHMS
# ----------------------------------------------------------------------------
def build_graph():
    g = {c: [] for c in CITIES}
    for a, b, w in ROADS:
        g[a].append((b, w))
        g[b].append((a, w))
    return g


def dijkstra(graph, src, dst):
    """Greedy single-source shortest path with a min-heap.  O((V+E) log V)"""
    dist = {v: float("inf") for v in graph}
    prev, dist[src] = {}, 0
    pq, order = [(0, src)], []
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        order.append((u, d))
        if u == dst:
            break
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v], prev[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    path, node = [], dst
    while node != src and node in prev:
        path.append(node)
        node = prev[node]
    path.append(src)
    return dist[dst], path[::-1], order


class DisjointSet:
    def __init__(self, items):
        self.p = {i: i for i in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]        # path compression
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.p[ra] = rb
        return True


def kruskal(nodes, edges):
    """Sort edges, add the cheapest that does not form a cycle.  O(E log E)"""
    ds, steps, total = DisjointSet(nodes), [], 0
    for a, b, w in sorted(edges, key=lambda e: e[2]):
        ok = ds.union(a, b)
        total += w if ok else 0
        steps.append((a, b, w, ok))
    return total, steps


def prim(graph, start):
    """Grow a tree from `start`, always adding the cheapest crossing edge."""
    seen, steps, total = {start}, [], 0
    pq = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(pq)
    while pq and len(seen) < len(graph):
        w, u, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        total += w
        steps.append((u, v, w, True))
        for x, wx in graph[v]:
            if x not in seen:
                heapq.heappush(pq, (wx, v, x))
    return total, steps


def fractional_knapsack(items, capacity):
    """Greedy: take items in decreasing value/weight ratio.  O(n log n)"""
    ranked = sorted(items, key=lambda i: i[2] / i[1], reverse=True)
    left, value, plan = capacity, 0.0, []
    for name, wt, val in ranked:
        if left <= 0:
            plan.append((name, wt, val, 0.0))
            continue
        take = min(wt, left)
        frac = take / wt
        plan.append((name, wt, val, frac))
        value += val * frac
        left -= take
    return value, plan


def bubble_sort(a):
    a = a[:]
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def merge_sort(a, key=lambda x: x):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left, right = merge_sort(a[:mid], key), merge_sort(a[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]


def quick_sort(a):
    if len(a) <= 1:
        return a[:]
    pivot = a[len(a) // 2]
    return (quick_sort([x for x in a if x < pivot]) +
            [x for x in a if x == pivot] +
            quick_sort([x for x in a if x > pivot]))


class HNode:
    def __init__(self, freq, ch=None, left=None, right=None):
        self.freq, self.ch, self.left, self.right = freq, ch, left, right

    def __lt__(self, other):
        return self.freq < other.freq


def huffman(text):
    """Greedy: repeatedly merge the two least frequent nodes.  O(n log n)"""
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    heap = [HNode(f, ch) for ch, f in freq.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        heap = [HNode(heap[0].freq, None, heap[0], None)]
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, HNode(a.freq + b.freq, None, a, b))
    root, codes = heap[0], {}

    def walk(n, code):
        if n.ch is not None:
            codes[n.ch] = code or "0"
            return
        if n.left:
            walk(n.left, code + "0")
        if n.right:
            walk(n.right, code + "1")
    walk(root, "")
    return root, codes, freq


# ----------------------------------------------------------------------------
#  GUI
# ----------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CityNet Optimizer - Smart City Network & Resource Planner")
        self.geometry("1180x700")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.graph = build_graph()
        self.after_ids = []
        self.style_setup()
        self.build_layout()
        self.show_dijkstra()

    # ---------- layout ----------
    def style_setup(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TCombobox", fieldbackground=CARD, background=CARD,
                    foreground=TXT, arrowcolor=TXT)
        s.map("TCombobox", fieldbackground=[("readonly", CARD)],
              foreground=[("readonly", TXT)], background=[("readonly", CARD)],
              selectbackground=[("readonly", CARD)], selectforeground=[("readonly", TXT)])
        s.configure("Treeview", background=CARD, fieldbackground=CARD,
                    foreground=TXT, rowheight=24, borderwidth=0)
        s.configure("Treeview.Heading", background=PANEL, foreground=BLUE)
        self.option_add("*TCombobox*Listbox.background", CARD)
        self.option_add("*TCombobox*Listbox.foreground", TXT)

    def build_layout(self):
        head = tk.Frame(self, bg=PANEL, height=64)
        head.pack(fill="x")
        tk.Label(head, text="\u25C6 CityNet Optimizer", bg=PANEL, fg=BLUE,
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(head, text="Smart City Network & Resource Planner  |  DAA Mini Project",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).pack(side="left")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        nav = tk.Frame(body, bg=PANEL, width=200)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        tk.Label(nav, text="MODULES", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=16, pady=(16, 6))
        self.nav_buttons = []
        for text, cmd in [("1  Emergency Route", self.show_dijkstra),
                          ("2  Fibre Network", self.show_mst),
                          ("3  Relief Loading", self.show_knapsack),
                          ("4  Msg Compressor", self.show_huffman),
                          ("5  Sorting Benchmark", self.show_benchmark)]:
            b = tk.Button(nav, text=text, anchor="w", bg=PANEL, fg=TXT, bd=0,
                          activebackground=CARD, activeforeground=BLUE,
                          font=("Segoe UI", 11), padx=16, pady=10, cursor="hand2",
                          command=cmd)
            b.pack(fill="x")
            self.nav_buttons.append((text, b))

        center = tk.Frame(body, bg=BG)
        center.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(center, width=640, height=500, bg=CARD,
                                highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(center, text="", bg=BG, fg=AMBER,
                               font=("Segoe UI", 12, "bold"))
        self.status.pack(pady=6)

        right = tk.Frame(body, bg=PANEL, width=310)
        right.pack(side="left", fill="y")
        right.pack_propagate(False)
        self.title_lbl = tk.Label(right, text="", bg=PANEL, fg=TXT,
                                  font=("Segoe UI", 14, "bold"), wraplength=280,
                                  justify="left")
        self.title_lbl.pack(anchor="w", padx=14, pady=(14, 0))
        self.algo_lbl = tk.Label(right, text="", bg=PANEL, fg=PURPLE,
                                 font=("Segoe UI", 9), wraplength=280, justify="left")
        self.algo_lbl.pack(anchor="w", padx=14, pady=(0, 8))
        self.controls = tk.Frame(right, bg=PANEL)
        self.controls.pack(fill="x", padx=14)
        self.log = tk.Text(right, bg=CARD, fg=TXT, bd=0, font=("Consolas", 9),
                           wrap="word", height=20)
        self.log.pack(fill="both", expand=True, padx=14, pady=12)
        for tag, col in [("g", GREEN), ("a", AMBER), ("r", RED), ("b", BLUE), ("m", MUTED)]:
            self.log.tag_config(tag, foreground=col)

    # ---------- helpers ----------
    def reset(self, title, algo, nav_index):
        for aid in self.after_ids:
            self.after_cancel(aid)
        self.after_ids = []
        self.canvas.delete("all")
        self.status.config(text="")
        for w in self.controls.winfo_children():
            w.destroy()
        self.log.delete("1.0", "end")
        self.title_lbl.config(text=title)
        self.algo_lbl.config(text=algo)
        for i, (_, b) in enumerate(self.nav_buttons):
            b.config(bg=CARD if i == nav_index else PANEL,
                     fg=BLUE if i == nav_index else TXT)

    def say(self, text, tag=None):
        self.log.insert("end", text + "\n", tag)
        self.log.see("end")

    def button(self, text, cmd, color=BLUE):
        tk.Button(self.controls, text=text, command=cmd, bg=color, fg="#06101f",
                  bd=0, font=("Segoe UI", 10, "bold"), padx=10, pady=6,
                  cursor="hand2").pack(fill="x", pady=4)

    def combo(self, label, values, default):
        tk.Label(self.controls, text=label, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w")
        var = tk.StringVar(value=default)
        ttk.Combobox(self.controls, textvariable=var, values=values,
                     state="readonly").pack(fill="x", pady=(0, 6))
        return var

    def later(self, ms, fn):
        self.after_ids.append(self.after(ms, fn))

    # ---------- map drawing ----------
    def draw_map(self, hi_edges=None, rej_edges=None, hi_nodes=None, col=GREEN):
        c = self.canvas
        c.delete("all")
        hi_edges = {frozenset(e) for e in (hi_edges or [])}
        rej_edges = {frozenset(e) for e in (rej_edges or [])}
        for a, b, w in ROADS:
            x1, y1, _ = CITIES[a]
            x2, y2, _ = CITIES[b]
            k = frozenset((a, b))
            if k in hi_edges:
                c.create_line(x1, y1, x2, y2, fill=col, width=5)
            elif k in rej_edges:
                c.create_line(x1, y1, x2, y2, fill=RED, width=2, dash=(4, 4))
            else:
                c.create_line(x1, y1, x2, y2, fill="#2b3b5e", width=2)
            c.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 8, text=str(w),
                          fill=MUTED, font=("Segoe UI", 8))
        for n, (x, y, _) in CITIES.items():
            lit = hi_nodes and n in hi_nodes
            c.create_oval(x - 11, y - 11, x + 11, y + 11,
                          fill=col if lit else BLUE, outline="white", width=2)
            c.create_text(x, y + 25, text=n, fill=TXT, font=("Segoe UI", 10, "bold"))

    # ---------- module 1 : Dijkstra ----------
    def show_dijkstra(self):
        self.reset("Emergency Route Finder",
                   "Algorithm: Dijkstra's shortest path (Greedy, min-heap)  |  O((V+E) log V)", 0)
        names = sorted(CITIES)
        self.src = self.combo("Ambulance start city", names, "Ludhiana")
        self.dst = self.combo("Hospital / destination city", names, "Amritsar")
        self.button("\u25B6  Find shortest route", self.run_dijkstra, GREEN)
        self.draw_map()
        self.say("Pick two cities and press the button.\nEdge numbers = road distance in km.", "m")

    def run_dijkstra(self):
        s, d = self.src.get(), self.dst.get()
        self.log.delete("1.0", "end")
        if s == d:
            self.say("Source and destination are the same.", "r")
            return
        dist, path, order = dijkstra(self.graph, s, d)
        self.say("Cities settled by Dijkstra (nearest first):", "b")
        for u, du in order:
            self.say(f"  {u:<11}  {du} km")
        edges = list(zip(path, path[1:]))

        def step(i):
            self.draw_map(edges[:i], hi_nodes=path[:i + 1], col=GREEN)
            if i == len(edges):
                self.status.config(text=f"Shortest distance: {dist} km")
                self.say("\nBest route:", "g")
                self.say("  " + " -> ".join(path), "g")
                self.say(f"Total = {dist} km", "a")
            else:
                self.later(450, lambda: step(i + 1))
        step(0)

    # ---------- module 2 : MST ----------
    def show_mst(self):
        self.reset("Optical-Fibre Network Planner",
                   "Algorithms: Kruskal's (edge-based, union-find) and Prim's (vertex-based, min-heap)  |  O(E log V)", 1)
        self.mst_algo = self.combo("Choose algorithm", ["Kruskal", "Prim"], "Kruskal")
        self.button("\u25B6  Build cheapest network", self.run_mst, GREEN)
        self.draw_map()
        self.say("Goal: connect ALL cities with minimum total cable length.\n"
                 "Green = cable laid, red dashed = rejected (would form a cycle).", "m")

    def run_mst(self):
        self.log.delete("1.0", "end")
        algo = self.mst_algo.get()
        if algo == "Kruskal":
            total, steps = kruskal(list(CITIES), ROADS)
        else:
            total, steps = prim(self.graph, "Ludhiana")
        full = sum(w for _, _, w in ROADS)
        self.say(f"{algo}'s algorithm - step log", "b")
        chosen, rejected = [], []

        def step(i):
            self.draw_map(chosen, rejected, hi_nodes={n for e in chosen for n in e})
            if i == len(steps):
                self.status.config(text=f"Minimum cable = {total} km")
                self.say(f"\nMST cost : {total} km", "g")
                self.say(f"All roads: {full} km", "m")
                self.say(f"Saved    : {full - total} km ({100 * (full - total) / full:.0f}%)", "a")
                return
            a, b, w, ok = steps[i]
            (chosen if ok else rejected).append((a, b))
            self.say(f"{'ADD   ' if ok else 'SKIP  '}{a}-{b} ({w} km)", "g" if ok else "r")
            self.draw_map(chosen, rejected, hi_nodes={n for e in chosen for n in e})
            self.later(380, lambda: step(i + 1))
        step(0)

    # ---------- module 3 : knapsack ----------
    def show_knapsack(self):
        self.reset("Relief-Truck Loading",
                   "Algorithm: Fractional Knapsack (Greedy, sort by value/weight)  |  O(n log n)", 2)
        tk.Label(self.controls, text="Truck capacity (kg)", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.cap = tk.StringVar(value="120")
        tk.Entry(self.controls, textvariable=self.cap, bg=CARD, fg=TXT, bd=0,
                 insertbackground=TXT, font=("Segoe UI", 12)).pack(fill="x", pady=(0, 6), ipady=4)
        self.button("\u25B6  Load the truck", self.run_knapsack, GREEN)
        self.say("Items (weight kg / priority value):", "b")
        for n, w, v in RELIEF_ITEMS:
            self.say(f"  {n:<13}{w:>3} kg   {v}", "m")
        self.canvas.create_text(320, 250, text="Enter capacity and load the truck",
                                fill=MUTED, font=("Segoe UI", 14))

    def run_knapsack(self):
        try:
            cap = float(self.cap.get())
            assert cap > 0
        except Exception:
            self.status.config(text="Enter a positive number")
            return
        value, plan = fractional_knapsack(RELIEF_ITEMS, cap)
        self.log.delete("1.0", "end")
        self.say("Ranked by value / weight:", "b")
        c = self.canvas
        c.delete("all")
        c.create_text(320, 30, text=f"Truck capacity: {cap:g} kg", fill=TXT,
                      font=("Segoe UI", 14, "bold"))
        palette = [GREEN, BLUE, AMBER, PURPLE, CYAN, "#f472b6"]
        x0, x1, y = 30, 610, 90
        scale = (x1 - x0) / max(cap, 1)
        x, used = x0, 0
        c.create_rectangle(x0, y, x1, y + 50, outline=MUTED, width=2)
        for i, (n, wt, val, frac) in enumerate(plan):
            taken = wt * frac
            ratio = val / wt
            tag = "g" if frac == 1 else ("a" if frac > 0 else "r")
            self.say(f"{n:<13}r={ratio:4.2f}  take {frac * 100:3.0f}%", tag)
            if taken > 0:
                w = taken * scale
                c.create_rectangle(x, y, x + w, y + 50, fill=palette[i % 6], outline=BG)
                if w > 38:
                    c.create_text(x + w / 2, y + 25, text=f"{taken:g}",
                                  fill="#06101f", font=("Segoe UI", 10, "bold"))
                x += w
                used += taken
        c.create_text(320, 165, text=f"Loaded {used:g} / {cap:g} kg", fill=MUTED,
                      font=("Segoe UI", 11))
        # table
        c.create_text(30, 210, text="Item", fill=BLUE, anchor="w", font=("Segoe UI", 10, "bold"))
        c.create_text(240, 210, text="Value/Weight", fill=BLUE, anchor="w", font=("Segoe UI", 10, "bold"))
        c.create_text(380, 210, text="Fraction taken", fill=BLUE, anchor="w", font=("Segoe UI", 10, "bold"))
        c.create_text(520, 210, text="Value", fill=BLUE, anchor="w", font=("Segoe UI", 10, "bold"))
        for i, (n, wt, val, frac) in enumerate(plan):
            yy = 240 + i * 36
            c.create_rectangle(10, yy - 2, 22, yy + 10, fill=palette[i % 6], outline="")
            c.create_text(32, yy + 4, text=n, fill=TXT, anchor="w", font=("Segoe UI", 11))
            c.create_text(240, yy + 4, text=f"{val / wt:.2f}", fill=TXT, anchor="w", font=("Segoe UI", 11))
            c.create_text(380, yy + 4, text=f"{frac * 100:.0f}%", fill=GREEN if frac == 1 else (AMBER if frac else RED),
                          anchor="w", font=("Segoe UI", 11, "bold"))
            c.create_text(520, yy + 4, text=f"{val * frac:.1f}", fill=TXT, anchor="w", font=("Segoe UI", 11))
        self.status.config(text=f"Maximum total priority value = {value:.1f}")
        self.say(f"\nTotal value = {value:.1f}", "a")

    # ---------- module 4 : Huffman ----------
    def show_huffman(self):
        self.reset("Emergency Message Compressor",
                   "Algorithm: Huffman coding (Greedy optimal tree, min-heap)  |  O(n log n)", 3)
        tk.Label(self.controls, text="Broadcast message", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w")
        self.msg = tk.StringVar(value="SEND HELP TO AMRITSAR")
        tk.Entry(self.controls, textvariable=self.msg, bg=CARD, fg=TXT, bd=0,
                 insertbackground=TXT, font=("Segoe UI", 12)).pack(fill="x", pady=(0, 6), ipady=4)
        self.button("\u25B6  Compress with Huffman", self.run_huffman, GREEN)
        self.canvas.create_text(320, 250, text="Type a message and press Compress",
                                fill=MUTED, font=("Segoe UI", 14))
        self.say("Frequent letters get SHORT codes,\nrare letters get LONG codes.\n"
                 "Normal text uses 8 bits per character.", "m")

    def run_huffman(self):
        text = self.msg.get().upper()[:40]
        self.log.delete("1.0", "end")
        if len(text) < 2:
            self.status.config(text="Type at least 2 characters")
            return
        root, codes, freq = huffman(text)
        encoded = "".join(codes[ch] for ch in text)
        inv = {v: k for k, v in codes.items()}          # decode check
        out, buf = "", ""
        for bit in encoded:
            buf += bit
            if buf in inv:
                out, buf = out + inv[buf], ""
        assert out == text
        c = self.canvas
        c.delete("all")
        leaves = []
        def collect(n):
            if n.ch is not None or (n.left is None and n.right is None):
                leaves.append(n)
                return
            for k in (n.left, n.right):
                if k:
                    collect(k)
        collect(root)
        def depth(n):
            return 0 if n is None else 1 + max(depth(n.left), depth(n.right))
        D = depth(root)
        dy = min(62, 400 // max(D - 1, 1))
        step_x = 600 / max(len(leaves), 1)
        pos = {}
        idx = [0]
        def layout(n, d):
            if n.ch is not None or (n.left is None and n.right is None):
                pos[id(n)] = (20 + step_x * (idx[0] + 0.5), 45 + d * dy)
                idx[0] += 1
            else:
                kids = [k for k in (n.left, n.right) if k]
                for k in kids:
                    layout(k, d + 1)
                xs = [pos[id(k)][0] for k in kids]
                pos[id(n)] = (sum(xs) / len(xs), 45 + d * dy)
        layout(root, 0)
        def draw(n):
            x, y = pos[id(n)]
            for bit, k in (("0", n.left), ("1", n.right)):
                if k:
                    kx, ky = pos[id(k)]
                    c.create_line(x, y, kx, ky, fill="#3b4f7a", width=2)
                    c.create_text((x + kx) / 2 + (-8 if bit == "0" else 8), (y + ky) / 2,
                                  text=bit, fill=AMBER, font=("Segoe UI", 9, "bold"))
                    draw(k)
        draw(root)
        def nodes(n):
            yield n
            for k in (n.left, n.right):
                if k:
                    yield from nodes(k)
        for n in nodes(root):
            x, y = pos[id(n)]
            if n.ch is not None:
                label = "_" if n.ch == " " else n.ch
                c.create_rectangle(x - 15, y - 15, x + 15, y + 15, fill=GREEN, outline="white")
                c.create_text(x, y, text=label, fill="#06101f", font=("Segoe UI", 11, "bold"))
                c.create_text(x, y + 26, text=str(n.freq), fill=MUTED, font=("Segoe UI", 8))
            else:
                c.create_oval(x - 14, y - 14, x + 14, y + 14, fill=BLUE, outline="white")
                c.create_text(x, y, text=str(n.freq), fill="#06101f", font=("Segoe UI", 9, "bold"))
        orig, comp = 8 * len(text), len(encoded)
        self.say("Char  Freq  Code", "b")
        for ch, cd in sorted(codes.items(), key=lambda kv: (len(kv[1]), kv[1])):
            self.say(f" {'_' if ch == ' ' else ch:<4}  {freq[ch]:<4}  {cd}", "g")
        self.say(f"\nOriginal   : {orig} bits", "m")
        self.say(f"Compressed : {comp} bits", "a")
        self.say(f"Saved      : {100 * (orig - comp) / orig:.0f}%", "g")
        self.status.config(text=f"{orig} bits  \u2192  {comp} bits   ({100 * (orig - comp) / orig:.0f}% smaller)")

    # ---------- module 5 : benchmark ----------
    def show_benchmark(self):
        self.reset("Sorting Benchmark",
                   "Bubble O(n\u00b2)  vs  Merge O(n log n)  vs  Quick O(n log n) average", 4)
        self.button("\u25B6  Run benchmark", self.run_benchmark, GREEN)
        self.say("Sorts random lists of growing size and\nmeasures real running time.\n\n"
                 "This verifies the asymptotic notations\n(Big-Oh) from Unit 1 experimentally.", "m")
        self.canvas.create_text(320, 250, text="Press 'Run benchmark'", fill=MUTED,
                                font=("Segoe UI", 14))

    def run_benchmark(self):
        sizes = [200, 400, 800, 1200, 1600]
        algos = [("Bubble", bubble_sort, RED), ("Merge", merge_sort, BLUE),
                 ("Quick", quick_sort, GREEN)]
        times = {n: [] for n, _, _ in algos}
        self.log.delete("1.0", "end")
        self.say(f"{'n':>6}{'Bubble':>9}{'Merge':>9}{'Quick':>9}  ", "b")
        for n in sizes:
            data = [random.randint(1, 10 ** 6) for _ in range(n)]
            row = f"{n:>6}"
            for name, fn, _ in algos:
                t = time.perf_counter()
                res = fn(data)
                ms = (time.perf_counter() - t) * 1000
                assert res == sorted(data)
                times[name].append(ms)
                row += f"{ms:>9.1f}"
            self.say(row)
        c = self.canvas
        c.delete("all")
        left, bottom, top, right = 70, 440, 60, 610
        peak = max(max(v) for v in times.values())
        c.create_text(200, 25, text="Running time vs input size (ms)", fill=TXT,
                      font=("Segoe UI", 14, "bold"))
        for k in range(5):
            yy = bottom - k * (bottom - top) / 4
            c.create_line(left, yy, right, yy, fill="#26365a")
            c.create_text(left - 8, yy, text=f"{peak * k / 4:.0f}", fill=MUTED,
                          anchor="e", font=("Segoe UI", 9))
        c.create_text(20, 250, text="ms", fill=MUTED, font=("Segoe UI", 9))
        xs = [left + 20 + i * (right - left - 40) / (len(sizes) - 1) for i in range(len(sizes))]
        for i, n in enumerate(sizes):
            c.create_text(xs[i], bottom + 16, text=str(n), fill=MUTED, font=("Segoe UI", 9))
        c.create_text(340, bottom + 40, text="n  (number of elements)", fill=MUTED, font=("Segoe UI", 9))
        for li, (name, _, col) in enumerate(algos):
            pts = [(xs[i], bottom - times[name][i] / peak * (bottom - top)) for i in range(len(sizes))]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                c.create_line(x1, y1, x2, y2, fill=col, width=3)
            for x, y in pts:
                c.create_oval(x - 4, y - 4, x + 4, y + 4, fill=col, outline="")
            c.create_rectangle(400 + li * 75, 46, 412 + li * 75, 58, fill=col, outline="")
            c.create_text(417 + li * 75, 52, text=name, fill=TXT, anchor="w", font=("Segoe UI", 10))
        self.status.config(text=f"At n = {sizes[-1]}: Bubble is {times['Bubble'][-1] / times['Merge'][-1]:.0f}x slower than Merge")


if __name__ == "__main__":
    App().mainloop()
