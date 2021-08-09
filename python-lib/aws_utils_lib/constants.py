import os

"""Directory to store package metadata."""
META_DIR: str = os.path.join(
    os.path.expanduser("~"),
    ".ds-utils-data"
)

"""Path to library's .env file."""
ENV_PATH: str = os.path.join(META_DIR, ".env")
