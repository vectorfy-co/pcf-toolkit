#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pydantic>=2.6",
#   "playwright>=1.40",
#   "rich>=13.7",
#   "typer>=0.12",
# ]
# ///

"""Extract PCF manifest schema reference content from Microsoft Learn.

This script uses Playwright to scrape the PCF manifest schema reference pages
from Microsoft Learn into a single JSON file.

Notes:
  Playwright requires browser binaries. If you haven't installed them yet:
    uv run --python 3.13 python -m playwright install
"""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin

import typer
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright
from pydantic import BaseModel, Field
from rich.console import Console

APP = typer.Typer(add_completion=False)
CONSOLE = Console()

ROOT_URL = "https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/"
OUTPUT_PATH = Path("data/spec_raw.json")


def _dedupe(items: list[str]) -> list[str]:
    """Deduplicate items while preserving order."""
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


class ExtractedTable(BaseModel):
    """A table extracted from a Learn page."""

    label: str | None = Field(default=None, description="Table label/caption (if present).")
    heading: str | None = Field(default=None, description="Nearest heading title.")
    headers: list[str] = Field(default_factory=list, description="Column headers.")
    rows: list[list[str]] = Field(default_factory=list, description="Row cell values.")


class ExtractedCodeBlock(BaseModel):
    """A code snippet extracted from a Learn page."""

    language: str | None = Field(default=None, description="Language identifier (if detected).")
    code: str = Field(default="", description="Code snippet text.")
    heading: str | None = Field(default=None, description="Nearest heading title.")


class ExtractedPageContent(BaseModel):
    """Extracted content for a single Learn page (excluding slug/url)."""

    title: str = Field(default="", description="Page H1 title.")
    summary: str = Field(default="", description="First summary paragraph under H1.")
    available_for: list[str] = Field(default_factory=list, description="Availability list.")
    sections: dict[str, list[str]] = Field(default_factory=dict, description="Section text keyed by heading.")
    tables: list[ExtractedTable] = Field(default_factory=list, description="Tables on the page.")
    code_blocks: list[ExtractedCodeBlock] = Field(default_factory=list, description="Code blocks on the page.")


class ExtractedPage(ExtractedPageContent):
    """Extracted content for a single Learn page."""

    slug: str = Field(..., description="Relative slug for the page.")
    url: str = Field(..., description="Absolute URL.")


class ExtractionResult(BaseModel):
    """Root JSON payload written to `data/spec_raw.json`."""

    root_url: str = Field(..., description="Root URL used for extraction.")
    slugs: list[str] = Field(default_factory=list, description="Sorted list of slugs.")
    pages: list[ExtractedPage] = Field(default_factory=list, description="Extracted pages.")


