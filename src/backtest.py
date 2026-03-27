import pandas as pd


def backtest_strategy(weights: pd.DataFrame,
                      monthly_returns: pd.DataFrame) -> pd.Series:
    strategy_returns = (weights * monthly_returns).sum(axis=1)
    strategy_returns.name = "strategy_return"
    return strategy_returns


def backtest_all(signals: dict[str, pd.DataFrame],
                 monthly_returns: pd.DataFrame) -> pd.DataFrame:
    results = {}
    for name, weights in signals.items():
        ret = backtest_strategy(weights, monthly_returns)
        first_nonzero = (ret != 0).idxmax()
        results[name] = ret.loc[first_nonzero:]
    df = pd.DataFrame(results).dropna(how="all")
    print(f"[backtest] Backtest period: {df.index.min().date()} → {df.index.max().date()}")
    return df
