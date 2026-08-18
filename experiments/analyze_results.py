import csv
import os
import statistics


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(__file__)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "results"
)

INPUT_FILE = os.path.join(
    RESULTS_DIR,
    "depth_comparison_games.csv"
)

OUTPUT_FILE = os.path.join(
    RESULTS_DIR,
    "statistical_analysis.csv"
)


# ============================================================
# LOAD CSV
# ============================================================

def load_results(filepath):
    """
    Load game-level benchmark results from CSV.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Results file not found:\n{filepath}"
        )

    results = []

    with open(
        filepath,
        "r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            results.append({
                "game_id": int(row["game_id"]),
                "seed": int(row["seed"]),
                "depth": int(row["depth"]),
                "score": float(row["score"]),
                "max_tile": int(row["max_tile"]),
                "moves": int(row["moves"]),
                "win": int(row["win"]),
                "average_decision_time": float(
                    row["average_decision_time"]
                ),
                "total_time": float(
                    row["total_time"]
                )
            })

    return results


# ============================================================
# SAFE MEAN
# ============================================================

def safe_mean(values):

    if not values:
        return 0.0

    return statistics.mean(values)


# ============================================================
# SAFE STANDARD DEVIATION
# ============================================================

def safe_stdev(values):

    if len(values) < 2:
        return 0.0

    return statistics.stdev(values)


# ============================================================
# SAFE MEDIAN
# ============================================================

def safe_median(values):

    if not values:
        return 0.0

    return statistics.median(values)


# ============================================================
# ANALYZE ONE DEPTH
# ============================================================

def analyze_depth(results, depth):
    """
    Calculate statistics for one Expectimax depth.
    """

    depth_results = [
        result
        for result in results
        if result["depth"] == depth
    ]

    if not depth_results:
        return None

    scores = [
        result["score"]
        for result in depth_results
    ]

    max_tiles = [
        result["max_tile"]
        for result in depth_results
    ]

    moves = [
        result["moves"]
        for result in depth_results
    ]

    decision_times = [
        result["average_decision_time"]
        for result in depth_results
    ]

    total_times = [
        result["total_time"]
        for result in depth_results
    ]

    wins = [
        result["win"]
        for result in depth_results
    ]

    analysis = {

        "depth": depth,

        "games": len(depth_results),

        # --------------------------------------------
        # SCORE
        # --------------------------------------------

        "average_score":
            safe_mean(scores),

        "median_score":
            safe_median(scores),

        "score_std":
            safe_stdev(scores),

        "best_score":
            max(scores),

        "worst_score":
            min(scores),

        # --------------------------------------------
        # MAXIMUM TILE
        # --------------------------------------------

        "average_max_tile":
            safe_mean(max_tiles),

        "best_max_tile":
            max(max_tiles),

        # --------------------------------------------
        # MOVES
        # --------------------------------------------

        "average_moves":
            safe_mean(moves),

        "max_moves":
            max(moves),

        # --------------------------------------------
        # WIN RATE
        # --------------------------------------------

        "wins":
            sum(wins),

        "win_rate":
            (
                sum(wins)
                / len(wins)
                * 100
            ),

        # --------------------------------------------
        # COMPUTATION TIME
        # --------------------------------------------

        "average_decision_time":
            safe_mean(decision_times),

        "average_total_time":
            safe_mean(total_times),

        "total_computation_time":
            sum(total_times)
    }

    return analysis


# ============================================================
# ANALYZE ALL DEPTHS
# ============================================================

def analyze_all_depths(results):

    depths = sorted(
        set(
            result["depth"]
            for result in results
        )
    )

    analyses = []

    for depth in depths:

        analysis = analyze_depth(
            results,
            depth
        )

        if analysis is not None:
            analyses.append(
                analysis
            )

    return analyses


# ============================================================
# PRINT RESULTS
# ============================================================

def print_analysis(analyses):

    print()
    print("=" * 120)
    print("STATISTICAL ANALYSIS")
    print("=" * 120)

    header = (
        f"{'Depth':>7}"
        f"{'Games':>8}"
        f"{'Avg Score':>15}"
        f"{'Median':>15}"
        f"{'Std Dev':>15}"
        f"{'Best':>12}"
        f"{'Avg Tile':>12}"
        f"{'Win %':>10}"
        f"{'Avg Time':>15}"
    )

    print(header)

    print("-" * 120)

    for result in analyses:

        print(
            f"{result['depth']:>7}"
            f"{result['games']:>8}"
            f"{result['average_score']:>15.2f}"
            f"{result['median_score']:>15.2f}"
            f"{result['score_std']:>15.2f}"
            f"{result['best_score']:>12.0f}"
            f"{result['average_max_tile']:>12.2f}"
            f"{result['win_rate']:>10.2f}"
            f"{result['average_decision_time']:>15.6f}"
        )

    print("=" * 120)


# ============================================================
# FIND BEST DEPTH
# ============================================================

def find_best_depth(analyses):

    if not analyses:
        return None

    return max(
        analyses,
        key=lambda x: x["average_score"]
    )


# ============================================================
# PRINT INTERPRETATION
# ============================================================

def print_interpretation(analyses):

    if not analyses:
        return

    best_score_depth = max(
        analyses,
        key=lambda x: x["average_score"]
    )

    fastest_depth = min(
        analyses,
        key=lambda x: x["average_decision_time"]
    )

    best_tile_depth = max(
        analyses,
        key=lambda x: x["average_max_tile"]
    )

    highest_win_depth = max(
        analyses,
        key=lambda x: x["win_rate"]
    )

    print()
    print("=" * 70)
    print("RESEARCH INTERPRETATION")
    print("=" * 70)

    print(
        f"\nHighest average score:"
    )

    print(
        f"  Depth {best_score_depth['depth']} "
        f"→ "
        f"{best_score_depth['average_score']:.2f}"
    )

    print(
        f"\nHighest average maximum tile:"
    )

    print(
        f"  Depth {best_tile_depth['depth']} "
        f"→ "
        f"{best_tile_depth['average_max_tile']:.2f}"
    )

    print(
        f"\nFastest decision-making:"
    )

    print(
        f"  Depth {fastest_depth['depth']} "
        f"→ "
        f"{fastest_depth['average_decision_time']:.6f} s"
    )

    print(
        f"\nHighest win rate:"
    )

    print(
        f"  Depth {highest_win_depth['depth']} "
        f"→ "
        f"{highest_win_depth['win_rate']:.2f}%"
    )

    # --------------------------------------------------------
    # PERFORMANCE VS COMPUTATION
    # --------------------------------------------------------

    print()
    print(
        "Performance vs Computational Cost:"
    )

    for result in analyses:

        print(
            f"  Depth {result['depth']}: "
            f"Score = "
            f"{result['average_score']:.2f}, "
            f"Decision Time = "
            f"{result['average_decision_time']:.6f}s"
        )

    print("=" * 70)


# ============================================================
# SAVE ANALYSIS
# ============================================================

def save_analysis(analyses):

    if not analyses:
        return

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True
    )

    fieldnames = [
        "depth",
        "games",
        "average_score",
        "median_score",
        "score_std",
        "best_score",
        "worst_score",
        "average_max_tile",
        "best_max_tile",
        "average_moves",
        "max_moves",
        "wins",
        "win_rate",
        "average_decision_time",
        "average_total_time",
        "total_computation_time"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            analyses
        )

    print()
    print(
        "Statistical analysis saved to:"
    )

    print(
        OUTPUT_FILE
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "Loading benchmark results..."
    )

    results = load_results(
        INPUT_FILE
    )

    print(
        f"Loaded {len(results)} games."
    )

    analyses = analyze_all_depths(
        results
    )

    print_analysis(
        analyses
    )

    print_interpretation(
        analyses
    )

    save_analysis(
        analyses
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()