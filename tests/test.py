from ai.evaluation import BoardEvaluator


board = [
    [2, 4, 8, 16],
    [32, 64, 128, 256],
    [512, 0, 0, 0],
    [0, 0, 0, 0]
]


evaluator = BoardEvaluator()

score = evaluator.evaluate(board)

print("Board evaluation:", score)