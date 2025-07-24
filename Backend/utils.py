import os
import sys
import json
import random
import logging
import zipfile
import requests

from termcolor import colored

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_project_root() -> str:
    """Returns the absolute path to the project root."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def ensure_dir_exists(path: str) -> None:
    """Ensures that a directory exists, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")

def clean_dir(path: str) -> None:
    """
    Removes every file in a directory.

    Args:
        path (str): Path to directory.

    Returns:
        None
    """
    try:
        ensure_dir_exists(path)
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Removed file: {file_path}")

        logger.info(colored(f"Cleaned {path} directory", "green"))
    except Exception as e:
        logger.error(f"Error occurred while cleaning directory {path}: {str(e)}")

def fetch_songs(zip_url: str, songs_dir: str) -> None:
    """
    Downloads songs into songs/ directory to use with generated videos.

    Args:
        zip_url (str): The URL to the zip file containing the songs.
        songs_dir (str): The directory to save the songs to.

    Returns:
        None
    """
    try:
        logger.info(colored(f" => Fetching songs...", "magenta"))

        if not os.path.exists(songs_dir):
            os.makedirs(songs_dir)
            logger.info(colored(f"Created directory: {songs_dir}", "green"))
        
        # Skip if songs are already downloaded
        if os.listdir(songs_dir):
            return

        # Download songs
        response = requests.get(zip_url)

        # Save the zip file
        zip_path = os.path.join(songs_dir, "songs.zip")
        with open(zip_path, "wb") as file:
            file.write(response.content)

        # Unzip the file
        with zipfile.ZipFile(zip_path, "r") as file:
            file.extractall(songs_dir)

        # Remove the zip file
        os.remove(zip_path)

        logger.info(colored(f" => Downloaded Songs to {songs_dir}.", "green"))

    except Exception as e:
        logger.error(colored(f"Error occurred while fetching songs: {str(e)}", "red"))

# pyrefly: ignore  # bad-return
def choose_random_song(songs_dir: str) -> str:
    """
    Chooses a random song from the songs/ directory.

    Args:
        songs_dir (str): The directory to choose a song from.

    Returns:
        str: The path to the chosen song.
    """
    try:
        songs = os.listdir(songs_dir)
        song = random.choice(songs)
        logger.info(colored(f"Chose song: {song}", "green"))
        return os.path.join(songs_dir, song)
    except Exception as e:
        logger.error(colored(f"Error occurred while choosing random song: {str(e)}", "red"))


def check_env_vars() -> None:
    """
    Checks if the necessary environment variables are set.

    Returns:
        None

    Raises:
        SystemExit: If any required environment variables are missing.
    """
    try:
        required_vars = ["PEXELS_API_KEY", "TIKTOK_SESSION_ID", "IMAGEMAGICK_BINARY"]
        
        missing_vars = [var + (os.getenv(var) or "")  for var in required_vars if os.getenv(var) is None or (len(os.getenv(var) or "") == 0)]  

        if missing_vars:
            missing_vars_str = ", ".join(missing_vars)
            logger.error(colored(f"The following environment variables are missing: {missing_vars_str}", "red"))
            logger.error(colored("Please consult 'EnvironmentVariables.md' for instructions on how to set them.", "yellow"))
            sys.exit(1)  # Aborts the program
    except Exception as e:
        logger.error(f"Error occurred while checking environment variables: {str(e)}")
        sys.exit(1)  # Aborts the program if an unexpected error occurs

