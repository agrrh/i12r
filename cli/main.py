# TODO Tool to detect issues

import fire
import sys
import os
import glob


from rich import print as rprint


def eprint(s: str):
    rprint(s, file=sys.stderr)


def get_files(path: str):
    for root, dirs, files in os.walk(path, followlinks=False):
        for file in files:
            yield os.path.join(root, file)


def get_excludes(exclude: list):
    for pattern in exclude:
        for path in glob.glob(pattern, recursive=True):
            yield path


def get_includes(include: list):
    for pattern in include:
        for path in glob.glob(pattern, recursive=True):
            yield path


def cli_entrypoint(debug: bool = False, path: str = "./", include: list = [], exclude: list = ["./.git/**"]):
    eprint(f"# Working with root: {path}")
    eprint(f"# Include only: {include}")
    eprint(f"# Exclude from: {exclude}")

    files = list(get_files(path))

    if include:
        includes = list(get_includes(include))
        files = set(files).intersection(set(includes))

    excludes = list(get_excludes(exclude))
    files = [file for file in files if file not in excludes]

    eprint(f"# Files found: {files}")

    # TODO Call for i12r library to get issues
    # TODO Print issues found


if __name__ == "__main__":
    # TODO Get include/exclude from global config
    # TODO Get include/exclude from in-repository config

    fire.Fire(cli_entrypoint)
