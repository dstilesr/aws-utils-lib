import fire

# From package
from . import _cli_functions as cli
from ..load_env import load_env_vars

# Load environment variables
load_env_vars()


# Launch CLI with Fire
fire.Fire({
    "launch": cli.launch_stack,
    "delete": cli.delete_stack,
    "active-stacks": cli.active_stacks
})
