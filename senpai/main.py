"""
BashSenpai - A terminal assistant powered by ChatGPT.

This is the main entry point for the BashSenpai command line application.
It parses any command-line arguments and provides a get_version() function.

Copyright 2023 Bogdan Tatarov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import argparse
import sys

from .senpai import BashSenpai


class SimpleNargsFormatter(argparse.RawDescriptionHelpFormatter):
    """
    Custom argparse Formatter that skips metavar text formatting.

    This formatter is designed to avoid repetition of metavar text in the help
    output when nargs is used. The _format_args method is overridden to achieve
    this.
    """

    def _format_args(self, action: argparse.Action, default_metavar: str) -> str:
        """
        Returns a string representing the argument(s), replacing the default
        metavar.

        Args:
            action (argparse.Action): The action object containing information
                about the argument.
            default_metavar (str): The default metavar for the argument.

        Returns:
            str: A string representing the formatted argument(s).
        """
        get_metavar = self._metavar_formatter(action, default_metavar)
        return '%s' % get_metavar(1)


def get_version() -> str:
    """
    Get the current version of the application from __init__.py.

    The version is retrieved by importing the __version__ attribute from the
    __init__.py file.

    Returns:
        str: The version of the application as a string.
    """
    from . import __version__
    return __version__


async def run():
    """
    Entry point of the BashSenpai command-line interface.

    This function initializes the BashSenpai object, parses the provided
    command-line arguments, validates and sets the appropriate configurations
    based on the arguments, and handles any provided prompt.

    Raises:
        SystemExit: If an error occurs while parsing the command line arguments
            or setting configurations.
    """

    # initialize bash senpai
    senpai = BashSenpai()

    # parse any command-line arguments
    parser = argparse.ArgumentParser(
        prog='senpai',
        usage='%(prog)s [options] prompt',
        description='BashSenpai command-line interface.',
        epilog='\n'.join([
            'colors:',
            '  black, white, gray, red, greeen, yellow, blue, magenta and cyan',
            '  There are also brighter versions of each color, for example: "bright blue"',
            '  You can also make colors bold, for example: "bold red" or "bold bright cyan"',
            '',
            'prompts:',
            '  login                authenticate using your auth token',
            '  <question>           ask any shell-related question using common language',
            '  explain <command>    show most common use cases for a specific command',
            '  become <persona>     change the persona of BashSenpai, use "default" to reset',
            '',
            'example usage:',
            '  %(prog)s login',
            '  %(prog)s become angry pirate',
            '  %(prog)s explain tar',
            '  %(prog)s how to disable ssh connections',
            '',
            'For more information, visit: https://bashsenpai.com/docs'
        ]),
        formatter_class=SimpleNargsFormatter,
    )

    action = parser.add_argument(
        '-n', '--new',
        action=argparse.BooleanOptionalAction,
        help='ignore previous history when sending a question',
    )
    action.option_strings.remove('--no-new')

    action = parser.add_argument(
        '--command-color',
        type=str,
        metavar='col',
        nargs='+',
        help='set color for the commands, check the "available colors" ' + \
             'section for a list of all available options',
    )

    action = parser.add_argument(
        '--comment-color',
        type=str,
        metavar='col',
        nargs='+',
        help='set color for the comments',
    )

    action = parser.add_argument(
        '--meta',
        action=argparse.BooleanOptionalAction,
        default=senpai.config.get_value('metadata'),
        help='send information about your OS to imporove the responses',
    )

    action = parser.add_argument(
        '--run',
        action=argparse.BooleanOptionalAction,
        default=senpai.config.get_value('execute'),
        help='show menu prompt to execute each returned command',
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        help='show current version',
        version='%(prog)s ' + get_version(),
    )

    parser.add_argument(
        'prompt',
        action='store',
        type=str,
        nargs='*',
        metavar='<prompt>',
        help='ask a question or execute a special command',
    )

    # check for empty arguments first
    if len(sys.argv) < 2:
        print('Error! No arguments provided. For list of available options, run:')
        print(f'{parser.prog} --help')
        raise SystemExit(1)

    # parse the arguments
    args = parser.parse_args()

    # store the app name and version in the config
    senpai.config.set_value('prog', parser.prog)
    senpai.config.set_value('version', get_version())
    senpai.config.write()

    # set colors
    color_chunks = (
        'bold', 'bright', 'black', 'white', 'gray', 'red',
        'green', 'yellow', 'blue', 'magenta', 'cyan',
    )

    if args.command_color:
        command_color = ' '.join(args.command_color)
        command_color = command_color.lower().replace('grey', 'gray')
        for chunk in command_color.split():
            if not chunk in color_chunks:
                print(f'Error! Can\'t parse "{chunk}".')
                raise SystemExit(1)
        senpai.config.set_value('command_color', command_color)
        senpai.config.write()

    if args.comment_color:
        comment_color = ' '.join(args.comment_color)
        comment_color = comment_color.lower().replace('grey', 'gray')
        for chunk in comment_color.split():
            if not chunk in color_chunks:
                print(f'Error! Can\'t parse "{chunk}".')
                raise SystemExit(1)
        senpai.config.set_value('comment_color', comment_color)
        senpai.config.write()

    # whether to send OS metadata
    if args.meta:
        senpai.config.set_value('metadata', True)
    else:
        senpai.config.set_value('metadata', False)
    senpai.config.write()

    # whether to execute the provided commands
    if args.run:
        senpai.config.set_value('execute', True)
    else:
        senpai.config.set_value('execute', False)
    senpai.config.write()

    # clear the previous user history
    if args.new:
        senpai.history.clear()

    # parse the prompt
    if not args.prompt:
        raise SystemExit(0)

    prompt = args.prompt[0]
    if prompt == 'login':
        if len(args.prompt) > 1:
            print('Error! The "login" prompt takes no extra arguments.')
            raise SystemExit(1)

        # read the auth token from the stdin and send a login request
        token = input('Auth token: ')
        await senpai.login(token)

    elif prompt == 'become':
        if len(args.prompt) == 1:
            print('Error! Please provide the persona you wish BashSenpai to use.')
            raise SystemExit(1)

        persona = ' '.join(args.prompt[1:])
        senpai.config.set_value('persona', persona)
        senpai.config.write()
        print('New persona confirmed.')

    elif prompt == 'explain' and len(args.prompt) < 3:
        if len(args.prompt) == 1:
            print('Error! The "explain" prompt takes one extra argument in the form of a command name.')
            raise SystemExit(1)
        await senpai.explain(args.prompt[1])

    else:
        question = ' '.join(args.prompt)
        await senpai.ask_question(question)


def main():
    """Runs the CLI in async mode."""
    asyncio.run(run())


if __name__ == '__main__':
    main()
