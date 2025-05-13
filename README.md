# 🧪 Maze Escape – Save the Scientist

> Guide a trapped scientist through a dynamic, AI-locked research facility using the A* Search Algorithm.

---

## 🚀 Introduction
A rogue AI has triggered a lockdown in a high-tech facility, trapping a brilliant scientist inside. The building is now a hazardous 15x15 maze with locked doors, deadly traps, and blocked paths.  
Your mission: **use the A* Search Algorithm to navigate and safely guide the scientist to an exit.**

---

## 🎮 Features

- 🔲 **15x15 Grid-Based Maze:**  
  Maze includes walls, traps, locks, start & exit points.

- 🧠 **A* Search Algorithm:**  
  Efficient pathfinding using Manhattan distance as the heuristic.

- ♻️ **Dynamic Maze:**  
  After every successful escape, the maze regenerates with new challenges.

- 👣 **Step-by-Step Simulation:**  
  The scientist moves through the maze with real-time visualization using **Pygame**.

- 🔄 **Dynamic Replanning:**  
  If the maze changes mid-path, A* re-calculates from the current position.

- 📊 **Performance Evaluation:**  
  Tracks the path, steps, cost, and computational complexity after each trial.

---

## 🧩 Maze Design

Each cell in the 15x15 grid can be:
| Cell Type    | Symbol | Description                              | Cost |
|--------------|--------|------------------------------------------|------|
| Empty        | ▢      | Free space                               | 1    |
| Wall         | █      | Impassable                               | ∞    |
| Trap Zone    | ⚠️      | Random movement cost (10–20)             | 10–20 |
| Lock         | 🔒      | Becomes permanently locked after entry   | 1    |
| Exit         | 🚪      | Goal position                            | 1    |

> 🔄 Movement allowed in 4 directions: Up, Down, Left, Right (No diagonals)

---

## 🛠️ How It Works

1. **Maze Generation**  
   Randomly places walls, traps, locks, start, and exit.

2. **Path Planning**  
   Uses A* Search to find the optimal route.

3. **Simulation**  
   Scientist follows the path step-by-step. If the maze changes, the path is recalculated.

4. **Performance Report**  
   After each trial (total 3), key stats are shown:
   - Optimal Path
   - Total Steps
   - Total Cost
   - Time Complexity: `O(E log V)`
   - Space Complexity: `O(V)`

---
## 📦 Screenshots

![image](https://github.com/user-attachments/assets/dbd2005e-715e-4ce6-ad26-28f5259d7c34)


## 📦 Requirements

- Python 3.x  
- [Pygame](https://www.pygame.org/news)  
- [NumPy](https://numpy.org/)

Install dependencies with:

```bash
pip install pygame numpy
