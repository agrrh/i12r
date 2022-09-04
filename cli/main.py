"""CLI tool to detect issues."""

import sys
import os
import re

import fire

from rich import print as rprint

from .i12r.issue_manager import IssueManager


# TODO: That's a poor man's logging, rework later
def eprint(string: str):
    """Rich print to STDERR."""
    rprint(string, file=sys.stderr)


def get_files(path: str):
    """Generate paths for files in selected directory."""
    for root, _dirs, files in os.walk(path, followlinks=False):
        for file in files:
            yield os.path.join(root, file)


def cli_entrypoint(debug: bool = False, path: str = "./", include: int = None, exclude: iter = ("/.git/")) -> list:
    """CLI entrypoint."""
    # TODO: Implement debug output
    if debug:
        pass

    eprint(f"# Working with root: {path}")
    eprint(f"# Include only: {include}")
    eprint(f"# Exclude from: {exclude}")

    files = list(get_files(path))

    # Include only paths which match at least 1 include regex
    if include:
        files = filter(lambda x: any(re.search(regex, x) for regex in include), files)

    # Exclude paths which matches at least 1 exclude regex
    files = filter(lambda x: not any(re.search(regex, x) for regex in exclude), files)

    eprint(f"# Files found: {files}")

    i12r = IssueManager()

    for file in files:
        # TODO Skip non-text mime-types
        # TODO Process errors e.g. missing symlinks, non-text file contents
        with open(file, encoding="utf-8") as file_:
            data = file_.read()

        issues = list(i12r.find(file, data))

        for issue in issues:
            eprint(issue)

    # TODO Print found issues in pretty format
    # TODO Print found issues in machine-readable format


if __name__ == "__main__":
    # TODO Get include/exclude from global config
    # TODO Get include/exclude from in-repository config

    fire.Fire(cli_entrypoint)
