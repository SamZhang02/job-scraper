try:
    from typing import override  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - fallback for older runtimes
    def override(func):  # type: ignore[no-redef]
        return func

__all__ = ["override"]
