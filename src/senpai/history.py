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

import json
from pathlib import Path
from typing import Any, Dict, List, Union


class History:
    """
    This class is responsible for managing the user's interaction history with
    the BashSenpai tool.

    The class loads the previous history from a JSON file upon initialization.
    It allows adding new prompts to the history, clearing the history,
    retrieving the current history, and writing the history to the file.

    Attributes:
        path (Path): Path to the JSON file storing the history.
        _history (List[Dict[str, Union[str, List[Any]]]]): Loaded history data.

    Usage:
        >>> history = History(path=Path('/path/to/history'))
        >>> history.add({
        >>>     'question': 'how to list files', 'answer': 'ls -l', 'persona': ''
        >>> })
        >>> history.write()
        >>> prompts = history.get_history()
        >>> print(prompts)
    """

    def __init__(self, path: Path) -> None:
        """
        Initializes the History object, sets the path to the history file, and
        loads the history.

        Args:
            path (Path): The path to the directory where the history file is
                located.
        """
        self.path = path / 'history.json'
        self._load()

    def _load(self) -> None:
        """
        Private method to load user history from the history file.
        If the history file does not exist, initialize an empty history.
        """
        self._history = list()
        if self.path.exists():
            with open(self.path, 'r') as f:
                self._history = json.load(f)

        # convert old json history
        for idx, history_message in enumerate(self._history):
            if isinstance(history_message['answer'], list):
                answer = ''
                for line in history_message['answer']:
                    line_type = line.get('type')
                    if line_type == 'comment':
                        answer += '# ' + line['data'] + '\n'
                    elif line_type == 'command':
                        answer += '$ ' + line['data'] + '\n'
                self._history[idx]['answer'] = answer.strip()
            if isinstance(history_message['persona'], list):
                answer = ''
                for line in history_message['persona']:
                    line_type = line.get('type')
                    if line_type == 'comment':
                        answer += '# ' + line['data'] + '\n'
                    elif line_type == 'command':
                        answer += '$ ' + line['data'] + '\n'
                self._history[idx]['persona'] = answer.strip() or None
        self.write()


    def add(self, prompt: dict[str, Union[str, list[Any]]]) -> None:
        """
        Adds a new prompt to the user history.

        Args:
            prompt (Dict[str, Union[str, List[Any]]]): The prompt to be added to
                the history.
        """
        self._history.append(prompt)

    def clear(self) -> None:
        """Clear the previous user history."""
        self._history = list()

    def get_history(self) -> List[Union[Dict[str, str], Any]]:
        """
        Returns the current user interaction history.

        Returns:
            List[Dict[str, Union[str, List[Any]]]]: The current user's
                interaction history.
        """
        return self._history

    def write(self) -> None:
        """
        Writes the current user history to the history log file.
        Only the latest 5 prompts are kept.
        """
        with open(self.path, 'w') as f:
            # limit to latest 5 prompts only
            json.dump(self._history[-5:], f)
