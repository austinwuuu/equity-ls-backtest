import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from utils import CHARTS_DIR, MONTHS_PER_YEAR

plt.rcParams.update({
    "figure.figsize": (10, 5),
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
})

COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]


def plot_cumulative_returns(strategy_returns: pd.DataFrame,
                            save: bool = True) -> None:
    cum = (1 + strategy_returns).cumprod()

    fig, ax = plt.subplots()
    for i, col in enumerate(cum.columns):
        ax.plot(cum.index, cum[col], label=col, color=COLORS[i % len(COLORS)])
    ax.axhline(1.0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_title("Cumulative Returns by Strategy")
    ax.set_ylabel("Growth of $1")
    ax.set_xlabel("")
    ax.legend()
    fig.tight_layout()

    if save:
        path = CHARTS_DIR / "cumulative_returns.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)


def plot_sharpe_bars(metrics_table: pd.DataFrame,
                     save: bool = True) -> None:
    sharpes = metrics_table["Sharpe Ratio"]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(sharpes.index, sharpes.values, color=COLORS[: len(sharpes)])
    ax.axvline(0, color="grey", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Annualized Sharpe Ratio")
    ax.set_title("Sharpe Ratio Comparison")

    for bar, val in zip(bars, sharpes.values):
        offset = 0.03 if val >= 0 else -0.03
        ha = "left" if val >= 0 else "right"
        ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", ha=ha, fontsize=10)
    fig.tight_layout()

    if save:
        path = CHARTS_DIR / "sharpe_ratios.png"
        fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_rolling_volatility(strategy_returns: pd.DataFrame,
                            window: int = 12,
                            save: bool = True) -> None:
    rolling_vol = strategy_returns.rolling(window).std() * np.sqrt(MONTHS_PER_YEAR)

    fig, ax = plt.subplots()
    for i, col in enumerate(rolling_vol.columns):
        ax.plot(rolling_vol.index, rolling_vol[col],
                label=col, color=COLORS[i % len(COLORS)])
    ax.set_title(f"Rolling {window}-Month Annualized Volatility")
    ax.set_ylabel("Volatility")
    ax.set_xlabel("")
    ax.legend()
    fig.tight_layout()

    if save:
        path = CHARTS_DIR / "rolling_volatility.png"
        fig.savefig(path, dpi=150)
    plt.close(fig)


def generate_all_plots(strategy_returns: pd.DataFrame,
                       metrics_table: pd.DataFrame) -> None:
    plot_cumulative_returns(strategy_returns)
    plot_sharpe_bars(metrics_table)
    plot_rolling_volatility(strategy_returns)
