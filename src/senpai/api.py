from requests import post as POST
from typing import Optional

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
            config (Config): Config object containing the user settings.
            history (History): History object for storing previous interactions.

        """
        self._config = config
        self._history = history

    def login(self, token: str) -> None:
        """
        Send an auth request to the BasiSenpai API server and return the
        response.

        Args:
            token (str): The auth token provided by the user.

        Returns:
            dict: JSON response received from the API.

        """

        # validate the auth token using our API
        json_data = {
            'token': token,
        }
        response = POST(f'{self.HOST}/auth/', json=json_data).json()
        return response

    def question(
            self,
            question: str,
            metadata: Optional[dict[str, str]] = None,
        ) -> dict[str, str]:
        """
        Send a question to the BashSenpai API server and return the response.

        Args:
            question (str): The question to send to the API server.
            metadata Optional(dict): Optional user environment metadata.

        Returns:
            dict: JSON response received from the API.

        """

        # check if the user is authenticated
        token = self._config.get_value('token')
        if not token:
            return {
                'error': True,
                'type': 'auth',
                'message': 'You are not authenticated',
            }

        # send the question to our API
        try:
            json_data = {
                'token': token,
                'version': self._config.get_value('version'),
                'persona': self._config.get_value('persona'),
                'question': question,
                'history': self._history.get_history(),
                'metadata': metadata,
            }
            response = POST(f'{self.HOST}/prompt/', json=json_data)
            return response.json()
        except:
            return {
                'error': True,
                'type': 'server',
                'message': 'Unknown server error occured',
            }
