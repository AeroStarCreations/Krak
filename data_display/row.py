from dataclasses import dataclass


@dataclass
class _Row:
    data: list[any]
    id: str
