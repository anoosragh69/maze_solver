# Maze Solver using Genetic Algorithm

## Overview

This project demonstrates how a **Genetic Algorithm (GA)** can be used to solve a maze.
A maze is generated using `pyamaze`, and the algorithm evolves a set of possible paths over multiple generations in a **single evolution run**.

After evolution finishes, multiple decisions are extracted from the same final population:
- **Fastest path** (minimum time)
- **Cheapest path** (minimum cost)
- **Balanced path** (minimum time + cost)

The focus of this project is to show how evolutionary techniques can be applied to pathfinding problems.

---

## Features

* Maze generation using `pyamaze`
* Single-run Genetic Algorithm implementation:
  * Population initialization
  * Fitness evaluation
  * Selection
  * Crossover
  * Mutation
* Time-penalty and cost-penalty maze zones
* Post-evolution extraction of fastest, cheapest, and balanced paths from the same population
* Visualization of extracted paths using different agent colors

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
python main.py
```

---
