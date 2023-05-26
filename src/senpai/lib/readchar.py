# Initial code is borrowed from python-readchar:
# https://github.com/magmax/python-readchar
import sys

if sys.platform in ('win32', 'cygwin'):
    import msvcrt
    import win32console
else:
    import readline
    import termios


class BASE_KEYS:
    CTRL_C = '\x03'
    CTRL_D = '\x04'
    SPACE  = '\x20'


if sys.platform in ('win32', 'cygwin'):

    class SPECIFIC_KEYS:
        UP    = '\x00\x48'
        DOWN  = '\x00\x50'
        ENTER = '\x0D'

else:  # linux, macos

    class SPECIFIC_KEYS:
        UP    = '\x1B\x5B\x41'
        DOWN  = '\x1B\x5B\x42'
        ENTER = '\x0A'


def readchar() -> str:
    """
    Reads a single character from the input stream. Blocks until a character is
    available.

    """

    # handle for windows
    if sys.platform in ('win32', 'cygwin'):
        # manual byte decoding as some bytes in windows are not utf-8 encodable
        return chr(int.from_bytes(msvcrt.getch(), 'big'))

    # handle for linux and macos
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    term = termios.tcgetattr(fd)
    try:
        term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
        termios.tcsetattr(fd, termios.TCSAFLUSH, term)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readinput(prompt: str, default: str) -> str:
    """
    Reads user input with an extra default value provided and returns the result.

    Args:
        prompt (str): The default prompt to show when reading the input.
        default: The default value to set for editing.

    Returns:
        str: The value read from the user input.

    """

    # handle windows
    if sys.platform in ('win32', 'cygwin'):
        _stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)

        keys = []
        for c in str(default):
            evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            evt.Char = c
            evt.RepeatCount = 1
            evt.KeyDown = True
            keys.append(evt)

        _stdin.WriteConsoleInput(keys)
        return input(prompt)

    # handle linux and macos
    readline.set_startup_hook(
        lambda: readline.insert_text(default)
    )
    try:
        result = input(prompt)
    finally:
        readline.set_startup_hook()
    return result


def readkey() -> str:
    """
    Reads the next keypress. If an escaped key is pressed, the full sequence is
    read and returned.

    """

    c1 = readchar()

    if c1 == BASE_KEYS.CTRL_C:
        raise KeyboardInterrupt

    # handle for windows
    if sys.platform in ('win32', 'cygwin'):
        # if it is a normal character:
        if c1 not in '\x00\xE0':
            return c1

        # if it is a scpeal key, read second half:
        ch2 = readchar()
        return '\x00' + ch2

    # handle for linux and macos
    if c1 != '\x1B':
        return c1

    c2 = readchar()
    if c2 not in '\x4F\x5B':
        return c1 + c2

    c3 = readchar()
    if c3 not in '\x31\x32\x33\x35\x36':
        return c1 + c2 + c3

    c4 = readchar()
    if c4 not in '\x30\x31\x33\x34\x35\x37\x38\x39':
        return c1 + c2 + c3 + c4

    c5 = readchar()
    return c1 + c2 + c3 + c4 + c5
