# SwiftNode AI 🚀

A Python pathfinding and graph-search module implementing optimized graph traversal algorithms (A* Search and Breadth-First Search) over `networkx` graphs, incorporating spatial Euclidean heuristics and hazard-aware edge filtering.

---

## ⚡ Features

* **A\* Search Pathfinding**: Uses Euclidean distance heuristics with priority queue optimization for path finding.
* **Hazard Avoidance**: Dynamically ignores edges tagged with dynamic hazards during path generation (`ignore_hazards=False`).
* **Breadth-First Search (BFS)**: Unweighted shortest-path traversal fallback via Python's efficient `collections.deque`.
* **NetworkX Integration**: Native support for `networkx` graph attributes including node positions (`pos`) and edge metadata (`distance`, `hazard`).

---

## 🛠️ Algorithms Implemented

| Algorithm | Heuristic / Criteria | Key Features |
| :--- | :--- | :--- |
| **A\* Search** | Euclidean Distance ($\sqrt{\Delta x^2 + \Delta y^2}$) | Optimal weighted path search, hazard detection & cost calculation |
| **BFS** | Unweighted Traversal | Shortest path discovery based on node depth |

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/devashishdeshmukh205-del/swiftnode-ai.git](https://github.com/devashishdeshmukh205-del/swiftnode-ai.git)
   cd swiftnode-ai
