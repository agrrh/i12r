"""I12r s library."""

import re

from issue import Issue


class IssueManager:
    """Library to manage issues found in code."""

    def find(self, fname: str, text: str):
        """Generate Issue objects found in text."""
        lines = text.split("\n")

        for line_n, line in enumerate(lines, 1):
            # TODO Support more prefixes, e.g. FIXME

            # TODO Support more comment notations
            #   <!-- comment -->
            #   /* comment */
            #   // comment
            #   """comment"""

            # TODO Support multi-line comments

            match = re.search(r"#\s?TODO:?\s(?P<content>.+)", line)

            if match:
                content = match.group("content")
                issue = Issue(fname=fname, line_start=line_n, line_end=line_n, content=content)

                yield issue
