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
    "active-stacks": cli.active_stacks,
    "set-default-profile": cli.set_default_aws_profile,
    "clear-all-metadata": cli.clear_all_metadata,
    "clear-region-metadata": cli.clear_region_metadata,
    "print-metadata": cli.print_metadata
})
