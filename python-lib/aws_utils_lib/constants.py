from pathlib import Path

"""Directory to store package metadata."""
META_DIR: Path = Path.home() / ".ds-utils-data"

"""Path to library's .env file."""
ENV_PATH: Path = META_DIR / ".env"
