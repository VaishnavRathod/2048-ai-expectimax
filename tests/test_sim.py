from ai.simulator import BoardSimulator


board = [
    [2, 0, 2, 4],
    [0, 4, 4, 0],
    [2, 2, 0, 0],
    [0, 0, 0, 0]
]


simulator = BoardSimulator()


print("ORIGINAL BOARD:")

for row in board:
    print(row)


print("\nLEFT:")

left = simulator.move_left(board)

for row in left:
    print(row)


print("\nRIGHT:")

right = simulator.move_right(board)

for row in right:
    print(row)


print("\nUP:")

up = simulator.move_up(board)

for row in up:
    print(row)


print("\nDOWN:")

down = simulator.move_down(board)

for row in down:
    print(row)


print("\nPOSSIBLE MOVES:")

possible_moves = (
    simulator.get_possible_moves(board)
)

for move, result in possible_moves.items():

    print(f"\n{move.upper()}:")

    for row in result:

        print(row)