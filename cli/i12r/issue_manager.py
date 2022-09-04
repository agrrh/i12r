"""Issue manager."""

import re

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
                # TODO Handle errors (e.g. wrong types)
                # TODO Strip trailing newlines
                # TODO Remove common identation for strings
                issue = Issue(fname=fname, **match.groupdict())

                yield issue
                line_start = text[: match.start()].count("\n") + 1
                line_end = line_start + text[match.start() : match.end()].count("\n")
                    issue = Issue(fname=fname, **match.groupdict(), line_start=line_start, line_end=line_end)
                    yield issue
