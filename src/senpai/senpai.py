from pathlib import Path

from .api import API
from .config import Config
from .history import History


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

    CONFIG_DIR = Path.home() / '.config' / 'senpai'
    TERMINAL_COMMENT = '\x1B[37m%s\x1B[0m'
    TERMINAL_COMMAND = '\x1B[;1m\x1B[94m%s\x1B[0m'

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
                formatted_response += self.TERMINAL_COMMENT % line
            else:
                chunks = line.split(' # ', maxsplit=1)  # handle in-line comments
                formatted_response += self.TERMINAL_COMMAND % chunks[0]
                if len(chunks) > 1:
                    formatted_response += self.TERMINAL_COMMENT % f' # {chunks[1]}'
            formatted_response += '\n'

        return formatted_response
