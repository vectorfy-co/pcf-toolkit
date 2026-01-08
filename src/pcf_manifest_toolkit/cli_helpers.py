"""Shared CLI utilities for rich output."""

from __future__ import annotations

from typing import Iterable

try:
    from rich.console import Console
    from rich.table import Table
except Exception:  # pragma: no cover - fallback if rich isn't available
    Console = None
    Table = None


def rich_console(stderr: bool = False):
    """Return a Rich console if available, otherwise None."""
    if Console is None:
        return None
    return Console(stderr=stderr)


def render_validation_table(
    errors: Iterable[dict],
    *,
    title: str,
    stderr: bool = True,
) -> bool:
    """Render a validation error table. Returns True if rendered."""
    if Table is None:
        return False

    console = rich_console(stderr=stderr)
    if console is None:
        return False

    table = Table(title=title, show_lines=False)
    table.add_column("Location", style="bold")
    table.add_column("Message")
    table.add_column("Type", style="dim")
    for error in errors:
        loc = ".".join(str(part) for part in error.get("loc", [])) or "<root>"
        msg = error.get("msg", "Invalid value")
        err_type = error.get("type", "validation_error")
        table.add_row(loc, msg, err_type)
    console.print(table)
    return True
