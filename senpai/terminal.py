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
import os
import subprocess
import sys

from .lib.user_input import readkey, readinput, BASE_KEYS, OS_KEYS


class Terminal:
    """
    An object that handles all terminal manipulations and the command execution
    menu.

    This class provides an interactive menu for executing commands provided as a
    list of strings. The menu runs in an endless loop until the user
    cancels the execution or there are no commands left to run.

    Attributes:
        commands (list[str]): A list of commands provided to the menu to be run.
        index (int): The index of the currently selected command in the list.
        command_color (str): The ANSI color code used for printing for commands.
        comment_color (str): The ANSI color code for for printing comments.
        terminal_size (int): The width of the terminal in characters.
        extra_lines (int): The extra lines that need to be cleared on command
            wrapping.

    Usage:
        >>> terminal = Terminal(command_color, comment_color)
        >>> terminal.show_menu()
    """

    def __init__(self, command_color: str, comment_color: str) -> None:
        """
        Initialize the menu with a list of commands to run.

        Args:
            colors (tuple[str, str]): A tuple containing the command and comment
                color patterns.
        """
        self.command_color = command_color
        self.comment_color = comment_color

        self.terminal_size = os.get_terminal_size().columns

    def clear_line(self) -> None:
        """Clears any text from the last line in the console."""
        print(f'\x1B[1A\x1B[2K\r', end='')

    def hide_loading(self) -> None:
        """Hide the loading message."""
        print('\x1B[?25h', end='')  # show the cursor
        self.clear_line()

    async def show_loading(self) -> None:
        """
        Show a loading message while waiting for the response from the API.
        """
        # hide the cursor
        print('\x1B[?25l', end='')

        # separate the output from the shell command with a single line
        print('')

        # show the loading prompt
        terminal_height = os.get_terminal_size().lines
        print('\n' * (terminal_height - 1), end='')
        for _ in range(terminal_height - 1):
            self.clear_line()

        # animate the dots...
        i = 0
        backwards = True
        while True:
            print(
                self.comment_color % '⌛️ Your request is being processed',
                end='',
            )
            if backwards:
                print('.' * (2 - i))
            else:
                print('.' * (i + 1))
            sys.stdout.flush()

            i += 1
            if i == 3:
                backwards = not backwards
                i = 0

            await asyncio.sleep(0.55)
            self.clear_line()

    def show_menu(self, commands: list[str]) -> None:
        """
        Displays the menu and handles user input.

        In the menu, users can edit or run any command from the remaining
        commands in the list. Once a command is run, it's removed from the list.
        The execution ends once no commands are left in the list or the user
        aborts the execution either with the 'Q' key, or by using the regular
        interrupts.

        Args:
            commands (list[str]): The commands to select from.
        """
        self.commands = commands
        self.index = 0

        self._print_header()
        self._print_newlines()

        self.extra_lines = 0
        while True:
            # get the terminal width on each step
            self.terminal_size = os.get_terminal_size().columns

            for _ in range(len(self.commands) + 2 + self.extra_lines):
                self.clear_line()

            for index, command in enumerate(self.commands):
                # truncate longer commands
                if len(command) > self.terminal_size - 5:
                    command = f'{command[:self.terminal_size - 8]}...'

                if index == self.index:
                    print(self.command_color % f'👉 {command}')
                else:
                    print(self.comment_color % f'   {command}')

            self._print_separator()

            prompt_prefix = '🚀 Run: '
            print(
                self.command_color % prompt_prefix + \
                self.comment_color % self.commands[self.index],
            )

            # extra lines to clear if the prompt goes on more lines
            prompt_len = len(self.commands[self.index]) + len(prompt_prefix)
            self.extra_lines = prompt_len // self.terminal_size

            # handle user input
            key = readkey()
            if key in [OS_KEYS.UP, 'k', 'K']:
                if self.index > 0:
                    self.index -= 1
            elif key in [OS_KEYS.DOWN, 'j', 'J']:
                if self.index < len(self.commands) - 1:
                    self.index += 1
            elif key in ['e', 'E']:
                self._edit_command()
            elif key in [BASE_KEYS.SPACE, OS_KEYS.ENTER]:
                self._execute_command()
                if self.commands:
                    self._print_header()
                    self._print_newlines()
            elif key in ['q', 'Q', BASE_KEYS.CTRL_D]:
                break

            if not self.commands:
                break

    def _edit_command(self) -> None:
        """Allows the user to edit the currently selected command."""
        for _ in range(1 + self.extra_lines):
            self.clear_line()

        prompt_prefix = '📝 Edit: '
        self.commands[self.index] = readinput(
            self.command_color % prompt_prefix,
            self.commands[self.index],
        )

        # extra lines to clear if the prompt goes on more lines
        prompt_len = len(self.commands[self.index]) + len(prompt_prefix)
        self.extra_lines = prompt_len // self.terminal_size

    def _execute_command(self) -> None:
        """
        Executes the currently selected command and removes it from the command
        list.
        """

        # get current command
        command = self.commands.pop(self.index)

        # execute the command and print the result
        print('')
        command_result = subprocess.run(
            command,
            shell=True, capture_output=True, text=True,
        )
        if len(command_result.stdout.strip()):
            print(command_result.stdout)
        elif len(command_result.stderr.strip()):
            print(command_result.stderr)

        if self.index > 0:
            self.index -= 1

    def _print_header(self) -> None:
        """Prints the header of the menu."""
        self._print_separator()
        print(
            self.command_color % '💬 ' + \
            self.comment_color % 'Press ' + \
            self.command_color % '[Enter]' + \
            self.comment_color % ' to execute, ' + \
            self.command_color % '[E]' + \
            self.comment_color % ' to edit, or ' + \
            self.command_color % '[Q]' + \
            self.comment_color % ' to exit.'
        )
        self._print_separator()

    def _print_newlines(self) -> None:
        """Prints the new lines for a new menu prompt."""
        print('\n' * (len(self.commands) + 1))

    def _print_separator(self) -> None:
        """Prints a line separator."""
        print(self.comment_color % '—' * self.terminal_size)
