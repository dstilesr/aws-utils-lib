# From package
from ..constants import META_DIR
from .launcher import StackLauncher
from .stacktracker import StackTracker


def launch_stack(
        stack_name: str,
        aws_profile: str = "default",
        aws_region: str = "us-west-2",
        **parameters):
    """
    Launches the stack (for CLI use).
    :param stack_name: Name of the stack to launch (Template must be in
        aws-stacks).
    :param aws_profile: Profile to use for credentials.
    :param aws_region: Region where stack will be launched.
    :param parameters: Parameters for the stack.
    """
    launcher = StackLauncher(stack_name, aws_profile, aws_region)
    result = launcher.launch(**parameters)
    print(result)


def delete_stack(
        stack_name: str,
        aws_profile: str = "default",
        aws_region: str = "us-west-2"):
    """
    Launches the stack (for CLI use).
    :param stack_name: Name of the stack to launch (Template must be in
        aws-stacks).
    :param aws_profile: Profile to use for credentials.
    :param aws_region: Region where stack will be launched.
    """
    launcher = StackLauncher(stack_name, aws_profile, aws_region)
    result = launcher.delete_stack()
    print(result)


def active_stacks():
    """
    Print List of active stacks.
    :return:
    """
    tracker = StackTracker(META_DIR)
    print("Active stacks:")
    for name in tracker.active_stacks():
        print("- %s" % name)

