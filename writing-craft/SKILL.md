---
name: writing-craft
description: >-
  沉淀写作能力并多方向优化草稿：显式采纳的硬规则写入能力库（core 底盘 + 方向），
  单次建议单独存放，先推荐方向再出建议，默认不改稿；可导出跨平台提示词。
  触发词：「优化草稿」「写作能力」「沉淀建议」「采纳这条」「多方向改稿」
  「导出提示词」「writing-craft」。
---

# writing-craft · 写作能力沉淀与多方向优化

用已沉淀的硬规则优化新草稿；用户明确采纳的建议，写成可复用能力，供下次使用。

## 路径约定

本 skill 根目录即数据根目录（相对本 `SKILL.md`）：

| 路径 | 用途 |
|------|------|
| `directions.md` | 方向 / core 分层与中英映射 |
| `corpus.md` | 定稿语料指针（如 `D:\work\个人\文章`） |
| `capabilities/core/` | 全场景底盘（禁忌与底线） |
| `capabilities/<方向>/` | 方向专属能力 |
| `capabilities/index.md` | 能力索引 |
| `suggestions/` | 单次优化建议（与改稿分离） |
| `templates/` | 建议 / 能力模板 |
| `references/` | 跑偏自检、规则写法、导出说明 |
| `scripts/` | 安装、新建建议、采纳、列表、导出提示词 |

脚本一律：`uv run scripts/<name>.py ...`（UTF-8）。

## 工作流

### A. 优化草稿（默认）

1. 读草稿；加载 `capabilities/core/` + `index.md`；按相关方向打开能力文件。需要口吻范例时对照 `corpus.md` 中的定稿（勿整篇粘贴）。
2. 用 `references/ai-drift-checklist.md` 扫一遍常见跑偏（不必全文贴出）。
3. 推荐 2～3 个**写作方向**（不含 core），等用户确认。
4. 写可执行建议 → `suggestions/YYYY-MM-DD-简题.md`（可用 `new_suggestion.py`）。
5. 对话摘要展示；**默认不出全文改稿**。
6. 用户说「按某某方向改一版」时：先问优化强度（轻度 / 中度 / 结构重构，默认中度），再出改稿。

### B. 沉淀能力（仅显式采纳）

仅当用户说「采纳 / 记下这条 / 沉淀」时：

1. 定位建议条目。
2. 按 `references/capability-rules.md` 写成硬规则（禁止/要求 + 触发 + 优先级）。
3. 全场景 → `capabilities/core/`；仅某方向 → 对应目录。负面优先。
4. 更新 `index.md`（可用 `adopt.py`）。
5. 确认路径与规则原文。

未说采纳 → **禁止**写入 `capabilities/`。

### C. 导出跨平台提示词

用户说「导出提示词」或需要给豆包等非 skill 平台时：

- 读 `references/export-prompt.md`
- 或：`uv run scripts/export_prompt.py --directions lyrical`

### D. 安装

```bash
uv run scripts/install_links.py
# uv run scripts/install_links.py --force
```

软链到 `~/.agents/skills`、`~/.cursor/skills`、`~/.claude/skills`。

## 建议与能力质量

- 建议：问题 + 改法 + 原文短锚点；禁空话。
- 能力：必须是「禁止 X / 要求 Y」；见 `capability-rules.md`。
- 已有能力能覆盖的，优先引用再补新建议。

## 边界

- 未确认方向 → 不写完整建议文件。
- 未说改一版 → 不输出全文改稿。
- 与仓库内其他 skill 无依赖、不互相调用。

## References

- [directions.md](directions.md)
- [references/ai-drift-checklist.md](references/ai-drift-checklist.md)
- [references/capability-rules.md](references/capability-rules.md)
- [references/export-prompt.md](references/export-prompt.md)
