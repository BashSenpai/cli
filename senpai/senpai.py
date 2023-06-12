# Copyright 2023 Bogdan Tatarov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import os
from pathlib import Path
import platform
from requests import Response
import sys
from typing import Callable, Union

from .api import API
from .data.config import Config
from .data.history import History
from .lib.color import parse_color
from .terminal import Terminal


# default config storage based on OS type
if sys.platform in ('win32', 'cygwin'):
    CONFIG_BASE = Path(os.path.normpath(os.getenv('LOCALAPPDATA')))
elif sys.platform in ('darwin',):
    CONFIG_BASE = Path.home() / 'Library' / 'Application Support'
else:  # linux, freebsd, etc.
    CONFIG_BASE = Path.home() / '.config'


class BashSenpai:
    """
    BashSenpai is a tool that provides assistance to new Linux users working in
    the terminal. It allows users to ask questions about commands or features
    directly from the terminal.

    BashSenpai interacts with an API to send questions and receive formatted
    responses. The API provides concise explanations and commands for Linux
    shell environments using ChatGPT as a backend. It maintains a configuration
    file, user history, shows the menu for executing returned commands, and
    formats response output with configurable colors converted to ANSI-escaped
    sequences.

    Attributes:
        CONFIG_DIR (Path): The directory where configuration files are stored.
        DASHBOARD_URL (str): The URL for the dashboard of the application.
        config (Config): The configuration object managing the settings..
        history (History): The history object managing the user's interactions.
        terminal (Terminal): Object for manipulating the content on the screen.
        api (API): The API object managing the communication with the backend.
        command_color (str): The ANSI color code for commands.
        comment_color (str): The ANSI color code for comments.
        endline_color (str): THe ANSI color code to end the line.

    Usage:
        >>> senpai = BashSenpai()
        >>> senpai.ask_question('how do I list files in a directory')
        >>> senpai.explain('tar')
    """

    CONFIG_DIR = CONFIG_BASE / 'senpai'
    DASHBOARD_URL = 'https://bashsenpai.com/dashboard'

    def __init__(self) -> None:
        """
        Initialize the BashSenpai object.

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
        command_color = parse_color(self.config.get_value('command_color'))
        comment_color = parse_color(self.config.get_value('comment_color'))

        self.terminal = Terminal(command_color, comment_color)

        self.command_color, self.endline_color = command_color.split('%s')
        self.comment_color, _ = comment_color.split('%s')


    async def ask_question(self, question: str) -> None:
        """
        Send a question to the BashSenpai API and print a formatted response.

        If the user has command execution enabled, shows the menu for executing
        each command.

        Args:
            question (str): The question to send to the API.

        Raises:
            SystemExit: If an error occurs while parsing the response received
                from the API.
        """
        # send an API call with a question and get the response
        metadata = self._get_metadata()
        task = self.api.question
        response = await self._run_async_prompt(task, question, metadata)

        # if the response is a dict, it already contains an error
        if not isinstance(response, dict):
            response = self._parse_response(response)

        # check the response for errors
        self._handle_response_errors(response)

        # update the history
        self.history.add({
            'question': question,
            'answer': response.get('response'),
            'persona': response.get('persona'),
        })
        self.history.write()

        # if command execution is enabled, generate the menu and run it
        commands = response.get('commands')
        if self.config.get_value('execute') and commands:
            self.terminal.show_menu(commands=commands)

        # check if the tool is on the latest version, otherwise show a message
        self._check_version(response.get('version'))

    async def explain(self, command: str) -> None:
        """
        Send a request to the BashSenpai API to explain the usage of a shell
        command or a tool and print a formatted response.

        Args:
            command (str): The command to send to the API.

        Raises:
            SystemExit: If an error occurs while parsing the response received
                from the API.
        """
        # send an async API call with the command
        response = await self._run_async_prompt(self.api.explain, command)

        # if the response is a dict, it already contains an error
        if not isinstance(response, dict):
            response = self._parse_response(response)

        # check the response for errors
        self._handle_response_errors(response)

        # TODO: different interactive menu

        # check if the tool is on the latest version, otherwise show a message
        self._check_version(response.get('version'))

    async def login(self, token: str) -> None:
        """
        Validate the auth token and store it in the config file.

        Args:
            token (str): The auth token provided by the user.

        Raises:
            SystemExit: If there is an error with the authentication process.
        """
        response = await self.api.login(token)

        if not response['success']:
            if response['error']['code'] == 1:
                print('Error! No token provided.')
            elif response['error']['code'] == 2:
                print('Error! Invalid auth token provided.')
                print(f'Visit {self.DASHBOARD_URL} to retreive a valid token.')
            elif response['error']['code'] == 3:
                print('Error! Your user doesn\'t have a valid subscription.')
                print(f'Visit {self.DASHBOARD_URL} to subscribe.')
            raise SystemExit(2)

        # store the auth token in the config file
        self.config.set_value('token', token)
        self.config.write()

        print('Authentication successful.')

    async def _run_async_prompt(
        self,
        prompt_fn: Callable,
        *args,
    ) -> Union[Response, dict[str, str]]:
        """
        Animates the loading dots while waiting for the response.

        Args:
            prompt_fn (Callable): The API method to call
            *args: optional arguments to pass to the call

        Returns:
            Response | dict[str, str]: An API call response or an error.
        """
        async def run_prompt():
            global response
            response = await prompt_fn(*args)
            raise asyncio.CancelledError

        tasks = (run_prompt(), self.terminal.show_loading(),)
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            self.terminal.hide_loading()
            return response

    def _check_version(self, latest_version: str) -> None:
        """
        Check and notify if there's a new version of the CLI available.

        Args:
            latest_version (str): The latest version as a string.
        """
        if latest_version and latest_version > self.config.get_value('version'):
            print('')
            print('There is a new version available, please consider updating.')

    def _get_metadata(self) -> Union[dict[str, str], None]:
        """
        Gets user system information to include with the prompt.

        The user may disable this functionality for privacy or other reasons.

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

    def _handle_response_errors(self, response_data: dict[str, str]) -> None:
        """
        Validate the API response and handle errors.

        Args:
            response_data (dict): The response data from the API.

        Raises:
            SystemExit: If an error is found in the response data.
        """
        if response_data.get('error', False):
            print('Error! %s.' % response_data.get('message'))

            prog = self.config.get_value('prog')
            error_type = response_data.get('type', None)
            if error_type == 'auth':
                print(f'Run: {prog} login')
                raise SystemExit(2)
            elif error_type in ['timeout', 'server']:
                print('Try running the same command again a little later.')
                raise SystemExit(3)
            elif error_type == 'history':
                print(f'Try running: {prog} -n <question>')
                raise SystemExit(3)
            raise SystemExit(3)  # Unknown error

    def _parse_response(self, response: Response) -> dict[str, str]:
        """
        Parses the response received from the API.

        If there are no errors, prints the streamed response and returns a
        dictionary with all parsed data. Otherwise returns the error.

        Args:
            response (Response): The response object received from the API.

        Returns:
            dict: JSON data wtih all the parsed data from the response.
        """
        latest_version = None
        original_response = None
        printed_response = ''

        new_line = None
        new_line_text = ''
        new_line_type = None
        commands = list()
        for chunk in response.iter_lines(chunk_size=None):
            chunk = json.loads(chunk)

            # check for errors
            if 'error' in chunk:
                return chunk

            # parse the version
            if 'latest_version' in chunk:
                latest_version = chunk['latest_version']
                if 'original_response' in chunk:
                    original_response = chunk['original_response']
                continue

            if 'end' in chunk and chunk['end']:
                # append last command and stop
                if new_line_type == 'command':
                    commands.append(new_line_text)
                break

            if 'content' in chunk:
                printed_response += chunk['content']
                chunk = chunk['content']
                if chunk == '\n':
                    new_line = True
                    continue

                if new_line:
                    if new_line_text:
                        print(self.endline_color)
                    if new_line_type == 'command':
                        commands.append(new_line_text)
                    new_line_text = ''

                new_line_text += chunk
                # determine line type and separate commands
                if new_line or chunk.startswith('>'):
                    if chunk.startswith('$'):
                        new_line_type = 'command'
                        chunk = chunk.lstrip('$ ')
                        print(self.command_color, end='')
                    elif chunk.startswith('>'):
                        new_line_type = 'command'
                        print(self.comment_color, end='')
                    else:
                        if new_line_type == 'command':
                            print('')
                        print(self.comment_color, end='')
                        new_line_type = 'comment'

                # strip command indicator from new line and chunk
                new_line_text = new_line_text.lstrip('$')
                if new_line_text.startswith(' '):
                    new_line_text = new_line_text.lstrip()
                    chunk = chunk.lstrip()

                if new_line_text and chunk:
                    print(chunk, end='')
                    sys.stdout.flush()

                new_line = False

        print('\n')

        if original_response:
            return {
                'latest_version': latest_version,
                'response': original_response,
                'persona': printed_response,
                'commands': commands,
            }

        else:
            return {
                'latest_version': latest_version,
                'response': printed_response,
                'persona': None,
                'commands': commands,
            }
