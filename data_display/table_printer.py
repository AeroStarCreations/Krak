
import re
from data_display.header import _Header, DataType
from data_display.row import _Row
from data_display.table import SortDirection, Table
from ui.format_constants import *
from ui.input_output import CBG, CFG, RGBBG, RGBFG, print_with_basic_border, println

_is_dark_theme = True

# Light theme
_BG = CBG(254)
_BORDER = _BG + RGBFG(101, 39, 190)
_TXT1 = _BG + RGBFG(78, 49, 170)
_TXT2 = _BG + RGBFG(58, 16, 120)

# Dark theme
if _is_dark_theme:
    _BG = CBG(233)
    _BORDER = _BG + RGBFG(150, 129, 235)
    _TXT1 = _BG + RGBFG(69, 207, 221)
    _TXT2 = _BG + RGBFG(167, 237, 231)

def _true_len(string: str):
    # Credit: https://stackoverflow.com/a/68635860
    return len(re.sub(r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', string))

def _get_longest_len(items: list[str]) -> int:
    return _true_len(max(items, key=_true_len))

def _print_table_name(table: Table):
    if not table.name:
        return
    name_len = _true_len(table.name)
    println(_BORDER, ' ╔═', '═' * name_len, '═╗ ')
    println(_BORDER, ' ║ ', _TXT1, B, table.name, _BORDER, ' ║ ')
    println(_BORDER, ' ╠═', '═' * name_len, '═╝ ')

def _get_column_widths(headers: list[_Header], rows: list[_Row]) -> list[int]:
    cw = []
    # For each column
    for i, header in enumerate(headers):
        column_data = [header.name]
        # For each row cell
        for row in rows:
            data = row.data
            if i < len(data):
                match header.data_type:
                    case DataType.STRING:
                        column_data.append(str(data[i]))
                    case DataType.NUMBER:
                        column_data.append(f'{data[i]:,}')
                    case DataType.PERCENT:
                        column_data.append(f'{data[i]:,} %')
                    case DataType.DOLLAR:
                        column_data.append(f'$ {data[i]:,}')
                    case _:
                        raise Exception(f'Uknown DataType {header.data_type}')
        cw.append(_get_longest_len(column_data))
    return cw

def _print_headers(has_name: bool, headers: list[_Header], widths: list[int]):
    top = ' ╔═'
    if has_name:
        top = ' ╠═'
    mid = ' ║ '
    bot = ' ╚═'
    for i, header in enumerate(headers):
        top += '═' * widths[i] + '═╦═'
        mid += f'{_TXT1}{header.name:^{widths[i]}}{_BORDER} ║ '
        bot += '═' * widths[i] + '═╩═'
    top = top[:-2] + '╗ '
    mid = mid[:-1] + ' '
    bot = bot[:-2] + '╝ '
    println(_BORDER, top)
    println(_BORDER, B, mid)
    println(_BORDER, bot)

def _print_rows(headers: list[_Header], rows: list[_Row], widths: list[int]):
    if len(widths) < len(headers):
        raise Exception('Not enough width data')
    for row in rows:
        data = row.data
        mid = ' │ '
        bot = ' ├─'
        for i, header in enumerate(headers):
            bot += '─' * widths[i] + '─┼─'
            if i >= len(data):
                mid += ' ' * widths[i]
            else:
                data_str = ''
                match header.data_type:
                    case DataType.STRING:
                        data_str += f'{data[i]:{widths[i]}}'
                    case DataType.NUMBER:
                        data_str += f'{data[i]:>{widths[i]},}'
                    case DataType.PERCENT:
                        data_str += f'{data[i]:>{widths[i]-2},} {C}%'
                    case DataType.DOLLAR:
                        data_str += f'{G}${_TXT2} {data[i]:>{widths[i]-2},}'
                    case _:
                        raise Exception(f'Uknown DataType {header.data_type}')
                mid += f'{_TXT2}{data_str}{_BORDER}'
            mid += ' │ '
        mid = mid[:-1] + ' '
        bot = bot[:-2] + '┤ '
        println(_BORDER, mid)
        println(_BORDER, bot)
    bot = ' └─'
    for w in widths:
        bot += '─' * w + '─┴─'
    println(UL, _BORDER, bot[:-2], '┘ ')


def _print_table(table: Table, header_id: str, sort_direction: SortDirection):
    headers = list(table._headers.values())
    rows = list(table._rows.values())
    # Sorting -------
    if header_id:
        index = 0
        for i, header in enumerate(headers):
            if header.id == header_id:
                index = i
                break
        rows.sort(key=lambda r: r.data[index], reverse=sort_direction==SortDirection.DESC)
        headers[index].name += f'{_BORDER} ↑' if sort_direction==SortDirection.ASC else f'{_BORDER} ↓'
    # ---------------
    col_widths = _get_column_widths(headers, rows)
    _print_headers(table.name, headers, col_widths)
    _print_rows(headers, rows, col_widths)

def print_table(table: Table, sort_by_header_id: str=None, sort_direction: SortDirection=SortDirection.ASC):
    if sort_by_header_id:
        assert sort_by_header_id in table._headers
    _print_table_name(table)
    _print_table(table, sort_by_header_id, sort_direction)
