import os
import json
from typing import Dict, List
from datetime import datetime


class StackTracker:
    """
    Class to handle the tracking of the stacks (which are currently active
    or deployed). The metadata is stored in a JSON file in the metadata
    directory.

    The metadata file contains a JSON object whose keys are the names of the
    stacks and each is associated with a dictionary that has the following
    structure:
    - region1
        - is_active: Boolean
        - last_launched: Datetime in DATETIME_FMT format
    - region2
        - is_active
        -last_launched
    ...

    Methods
    -------
    - log_stack_launch
    - log_stack_deletion
    - is_stack_active
    """

    DATETIME_FMT: str = "%Y-%m-%d %H:%M:%S"  #: Format for datetime metadata
    META_FILE: str = "stacks-metadata.json"  #: Name of metadata file

    def __init__(self, meta_dir: str, aws_region: str = "us-west-2"):
        """
        :param meta_dir: Directory where metadata is stored.
        """
        self.__aws_region = aws_region
        if not os.path.isdir(meta_dir):
            raise FileNotFoundError("Metadata directory not found.")
        self.__meta_dir = meta_dir

        if os.path.isfile(self.meta_file):
            self.__metadata = self._load_metadata()
        else:
            self.__metadata = {}

    @property
    def aws_region(self) -> str:
        """
        AWS Region that is currently being tracked.
        """
        return self.__aws_region

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

    def stack_info(self, stack_name: str) -> Dict:
        """
        Get the metadata of the given stack.
        :param stack_name:
        :return: Stack's metadata. Returns empty dictionary if no metadata is
            currently stored for this stack.
        """
        return self.metadata.get(stack_name, {}).get(self.aws_region, {})

    def is_stack_active(self, stack_name: str) -> bool:
        """
        Tells whether the given stack is currently active / running in the
        given region.
        :param stack_name: Name of stack.
        :return: Boolean
        """
        return self.stack_info(stack_name).get("is_active", False)

    def _update_stack_data(self, stack_name: str, new_data: Dict):
        """
        Update a stack's metadata.
        :param stack_name:
        :param new_data: New metadata dictionary corresponding to the given
            stack and the aws region set in `__init__`.
        """
        meta = self.metadata

        stack_meta = meta.get(stack_name, {})
        stack_meta[self.aws_region] = new_data
        meta[stack_name] = stack_meta

        self.metadata = meta

    def log_stack_launch(self, stack_name: str):
        """
        Record the launch of a new stack in the metadata.
        :param stack_name: Name of stack.
        """
        new_meta = {
            "is_active": True,
            "last_launched": datetime.now().strftime(self.DATETIME_FMT)
        }
        self._update_stack_data(stack_name, new_meta)

    def log_stack_deletion(self, stack_name: str):
        """
        Log the takedown / deletion of an existing stack.
        :param stack_name: Name of stack.
        """
        if not self.is_stack_active(stack_name):
            raise KeyError("Stack has not been launched!")

        stack_meta = self.stack_info(stack_name)
        stack_meta["is_active"] = False
        self._update_stack_data(stack_name, stack_meta)

    def active_stacks(self) -> List[str]:
        """
        Get the list of names of currently active stacks in the given region.
        :return: List of strings.
        """
        return [k for k in self.metadata.keys() if self.is_stack_active(k)]
