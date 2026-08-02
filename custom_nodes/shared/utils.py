import logging
import subprocess
import sys
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """
    Creates a logger that prints nicely formatted messages with
    timestamps and the node's name, so when many nodes run in a
    pipeline, you can tell which node produced which log line.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if this logger was already set up
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def run_command(command: list[str], logger: logging.Logger) -> str:
    """
    Runs an external command (like ffmpeg or colmap) safely.

    Why we need this instead of calling subprocess directly everywhere:
    - Logs the exact command being run (critical for debugging later)
    - Captures both stdout and stderr instead of letting them vanish
    - Raises a clear error if the command fails, instead of silently
      continuing with a broken pipeline

    command: a list of strings, e.g. ["ffmpeg", "-i", "input.mp4"]
             (NOT a single string — this avoids shell-injection issues
             and handles spaces in file paths correctly)
    """
    logger.info(f"Running command: {' '.join(command)}")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        logger.error(f"Command failed with exit code {result.returncode}")
        logger.error(f"stderr: {result.stderr}")
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\n{result.stderr}"
        )

    logger.info("Command completed successfully")
    return result.stdout


def ensure_dir(path: str) -> Path:
    """
    Makes sure a directory exists, creating it (and any missing
    parent folders) if needed. Returns a Path object for convenience.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p