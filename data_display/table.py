from enum import Enum
from typing import Self
from data_display.header import _Header, DataType
from data_display.row import _Row

# ASCII: https://theasciicode.com.ar/extended-ascii-code/box-drawing-character-double-line-lower-right-corner-ascii-code-188.html

SortDirection = Enum('SortDirection', ['ASC', 'DESC'])

class Table:
    def __init__(self, name: str=None):
        self.name = name
        self._headers: dict[str, _Header] = {}
        self._rows: dict[str, _Row] = {}
        self._header_id = -1
        self._row_id = -1

    def _get_next_header_id(self) -> str:
        self._header_id += 1
        return str(self._header_id)

    def _get_next_row_id(self) -> str:
        self._row_id += 1
        return str(self._row_id)
    
    def num_columns(self):
        return len(self._headers)
    
    def num_rows(self):
        return len(self._rows)
    
    def get_headers(self) -> dict[str, str]:
        return { h.id: h.name for h in self._headers }
    
    def get_rows(self):
        return { r.id: r.data for r in self._rows}

    def add_header(self, name: str, data_type: DataType=DataType.STRING) -> str:
        id = self._get_next_header_id()
        self._headers[id] = _Header(name, data_type, id)

    def with_header(self, name: str, data_type: DataType=DataType.STRING) -> Self:
        self.add_header(name, data_type)
        return self

    def remove_header(self, header_id: str) -> str:
        try:
            return self._headers.pop(header_id).id
        except KeyError:
            return None
    
    def add_row(self, data: list[any]) -> str:
        id = self._get_next_row_id()
        self._rows[id] = _Row(data, id)

    def with_row(self, data: list[any]) -> Self:
        self.add_row(data)
        return self
    
    def remove_row(self, row_id: str) -> str:
        try:
            return self._rows.pop(row_id).id
        except KeyError:
            return None

    def _validate_row(self):
        pass

    def _validate_header(self):
        pass