# Experimental Methodology

## 1. Objective

The purpose of this experiment is to evaluate the performance of the 2048 AI under different configurations.

The main objective is to determine how the Expectimax search depth affects:

- Game score
- Maximum tile achieved
- Number of moves
- Win rate
- AI decision time
- Overall computational cost

Since 2048 contains random tile generation, a single game is not sufficient to evaluate the AI. Multiple games will therefore be played for each configuration.

---

# 2. Research Questions

This project investigates the following questions:

### RQ1
How does Expectimax search depth affect the performance of the 2048 AI?

### RQ2
Does increasing search depth consistently improve the maximum tile achieved?

### RQ3
How does increasing search depth affect computation time?

### RQ4
Is there a point where increasing search depth provides diminishing returns?

### RQ5
How does the Expectimax agent compare with simpler strategies such as random and greedy agents?

---

# 3. Experimental Variables

## Independent Variable

The primary independent variable is:

\[
d = \text{Expectimax Search Depth}
\]

Example values:

```text
Depth 1
Depth 2
Depth 3
Depth 4


# 4. Experimental Procedure


Select Search Depth
        |
        v
Initialize New Game
        |
        v
Read Current Board
        |
        v
AI Calculates Best Move
        |
        v
Execute Move
        |
        v
Generate Random Tile
        |
        v
Record Statistics
        |
        v
Game Over?
     /       \
   No         Yes
   |           |
   |           v
   +------> Save Results