#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 writing-craft 软链到 ~/.agents、~/.cursor、~/.claude 的 skills 目录。"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import SKILL_ROOT, ensure_utf8_stdio  # noqa: E402


TARGETS = [
    Path.home() / ".agents" / "skills" / "writing-craft",
    Path.home() / ".cursor" / "skills" / "writing-craft",
    Path.home() / ".claude" / "skills" / "writing-craft",
]


def _is_link_or_junction(path: Path) -> bool:
    if path.is_symlink():
        return True
    if os.name == "nt" and path.exists():
        try:
            import ctypes

            FILE_ATTRIBUTE_REPARSE_POINT = 0x400
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))  # type: ignore[attr-defined]
            return attrs != -1 and bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)
        except Exception:
            return False
    return False


def link_one(target: Path, force: bool) -> str:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink() or _is_link_or_junction(target):
        if not force:
            return f"跳过（已存在）: {target}"
        if target.is_symlink() or _is_link_or_junction(target):
            target.unlink()
        elif target.is_dir():
            # 真实目录：不擅自删除，避免误伤
            return f"失败（是真实目录，请手动处理）: {target}"
        else:
            target.unlink()

    src = SKILL_ROOT
    try:
        os.symlink(src, target, target_is_directory=True)
        return f"软链: {target} → {src}"
    except OSError as e:
        if os.name == "nt":
            # 无管理员权限时尝试 directory junction
            import subprocess

            r = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(target), str(src)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if r.returncode == 0:
                return f"junction: {target} → {src}"
            return f"失败: {target}: {e}; junction: {r.stderr or r.stdout}"
        return f"失败: {target}: {e}"


def main() -> None:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="安装 writing-craft 到本地 AI 平台 skills 目录")
    parser.add_argument("--force", action="store_true", help="覆盖已有软链/junction")
    args = parser.parse_args()

    print(f"源目录: {SKILL_ROOT}")
    for t in TARGETS:
        print(link_one(t, args.force))


if __name__ == "__main__":
    main()
