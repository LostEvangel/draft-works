# draft-works · 文稿工坊

中文写作相关的 Agent Skill 合集。各 skill 相互独立。

## 包含的 skill

### writing-craft — 写作能力沉淀与多方向优化

沉淀已采纳的**硬规则**（core 底盘 + 方向）；多方向优化建议单独存放；默认不改稿；可导出跨平台提示词。

触发词：`优化草稿` `写作能力` `沉淀建议` `采纳这条` `导出提示词` `writing-craft`

```bash
cd writing-craft
uv run scripts/install_links.py          # 软链到 ~/.agents、~/.cursor、~/.claude
uv run scripts/export_prompt.py --directions lyrical
```

### editorial-review — 编辑审阅

专业的第三方审稿人角色。分析文章的结构、内容、文字三个维度，给出分级修改意见，支持多轮迭代直至定稿。

触发词：`审阅这篇文章` `编辑审阅` `帮我改文章` `看一篇稿子`

### revision-article — 作者-编辑协作改稿

我是作者，你是编辑——你给我意见，我根据意见修改。文艺向文风，多轮迭代直至定稿。

触发词：`帮我改改这篇文章` `revision` `看看这篇稿子`

### literary-compare — 文学对照讲评

对比优化前/优化后两个版本，讲清改动思路与可迁移能力。

触发词：`对比两个版本` `优化前后` `文学老师` `讲评改稿`

## 安装

```bash
# 进入你的项目目录后，复制或软链需要的 skill
cp -r draft-works/editorial-review ~/.claude/skills/
cp -r draft-works/revision-article ~/.claude/skills/

# writing-craft 推荐用安装脚本（同时链到 agents / cursor / claude）
cd draft-works/writing-craft
uv run scripts/install_links.py
```
