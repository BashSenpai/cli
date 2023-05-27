import os
from pathlib import Path
import sys

from .api import API
from .config import Config
from .history import History
from .menu import Menu
from .lib.color import parse_color


# default config storage based on OS type
if sys.platform.startswith('win'):
    CONFIG_BASE = Path(os.path.normpath(os.getenv('LOCALAPPDATA')))
elif sys.platform.startswith('darwin'):
    CONFIG_BASE = Path.home() / 'Library' / 'Application Support'
else:  # linux, freebsd, etc.
    CONFIG_BASE = Path.home() / '.config'


class BashSenpai:
    """
    BashSenpai is a tool that helps new Linux users work in the terminal by
    providing the ability to ask questions about commands or features directly
    from the terminal.

    It interacts with the BashSenpai API to send questions and receive formatted
    responses. The API provides concise explanations and commands for Linux
    shell environments using ChatGPT as a backend.

    The tool maintains a configuration file, user history, can generate a menu
    for executing the returned commands, and uses configurable colors converted
    to ANSI-escaped sequences for formatting the response output.

    Usage:
    >>> senpai = BashSenpai()
    >>> senpai.ask_question('How do I list files in a directory')

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

    def ask_question(self, question: str) -> None:
        """
        Send a question to the BashSenpai API and print a formatted response. If
        the user has command execution enabled, generates a menu for executing
        each command.

        Args:
            question (str): The question to send to the API.

        """

        # send an API call with the question and get a plain-text response
        response = self.api.question(question)

        if response.get('error', False):
            print('Error! %s.' % response.get('message'))

            prog = self.config.get_value('prog')
            error_type = response.get('type', None)
            if error_type == 'auth':
                print(f'Run first: {prog} login')
                sys.exit(6)
            elif error_type in ['timeout', 'server']:
                print('Try running the same command again a little later.')
                sys.exit(7)
            elif error_type == 'history':
                print(f'Try running: {prog} -n <question>')
                sys.exit(8)
            sys.exit(9)  # Unknown error

        # write the new question/persona pair in the user history
        self.history.add({
            'question': question,
            'answer': response.get('response', ''),
            'persona': response.get('persona', None),
        })
        self.history.write()

        # determine whether to show the regular response or the persona one
        response_text = response.get('response', '')
        persona_text = response.get('persona', None)
        if persona_text:
            response_text = persona_text

        # format the response and collect a list of commands
        commands = list()
        formatted_response = '\n'
        for line in response_text.splitlines():
            if line.startswith('#'):
                formatted_response += self.comment_color % line
            else:
                chunks = line.split(' # ', maxsplit=1)  # handle in-line comments
                if len(chunks[0].strip()) > 0:
                    commands.append(chunks[0].strip())
                formatted_response += self.command_color % chunks[0]
                if len(chunks) > 1:
                    formatted_response += self.comment_color % f' # {chunks[1]}'
            formatted_response += '\n'

        # print the formatted response
        print(formatted_response)

        # if command execution is enabled, generate the menu and run it
        if self.config.get_value('execute') and len(commands) > 0:
            menu = Menu(
                commands=commands,
                colors=(self.command_color, self.comment_color),
            )
            menu.display()
