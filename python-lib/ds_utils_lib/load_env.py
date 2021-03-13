import os
import dotenv
from .constants import META_DIR


def load_env_vars():
    """
    Loads the environment variables from META_DIR/.env.
    """
    dotenv.load_dotenv(os.path.join(META_DIR, ".env"))
