import dotenv
from .constants import ENV_PATH


def load_env_vars():
    """
    Loads the environment variables from META_DIR/.env.
    """
    dotenv.load_dotenv(ENV_PATH)
