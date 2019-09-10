"""PRINT_PRETTY_FOrMAT function"""

COL_SIZE = 25
SP = ': '


def print_format_pretty(desc, val):
    """Prints out a string and value in formatted columns. The left columnnwidth is determined
    by COL_SIZE module global"""
    print('{0}{1}{2}'.format(str(desc).ljust(COL_SIZE), SP, val))