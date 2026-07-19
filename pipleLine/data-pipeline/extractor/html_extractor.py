"""
Purpose:
- HTML extractor for automotive repair knowledge pages and technical web documents.

Input:
- Raw HTML string.

Output:
- Structured dictionary with headings, paragraphs, and table rows.

Responsibilities:
- Parse HTML into meaningful text segments.
- Remove script/style noise.

TODO implementation notes:
- Add section classification for warnings, steps, and notes.
- Add robust handling for malformed HTML.
"""

from __future__ import annotations

from html.parser import HTMLParser


class _SimpleHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current_tag: str | None = None
        self._skip_depth = 0
        self.headings: list[str] = []
        self.paragraphs: list[str] = []
        self.table_rows: list[str] = []
        self._current_row: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        self.current_tag = tag
        if tag == "tr":
            self._current_row = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag == "tr" and self._current_row:
            self.table_rows.append(" | ".join(self._current_row))
            self._current_row = []
        self.current_tag = None

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.strip()
        if not text or self.current_tag is None:
            return
        if self.current_tag in {"h1", "h2", "h3"}:
            self.headings.append(text)
        elif self.current_tag == "p":
            self.paragraphs.append(text)
        elif self.current_tag in {"th", "td"}:
            self._current_row.append(text)


class HtmlExtractor:
    def extract(self, html: str) -> dict[str, list[str]]:
        parser = _SimpleHtmlParser()
        parser.feed(html or "")
        parser.close()

        return {
            "headings": parser.headings,
            "paragraphs": parser.paragraphs,
            "table_rows": parser.table_rows,
        }
