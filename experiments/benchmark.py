import csv
import os
import random
import time

from game.board import Board
from game.game_logic import GameLogic
from ai.expectimax import ExpectimaxAI


# ============================================================
# DIRECTORY CONFIGURATION
# ============================================================

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "results"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_max_tile(board):
    """
    Return the largest tile currently present on the board.
    """

    max_tile = 0

    for row in board.grid:
        for value in row:
            if value > max_tile:
                max_tile = value

    return max_tile


def get_average(values):
    """
    Return the average of a list.
    """

    if not values:
        return 0.0

    return sum(values) / len(values)


# ============================================================
# PLAY ONE GAME
# ============================================================

def play_game(
    depth=3,
    seed=None,
    verbose=False
):
    """
    Let the Expectimax AI play one complete game.

    Parameters
    ----------
    depth : int
        Expectimax search depth.

    seed : int or None
        Random seed used for reproducibility.

    verbose : bool
        Print game progress if True.

    Returns
    -------
    dict
        Statistics from the game.
    """

    # --------------------------------------------------------
    # SET RANDOM SEED
    # --------------------------------------------------------

    if seed is not None:
        random.seed(seed)

    # --------------------------------------------------------
    # CREATE NEW GAME
    # --------------------------------------------------------

    board = Board()

    game = GameLogic(board)

    ai = ExpectimaxAI(
        depth=depth
    )

    # --------------------------------------------------------
    # GAME STATISTICS
    # --------------------------------------------------------

    move_count = 0

    decision_times = []

    start_total_time = time.perf_counter()

    # --------------------------------------------------------
    # MAIN AI GAME LOOP
    # --------------------------------------------------------

    while True:

        # -----------------------------------------------
        # CHECK GAME OVER
        # -----------------------------------------------

        if game.check_game_over():
            break

        # -----------------------------------------------
        # STOP WHEN WINNING TILE IS REACHED
        # -----------------------------------------------

        if game.won:
            break

        # -----------------------------------------------
        # CURRENT BOARD
        # -----------------------------------------------

        current_board = board.copy()

        # -----------------------------------------------
        # CALCULATE BEST MOVE
        # -----------------------------------------------

        start_decision = time.perf_counter()

        best_move = ai.get_best_move(
            current_board
        )

        end_decision = time.perf_counter()

        decision_time = (
            end_decision
            - start_decision
        )

        decision_times.append(
            decision_time
        )

        # -----------------------------------------------
        # NO LEGAL MOVE
        # -----------------------------------------------

        if best_move is None:
            break

        # -----------------------------------------------
        # EXECUTE MOVE
        # -----------------------------------------------

        changed, old_board, new_board = (
            execute_move(
                game,
                best_move
            )
        )

        # -----------------------------------------------
        # INVALID MOVE
        # -----------------------------------------------

        if not changed:
            break

        move_count += 1

        # -----------------------------------------------
        # ADD RANDOM TILE
        # -----------------------------------------------

        game.add_random_tile()

        # -----------------------------------------------
        # CHECK WIN
        # -----------------------------------------------

        game.check_win()

        if game.won:
            break

        # -----------------------------------------------
        # CHECK GAME OVER
        # -----------------------------------------------

        game.check_game_over()

        if game.game_over:
            break

        # -----------------------------------------------
        # OPTIONAL OUTPUT
        # -----------------------------------------------

        if verbose:

            print(
                f"Move {move_count:4d} | "
                f"Move: {best_move:5s} | "
                f"Score: {game.score:8d} | "
                f"Max Tile: {get_max_tile(board)}"
            )

    # --------------------------------------------------------
    # TOTAL TIME
    # --------------------------------------------------------

    end_total_time = time.perf_counter()

    total_time = (
        end_total_time
        - start_total_time
    )

    # --------------------------------------------------------
    # FINAL STATISTICS
    # --------------------------------------------------------

    final_score = game.score

    maximum_tile = get_max_tile(board)

    average_decision_time = get_average(
        decision_times
    )

    result = {
        "seed": seed,
        "depth": depth,
        "score": final_score,
        "max_tile": maximum_tile,
        "moves": move_count,
        "win": int(game.won),
        "average_decision_time": average_decision_time,
        "total_time": total_time
    }

    return result


