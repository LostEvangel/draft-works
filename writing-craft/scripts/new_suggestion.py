#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按模板在 suggestions/ 新建单次优化建议文件。"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    DIRECTION_ZH,
    SUGGESTIONS,
    TEMPLATES,
    ensure_utf8_stdio,
    parse_directions,
    read_text,
    slugify,
    write_text,
)


def main() -> None:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="新建 suggestions 文件")
    parser.add_argument("--title", required=True, help="建议标题（简题）")
    parser.add_argument("--draft", default="", help="原文标题或路径")
    parser.add_argument(
        "--directions",
        required=True,
        help="方向，逗号分隔，如 lyrical,argumentative 或 抒情,议论",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="日期 YYYY-MM-DD，默认今天",
    )
    args = parser.parse_args()

    dirs = parse_directions(args.directions, allow_core=False)
    dirs_yaml = "[" + ", ".join(dirs) + "]"
    tpl = read_text(TEMPLATES / "suggestion.md")

    # 填充前两个方向区块；其余方向追加空节
    zh_list = [DIRECTION_ZH[d] for d in dirs]
    body = tpl
    body = body.replace("{{date}}", args.date)
    body = body.replace("{{draft}}", args.draft or args.title)
    body = body.replace("{{directions}}", dirs_yaml)
    body = body.replace("{{title}}", args.title)
    body = body.replace("{{direction_zh_1}}", zh_list[0] if zh_list else "（方向）")
    body = body.replace(
        "{{direction_zh_2}}",
        zh_list[1] if len(zh_list) > 1 else "（可选方向）",
    )

    if len(zh_list) > 2:
        extra = []
        for zh in zh_list[2:]:
            extra.append(
                f"\n## 方向：{zh}\n\n### 建议 1\n\n- 问题：\n- 改法：\n- 示例：\n"
            )
        body = body.rstrip() + "\n" + "".join(extra)

    # 若只有一个方向，去掉第二个占位节
    if len(zh_list) == 1:
        marker = "## 方向：（可选方向）"
        if marker in body:
            body = body.split(marker)[0].rstrip() + "\n"

    fname = f"{args.date}-{slugify(args.title)}.md"
    path = SUGGESTIONS / fname
    if path.exists():
        raise SystemExit(f"已存在: {path}")
    write_text(path, body)
    print(str(path))


if __name__ == "__main__":
    main()
