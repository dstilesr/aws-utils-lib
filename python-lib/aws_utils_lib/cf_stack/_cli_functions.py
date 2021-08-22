import os
import re
from pprint import pprint
from typing import Optional

# From package
from .launcher import StackLauncher
from .stacktracker import StackTracker
from ..constants import META_DIR, ENV_PATH


def launch_stack(
        stack_name: str,
        aws_profile: Optional[str] = None,
        aws_region: str = "us-west-2",
        **parameters):
    """
    Launches the stack (for CLI use).
    :param stack_name: Name of the stack to launch (Template must be in
        aws-stacks).
    :param aws_profile: Profile to use for credentials. Default is
        DEFAULT_PROFILE (if it has been set) or otherwise "default".
    :param aws_region: Region where stack will be launched.
    :param parameters: Parameters for the stack.
    """
    if aws_profile is None:
        aws_profile = os.getenv("DEFAULT_PROFILE", "default")

    launcher = StackLauncher(stack_name, aws_profile, aws_region)
    result = launcher.launch(**parameters)
    print(result)


def delete_stack(
        stack_name: str,
        aws_profile: Optional[str] = None,
        aws_region: str = "us-west-2"):
    """
    Launches the stack (for CLI use).
    :param stack_name: Name of the stack to launch (Template must be in
        aws-stacks).
    :param aws_profile: Profile to use for credentials. Default is
        DEFAULT_PROFILE (if it has been set) or otherwise "default".
    :param aws_region: Region where stack will be launched.
    """
    if aws_profile is None:
        aws_profile = os.getenv("DEFAULT_PROFILE", "default")

    launcher = StackLauncher(stack_name, aws_profile, aws_region)
    result = launcher.delete_stack()
    print(result)


def active_stacks(aws_region: str = "us-west-2"):
    """
    Print List of active stacks.
    :param aws_region: AWS region to look for stacks in.
    :return:
    """
    tracker = StackTracker(META_DIR, aws_region)
    print("Active stacks:")
    for name in tracker.active_stacks():
        print("- %s" % name)


def set_default_aws_profile(aws_profile: str):
    """
    Set the name of the default AWS profile to use and save it in the
    library's env file.
    :param aws_profile: Name of AWS profile to set as default.
    """
    aws_profile = aws_profile.strip()

    # Check if there is any whitespace in the string.
    if re.search(r"\s", aws_profile) is not None:
        raise ValueError("Profile name cannot contain whitespace!")

    with open(ENV_PATH, "r") as f:
        text = f.read()

    assign_txt = f"DEFAULT_PROFILE={aws_profile}"
    # Check if the variable has already been set
    if "DEFAULT_PROFILE" in text:
        new_text = re.sub(
            r"DEFAULT_PROFILE=[^\s]+",
            assign_txt,
            text
        )
    else:
        new_text = text if text.endswith("\n") else (text + "\n")
        new_text += f"export {assign_txt}\n"

    # Write to env file
    with open(ENV_PATH, "w") as f:
        f.write(new_text)


def clear_all_metadata():
    """
    Clear all stored metadata.
    :return:
    """
    tracker = StackTracker(META_DIR)
    tracker.clear_metadata()


def print_metadata():
    """
    Print stored metadata.
    :return:
    """
    tracker = StackTracker(META_DIR)
    pprint(tracker.metadata)