def _extract_page_data(page: Page) -> ExtractedPageContent:
    """Extract structured page content from the DOM.

    Args:
      page: Playwright page.

    Returns:
      Extracted page content.

    Raises:
      ValueError: If the page evaluation result can't be validated.
    """
    raw = page.evaluate(
        """
        () => {
          const main = document.querySelector('main');
          if (!main) {
            return { error: 'main-not-found' };
          }

          const heading = main.querySelector('h1');
          const title = heading ? heading.textContent.trim() : '';

          const elements = Array.from(main.querySelectorAll('*'));
          const isHeading = (el) => ['H2', 'H3', 'H4'].includes(el.tagName);

          let summary = '';
          if (heading) {
            const startIndex = elements.indexOf(heading);
            for (let i = startIndex + 1; i < elements.length; i += 1) {
              const el = elements[i];
              if (isHeading(el)) {
                break;
              }
              if (el.tagName === 'P' && el.textContent.trim()) {
                summary = el.textContent.trim();
                break;
              }
            }
          }

          const headings = elements
            .filter((node) => isHeading(node))
            .map((node) => ({ node, title: node.textContent.trim() }));

          const headingLookup = new Map();
          let currentHeading = null;
          for (const el of elements) {
            if (isHeading(el)) {
              currentHeading = el.textContent.trim();
            }
            headingLookup.set(el, currentHeading);
          }

          const findLastHeadingTitle = (node) => headingLookup.get(node) || null;

          const sectionTexts = {};
          for (let i = 0; i < headings.length; i += 1) {
            const headingNode = headings[i].node;
            const title = headings[i].title;
            const startIndex = elements.indexOf(headingNode);
            const endIndex = i + 1 < headings.length ? elements.indexOf(headings[i + 1].node) : elements.length;
            const texts = [];
            for (let j = startIndex + 1; j < endIndex; j += 1) {
              const el = elements[j];
              if (el.tagName === 'P' || el.tagName === 'LI') {
                const text = el.textContent.trim();
                if (text) {
                  texts.push(text);
                }
              }
            }
            sectionTexts[title] = texts;
          }

          const tables = Array.from(main.querySelectorAll('table')).map((table) => {
            const headerRow = table.querySelector('thead tr') || table.querySelector('tr');
            const headers = headerRow
              ? Array.from(headerRow.querySelectorAll('th, td')).map((cell) => cell.textContent.trim())
              : [];
            const bodyRows = Array.from(table.querySelectorAll('tbody tr'));
            const rows = bodyRows.length
              ? bodyRows.map((row) => Array.from(row.querySelectorAll('td, th')).map((cell) => cell.textContent.trim()))
              : [];
            const label =
              table.getAttribute('aria-label') ||
              table.querySelector('caption')?.textContent?.trim() ||
              null;
            return {
              label,
              heading: findLastHeadingTitle(table),
              headers,
              rows,
            };
          });

          const codeBlocks = Array.from(
            main.querySelectorAll('pre code, code[class*="lang-"]')
          ).map((node) => {
            const className = node.getAttribute('class') || '';
            const langMatch = className.match(/lang-([A-Za-z0-9_-]+)/i);
            const language = langMatch ? langMatch[1].toLowerCase() : null;
            return {
              language,
              code: node.textContent.trim(),
              heading: findLastHeadingTitle(node),
            };
          });

          const availableFor = sectionTexts['Available for'] || [];

          return {
            title,
            summary,
            available_for: availableFor,
            sections: sectionTexts,
            tables,
            code_blocks: codeBlocks,
          };
        }
        """
    )
    return ExtractedPageContent.model_validate(raw)


def extract(root_url: str) -> ExtractionResult:
    """Extract the full manifest schema reference into a single JSON payload.

    Args:
      root_url: Root Learn URL.

    Returns:
      Extraction result model.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(root_url)
        page.wait_for_selector("main")

        slugs = page.eval_on_selector_all(
            "main table a",
            """
            (anchors) => anchors
              .map((a) => a.getAttribute('href'))
              .filter((href) => href && !href.startsWith('http') && !href.startsWith('../') && !href.includes('#'))
            """,
        )
        slugs = _dedupe(sorted(slugs))

        pages: list[ExtractedPage] = []
        for slug in slugs:
            url = urljoin(root_url, slug)
            page.goto(url)
            page.wait_for_selector("main")

            # Expand tables for wider view; should not alter the data content.
            for button in page.get_by_role("button", name="Expand table").all():
                try:
                    button.click(timeout=1000)
                except PlaywrightTimeoutError:
                    continue

            # Ensure details blocks are opened.
            for detail in page.query_selector_all("details"):
                try:
                    page.evaluate("(el) => { el.open = true; }", detail)
                except PlaywrightTimeoutError:
                    continue

            content = _extract_page_data(page)
            pages.append(
                ExtractedPage(
                    title=content.title,
                    summary=content.summary,
                    available_for=content.available_for,
                    sections=content.sections,
                    tables=content.tables,
                    code_blocks=content.code_blocks,
                    slug=slug,
                    url=url,
                )
            )

        browser.close()

    return ExtractionResult(root_url=root_url, slugs=slugs, pages=pages)


@APP.command()
def main(
    root_url: str = typer.Option(ROOT_URL, help="Root Microsoft Learn URL to scrape."),
    output: Path = typer.Option(OUTPUT_PATH, help="Output JSON path."),
) -> None:
    """Run extraction and write output JSON."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = extract(root_url)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload.model_dump_json(indent=2), encoding="utf-8")
    CONSOLE.print(f"[green]Wrote[/green] {output}")


if __name__ == "__main__":
    APP()
