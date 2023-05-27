import json
from pathlib import Path
import os
import platform
from requests import post as POST
import sys
from typing import Union

from .config import Config
from .history import History


class API:
    """
    API handles the communication with the BashSenpai API server.

    It provides methods to authenticate the user, send questions to the API
    server, and retrieve the responses.

    Usage:
    >>> api = API(config=config, history=history)
    >>> api.login('<your_auth_token>')
    >>> response = api.question('how do I create a new directory')
    >>> print(response)

    """
    # HOST = 'http://localhost:8000'
    HOST = 'https://api.bashsenpai.com'

    def __init__(self, config: Config, history: History) -> None:
        """Initialize the API object.

        Args:
            config (Config): The Config object containing user configuration settings.
            history (History): The History object for storing user interaction history.

        """
        self._config = config
        self._history = history

    def login(self, token: str) -> None:
        """Validate the auth token and store it in the config file.

        Args:
            token (str): The auth token provided by the user.

        """

        # validate if the credentials are valid using our API
        response = POST(f'{self.HOST}/auth/', json={'token': token}).json()

        if not response['success']:
            if response['error']['code'] == 1:
                print('Error! No token provided.')
            elif response['error']['code'] == 2:
                print('Error! Invalid auth token provided.')
                print('Visit https://bashsenpai.com/dashboard for more information.')
            elif response['error']['code'] == 3:
                print('Error! Your user doesn\'t have a subscription.')
                print('Visit https://bashsenpai.com/dashboard and subscribe.')
            sys.exit(5)

        # store the auth token in the config file
        self._config.set_value('token', token)
        self._config.write()

    def question(self, question: str) -> str:
        """Send a question to the BashSenpai API server and receive a response.

        Args:
            question (str): The question to send to the API server.

        Returns:
            str: The response received from the API server.

        """

        token = self._config.get_value('token')
        if not token:
            prog = self._config.get_value('prog')
            print(f'You are not authenticated. First run:\n{prog} login')
            sys.exit(6)

        # send the question to our API
        response = POST(f'{self.HOST}/prompt/', json={
            'token': token,
            'persona': self._config.get_value('persona'),
            'question': question,
            'history': self._history.get_history(),
            'metadata': self.get_metadata(),
        })
        try:
            return response.json()
        except:
            return json.dumps({
                'error': True,
                'type': 'server',
                'message': 'Unknown server error occured',
            })

    def get_metadata(self) -> Union[dict[str, str], None]:
        """
        Gets user system information to include with the prompt. The user may
        disable this functionality for privacy or other reasons.

        Returns:
            dict or None: The dictionary containing the metadata.
        """

        if not self._config.get_value('metadata'):
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
