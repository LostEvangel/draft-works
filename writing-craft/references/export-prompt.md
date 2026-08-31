# 导出跨平台优化提示词

把已沉淀能力拼成纯文本提示词，可粘贴到豆包 / ChatGPT 等非 skill 平台。

## 何时用

- 用户说「导出提示词」「生成优化 prompt」
- 或运行：`uv run scripts/export_prompt.py --directions lyrical,argumentative`

## 拼接顺序

1. 角色与权限边界（固定短前言）
2. `capabilities/core/` 全部规则（按 priority：high → medium → low）
3. 用户指定方向目录下的规则
4. 优化强度（轻度 / 中度 / 结构重构，默认中度）
5. 「待优化草稿」占位

## Agent 手工导出时

1. 读 `capabilities/index.md` 与相关文件
2. 每条写成：`【优先级】禁止/要求…（触发：…）`
3. 输出完整可复制块；不要只给摘要
4. 可选写入 `suggestions/prompt-YYYY-MM-DD.md` 备案

脚本输出到 stdout；加 `--out path` 写文件。
