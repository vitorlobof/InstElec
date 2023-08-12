import os
import sys
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).parent.resolve()


def create_default_start_files(dst):
    src = BASE_DIR / 'default'

    # Iterate through the contents of the source directory
    for item in os.listdir(src):
        if item == '__pycache__':
            continue

        source_item = os.path.join(src, item)
        destination_item = os.path.join(dst, item)

        # Copy the item to the destination directory
        if os.path.isfile(source_item):
            shutil.copy(source_item, destination_item)
        elif os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item)


def run_command_line():
    args = sys.argv[1:]

    if len(args) != 1:
        return NotImplemented

    if args[0] == 'settings':
        destination_directory = ''
        create_default_start_files(destination_directory)
    else:
        return NotImplemented


if __name__ == "__main__":
    run_command_line()
