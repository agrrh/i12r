# TODO Tool to detect issues

import fire
import sys
import os
import re

from rich import print as rprint

from i12r.issue_manager import IssueManager


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
        files = list(filter(filter_includes, files))

    files = list(filter(filter_excludes, files))

    eprint(f"# Files found: {files}")

    i12r = IssueManager()

    for file in files:
        # TODO Skip non-text mime-types
        # TODO Process errors e.g. missing symlinks, non-text file contents
        with open(file) as fp:
            data = fp.read()

        issues = list(i12r.find(file, data))

        [rprint(i) for i in issues]

    # TODO Print found issues in pretty format
    # TODO Print found issues in machine-readable format


if __name__ == "__main__":
    # TODO Get include/exclude from global config
    # TODO Get include/exclude from in-repository config

    fire.Fire(cli_entrypoint)
