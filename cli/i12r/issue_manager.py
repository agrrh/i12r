"""Issue manager."""

import re

from .issue import Issue


class IssueManager:
    """Library to manage issues found in code."""

    def find(self, fname: str, text: str):
        """Generate Issue objects found in text."""
        # TODO Support more comment notations
        #   <!-- comment -->
        #   /* comment */
        #   // comment
        #   """comment"""

        # TODO Support multi-line comments

        """TODO Test 123. Test: hey #!@"""
        """TODO Test 123. Test: hey #!@
            foo
            bar
        """

        regexes = (
            r"(#|//)\s?(?P<level>TODO|FIXME):?\s(?P<content>.+)",
            r'("""|<!--|/\*)\s?(?P<level>TODO|FIXME):?\s(?P<content>.+)\s?("""|-->|\*/)',
        )

        for regex in regexes:
            matches = re.finditer(
                regex,
                text,
                re.MULTILINE,
            )

            for match in matches:
                # TODO Handle errors (e.g. wrong types)
                # FIXME Get start/end lines
                issue = Issue(fname=fname, **match.groupdict())

                yield issue
