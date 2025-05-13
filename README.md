# Maze Escape – Save the Scientist

## Introduction
A scientist is trapped inside a high-tech research facility after an AI system locks down the building due to a security breach. The facility is a complex maze filled with blocked paths, trap zones, and high-security doors. Your mission: guide the scientist safely to an exit using the A* Search Algorithm.

## Features
- **15x15 Grid-Based Maze:** Each cell can be empty, a wall, a trap zone (with random cost), an exit, or a lock (dead-end).
- **A* Search Algorithm:** Finds the optimal path using Manhattan distance as the heuristic.
- **Dynamic Maze:** After each escape, the maze changes (walls, traps, locks), and new start/exit points are assigned.
- **Step-by-Step Simulation:** The scientist follows the computed path, with real-time visualization using Pygame.
- **Dynamic Replanning:** If the maze changes mid-path, the algorithm replans from the current position.
- **Performance Evaluation:** For each escape, the program reports the optimal path, total steps, total cost, time complexity, and space complexity.

## Problem Description
- The maze is a 15x15 grid.
- **Cell Types:**
  - **Empty:** Free space, cost = 1.
  - **Wall:** Impassable.
  - **Trap Zone:** Increases movement cost (randomly 10–20).
  - **Exit:** Goal state.
  - **Lock:** Dead-end; once entered, it locks permanently.
- The scientist can move up, down, left, or right (no diagonals).
- The A* algorithm uses Manhattan distance as the heuristic.
- After each successful escape, the maze is modified and the process repeats for a total of 3 trials.

## How It Works
1. **Maze Generation:** Randomly generates walls, traps, locks, start, and exit positions.
2. **Path Planning:** Uses A* to find the optimal path from the scientist to the exit.
3. **Simulation:** The scientist moves step-by-step along the path. If the maze changes, the path is replanned.
4. **Performance Reporting:** After each trial, the program displays the path, steps, cost, and complexity analysis.

## Requirements
- Python 3.x
- Pygame
- Numpy

Install dependencies with:
```powershell
pip install pygame numpy
```

## Running the Simulation
Run the main script:
```powershell
python Q1.py
```
A Pygame window will open, visualizing the maze and the scientist's escape. After each trial, press any key to proceed.

## Project Structure
- `Q1.py` – Main source code containing maze generation, A* algorithm, simulation, and visualization.

## Performance Evaluation
For each escape, the following are reported:
- **Optimal Path**
- **Total Steps**
- **Total Cost**
- **Time Complexity:** O(E log V)
- **Space Complexity:** O(V)

## License
This project is for educational purposes.
