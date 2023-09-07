from dataclasses import dataclass
from enum import Enum

DataType = Enum('DataType', ['STRING', 'PERCENT', 'DOLLAR', 'NUMBER'])

@dataclass
class _Header:
    name: str
    data_type: DataType
    id: str
