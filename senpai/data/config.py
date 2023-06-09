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

from pathlib import Path
import toml
from typing import Union


class Config:
    """
    Config handles the user configuration settings for the BashSenpai tool.

    It loads the user's config file in TOML format, allows getting and setting
    specific configuration values, and writing the updated configuration file.

    Attributes:
        path (Path): The path to the user configuration file.
        _config (dict): The dictionary holding the current configuration values.

    Usage:
        >>> config = Config(path=Path('/path/to/config'))
        >>> token = config.get_value('token')
        >>> config.set_value('token', '<your_auth_token>')
        >>> config.write()
    """

    def __init__(self, path: Path) -> None:
        """
        Initialize the Config object with the provided configuration file path.

        Args:
            path (Path): The path to the directory where the config file is
                located.
        """
        self.path = path / 'config.toml'
        self._load()

    def _load(self) -> None:
        """
        Load the configuration file and set the configuration values.

        If the file doesn't exist, creates a new dictionary with default values.
        """
        try:
            with open(self.path, 'r') as f:
                config = toml.load(f)
        except FileNotFoundError:
            config = {'main': {}}

        self._config = {
            'TOKEN': config['main'].get('token', None),
            'PERSONA': config['main'].get('persona', 'default'),
            'PROG': config['main'].get('prog', 'senpai'),
            'VERSION': config['main'].get('version', '0'),
            'COMMAND_COLOR': config['main'].get('command_color', 'bold bright blue'),
            'COMMENT_COLOR': config['main'].get('comment_color', 'bright gray'),
            'EXECUTE': config['main'].get('execute', True),
            'METADATA': config['main'].get('metadata', True),
        }

    def get_value(self, setting: str) -> Union[str, None]:
        """
        Get the value of a specific configuration setting.

        Args:
            setting (str): The name of the configuration setting.

        Returns:
            str or None: The value of the configuration setting, or None if
            not found.
        """
        return self._config.get(setting.upper(), None)

    def set_value(self, setting: str, value: Union[str, bool]) -> None:
        """
        Set the value of a specific configuration setting.

        Args:
            setting (str): The name of the configuration setting.
            value (str | bool): The new value for the configuration setting.
        """
        self._config[setting.upper()] = value

    def write(self) -> None:
        """
        Write the current configuration values to the user config file.

        The config file is stored in TOML format. If a configuration file does
        not exist, a new one is created.
        """
        with open(self.path, 'w') as f:
            config_data = {
                'main': {
                    'token': self._config['TOKEN'],
                    'persona': self._config['PERSONA'],
                    'prog': self._config['PROG'],
                    'version': self._config['VERSION'],
                    'command_color': self._config['COMMAND_COLOR'],
                    'comment_color': self._config['COMMENT_COLOR'],
                    'execute': self._config['EXECUTE'],
                    'metadata': self._config['METADATA'],
                }
            }
            toml.dump(config_data, f)