# ============================================================
# EXECUTE GAME MOVE
# ============================================================

def execute_move(
    game,
    move
):
    """
    Execute an AI-selected move using the real GameLogic.

    Returns
    -------
    tuple
        (changed, old_board, new_board)
    """

    if move == "left":

        return game.move_left()

    elif move == "right":

        return game.move_right()

    elif move == "up":

        return game.move_up()

    elif move == "down":

        return game.move_down()

    return (
        False,
        game.board.copy(),
        game.board.copy()
    )


# ============================================================
# RUN MULTIPLE GAMES
# ============================================================

def run_benchmark(
    depth=3,
    num_games=10,
    start_seed=42,
    verbose=False
):
    """
    Run multiple AI games.

    Parameters
    ----------
    depth : int
        Expectimax search depth.

    num_games : int
        Number of games to play.

    start_seed : int
        Starting random seed.

    verbose : bool
        Print progress.

    Returns
    -------
    list
        List of result dictionaries.
    """

    results = []

    print()
    print("=" * 60)
    print("2048 AI BENCHMARK")
    print("=" * 60)
    print(f"Search Depth : {depth}")
    print(f"Games        : {num_games}")
    print(f"Starting Seed: {start_seed}")
    print("=" * 60)
    print()

    for game_number in range(
        1,
        num_games + 1
    ):

        seed = start_seed + game_number - 1

        if verbose:
            print(
                f"\nStarting Game {game_number}/{num_games}"
            )

        result = play_game(
            depth=depth,
            seed=seed,
            verbose=verbose
        )

        # Add game ID
        result["game_id"] = game_number

        results.append(result)

        print(
            f"Game {game_number:3d}/{num_games} | "
            f"Score: {result['score']:8d} | "
            f"Max Tile: {result['max_tile']:5d} | "
            f"Moves: {result['moves']:5d} | "
            f"Win: {result['win']} | "
            f"Avg Decision: "
            f"{result['average_decision_time']:.5f}s"
        )

    return results


# ============================================================
# SAVE RESULTS TO CSV
# ============================================================

def save_results(
    results,
    filename=None
):
    """
    Save benchmark results to a CSV file.
    """

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    if filename is None:

        if results:

            depth = results[0]["depth"]

        else:

            depth = "unknown"

        filename = (
            f"benchmark_depth_{depth}.csv"
        )

    filepath = os.path.join(
        RESULTS_DIR,
        filename
    )

    fieldnames = [
        "game_id",
        "seed",
        "depth",
        "score",
        "max_tile",
        "moves",
        "win",
        "average_decision_time",
        "total_time"
    ]

    with open(
        filepath,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            results
        )

    print()
    print(
        f"Results saved to:"
    )
    print(
        filepath
    )

    return filepath


# ============================================================
# SUMMARY
# ============================================================

def print_summary(results):
    """
    Print statistical summary of benchmark results.
    """

    if not results:

        print(
            "No results available."
        )

        return

    scores = [
        result["score"]
        for result in results
    ]

    max_tiles = [
        result["max_tile"]
        for result in results
    ]

    moves = [
        result["moves"]
        for result in results
    ]

    decision_times = [
        result["average_decision_time"]
        for result in results
    ]

    wins = [
        result["win"]
        for result in results
    ]

    average_score = get_average(
        scores
    )

    average_max_tile = get_average(
        max_tiles
    )

    average_moves = get_average(
        moves
    )

    average_decision_time = get_average(
        decision_times
    )

    win_rate = (
        sum(wins)
        / len(wins)
        * 100
    )

    print()
    print("=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)

    print(
        f"Average Score       : "
        f"{average_score:.2f}"
    )

    print(
        f"Average Max Tile    : "
        f"{average_max_tile:.2f}"
    )

    print(
        f"Average Moves       : "
        f"{average_moves:.2f}"
    )

    print(
        f"Win Rate            : "
        f"{win_rate:.2f}%"
    )

    print(
        f"Average Decision    : "
        f"{average_decision_time:.6f} seconds"
    )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    results = run_benchmark(
        depth=3,
        num_games=10,
        start_seed=42,
        verbose=False
    )

    print_summary(
        results
    )

    save_results(
        results
    )