import fire

# From package
from .launcher import StackLauncher
from ..load_env import load_env_vars

# Load environment variables
load_env_vars()


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


# Launch CLI with Fire
fire.Fire({
    "launch": launch_stack,
    "delete": delete_stack
})
