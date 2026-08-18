# Mathematical Formulation of the 2048 AI

## 1. Introduction

2048 can be formulated as a stochastic sequential decision-making problem.

At every time step, the player selects an action from a finite action space. The selected action modifies the board, after which the environment introduces a random tile.

Therefore, the future state of the game is not completely deterministic.

---

# 2. State Representation

The 2048 board is represented as a 4 × 4 matrix:

\[
S =
\begin{bmatrix}
x_{11} & x_{12} & x_{13} & x_{14}\\
x_{21} & x_{22} & x_{23} & x_{24}\\
x_{31} & x_{32} & x_{33} & x_{34}\\
x_{41} & x_{42} & x_{43} & x_{44}
\end{bmatrix}
\]

where \(x_{ij}\) represents the tile value at position \((i,j)\).

An empty cell is represented by:

\[
x_{ij}=0
\]

---

# 3. Action Space

The AI can select one of four actions:

\[
A=\{Left, Right, Up, Down\}
\]

The AI therefore solves:

\[
a^* = \arg\max_{a \in A} Q(S,a)
\]

where \(Q(S,a)\) represents the expected value of performing action \(a\) from state \(S\).

---

# 4. State Transition

The game transition consists of two stages.

### Stage 1: Deterministic movement

The selected action moves and merges tiles.

\[
S' = T(S,a)
\]

where \(T\) is the deterministic transition function.

### Stage 2: Random tile generation

After a valid move, a new tile is generated in an empty cell.

The standard 2048 probabilities are:

\[
P(X=2)=0.9
\]

and

\[
P(X=4)=0.1
\]

Therefore, the complete transition is stochastic.

---

# 5. Expectimax

Because the environment contains randomness, the project uses Expectimax.

Expectimax contains two types of nodes.

## MAX Node

At a MAX node, the AI selects the action with the largest value:

\[
V(S)=
\max_{a\in A}V(T(S,a))
\]

## CHANCE Node

At a chance node, the environment randomly generates a new tile.

The expected value is:

\[
V(S)=
\sum_{s'}P(s'|S)V(s')
\]

The AI therefore considers multiple possible future states.

---

# 6. Heuristic Evaluation

The search cannot continue indefinitely because the number of possible states grows rapidly.

Therefore, a heuristic evaluation function estimates the quality of a board.

The evaluation function is represented as:

\[
H(S)=
w_eE(S)
+w_mM(S)
+w_sS(S)
+w_tT(S)
+w_cC(S)
\]

where:

- \(E(S)\) = empty-cell score
- \(M(S)\) = monotonicity score
- \(S(S)\) = smoothness score
- \(T(S)\) = maximum-tile score
- \(C(S)\) = corner-position score

and

\[
w_e,w_m,w_s,w_t,w_c
\]

are the corresponding weights.

---

# 7. Empty Cell Heuristic

Empty cells provide flexibility.

Let:

\[
E(S)=\text{number of empty cells}
\]

A board with more empty cells is generally considered safer because it has more possible future moves.

---

# 8. Smoothness

Neighboring tiles with similar values are preferred.

Because 2048 values grow exponentially, logarithmic values can be used:

\[
L(x)=\log_2(x)
\]

The smoothness component can be represented as:

\[
S(S)=
-\sum_{(i,j)}
|L(x_{ij})-L(x_{neighbor})|
\]

A smaller difference produces a better smoothness score.

---

# 9. Monotonicity

Monotonicity measures whether tile values increase or decrease consistently along rows and columns.

For example:

\[
2,4,8,16
\]

is strongly monotonic.

This encourages the AI to create organized board structures.

---

# 10. Maximum Tile

The maximum tile is an important indicator of game progress.

The heuristic can use:

\[
T(S)=\log_2(\max(S))
\]

Using the logarithm prevents very large tile values from dominating the complete evaluation.

---

# 11. Corner Strategy

The AI can encourage large tiles to remain near a selected corner.

This is useful because stable corner configurations can preserve board structure and create space for future merges.

---

# 12. Expected Utility

For each possible action, the AI calculates an expected utility:

\[
Q(S,a)
=
\sum_{s'}
P(s'|S,a)V(s')
\]

The final decision is:

\[
a^*=
\arg\max_{a\in A}Q(S,a)
\]

Therefore, the selected move is not necessarily the move that produces the largest immediate score.

Instead, it is the move with the highest estimated long-term expected value.

---

# 13. Computational Complexity

If \(b\) represents the effective branching factor and \(d\) represents search depth, the approximate complexity grows as:

\[
O(b^d)
\]

Increasing search depth generally improves the ability to reason about future states but also increases computation time.

This creates a fundamental trade-off:

\[
\text{Decision Quality}
\leftrightarrow
\text{Computational Cost}
\]

The experiments in this project investigate this relationship.

---

# 14. Summary

The AI therefore follows:

\[
\boxed{
\text{Board}
\rightarrow
\text{Actions}
\rightarrow
\text{Simulation}
\rightarrow
\text{Chance States}
\rightarrow
\text{Evaluation}
\rightarrow
\text{Expectimax}
\rightarrow
\text{Best Action}
}
\]

This mathematical formulation provides the foundation for evaluating and extending the system toward reinforcement learning and other optimization methods.