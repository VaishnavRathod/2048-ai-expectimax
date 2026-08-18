import csv
import os
import statistics

from experiments.benchmark import run_benchmark

# ============================================================
# CONFIGURATION
# ============================================================

DEPTHS = [
    1,
    2,
    3,
    4
]

GAMES_PER_DEPTH = 10

START_SEED = 42

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__),
    "results"
)


# ============================================================
# STATISTICS
# ============================================================

def mean(values):

    if not values:
        return 0.0

    return statistics.mean(values)


def standard_deviation(values):

    if len(values) < 2:
        return 0.0

    return statistics.stdev(values)


# ============================================================
# ANALYZE RESULTS
# ============================================================

def analyze_results(
    results,
    depth
):

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

    summary = {

        "depth": depth,

        "games": len(results),

        "average_score":
            mean(scores),

        "score_std":
            standard_deviation(scores),

        "average_max_tile":
            mean(max_tiles),

        "average_moves":
            mean(moves),

        "win_rate":
            (
                sum(wins)
                / len(wins)
                * 100
            ),

        "average_decision_time":
            mean(decision_times)
    }

    return summary


# ============================================================
# SAVE COMBINED RESULTS
# ============================================================

def save_combined_results(
    all_results
):

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    filepath = os.path.join(
        RESULTS_DIR,
        "depth_comparison_games.csv"
    )

    if not all_results:
        return filepath

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
            all_results
        )

    return filepath


# ============================================================
# SAVE SUMMARY
# ============================================================

def save_summary(
    summaries
):

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    filepath = os.path.join(
        RESULTS_DIR,
        "depth_comparison_summary.csv"
    )

    fieldnames = [
        "depth",
        "games",
        "average_score",
        "score_std",
        "average_max_tile",
        "average_moves",
        "win_rate",
        "average_decision_time"
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
            summaries
        )

    return filepath


# ============================================================
# PRINT SUMMARY TABLE
# ============================================================

def print_summary_table(
    summaries
):

    print()
    print("=" * 100)

    print(
        "EXPECTIMAX SEARCH DEPTH COMPARISON"
    )

    print("=" * 100)

    print(
        f"{'Depth':>7}"
        f"{'Games':>8}"
        f"{'Avg Score':>15}"
        f"{'Std Dev':>15}"
        f"{'Avg Max':>12}"
        f"{'Win %':>10}"
        f"{'Avg Time':>15}"
    )

    print("-" * 100)

    for summary in summaries:

        print(
            f"{summary['depth']:>7}"
            f"{summary['games']:>8}"
            f"{summary['average_score']:>15.2f}"
            f"{summary['score_std']:>15.2f}"
            f"{summary['average_max_tile']:>12.2f}"
            f"{summary['win_rate']:>10.2f}"
            f"{summary['average_decision_time']:>15.6f}"
        )

    print("=" * 100)


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print()
    print("=" * 70)
    print("2048 EXPECTIMAX DEPTH EXPERIMENT")
    print("=" * 70)

    print(
        f"Depths: {DEPTHS}"
    )

    print(
        f"Games per depth: "
        f"{GAMES_PER_DEPTH}"
    )

    print("=" * 70)

    all_results = []

    summaries = []

    # --------------------------------------------------------
    # RUN EACH DEPTH
    # --------------------------------------------------------

    for depth in DEPTHS:

        print()
        print(
            f"\n>>> Testing Search Depth {depth}"
        )

        # Use different seed range for each depth
        depth_seed = (
            START_SEED
            + (
                depth * 1000
            )
        )

        results = run_benchmark(

            depth=depth,

            num_games=GAMES_PER_DEPTH,

            start_seed=depth_seed,

            verbose=False
        )

        # Add results
        all_results.extend(
            results
        )

        # Analyze
        summary = analyze_results(
            results,
            depth
        )

        summaries.append(
            summary
        )

    # --------------------------------------------------------
    # PRINT FINAL SUMMARY
    # --------------------------------------------------------

    print_summary_table(
        summaries
    )

    # --------------------------------------------------------
    # SAVE GAME RESULTS
    # --------------------------------------------------------

    game_results_file = (
        save_combined_results(
            all_results
        )
    )

    # --------------------------------------------------------
    # SAVE SUMMARY RESULTS
    # --------------------------------------------------------

    summary_file = (
        save_summary(
            summaries
        )
    )

    print()

    print(
        "Game-level results:"
    )

    print(
        game_results_file
    )

    print()

    print(
        "Depth summary:"
    )

    print(
        summary_file
    )

    print()
    print(
        "Experiment completed."
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()