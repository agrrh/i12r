# TODO Library

import re

from i12r.issue import Issue


class IssueManager:
    def find(self, fname, text):
        for line_n, line in enumerate(text.split("\n")):
            # TODO Support more prefixes, e.g. FIXME

            # TODO Support more comment notations
            #   <!-- comment -->
            #   /* comment */
            #   // comment
            #   """comment"""

            # TODO Support multi-line comments

            match = re.search(r"#\s?TODO\s(?P<content>.+)", line)

            if match:
                content = match.group("content")
                issue = Issue(fname=fname, line_start=line_n, line_end=line_n, content=content)

                yield issue
