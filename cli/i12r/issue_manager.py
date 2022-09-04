"""Issue manager."""

import re

from pydantic import ValidationError

from .issue import Issue


class IssueManager:
    """Library to manage issues found in code."""

    def find(self, fname: str, text: str):
        """Generate Issue objects found in text."""
        regexes = (
            r"(#|//)\s?(?P<level>TODO|FIXME):?\s(?P<content>.+?)$",
            r'("""|<!--|/\*)\s?(?P<level>TODO|FIXME):?\s(?P<content>.+?)\s?("""|-->|\*/)$',
        )

        for regex in regexes:
            matches = re.finditer(
                regex,
                text,
                re.MULTILINE | re.DOTALL,
            )

            for match in matches:
                # TODO Strip trailing whitespaces and newlines
                # TODO Remove common identation for strings

                pos_start = match.start()
                pos_end = match.end()

                line_start = text[: match.start()].count("\n") + 1
                line_end = line_start + text[pos_start:pos_end].count("\n")

                # TODO Strip trailing whitespaces and newlines

                try:
                    issue = Issue(fname=fname, line_start=line_start, line_end=line_end, **match.groupdict())
                    yield issue
                except ValidationError:
                    print(f"Could not parse as Issue: {match}")
