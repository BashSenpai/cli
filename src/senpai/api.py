from requests import post as POST
from typing import Optional

from .config import Config
from .history import History


class API:
    """
    API is a class responsible for interacting with the BashSenpai API server.

    It encapsulates methods for user authentication and sending/receiving
    queries to/from the API server.

    Attributes:
        HOST: An URL to the BashSenpai API server.
        _config: A Config object storing the user settings.
        _history: A History object to maintain the log of user interactions.

    Usage:
        >>> api = API(config=config, history=history)
        >>> api.login('<your_auth_token>')
        >>> response = api.question('how do I create a new directory')
        >>> print(response)
    """

    # HOST = 'http://localhost:8000'
    HOST = 'https://api.bashsenpai.com'

    def __init__(self, config: Config, history: History) -> None:
        """
        Initializes the API object with user config and history.

        Args:
            config (Config): An instance of the Config class containing the user
                settings.
            history (History): An instance of the History class for storing the
                log of user interactions.
        """
        self._config = config
        self._history = history

    def login(self, token: str) -> dict[str, str]:
        """
        Authenticates the user with the BashSenpai API server using the provided
        token.

        Args:
            token (str): The authentication token provided by the user.

        Returns:
            dict: JSON response received from the API server indicating the
                result of the authentication process.
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
        Sends a question to the BashSenpai API server and returns the response.

        Args:
            question (str): The question to send to the API server.
            metadata Optional(dict[str, str]): Optional dictionary containing
                user environment metadata.

        Returns:
            dict: JSON response received from the API server containing the
                answer to the question or error message.

        Raises:
            Exception: In case of server communication issues or unexpected
                errors.
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
        except Exception as e:
            return {
                'error': True,
                'type': 'server',
                'message': 'Unknown server error occured: {str(e)}',
            }
