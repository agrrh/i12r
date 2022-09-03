# TODO Tool to detect issues

import fire
import sys
import os
import re

from rich import print as rprint


def eprint(s: str):
    rprint(s, file=sys.stderr)


def get_files(path: str):
    for root, dirs, files in os.walk(path, followlinks=False):
        for file in files:
            yield os.path.join(root, file)


def cli_entrypoint(debug: bool = False, path: str = "./", include: list = [], exclude: list = ["/.git/"]) -> list:
    def filter_includes(candidate):
        for regex in include:
            if re.search(regex, candidate):
                return True

        return False

    def filter_excludes(candidate):
        for regex in exclude:
            if re.search(regex, candidate):
                return False

        return True

    eprint(f"# Working with root: {path}")
    eprint(f"# Include only: {include}")
    eprint(f"# Exclude from: {exclude}")

    files = list(get_files(path))

    if include:
        files = filter(filter_includes, files)

    files = filter(filter_excludes, files)

    files = list(files)

    eprint(f"# Files found: {files}")

    # TODO Call for i12r library to get issues
    # TODO Print issues found


if __name__ == "__main__":
    # TODO Get include/exclude from global config
    # TODO Get include/exclude from in-repository config

    fire.Fire(cli_entrypoint)
