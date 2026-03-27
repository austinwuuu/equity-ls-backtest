import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import ensure_dirs, clear_backtest_output, DATA_DIR, REPORTS_DIR, fmt_pct, fmt_float
from data_loader import load_all_data
from strategy_registry import build_signals, discover_strategies
from backtest import backtest_all
from metrics import compute_metrics_table
from regression import regression_table
from plots import generate_all_plots


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Backtest equity factor strategies with optional FF3 attribution."
    )
    p.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List discovered strategies and exit.",
    )
    p.add_argument(
        "-s",
        "--strategy",
        action="append",
        dest="strategies",
        metavar="NAME",
        help=(
            "Strategy to run (repeat for several). "
            "Use 'all' or omit to run every module in src/strategies/."
        ),
    )
    p.add_argument(
        "--clean",
        action="store_true",
        help="Delete output/, data/raw/, data/processed/, then exit.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.clean:
        clear_backtest_output()
        print(
            f"[main] Cleared output → {REPORTS_DIR.parent}  "
            f"and fetched data → {DATA_DIR / 'raw'}, {DATA_DIR / 'processed'}"
        )
        return

    if args.list:
        reg = discover_strategies()
        print("Strategies:")
        for name in sorted(reg):
            print(f"  {name}")
        return

    print("=" * 60)
    print("  systematic-equity-strategies")
    print("=" * 60)

    ensure_dirs()
    prices, monthly_returns, ff3 = load_all_data()

    signals = build_signals(monthly_returns, args.strategies)
    strategy_returns = backtest_all(signals, monthly_returns)

    metrics = compute_metrics_table(strategy_returns)
    metrics.to_csv(REPORTS_DIR / "performance_metrics.csv")

    reg = regression_table(strategy_returns, ff3)

    generate_all_plots(strategy_returns, metrics)

    print("\n" + "=" * 60)
    print("  PERFORMANCE SUMMARY")
    print("=" * 60)
    for name in metrics.index:
        row = metrics.loc[name]
        print(f"\n  {name}")
        print(f"    Ann. Return    : {fmt_pct(row['Ann. Return'])}")
        print(f"    Ann. Volatility: {fmt_pct(row['Ann. Volatility'])}")
        print(f"    Sharpe Ratio   : {fmt_float(row['Sharpe Ratio'], 2)}")
        print(f"    Max Drawdown   : {fmt_pct(row['Max Drawdown'])}")

    print("\n" + "=" * 60)
    print("  FF3 REGRESSION SUMMARY")
    print("=" * 60)
    for name in reg.index:
        r = reg.loc[name]
        print(f"\n  {name}")
        print(f"    Alpha (monthly): {fmt_float(r['Alpha (monthly)'], 4)}  "
              f"(t = {fmt_float(r['Alpha t-stat'], 2)})")
        print(f"    Mkt-RF beta    : {fmt_float(r['Mkt-RF beta'], 3)}  "
              f"(t = {fmt_float(r['Mkt-RF t-stat'], 2)})")
        print(f"    SMB beta       : {fmt_float(r['SMB beta'], 3)}  "
              f"(t = {fmt_float(r['SMB t-stat'], 2)})")
        print(f"    HML beta       : {fmt_float(r['HML beta'], 3)}  "
              f"(t = {fmt_float(r['HML t-stat'], 2)})")
        print(f"    R²             : {fmt_float(r['R²'], 3)}")

    print("\n" + "=" * 60)
    print("  Done. Charts → output/charts/  Reports → output/reports/")
    print("=" * 60)


if __name__ == "__main__":
    main()
