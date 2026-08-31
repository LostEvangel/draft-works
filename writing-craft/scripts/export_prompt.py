#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 capabilities 拼成跨平台优化提示词（stdout 或 --out）。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    CAPABILITIES,
    DIRECTION_ZH,
    PRIORITY_ZH,
    WRITING_DIRECTION_IDS,
    ensure_utf8_stdio,
    parse_directions,
    parse_frontmatter,
    read_text,
    section_after,
    write_text,
)

INTENSITY = {
    "light": (
        "轻度润色",
        "仅修正语病、错别字、标点，调整语序；禁止改段落结构、替换核心措辞、增删内容。",
    ),
    "medium": (
        "中度优化",
        "可优化过渡、衔接与措辞；禁止重构结构、改变核心观点、大幅改写段落。",
    ),
    "restructure": (
        "结构重构",
        "可调段落顺序、拆合并段落、重构框架；禁止改变核心观点、新增原文没有的内容、替换标志性表达。",
    ),
}


def load_caps(direction: str) -> list[tuple[str, str, str, str]]:
    """Return list of (priority, title, rule, trigger)."""
    folder = CAPABILITIES / direction
    if not folder.is_dir():
        return []
    order = {"high": 0, "medium": 1, "low": 2}
    items: list[tuple[str, str, str, str]] = []
    for path in folder.glob("*.md"):
        text = read_text(path)
        meta = parse_frontmatter(text)
        title = next(
            (ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")),
            path.stem,
        )
        rule = section_after(text, "规则") or meta.get("rule", "")
        trigger = section_after(text, "触发场景")
        priority = meta.get("priority", "medium")
        if rule:
            items.append((priority, title, rule.strip(), trigger.strip()))
    items.sort(key=lambda x: order.get(x[0], 9))
    return items


def format_block(direction: str, caps: list[tuple[str, str, str, str]]) -> str:
    zh = DIRECTION_ZH.get(direction, direction)
    lines = [f"【{zh} | direction={direction}】"]
    if not caps:
        lines.append("（暂无已沉淀规则）")
        return "\n".join(lines)
    for priority, title, rule, trigger in caps:
        pz = PRIORITY_ZH.get(priority, priority)
        trig = f"（触发：{trigger}）" if trigger and trigger != "（待补）" else ""
        lines.append(f"- 【{pz}】{title}：{rule}{trig}")
    return "\n".join(lines)


def build_prompt(directions: list[str], intensity_key: str) -> str:
    name, desc = INTENSITY[intensity_key]
    parts = [
        "【角色设定】",
        "你是润色助手，不是创作者。只优化表达，不替代思考；只调整措辞，不篡改观点。",
        "",
        "【核心底盘 | 全场景生效 | 优先级最高】",
        format_block("core", load_caps("core")),
        "",
    ]
    for d in directions:
        parts.append(f"【风格方向：{DIRECTION_ZH.get(d, d)}】")
        parts.append(format_block(d, load_caps(d)))
        parts.append("")
    parts.extend(
        [
            f"【优化强度：{name}】",
            desc,
            "",
            "【执行要求】",
            "1. 严格遵守上方全部「禁止/要求」条款。",
            "2. 输出优化后的全文；若违反硬规则，先修正再输出。",
            "3. 文末用三行列出：改了什么 / 刻意保留了什么 / 是否触及结构。",
            "",
            "【待优化草稿】",
            "（在此粘贴草稿）",
            "",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="导出跨平台优化提示词")
    parser.add_argument(
        "--directions",
        default="",
        help="写作方向，逗号分隔；空则只导出 core",
    )
    parser.add_argument(
        "--intensity",
        default="medium",
        choices=sorted(INTENSITY.keys()),
        help="light / medium / restructure",
    )
    parser.add_argument("--out", default="", help="写入文件路径；默认 stdout")
    args = parser.parse_args()

    dirs: list[str] = []
    if args.directions.strip():
        dirs = parse_directions(args.directions, allow_core=False)
        bad = [d for d in dirs if d not in WRITING_DIRECTION_IDS]
        if bad:
            raise SystemExit(f"非法写作方向: {bad}")

    prompt = build_prompt(dirs, args.intensity)
    if args.out:
        out = Path(args.out)
        write_text(out, prompt)
        print(str(out.resolve()))
    else:
        print(prompt)


if __name__ == "__main__":
    main()
