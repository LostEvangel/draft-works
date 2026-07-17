# draft-works · 文稿工坊

中文文章编辑审阅的 Claude Code skill 合集。

## 包含的 skill

### editorial-review — 编辑审阅

专业的第三方审稿人角色。分析文章的结构、内容、文字三个维度，给出分级修改意见，支持多轮迭代直至定稿。

触发词：`审阅这篇文章` `编辑审阅` `帮我改文章` `看一篇稿子`

### revision-article — 作者-编辑协作改稿

我是作者，你是编辑——你给我意见，我根据意见修改。文艺向文风，多轮迭代直至定稿。

触发词：`帮我改改这篇文章` `revision` `看看这篇稿子`

## 区别

| skill | 角色 | 谁动手改 | 适用场景 |
|-------|------|----------|----------|
| editorial-review | 审稿人 | 用户自己 | 需要第三方客观判断 |
| revision-article | 作者 | AI（以作者身份） | 有自己的判断，需要改稿人手 |

## 安装

```bash
# 进入你的项目目录
cd your-project

# 复制需要的 skill
cp -r draft-works/editorial-review .claude/skills/
cp -r draft-works/revision-article .claude/skills/
```

重启 Claude Code 后即可使用。
