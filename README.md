# L/S Equity Strategy Backtest

## Overview

This project is a Python-based workflow for back-testing L/S equity factor strategies. It uses stock price data to construct signals such as momentum, reversal, and volatility-based factors, and evaluates their performance through backtesting.

Strategy returns are assessed using metrics including annualized return, volatility, Sharpe ratio, and drawdown. Each strategy is also regressed against Fama-French 3 factors to estimate alpha and factor exposures.

## Structure

```
equity-ls-backtest/
├── LICENSE
├── README.md
├── requirements.txt
├── data/
│   ├── universe.csv
│   ├── raw/
│   │   ├── daily_prices.csv
│   │   └── ff3_factors.csv
│   └── processed/
│       └── monthly_returns.csv
├── output/
│   ├── charts/
│   │   ├── cumulative_returns.png
│   │   ├── sharpe_ratios.png
│   │   └── rolling_volatility.png
│   └── reports/
│       ├── performance_metrics.csv
│       └── ff3_regression.csv
└── src/
    ├── main.py
    ├── strategy_registry.py
    ├── strategy_lib.py
    ├── strategies/
    │   ├── __init__.py
    │   └── private/          # gitignored for local strategies
    ├── data_loader.py
    ├── backtest.py
    ├── metrics.py
    ├── regression.py
    ├── plots.py
    └── utils.py
```

Add a new strategy under `src/strategies/`

## Usage

```bash
pip install -r requirements.txt

python3 src/main.py
python3 src/main.py --list
python3 src/main.py --strategy <strategy_name>
python3 src/main.py -s <strategy_name1> -s <strategy_name2>
python3 src/main.py --strategy all
python3 src/main.py --clean
```

## License

MIT License — permissive use with attribution; see `LICENSE` for full text.
