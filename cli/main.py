"""CLI tool to detect issues."""

import sys
import os
import re

import fire

from rich import print as rprint

from i12r.issue_manager import IssueManager


# TODO Use default logging system
def _eprint(string: str):
    """Rich print to STDERR."""
    rprint(string, file=sys.stderr)


def _get_files(path: str):
    """Generate paths for files in selected directory."""
    for root, _dirs, files in os.walk(path, followlinks=False):
        for file in files:
            yield os.path.join(root, file)


def _print_result(result_dict: dict, machine_readable: bool = False):
    if machine_readable:
        rprint(result_dict)

    else:
        for file, issues in result_dict.items():
            if issues:
                file = f"[purple]{file}[/purple]"

                for issue in issues:
                    level = f"[bold blue]{issue['level']}[/bold blue]"
                    lines = (
                        f"[blue]{issue['line_start']}:{issue['line_end']}[/blue]"
                        if issue["line_start"] != issue["line_end"]
                        else f"[blue]{issue['line_start']}[/blue]"
                    )
                    content = f"{issue['content']}"

                    rprint(f"{level}\t{file}:{lines}\n{content}")

                    print("")


def cli_entrypoint(
    debug: bool = False,
    path: str = "./",
    include: int = None,
    exclude: iter = ("/.git/",),
    json: bool = False,
) -> list:
    """CLI entrypoint."""
    if debug:
        _eprint(f"# Working with root: {path}")
        _eprint(f"# Include only: {include}")
        _eprint(f"# Exclude from: {exclude}")

    files = list(_get_files(path))

    # Include only paths which match at least 1 include regex
    if include:
        files = filter(lambda x: any(re.search(regex, x) for regex in include), files)

    # Exclude paths which matches at least 1 exclude regex
    files = filter(lambda x: not any(re.search(regex, x) for regex in exclude), files)

    files = list(files)

    if debug:
        _eprint(f"# Files found: {files}")

    i12r = IssueManager()

    result_dict = {}

    for file in files:
        # TODO Skip non-text mime-types
        # TODO Process errors e.g. missing symlinks, non-text file contents
        with open(file, encoding="utf-8") as file_:
            data = file_.read()

        issues = list(i12r.find(file, data))

        result_dict[file] = [issue.dict(exclude={"fname"}, exclude_defaults=True) for issue in issues]

    _print_result(result_dict, json)


if __name__ == "__main__":
    # TODO Get include/exclude from global config
    # TODO Get include/exclude from in-repository config

    fire.Fire(cli_entrypoint)
