from pydantic import BaseModel
from typing import TypeVar, Callable, Type, Any, Dict

T = TypeVar("T")
F = TypeVar("F")


def compose(f: Callable[..., F], g: Callable[..., Any]) -> Callable[..., F]:
    return lambda *a, **kw: f(g(*a, **kw))


def is_type(data: Any, Data: Callable[..., Any]) -> bool:
    try:
        Data(**data)
        return True
    except ValueError:
        return False
