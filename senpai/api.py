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
from requests import post as POST, Response
from typing import Optional, Union

from .data.config import Config
from .data.history import History


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
        >>> response = api.explain('ffmpeg')
    """

    # HOST = 'http://localhost:8000/v1'
    HOST = 'https://api.bashsenpai.com/v1'

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

    async def explain(self, command: str) -> Union[Response, dict[str, str]]:
        """
        Explains the given command by querying the BashSenpai API.

        Args:
            command (str): The command to be explained.

        Returns:
            Resonse | dict: The API response or an error message if the user is
                not authenticated or if an unknown server error occurs.

        Raises:
            Exception: In case of server communication issues or other errors.
        """
        # check if the user is authenticated first
        token = self._config.get_value('token')
        if not token:
            return {
                'error': True,
                'type': 'auth',
                'message': 'You are not authenticated',
            }

        # send the question to our API
        try:
            data = {
                'token': token,
                'version': self._config.get_value('version'),
                'persona': self._config.get_value('persona'),
                'question': command,
            }
            return await asyncio.to_thread(
                POST, f'{self.HOST}/explain/', json=data, stream=True,
            )
        except Exception as e:
            return {
                'error': True,
                'type': 'server',
                'message': f'Unknown server error occured: {str(e)}',
            }

    async def login(self, token: str) -> dict[str, str]:
        """
        Authenticates the user with the BashSenpai API server using the provided
        token.

        Args:
            token (str): The authentication token provided by the user.

        Returns:
            dict: JSON response received from the API server indicating the
                result of the authentication process.
        """
        data = {
            'token': token,
        }
        response = await asyncio.to_thread(POST, f'{self.HOST}/auth/', json=data)
        return response.json()

    async def question(
            self,
            question: str,
            metadata: Optional[dict[str, str]] = None,
        ) -> Union[Response, dict[str, str]]:
        """
        Sends a question to the BashSenpai API server and returns the response.

        Args:
            question (str): The question to send to the API server.
            metadata Optional(dict[str, str]): Optional dictionary containing
                user environment metadata.

        Returns:
            Resonse | dict: Response received from the API server containing the
                answer to the question or an error message.

        Raises:
            Exception: In case of server communication issues or other errors.
        """
        # check if the user is authenticated first
        token = self._config.get_value('token')
        if not token:
            return {
                'error': True,
                'type': 'auth',
                'message': 'You are not authenticated',
            }

        # send the question to our API
        try:
            data = {
                'token': token,
                'version': self._config.get_value('version'),
                'persona': self._config.get_value('persona'),
                'question': question,
                'history': self._history.get_history(),
                'metadata': metadata,
            }
            return await asyncio.to_thread(
                POST, f'{self.HOST}/prompt/', json=data, stream=True,
            )
        except Exception as e:
            return {
                'error': True,
                'type': 'server',
                'message': f'Unknown server error occured: {str(e)}',
            }
