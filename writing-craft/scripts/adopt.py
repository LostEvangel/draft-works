#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将已采纳的建议沉淀为硬规则能力，并更新 index.md。"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    CAPABILITIES,
    DIRECTION_ZH,
    INDEX,
    SKILL_ROOT,
    TEMPLATES,
    ensure_utf8_stdio,
    parse_priority,
    read_text,
    resolve_direction,
    slugify,
    write_text,
)


def rel_posix(path: Path) -> str:
    try:
        return path.resolve().relative_to(SKILL_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def append_index(
    direction: str,
    title: str,
    priority: str,
    tags: list[str],
    file_rel: str,
) -> None:
    zh = DIRECTION_ZH.get(direction, direction)
    tag_str = ", ".join(tags) if tags else ""
    row = f"| {zh} | {title} | {priority} | {tag_str} | [{file_rel}]({file_rel}) |"

    if INDEX.exists():
        text = read_text(INDEX)
    else:
        text = (
            "# 能力索引\n\n"
            "| 分层 | 能力名 | 优先级 | 标签 | 文件 |\n"
            "|------|--------|--------|------|------|\n"
        )

    lines = [ln for ln in text.splitlines() if "（尚无）" not in ln]
    if not any("| 分层 |" in ln or "| 方向 |" in ln for ln in lines):
        lines = [
            "# 能力索引",
            "",
            "| 分层 | 能力名 | 优先级 | 标签 | 文件 |",
            "|------|--------|--------|------|------|",
        ]
    # 旧表头升级
    lines = [
        ln.replace("| 方向 | 能力名 | 标签 | 文件 |", "| 分层 | 能力名 | 优先级 | 标签 | 文件 |")
        .replace("|------|--------|------|------|", "|------|--------|--------|------|------|")
        for ln in lines
    ]

    lines.append(row)
    write_text(INDEX, "\n".join(lines).rstrip() + "\n")


def main() -> None:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="采纳建议 → 硬规则写入能力库")
    parser.add_argument("--title", required=True, help="能力名")
    parser.add_argument(
        "--direction",
        required=True,
        help="core / lyrical / … 或 核心底盘 / 抒情 / …",
    )
    parser.add_argument(
        "--rule",
        required=True,
        help="硬规则：必须以「禁止」或「要求」开头",
    )
    parser.add_argument("--trigger", default="", help="触发场景")
    parser.add_argument(
        "--priority",
        default="medium",
        help="high/medium/low 或 高/中/低，默认 medium",
    )
    parser.add_argument("--example-good", default="", help="正例")
    parser.add_argument("--example-bad", default="", help="反例")
    parser.add_argument("--tags", default="", help="逗号分隔标签")
    parser.add_argument("--source", default="", help="来源 suggestions 路径")
    parser.add_argument("--id", default="", help="能力 id，默认自动生成")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()

    direction = resolve_direction(args.direction)
    priority = parse_priority(args.priority)
    rule = args.rule.strip()
    if not (rule.startswith("禁止") or rule.startswith("要求")):
        raise SystemExit("规则必须以「禁止」或「要求」开头（见 references/capability-rules.md）")

    tags = [t.strip() for t in re.split(r"[,，]", args.tags) if t.strip()]
    cap_id = args.id or f"{direction}-{slugify(args.title, 32)}"
    tags_yaml = "[" + ", ".join(tags) + "]" if tags else "[]"

    source_rel = ""
    if args.source:
        sp = Path(args.source)
        if not sp.is_absolute():
            sp = (SKILL_ROOT / args.source).resolve()
        source_rel = rel_posix(sp)

    tpl = read_text(TEMPLATES / "capability.md")
    body = (
        tpl.replace("{{id}}", cap_id)
        .replace("{{direction}}", direction)
        .replace("{{priority}}", priority)
        .replace("{{tags}}", tags_yaml)
        .replace("{{source_suggestion}}", source_rel)
        .replace("{{adopted_at}}", args.date)
        .replace("{{title}}", args.title)
        .replace("{{rule}}", rule)
        .replace("{{trigger}}", args.trigger or "（待补）")
        .replace("{{example_good}}", args.example_good or "（待补）")
        .replace("{{example_bad}}", args.example_bad or "（待补）")
    )

    out = CAPABILITIES / direction / f"{slugify(args.title)}.md"
    if out.exists():
        raise SystemExit(f"已存在: {out}")
    write_text(out, body)

    file_rel = rel_posix(out)
    append_index(direction, args.title, priority, tags, file_rel)
    print(str(out))
    print(f"索引已更新: {INDEX}")


if __name__ == "__main__":
    main()
