import json
from pathlib import Path
from typing import Any, Dict, List, Union


class History:
    """
    History is responsible for managing the user's interaction history with the
    BashSenpai tool.

    It loads the previous history from a JSON file and allows adding new prompts
    to the history, clearing the history, retrieving the current history, and
    writing the history to the file.

    Usage:
    >>> history = History(path=Path('/path/to/history'))
    >>> history.add({
    >>>     'question': 'how do I list files', 'answer': 'ls -l', 'persona': ''
    >>> })
    >>> history.write()
    >>> prompts = history.get_history()
    >>> print(prompts)

    """

    def __init__(self, path: Path) -> None:
        """Initialize the History object.

        Args:
            path (Path): The path to the directory where the history file is
            located.

        """

        self.path = path / 'history.json'
        self._load()

    def _load(self) -> None:
        """
        Load user history with previous interactions from the history file.

        """

        self._history = list()
        if self.path.exists():
            with open(self.path, 'r') as f:
                self._history = json.load(f)

    def add(self, prompt: dict[str, Union[str, list[Any]]]) -> None:
        """Add a new prompt to the user history.

        Args:
            prompt (dict): The prompt containing the question and answer.

        """

        self._history.append(prompt)

    def clear(self) -> None:
        """Clear the previous user history."""

        self._history = list()

    def get_history(self) -> List[Union[Dict[str, str], Any]]:
        """Get the current user history.

        Returns:
            list: The list of prompts in the user's history.

        """

        return self._history

    def write(self) -> None:
        """Write the current user history to the history log file."""

        with open(self.path, 'w') as f:
            # limit to latest 5 prompts only
            json.dump(self._history[-5:], f)
