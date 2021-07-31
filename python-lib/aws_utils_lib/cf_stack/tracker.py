import os
import json
from typing import Dict
from datetime import datetime


class Tracker:
    """
    Class to handle the tracking of the stacks (which are currently active
    or deployed). The metadata is stored in a JSON file in the metadata
    directory.

    The metadata file contains a JSON object whose keys are the names of the
    stacks and each is associated with a dictionary that has the following
    values:
    - is_active: Boolean
    - last_launched: Datetime in DATETIME_FMT format

    Methods
    -------
    - log_stack_launch
    - log_stack_deletion
    - is_stack_active
    """

    DATETIME_FMT: str = "%Y-%m-%d %H:%M:%S"  #: Format for datetime metadata
    META_FILE: str = "stacks-metadata.json"  #: Name of metadata file

    def __init__(self, meta_dir: str):
        """
        :param meta_dir: Directory where metadata is stored.
        """
        if not os.path.isdir(meta_dir):
            raise FileNotFoundError("Metadata directory not found.")
        self.__meta_dir = meta_dir

        if os.path.isfile(self.meta_file):
            self.__metadata = self._load_metadata()
        else:
            self.__metadata = {}

    @property
    def meta_dir(self) -> str:
        """
        Metadata directory (Read-only).
        """
        return self.__meta_dir

    @property
    def meta_file(self) -> str:
        """
        Metadata filename (Read-only)
        """
        return os.path.join(self.__meta_dir, self.META_FILE)

    @property
    def metadata(self) -> Dict[str, Dict]:
        """
        Metadata dictionary.
        """
        return self.__metadata

    @metadata.setter
    def metadata(self, metadata: Dict[str, Dict]):
        """
        Setter for metadata dictionary. Saves the metadata to file when set.
        :param metadata: New metadata dictionary.
        """
        with open(self.meta_file, "w") as f:
            json.dump(metadata, f)
        self.__metadata = metadata

    def _load_metadata(self) -> Dict[str, Dict]:
        """
        Load the metadata from the json file.
        :return: Metadata dictionary.
        """
        with open(self.meta_file, "r") as f:
            meta = json.load(f)
        return meta

    def stack_info(self, stack_name: str) -> Dict[str, Dict]:
        """
        Get the metadata of the given stack.
        :param stack_name:
        :return: Stack's metadata. Returns empty dictionary if no metadata is
            currently stored for this stack.
        """
        return self.metadata.get(stack_name, {})

    def is_stack_active(self, stack_name: str) -> bool:
        """
        Tells whether the given stack is currently active / running.
        :param stack_name: Name of stack.
        :return: Boolean
        """
        return self.stack_info(stack_name).get("is_active", False)

    def log_stack_launch(self, stack_name: str):
        """
        Record the launch of a new stack in the metadata.
        :param stack_name: Name of stack.
        """
        raise NotImplementedError

    def log_stack_deletion(self, stack_name: str):
        """
        Log the takedown / deletion of an existing stack.
        :param stack_name: Name of stack.
        """
        raise NotImplementedError
