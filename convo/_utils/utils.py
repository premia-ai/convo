import os


def get_file_name(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]
