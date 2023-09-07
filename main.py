from data_display.table import DataType, SortDirection, Table
from data_display.table_printer import print_table
from ui.main_menu import init_main_menu


def main():
    init_main_menu()
    # table = (Table('Terrific Table')
    #          .with_header('Col 1', DataType.STRING)
    #          .with_header('Col 2', DataType.DOLLAR)
    #          .with_header('Col 3', DataType.PERCENT)
    #          .with_header('Col 4', DataType.NUMBER)
    #          .with_row(['Nathan', 123, 42, 99999999+1.0/3.0])
    #          .with_row(['Phillip', 123456789, 321.9, -123])
    #          .with_row(['Balli', -987654321, 0, 12345.6789]))
    # print_table(table, '2', SortDirection.DESC)

if __name__ == "__main__":
    main()