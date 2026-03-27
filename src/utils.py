import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORTS_DIR = OUTPUT_DIR / "reports"
UNIVERSE_FILE = DATA_DIR / "universe.csv"

TRADING_DAYS_PER_YEAR = 252
MONTHS_PER_YEAR = 12
START_DATE = "2005-01-01"
END_DATE = "2024-12-31"


def ensure_dirs():
    for d in [RAW_DIR, PROCESSED_DIR, CHARTS_DIR, REPORTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def clear_backtest_output() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    for d in (RAW_DIR, PROCESSED_DIR):
        if d.exists():
            shutil.rmtree(d)
    ensure_dirs()


def fmt_pct(value: float, decimals: int = 2) -> str:
    return f"{value * 100:.{decimals}f}%"


def fmt_float(value: float, decimals: int = 4) -> str:
    return f"{value:.{decimals}f}"
