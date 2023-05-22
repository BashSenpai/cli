import argparse
import sys

from .senpai import BashSenpai


def main():
    """Entry point of the BashSenpai command line interface."""

    # parse any command line arguments
    parser = argparse.ArgumentParser(
        prog='senpai',
        usage='%(prog)s [-h | --help] [-n | --new] prompt',
        description='BashSenpai command line interface.',
        epilog='\n'.join([
            'valid commands:',
            '%(prog)s login',
            '%(prog)s become <character>  # use "default" to revert back to normal comments',
            '',
            'example usage:',
            '%(prog)s become angry pirate',
            '%(prog)s how to disable ssh connections',
        ]),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    action = parser.add_argument(
        '-n', '--new',
        required=False,
        action=argparse.BooleanOptionalAction,
        help='ignore previous history when sending a question',
    )
    action.option_strings.remove('--no-new')

    parser.add_argument(
        'prompt',
        action='store',
        type=str,
        nargs='+',
        help='question to ask or command to execute',
    )

    args = parser.parse_args()

    # initialize bash senpai
    senpai = BashSenpai()

    # store the app name in the config
    senpai.config.set_value('prog', parser.prog)
    senpai.config.write()

    # clear the previous user history
    if args.new:
        senpai.history.clear()

    # parse the prompt
    match args.prompt[0]:
        case 'login':
            if len(args.prompt) > 1:
                print('Error! The login command takes no extra arguments.')
                sys.exit(1)

            # read the auth token from the stdin and send a login request
            token = input('Auth token: ')
            senpai.api.login(token)

        case 'become':
            if len(args.prompt) == 1:
                print('Error! Please provide the character you wish BashSenpai to impersonate.')
                sys.exit(2)

            persona = ' '.join(args.prompt[1:])
            senpai.config.set_value('persona', persona)
            senpai.config.write()
            print('New persona confirmed.')

        case _:
            question = ' '.join(args.prompt)
            response = senpai.ask_question(question)
            print(response)
