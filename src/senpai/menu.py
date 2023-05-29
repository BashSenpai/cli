import os
import subprocess

from .lib.user_input import clear_line, readkey, readinput, BASE_KEYS, OS_KEYS


class Menu:
    """
    Menu is responsible for prompting the user to execute commands provided as a
    list of strings.

    Once the display method is called, it runs in an endless loop until the user
    cancels the execution or there are no commands left to run. The user can
    choose to to edit or execute the currently selected command. Command
    selection is done using the arrow keys.

    Usage:
    >>> menu = Menu(commands=commands, colors=(command_color, comment_color))
    >>> menu.display()

    """

    def __init__(self, commands: list[str], colors: tuple[str, str]) -> None:
        """
        Initialize the menu with a list of commands to run.

        Args:
            options (list[str]): The options to select from.
            colors (tuple[str, str]): A tuple containing the command and comment
                color patterns.

        """
        self.commands = commands
        self.index = 0

        self.command_color = colors[0]
        self.comment_color = colors[1]

        self.terminal_size = os.get_terminal_size().columns

    def display(self) -> None:
        """
        Handles drawing the manu and handling all user input. Users can edit or
        run any command from the remaining commands in the list. Once a command
        is run, it's removed from the list. The execution ends once no commands
        are left in the list or the user aborts the execution either with the
        Q key, or by using the regular interrupts.

        """

        self._print_header()
        self._print_newlines()

        self.extra_lines = 0
        while True:
            # get the terminal width on each step
            self.terminal_size = os.get_terminal_size().columns

            for _ in range(len(self.commands) + 2 + self.extra_lines):
                clear_line()

            for index, command in enumerate(self.commands):
                # truncate longer commands
                if len(command) > self.terminal_size - 5:
                    command = f'{command[:self.terminal_size - 8]}...'

                if index == self.index:
                    print(self.command_color % f'👉 {command}')
                else:
                    print(self.comment_color % f'   {command}')

            self._print_separator()

            prompt_prefix = '🧰 Run: '
            print(
                self.command_color % prompt_prefix + \
                self.comment_color % self.commands[self.index],
            )

            # extra lines to clear if the prompt goes on more lines
            prompt_len = len(self.commands[self.index]) + len(prompt_prefix)
            self.extra_lines = (prompt_len - 1) // self.terminal_size

            # handle user input
            key = readkey()
            if key in [OS_KEYS.UP, 'k', 'K']:
                if self.index > 0:
                    self.index -= 1
            elif key in [OS_KEYS.DOWN, 'j', 'J']:
                if self.index < len(self.commands) - 1:
                    self.index += 1
            elif key in ['e', 'E']:
                self.edit()
            elif key in [BASE_KEYS.SPACE, OS_KEYS.ENTER]:
                self.execute()
                if self.commands:
                    self._print_header()
                    self._print_newlines()
            elif key in ['q', 'Q', BASE_KEYS.CTRL_D]:
                break

            if not self.commands:
                break

    def edit(self) -> None:
        """Edit the current selected command from the command list."""

        for _ in range(1 + self.extra_lines):
            clear_line()

        prompt_prefix = '📝 Edit: '
        self.commands[self.index] = readinput(
            self.command_color % prompt_prefix,
            self.commands[self.index],
        )

        # extra lines to clear if the prompt goes on more lines
        prompt_len = len(self.commands[self.index]) + len(prompt_prefix)
        self.extra_lines = (prompt_len - 1) // self.terminal_size

    def execute(self) -> None:
        """Execute the current selected command from the command list."""

        for _ in range(1 + self.extra_lines):
            clear_line()

        # get current command
        command = self.commands.pop(self.index)

        # print the execute prompt line
        print(
            self.command_color % f'🚀 Execute: ' + \
            self.comment_color % command
        )
        print('')

        # execute the command and print the result
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
            self.command_color % '⚙️  ' + \
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
        """Prints the expected new lines for a new menu prompt."""

        print('\n' * (len(self.commands) + 1))

    def _print_separator(self) -> None:
        """Prints a line separator."""

        print(self.comment_color % '—' * self.terminal_size)
