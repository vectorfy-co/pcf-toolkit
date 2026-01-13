"""Extract PCF manifest schema reference content from Microsoft Learn."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

ROOT_URL = "https://learn.microsoft.com/en-us/power-apps/developer/component-framework/manifest-schema-reference/"
OUTPUT_PATH = Path("data/spec_raw.json")


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _extract_page_data(page) -> dict[str, Any]:
    return page.evaluate(
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


def extract() -> dict[str, Any]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(ROOT_URL)
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

        pages: list[dict[str, Any]] = []
        for slug in slugs:
            url = urljoin(ROOT_URL, slug)
            page.goto(url)
            page.wait_for_selector("main")

            # Expand tables for wider view; should not alter the data content.
            for button in page.get_by_role("button", name="Expand table").all():
                try:
                    button.click(timeout=1000)
                except Exception:
                    continue

            # Ensure details blocks are opened.
            for detail in page.query_selector_all("details"):
                try:
                    page.evaluate("(el) => { el.open = true; }", detail)
                except Exception:
                    continue

            data = _extract_page_data(page)
            data["slug"] = slug
            data["url"] = url
            pages.append(data)

        browser.close()

    return {
        "root_url": ROOT_URL,
        "slugs": slugs,
        "pages": pages,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = extract()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True))
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
