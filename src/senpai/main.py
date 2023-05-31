import argparse
import sys

from .senpai import BashSenpai


class SimpleNargsFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom argparse Formatter that skips metavar text formatting."""

    def _format_args(self, action, default_metavar):
        get_metavar = self._metavar_formatter(action, default_metavar)
        return '%s' % get_metavar(1)


# get __version__ from __init__.py
def get_version() -> str:
    """
    Get the current version of the application from __init__.py.

    Returns:
        str: The version of the application

    """

    from . import __version__
    return __version__


def main():
    """
    Entry point of the BashSenpai command-line interface.

    Parses the provided command line arguments and runs any provided commands.

    """

    # initialize bash senpai
    senpai = BashSenpai()

    # parse any command-line arguments
    parser = argparse.ArgumentParser(
        prog='senpai',
        usage='%(prog)s [options] command',
        description='BashSenpai command-line interface.',
        epilog='\n'.join([
            'available colors:',
            '  black, white, gray, red, greeen, yellow, blue, magenta and cyan',
            '  there are also brighter versions of each color, for example: "bright blue"',
            '  you can also make colors bold, for example: "bold red" or "bold bright cyan"',
            '',
            'available commands:',
            '  <ask a question>',
            '  login',
            '  become <persona>     # use "default" to revert back to normal messages',
            '',
            'example usage:',
            '  %(prog)s become angry pirate',
            '  %(prog)s how to disable ssh connections',
            '',
            'For more information, visit: https://bashsenpai.com/'
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
        help='question to ask or command to execute',
    )

    # check for empty arguments first
    if len(sys.argv) < 2:
        print('Error! No arguments provided. For list of available options, run:')
        print(f'{parser.prog} --help')
        sys.exit(1)

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
                sys.exit(1)
        senpai.config.set_value('command_color', command_color)
        senpai.config.write()

    if args.comment_color:
        comment_color = ' '.join(args.comment_color)
        comment_color = comment_color.lower().replace('grey', 'gray')
        for chunk in comment_color.split():
            if not chunk in color_chunks:
                print(f'Error! Can\'t parse "{chunk}".')
                sys.exit(1)
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
        sys.exit(0)

    prompt = args.prompt[0]
    if prompt == 'login':
        if len(args.prompt) > 1:
            print('Error! The login command takes no extra arguments.')
            sys.exit(1)

        # read the auth token from the stdin and send a login request
        token = input('Auth token: ')
        senpai.login(token)

    elif prompt == 'become':
        if len(args.prompt) == 1:
            print('Error! Please provide the persona you wish BashSenpai to use.')
            sys.exit(1)

        persona = ' '.join(args.prompt[1:])
        senpai.config.set_value('persona', persona)
        senpai.config.write()
        print('New persona confirmed.')

    else:
        question = ' '.join(args.prompt)
        senpai.ask_question(question)
