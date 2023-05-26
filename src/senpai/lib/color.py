# dictionary of all 4-bit ANSI colors
COLOR = {
    'black':   ('30', '30'),
    'white':   ('97', '97'),
    'gray':    ('90', '37'),
    'red':     ('31', '91'),
    'green':   ('32', '92'),
    'yellow':  ('33', '93'),
    'blue':    ('34', '94'),
    'magenta': ('35', '95'),
    'cyan':    ('36', '96'),
}

def parse_color(color: str) -> str:
    """Conver color name to ANSI-formatted string.

    Args:
        color (str): The color name to parse.

    Returns:
        str: ANSI-formatted string representing the color.

    """

    pos = 1 if 'bright' in color else 0
    col_prefix = '\x1B[;1m' if 'bold' in color else ''
    for col_name, col_values in COLOR.items():
        if col_name in color:
            return f'{col_prefix}\x1B[{col_values[pos]}m%s\x1B[0m'
