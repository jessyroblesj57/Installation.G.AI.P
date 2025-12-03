import os
import hashlib
import platform
import sys
from typing import List, Dict, Union

def list_files(directory: str = ".") -> List[str]:
    """
    Lists all files and directories in the specified directory.

    Args:
        directory: The path to the directory to list. Defaults to current directory.

    Returns:
        A list of filenames and directory names.
    """
    try:
        return os.listdir(directory)
    except OSError as e:
        return [f"Error: {e}"]

def read_file(filepath: str) -> str:
    """
    Reads the content of a file.

    Args:
        filepath: The path to the file to read.

    Returns:
        The content of the file as a string, or an error message.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def write_file(filepath: str, content: str) -> str:
    """
    Writes content to a file. Overwrites existing content.

    Args:
        filepath: The path to the file to write to.
        content: The content to write.

    Returns:
        A success message or error message.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {e}"

def get_file_hash(filepath: str) -> str:
    """
    Calculates the SHA256 hash of a file. Useful for verifying file integrity.

    Args:
        filepath: The path to the file.

    Returns:
        The hexadecimal digest of the hash, or an error message.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"Error calculating hash: {e}"

def system_info() -> Dict[str, str]:
    """
    Returns basic information about the system.

    Returns:
        A dictionary containing system info.
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "python_version": sys.version
    }
