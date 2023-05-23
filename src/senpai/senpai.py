import os
from pathlib import Path
import sys

from .api import API
from .config import Config
from .history import History


# default config storage based on OS type
if sys.platform.startswith('win'):
    CONFIG_BASE = Path(os.path.normpath(os.getenv('LOCALAPPDATA')))
elif sys.platform.startswith('darwin'):
    CONFIG_BASE = Path.home() / 'Library' / 'Application Support'
else:  # linux, freebsd, etc.
    CONFIG_BASE = Path.home() / '.config'


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


class BashSenpai:
    """
    BashSenpai is a tool that helps new Linux users work in the terminal by
    providing the ability to ask questions about commands or features directly
    from the terminal.

    It interacts with the BashSenpai API to send questions and receive formatted
    responses. The API provides concise explanations and commands for Linux
    shell environments using ChatGPT as a backend.

    The tool maintains a configuration file, user history, and uses ANSI escape
    sequences for formatting the response output with colored text.

    Usage:
    >>> senpai = BashSenpai()
    >>> response = senpai.ask_question('How do I list files in a directory')
    >>> print(response)

    """

    CONFIG_DIR = CONFIG_BASE / 'senpai'

    def __init__(self) -> None:
        """Initialize the BashSenpai object.

        Creates the configuration directory if it doesn't exist and initializes
        the `config`, `history`, and `api` objects.

        """

        # create config dir if it doesn't exist
        path = Path(self.CONFIG_DIR)
        path.mkdir(parents=True, exist_ok=True)

        self.config = Config(path=self.CONFIG_DIR)
        self.history = History(path=self.CONFIG_DIR)
        self.api = API(config=self.config, history=self.history)

        # parse colors
        self.command_color = parse_color(self.config.get_value('command_color'))
        self.comment_color = parse_color(self.config.get_value('comment_color'))

    def ask_question(self, question: str) -> str:
        """Send a question to the BashSenpai API and return a formatted response.

        Args:
            question (str): The question to send to the API.

        Returns:
            str: The response from the API formatted with huepy.

        """

        # send an API call with the question and get a plain-text response
        response = self.api.question(question)

        # write the new question/answer pair in the user history
        self.history.add({'question': question, 'answer': response})
        self.history.write()

        # format the response using huepy
        formatted_response = '\n'
        for line in response.splitlines():
            if line.startswith('#'):
                formatted_response += self.comment_color % line
            else:
                chunks = line.split(' # ', maxsplit=1)  # handle in-line comments
                formatted_response += self.command_color % chunks[0]
                if len(chunks) > 1:
                    formatted_response += self.comment_color % f' # {chunks[1]}'
            formatted_response += '\n'

        return formatted_response
