from ai.expectimax import ExpectimaxAI


board = [
    [2, 4, 8, 16],
    [32, 64, 128, 0],
    [2, 4, 0, 0],
    [2, 2, 0, 0]
]


ai = ExpectimaxAI(
    depth=5
)


best_move = ai.get_best_move(
    board
)


print(
    "AI recommends:",
    best_move
)