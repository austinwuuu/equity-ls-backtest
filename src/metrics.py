import pandas as pd
import numpy as np

from utils import MONTHS_PER_YEAR


def annualized_return(monthly_returns: pd.Series) -> float:
    total = (1 + monthly_returns).prod()
    n_years = len(monthly_returns) / MONTHS_PER_YEAR
    if n_years <= 0:
        return 0.0
    return total ** (1 / n_years) - 1


def annualized_volatility(monthly_returns: pd.Series) -> float:
    return monthly_returns.std() * np.sqrt(MONTHS_PER_YEAR)


def sharpe_ratio(monthly_returns: pd.Series) -> float:
    ann_ret = annualized_return(monthly_returns)
    ann_vol = annualized_volatility(monthly_returns)
    if ann_vol == 0:
        return 0.0
    return ann_ret / ann_vol


def max_drawdown(monthly_returns: pd.Series) -> float:
    cum = (1 + monthly_returns).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    return drawdown.min()


def compute_metrics_table(strategy_returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name in strategy_returns.columns:
        ret = strategy_returns[name].dropna()
        rows.append({
            "Strategy": name,
            "Ann. Return": annualized_return(ret),
            "Ann. Volatility": annualized_volatility(ret),
            "Sharpe Ratio": sharpe_ratio(ret),
            "Max Drawdown": max_drawdown(ret),
            "Months": len(ret),
        })
    return pd.DataFrame(rows).set_index("Strategy")
