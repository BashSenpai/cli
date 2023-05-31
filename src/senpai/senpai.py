import os
from pathlib import Path
import platform
import sys
import textwrap
import time
from typing import Union

from .api import API
from .config import Config
from .history import History
from .menu import Menu
from .lib.color import parse_color
from .lib.user_input import clear_line


# default config storage based on OS type
if sys.platform in ('win32', 'cygwin'):
    CONFIG_BASE = Path(os.path.normpath(os.getenv('LOCALAPPDATA')))
elif sys.platform in ('darwin',):
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
    DASHBOARD_URL = 'https://bashsenpai.com/dashboard'

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

        self._api = API(config=self.config, history=self.history)

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

        # show the loading prompt
        terminal_height = os.get_terminal_size().lines
        print('\n' * (terminal_height - 1), end='')
        for _ in range(terminal_height - 1):
            clear_line()
        print(
            '⌛️ ' + self.comment_color % 'Your request is being processed...',
            end='',
        )
        sys.stdout.flush()

        # send an API call with the question and get a plain-text response
        response = self._api.question(question, metadata=self._get_metadata())

        # hide the loading prompt
        print('')
        clear_line()

        if response.get('error', False):
            print('Error! %s.' % response.get('message'))

            prog = self.config.get_value('prog')
            error_type = response.get('type', None)
            if error_type == 'auth':
                print(f'Run: {prog} login')
                sys.exit(2)
            elif error_type in ['timeout', 'server']:
                print('Try running the same command again a little later.')
                sys.exit(3)
            elif error_type == 'history':
                print(f'Try running: {prog} -n <question>')
                sys.exit(3)
            sys.exit(3)  # Unknown error

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
        formatted_response = ''
        commands = list()
        terminal_size = os.get_terminal_size().columns

        for line in response_text.splitlines():
            if line.startswith('#'):
                formatted_response += '\n'.join([
                    self.comment_color % line
                    for line in textwrap.wrap(line, terminal_size)
                ])

            else:
                # get the full command
                chunks = line.split(' # ', maxsplit=1)
                if len(chunks[0].strip()) > 0:
                    commands.append(chunks[0].strip())

                # text wrap
                color = self.command_color
                for i, wrapped in enumerate(textwrap.wrap(line, terminal_size)):
                    # split lines
                    if i > 0:
                        formatted_response += '\n'

                    # handle in-line comments
                    chunks = wrapped.split(' # ', maxsplit=1)
                    formatted_response += color % chunks[0]
                    if len(chunks) > 1:
                        # once we hit a comment, we change the color
                        color = self.comment_color
                        formatted_response += color % f' # {chunks[1]}'

            formatted_response += '\n'


        # print the formatted response with a typewriter effect
        for char in formatted_response:
            print(char, end='')
            sys.stdout.flush()
            if char.isprintable():
                time.sleep(0.0085)
        print('')
        time.sleep(0.55)

        # if command execution is enabled, generate the menu and run it
        if self.config.get_value('execute') and len(commands) > 0:
            menu = Menu(
                commands=commands,
                colors=(self.command_color, self.comment_color),
            )
            menu.display()

        # check if the tool is on the latest version, otherwise show a message
        latest_version = response.get('latest_version', '0')
        if latest_version > self.config.get_value('version'):
            print('')
            print('There is a new version available, please consider updating.')


    def login(self, token: str) -> None:
        """Validate the auth token and store it in the config file.

        Args:
            token (str): The auth token provided by the user.

        """

        # send an API call with the auth token and get a JSON response
        response = self._api.login(token)

        if not response['success']:
            if response['error']['code'] == 1:
                print('Error! No token provided.')
            elif response['error']['code'] == 2:
                print('Error! Invalid auth token provided.')
                print(f'Visit {self.DASHBOARD_URL} to retreive a valid token.')
            elif response['error']['code'] == 3:
                print('Error! Your user doesn\'t have a valid subscription.')
                print(f'Visit {self.DASHBOARD_URL} to subscribe.')
            sys.exit(2)

        # store the auth token in the config file
        self.config.set_value('token', token)
        self.config.write()

        print('Authentication successful.')

    def _get_metadata(self) -> Union[dict[str, str], None]:
        """
        Gets user system information to include with the prompt. The user may
        disable this functionality for privacy or other reasons.

        Returns:
            dict or None: Dictionary containing the user metadata.
        """

        if not self.config.get_value('metadata'):
            return None

        metadata = dict()

        if sys.platform in ('win32', 'cygwin'):  # windows
            metadata['os'] = 'Windows'
            metadata['version'] = platform.win32_ver()[0]

        elif sys.platform in ('darwin',):  # macos
            mac_ver = platform.mac_ver()
            metadata['os'] = 'macOS'
            metadata['version'] = mac_ver[0]
            metadata['arch'] = mac_ver[-1]
            metadata['shell'] = os.environ.get('SHELL', None)

        else:  # linux, freebsd, etc.
            metadata['os'] = 'Linux'
            metadata['version'] = None

            # raw-parse os-release as python 3.9 lacks freedesktop_os_release
            os_release_path = Path('/etc/os-release')
            if not os_release_path.exists():
                os_release_path = Path('/usr/lib/os-release')
                if not os_release_path.exists():
                    os_release_path = None

            if os_release_path:
                with open(os_release_path) as f:
                    os_release = f.read()

                for line in os_release.splitlines():
                    line = line.strip()
                    if line.upper().startswith('PRETTY_NAME'):
                        metadata['version'] = line.split('=')[1].strip('"\'')

            metadata['shell'] = os.environ.get('SHELL', None)

        return metadata
