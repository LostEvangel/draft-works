# writing-craft scripts — UTF-8, run via: uv run scripts/<name>.py
from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
CAPABILITIES = SKILL_ROOT / "capabilities"
SUGGESTIONS = SKILL_ROOT / "suggestions"
TEMPLATES = SKILL_ROOT / "templates"
INDEX = CAPABILITIES / "index.md"

# core = 全场景底盘；其余为写作方向
DIRECTION_ZH = {
    "core": "核心底盘",
    "lyrical": "抒情",
    "argumentative": "议论",
    "narrative": "叙事",
    "expository": "说明",
}

DIRECTION_IDS = set(DIRECTION_ZH)
WRITING_DIRECTION_IDS = DIRECTION_IDS - {"core"}

PRIORITY_IDS = {"high", "medium", "low"}
PRIORITY_ZH = {"high": "高", "medium": "中", "low": "低"}


def ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except Exception:
            pass


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    return raw.decode("utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def slugify(text: str, max_len: int = 40) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", text, flags=re.UNICODE)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return (text or "untitled")[:max_len]


def resolve_direction(token: str) -> str:
    p = token.strip()
    for did, zh in DIRECTION_ZH.items():
        if p in (did, zh):
            return did
    raise SystemExit(
        f"未知方向: {token}（可选: {', '.join(sorted(DIRECTION_IDS))} 或中文名）"
    )


def parse_directions(raw: str, *, allow_core: bool = True) -> list[str]:
    parts = [p.strip() for p in re.split(r"[,，\s]+", raw) if p.strip()]
    out: list[str] = []
    for p in parts:
        key = resolve_direction(p)
        if not allow_core and key == "core":
            raise SystemExit("此处不能指定 core（core 始终自动加载）")
        if key not in out:
            out.append(key)
    if not out:
        raise SystemExit("至少指定一个方向")
    return out


def parse_priority(raw: str) -> str:
    p = raw.strip().lower()
    mapping = {
        "high": "high",
        "h": "high",
        "高": "high",
        "medium": "medium",
        "m": "medium",
        "中": "medium",
        "low": "low",
        "l": "low",
        "低": "low",
    }
    if p not in mapping:
        raise SystemExit("优先级须为 high/medium/low（或 高/中/低）")
    return mapping[p]


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    meta: dict[str, str] = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta


def section_after(text: str, heading: str) -> str:
    """Extract markdown body under `## heading` until next ##."""
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line.strip()):
            start = i + 1
            break
    if start is None:
        return ""
    buf: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        buf.append(line)
    return "\n".join(buf).strip()
