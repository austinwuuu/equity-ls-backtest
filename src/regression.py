import pandas as pd
import statsmodels.api as sm

from utils import REPORTS_DIR


def run_ff3_regression(strategy_returns: pd.Series,
                       ff3: pd.DataFrame) -> dict:
    common = strategy_returns.index.intersection(ff3.index)
    y = strategy_returns.loc[common]
    X = ff3.loc[common, ["Mkt-RF", "SMB", "HML"]]
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    return {
        "alpha": model.params["const"],
        "alpha_t": model.tvalues["const"],
        "Mkt-RF_beta": model.params["Mkt-RF"],
        "Mkt-RF_t": model.tvalues["Mkt-RF"],
        "SMB_beta": model.params["SMB"],
        "SMB_t": model.tvalues["SMB"],
        "HML_beta": model.params["HML"],
        "HML_t": model.tvalues["HML"],
        "R_squared": model.rsquared,
        "N_obs": int(model.nobs),
    }


def regression_table(strategy_returns: pd.DataFrame,
                     ff3: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name in strategy_returns.columns:
        ret = strategy_returns[name].dropna()
        res = run_ff3_regression(ret, ff3)
        rows.append({
            "Strategy": name,
            "Alpha (monthly)": res["alpha"],
            "Alpha t-stat": res["alpha_t"],
            "Mkt-RF beta": res["Mkt-RF_beta"],
            "Mkt-RF t-stat": res["Mkt-RF_t"],
            "SMB beta": res["SMB_beta"],
            "SMB t-stat": res["SMB_t"],
            "HML beta": res["HML_beta"],
            "HML t-stat": res["HML_t"],
            "R²": res["R_squared"],
            "N": res["N_obs"],
        })
    df = pd.DataFrame(rows).set_index("Strategy")
    df.to_csv(REPORTS_DIR / "ff3_regression.csv")
    return df
