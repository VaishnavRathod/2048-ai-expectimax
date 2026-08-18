# AI Algorithm

## 1. Overview

The project uses Expectimax search to select actions in the stochastic 2048 environment.

The AI receives the current board and evaluates possible future states.

---

## 2. Decision Pipeline

```text
Current Board
      |
      v
Generate Legal Moves
      |
      v
Simulate Move
      |
      v
Generate Random Tile States
      |
      v
Evaluate Future States
      |
      v
Expectimax
      |
      v
Compare Actions
      |
      v
Best Move
