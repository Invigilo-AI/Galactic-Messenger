from pydantic import BaseModel, create_model_from_typeddict
from typing import TypeVar, Callable, Type, Any, Dict

T = TypeVar("T")
F = TypeVar("F")


def compose(f: Callable[..., F], g: Callable[..., Any]) -> Callable[..., F]:
    return lambda *a, **kw: f(g(*a, **kw))


def is_schema(data: Any, typedData: Type) -> bool:
    try:
        Schema = create_model_from_typeddict(typedData)
        Schema(**data)
        return True
    except ValueError:
        return False
