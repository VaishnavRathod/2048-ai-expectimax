import csv
import os

import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(__file__)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "results"
)

PLOTS_DIR = os.path.join(
    BASE_DIR,
    "plots"
)

INPUT_FILE = os.path.join(
    RESULTS_DIR,
    "statistical_analysis.csv"
)


# ============================================================
# LOAD ANALYSIS DATA
# ============================================================

def load_analysis(filepath):

    if not os.path.exists(filepath):

        raise FileNotFoundError(
            f"Statistical analysis file not found:\n"
            f"{filepath}\n\n"
            f"Run analyze_results.py first."
        )

    data = []

    with open(
        filepath,
        "r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            data.append({

                "depth":
                    int(row["depth"]),

                "average_score":
                    float(row["average_score"]),

                "median_score":
                    float(row["median_score"]),

                "score_std":
                    float(row["score_std"]),

                "best_score":
                    float(row["best_score"]),

                "average_max_tile":
                    float(row["average_max_tile"]),

                "best_max_tile":
                    float(row["best_max_tile"]),

                "average_moves":
                    float(row["average_moves"]),

                "win_rate":
                    float(row["win_rate"]),

                "average_decision_time":
                    float(
                        row["average_decision_time"]
                    ),

                "average_total_time":
                    float(
                        row["average_total_time"]
                    )
            })

    return data


# ============================================================
# CREATE PLOTS DIRECTORY
# ============================================================

def create_plot_directory():

    os.makedirs(
        PLOTS_DIR,
        exist_ok=True
    )


# ============================================================
# PLOT 1
# AVERAGE SCORE VS DEPTH
# ============================================================

def plot_average_score(data):

    depths = [
        row["depth"]
        for row in data
    ]

    scores = [
        row["average_score"]
        for row in data
    ]

    standard_deviation = [
        row["score_std"]
        for row in data
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.errorbar(
        depths,
        scores,
        yerr=standard_deviation,
        marker="o",
        capsize=5
    )

    plt.xlabel(
        "Expectimax Search Depth"
    )

    plt.ylabel(
        "Average Score"
    )

    plt.title(
        "Average 2048 Score vs Expectimax Search Depth"
    )

    plt.xticks(
        depths
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    filepath = os.path.join(
        PLOTS_DIR,
        "average_score_vs_depth.png"
    )

    plt.savefig(
        filepath,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {filepath}"
    )


# ============================================================
# PLOT 2
# MAXIMUM TILE VS DEPTH
# ============================================================

def plot_max_tile(data):

    depths = [
        row["depth"]
        for row in data
    ]

    max_tiles = [
        row["average_max_tile"]
        for row in data
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        depths,
        max_tiles,
        marker="o"
    )

    plt.xlabel(
        "Expectimax Search Depth"
    )

    plt.ylabel(
        "Average Maximum Tile"
    )

    plt.title(
        "Average Maximum Tile vs Search Depth"
    )

    plt.xticks(
        depths
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    filepath = os.path.join(
        PLOTS_DIR,
        "maximum_tile_vs_depth.png"
    )

    plt.savefig(
        filepath,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {filepath}"
    )


# ============================================================
# PLOT 3
# WIN RATE VS DEPTH
# ============================================================

def plot_win_rate(data):

    depths = [
        row["depth"]
        for row in data
    ]

    win_rates = [
        row["win_rate"]
        for row in data
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        depths,
        win_rates,
        marker="o"
    )

    plt.xlabel(
        "Expectimax Search Depth"
    )

    plt.ylabel(
        "Win Rate (%)"
    )

    plt.title(
        "2048 Win Rate vs Expectimax Search Depth"
    )

    plt.xticks(
        depths
    )

    plt.ylim(
        0,
        100
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    filepath = os.path.join(
        PLOTS_DIR,
        "win_rate_vs_depth.png"
    )

    plt.savefig(
        filepath,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {filepath}"
    )


# ============================================================
# PLOT 4
# DECISION TIME VS DEPTH
# ============================================================

def plot_decision_time(data):

    depths = [
        row["depth"]
        for row in data
    ]

    decision_times = [
        row["average_decision_time"]
        for row in data
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.plot(
        depths,
        decision_times,
        marker="o"
    )

    plt.xlabel(
        "Expectimax Search Depth"
    )

    plt.ylabel(
        "Average Decision Time (seconds)"
    )

    plt.title(
        "AI Decision Time vs Expectimax Search Depth"
    )

    plt.xticks(
        depths
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    filepath = os.path.join(
        PLOTS_DIR,
        "decision_time_vs_depth.png"
    )

    plt.savefig(
        filepath,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {filepath}"
    )


# ============================================================
# PLOT 5
# PERFORMANCE VS COMPUTATIONAL COST
# ============================================================

def plot_performance_vs_cost(data):

    scores = [
        row["average_score"]
        for row in data
    ]

    decision_times = [
        row["average_decision_time"]
        for row in data
    ]

    depths = [
        row["depth"]
        for row in data
    ]

    plt.figure(
        figsize=(9, 6)
    )

    plt.scatter(
        decision_times,
        scores,
        s=100
    )

    for i in range(
        len(data)
    ):

        plt.annotate(
            f"Depth {depths[i]}",
            (
                decision_times[i],
                scores[i]
            ),
            xytext=(8, 8),
            textcoords="offset points"
        )

    plt.xlabel(
        "Average Decision Time (seconds)"
    )

    plt.ylabel(
        "Average Score"
    )

    plt.title(
        "2048 AI Performance vs Computational Cost"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    filepath = os.path.join(
        PLOTS_DIR,
        "performance_vs_computational_cost.png"
    )

    plt.savefig(
        filepath,
        dpi=300
    )

    plt.close()

    print(
        f"Saved: {filepath}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "=" * 60
    )

    print(
        "2048 AI RESULT VISUALIZATION"
    )

    print(
        "=" * 60
    )

    create_plot_directory()

    data = load_analysis(
        INPUT_FILE
    )

    print(
        f"Loaded {len(data)} depth configurations."
    )

    print()

    plot_average_score(
        data
    )

    plot_max_tile(
        data
    )

    plot_win_rate(
        data
    )

    plot_decision_time(
        data
    )

    plot_performance_vs_cost(
        data
    )

    print()
    print(
        "=" * 60
    )

    print(
        "All plots generated successfully."
    )

    print(
        f"Location: {PLOTS_DIR}"
    )

    print(
        "=" * 60
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()