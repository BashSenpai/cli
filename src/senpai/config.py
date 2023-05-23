from pathlib import Path
import toml
from typing import Union


class Config:
    """
    Config handles the user configuration settings for the BashSenpai tool.

    It loads the user's config file in TOML format, allows getting and setting
    specific configuration values, and writing the updated configuration file.

    Usage:
    >>> config = Config(path=Path('/path/to/config'))
    >>> token = config.get_value('token')
    >>> config.set_value('token', '<your_auth_token>')
    >>> config.write()

    """

    def __init__(self, path: Path) -> None:
        """Initialize the Config object.

        Args:
            path (Path): The path to the directory where the config file is
            located.

        """
        self.path = path / 'config.toml'
        self._load()

    def _load(self) -> None:
        """Load the user configuration file and set the configuration values."""

        try:
            with open(self.path, 'r') as f:
                config = toml.load(f)
        except FileNotFoundError:
            config = {'main': {}}

        self._config = {
            'TOKEN': config['main'].get('token', None),
            'PERSONA': config['main'].get('persona', 'default'),
            'PROG': config['main'].get('prog', 'senpai'),
            'COMMAND_COLOR': config['main'].get('command_color', 'bold bright blue'),
            'COMMENT_COLOR': config['main'].get('comment_color', 'bright gray'),
        }

    def get_value(self, setting: str) -> Union[str, None]:
        """Get the value of a specific configuration setting.

        Args:
            setting (str): The name of the configuration setting.

        Returns:
            str or None: The value of the configuration setting, or None if
            not found.

        """
        return self._config.get(setting.upper(), None)

    def set_value(self, setting: str, value: str) -> None:
        """Set the value of a specific configuration setting.

        Args:
            setting (str): The name of the configuration setting.
            value (str): The new value for the configuration setting.

        """
        self._config[setting.upper()] = value

    def write(self) -> None:
        """Write the current configuration values to the user config file."""

        with open(self.path, 'w') as f:
            config_data = {
                'main': {
                    'token': self._config['TOKEN'],
                    'persona': self._config['PERSONA'],
                    'prog': self._config['PROG'],
                    'command_color': self._config['COMMAND_COLOR'],
                    'comment_color': self._config['COMMENT_COLOR'],
                }
            }
            toml.dump(config_data, f)
