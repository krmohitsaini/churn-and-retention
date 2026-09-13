from copy import deepcopy
from threading import Lock
from typing import Any, Callable

_CACHE: dict[tuple[str, str, tuple[tuple[str, str], ...]], Any] = {}
_LOCK = Lock()


def filter_key(filters: dict[str, Any]) -> tuple[tuple[str, str], ...]:
    return tuple(
        sorted(
            (key, str(value))
            for key, value in filters.items()
            if value not in (None, "", "All")
        )
    )


def get_or_set(namespace: str, source_version: str, filters: dict[str, Any], builder: Callable[[], Any]) -> Any:
    key = (namespace, source_version, filter_key(filters))
    with _LOCK:
        if key in _CACHE:
            return deepcopy(_CACHE[key])

    value = builder()

    with _LOCK:
        _CACHE[key] = deepcopy(value)

    return value


def stats() -> dict[str, Any]:
    with _LOCK:
        namespaces: dict[str, int] = {}
        for namespace, _, _ in _CACHE:
            namespaces[namespace] = namespaces.get(namespace, 0) + 1
        return {"entries": len(_CACHE), "namespaces": namespaces}


def clear() -> None:
    with _LOCK:
        _CACHE.clear()

