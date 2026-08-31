#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""列出已沉淀的写作能力。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    CAPABILITIES,
    DIRECTION_ZH,
    DIRECTION_IDS,
    ensure_utf8_stdio,
    parse_directions,
    parse_frontmatter,
    read_text,
)


def first_heading(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def main() -> None:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="列出 capabilities")
    parser.add_argument(
        "--direction",
        default="",
        help="过滤：core/lyrical/…；空=全部",
    )
    args = parser.parse_args()

    dirs: list[str] | None = None
    if args.direction.strip():
        dirs = parse_directions(args.direction, allow_core=True)

    # core 优先展示
    order = ["core"] + sorted(DIRECTION_IDS - {"core"})
    rows: list[tuple[str, str, str, str, Path]] = []
    for did in order:
        if dirs is not None and did not in dirs:
            continue
        folder = CAPABILITIES / did
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            text = read_text(path)
            meta = parse_frontmatter(text)
            title = first_heading(text) or path.stem
            tags = meta.get("tags", "")
            priority = meta.get("priority", "")
            rows.append((DIRECTION_ZH[did], title, priority, tags, path))

    if not rows:
        print("（尚无已沉淀能力）")
        return

    print(f"{'分层':<8} {'能力名':<22} {'优先级':<8} {'标签':<16} 文件")
    print("-" * 78)
    for zh, title, priority, tags, path in rows:
        print(f"{zh:<8} {title:<22} {priority:<8} {tags:<16} {path}")


if __name__ == "__main__":
    main()
