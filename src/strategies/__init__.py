"""
Each strategy module must define:

    def build_signal(monthly_returns: pd.DataFrame) -> pd.DataFrame: ...

Optional: STRATEGY_NAME: str (defaults to the filename without .py).

Shared helpers: from strategy_lib import rank_to_weights
"""
