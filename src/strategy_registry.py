import importlib.util
from pathlib import Path
from typing import Callable

import pandas as pd

BuildSignalFn = Callable[..., pd.DataFrame]


def discover_strategies() -> dict[str, BuildSignalFn]:
    strategies_dir = Path(__file__).resolve().parent / "strategies"
    out: dict[str, BuildSignalFn] = {}
    for path in sorted(strategies_dir.glob("*.py")):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, "build_signal"):
            continue
        name = getattr(mod, "STRATEGY_NAME", None) or path.stem
        if name in out:
            raise ValueError(f"Duplicate strategy name: {name!r}")
        out[name] = mod.build_signal
    if not out:
        raise RuntimeError(f"No strategies found in {strategies_dir}")
    return out


def resolve_strategy_names(
    requested: list[str] | None, registry: dict[str, BuildSignalFn]
) -> list[str]:
    if not requested:
        return list(registry.keys())
    if "all" in requested:
        return list(registry.keys())
    missing = [k for k in requested if k not in registry]
    if missing:
        avail = ", ".join(sorted(registry))
        raise SystemExit(
            f"Unknown strategy: {', '.join(repr(m) for m in missing)}. "
            f"Available: {avail}"
        )
    seen: set[str] = set()
    ordered: list[str] = []
    for k in requested:
        if k not in seen:
            seen.add(k)
            ordered.append(k)
    return ordered


def build_signals(
    monthly_returns: pd.DataFrame, strategy_names: list[str] | None
) -> dict[str, pd.DataFrame]:
    registry = discover_strategies()
    names = resolve_strategy_names(strategy_names, registry)
    signals: dict[str, pd.DataFrame] = {}
    for name in names:
        print(f"[strategy] Building signal: {name}")
        signals[name] = registry[name](monthly_returns)
    return signals
