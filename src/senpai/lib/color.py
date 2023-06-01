import sys

# Dictionary of all 4-bit ANSI colors
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
    """
    Convert a color name to an ANSI-formatted string.

    Args:
        color (str): The name of the color to be parsed. Valid color names
            include 'black', 'white', 'gray', 'red', 'green', 'yellow', 'blue',
            'magenta', and 'cyan'. The color name can be optionally preceded
            by 'bright' or 'bold' to create bright or bold color codes.

    Returns:
        str: ANSI-formatted string representing the color. The string includes
            escape sequences for changing the color of text on ANSI-compliant
            terminals. The returned string follows the format
            '\x1B[<color-code>m', where <color-code> is an ANSI color code.

    Note:
        If the system platform is either 'win32' or 'cygwin', the returned
        string does not include the initial '\1' and trailing '\2' characters.
        These are included on other platforms to enable changing the color of a
        portion of text, with the color change ending at the '\2' character.
    """
    pos = 1 if 'bright' in color else 0
    col_prefix = '\1\x1B[;1m\2' if 'bold' in color else ''
    for col_name, col_values in COLOR.items():
        if col_name in color:
            color = f'{col_prefix}\1\x1B[{col_values[pos]}m\2%s\1\x1B[0m\2'

            if sys.platform in ('win32', 'cygwin'):
                color = color.replace('\1', '').replace('\2', '')

            return color
