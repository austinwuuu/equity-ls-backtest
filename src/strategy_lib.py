import pandas as pd


def rank_to_weights(ranks: pd.Series, n_groups: int = 3) -> pd.Series:
    n = ranks.count()
    if n < n_groups:
        return pd.Series(0.0, index=ranks.index)

    bottom = ranks <= ranks.quantile(1 / n_groups)
    top = ranks >= ranks.quantile(1 - 1 / n_groups)

    weights = pd.Series(0.0, index=ranks.index)
    n_long = top.sum()
    n_short = bottom.sum()
    if n_long > 0:
        weights[top] = 1.0 / n_long
    if n_short > 0:
        weights[bottom] = -1.0 / n_short
    return weights
