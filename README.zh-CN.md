# KilaFrame Template 中文说明

主 README 为英文：[README.md](README.md)。本文是中文辅助说明。

KilaFrame Template 是一组用于论文审稿修改流程的 Codex skills。它本身不处理某一篇具体论文，而是提供可复用的 workflow skills，让用户把这些 skills 复制到某个 research repo 中使用。

## 核心边界

- 具体论文文件和修改输出属于目标 research repo。
- 修改工作区默认是 `Rev/`，但用户可以指定其他名称，例如 `Rev1/`。
- Codex 可以读取 `markup.docx`，但绝不能编辑、覆盖、移动、删除它，也不能在 markup 文件中接受修订。
- 论文正文替换必须由人类在 Word 中完成。
- Codex 可以从 markup DOCX 生成 clean DOCX，但必须输出为单独的 clean 文件，不能改变 markup 文件。
- 逐条 response 默认只输出给人类复制。只有人类在当次请求中明确授权写入时，Codex 才能写入 `{Rev}/revision/response-draft.md`。
- `{Rev}/origin/rawcomments.md` 和 `{Rev}/origin/editormessage.md` 只有在不存在时才创建；如果已经存在，不能覆盖。

## Skills 列表

当前包含七个 skills：

| Skill | 作用 |
| --- | --- |
| `init-revision-workspace` | 创建 `{Rev}/origin/`、`{Rev}/revision/`、`{Rev}/docs/`，只在缺失时创建空输入文件，并更新 `.gitignore`。 |
| `build-procedure` | 基于固定模板生成 `{Rev}/docs/procedure.md`，再做少量项目化修改。 |
| `execute-procedure` | 读取 procedure，检查当前状态，写 log，执行机器步骤，或提示人类下一步。 |
| `convert-origin-docx` | 将 `{Rev}/origin/{article_id}.docx` 转换为 `{Rev}/origin/origin.md` 和 `{Rev}/origin/originsrc/`。 |
| `make-clean-docx` | 将 `{Rev}/revision/{article_id}.rev.markup.docx` 复制为 `{Rev}/revision/{article_id}.rev.clean.docx`，只在 clean 文件中接受修订。 |
| `convert-response-docx` | 使用 skill 内置的 response DOCX 风格，将 `{Rev}/revision/response-draft.md` 转换为 `{Rev}/revision/response-draft.docx`。 |
| `build-response-draft` | 根据 structured comments、editor message 和 response template 生成 response 初稿或逐条 response 文本。 |

## 将 Skills 安装到目标 Research Repo

不要把本仓库 clone 到目标 research repo 内部。推荐使用临时 sparse checkout，然后只复制 `.codex/skills/`。

```bash
git clone --filter=blob:none --sparse https://github.com/<owner>/<repo>.git /tmp/kilaframe-template
cd /tmp/kilaframe-template
git sparse-checkout set .codex/skills

mkdir -p /path/to/research-repo/.codex
cp -R .codex/skills /path/to/research-repo/.codex/
```

把 `https://github.com/<owner>/<repo>.git` 替换为本模板仓库的 GitHub 地址，把 `/path/to/research-repo` 替换为目标 research repo。

`curl -O` 不作为默认推荐方式，因为 GitHub raw URL 适合下载单个文件，不适合可靠下载整个 `.codex/skills/` 目录。

## 目标工作区结构

初始化后，目标 repo 中的工作区结构如下。`{Rev}` 表示用户最终选择的工作区名称。

```text
{Rev}/
  origin/
    {article_id}.docx
    rawcomments.md
    editormessage.md
    origin.md
    originsrc/
  revision/
    {article_id}.rev.markup.docx
    {article_id}.rev.clean.docx
    response-draft.md
    response-draft.docx
  docs/
    procedure.md
    structuredcomments.md
    revisionplan.md
    procedure-execution.log
```

`{article_id}` 来自 `{Rev}/origin/{article_id}.docx` 的文件名。

`origin/` 是输入区，`revision/` 是输出和修改区，`docs/` 是 procedure、计划和日志区。

## 推荐 `.gitignore`

目标 repo 的 `.gitignore` 由 `init-revision-workspace` 更新。默认工作区为 `Rev/` 时，规则应类似：

```gitignore
.codex/skills/

Rev/*
!Rev/revision/
Rev/revision/*
!Rev/revision/response-draft.md
```

如果工作区叫 `Rev1/`，则把规则中的 `Rev/` 替换为 `Rev1/`。

## 推荐使用流程

1. 将 skills 复制到目标 research repo。
2. 让 Codex 运行 `$init-revision-workspace`。默认使用 `Rev/`，也可以指定其他工作区名称。
3. 人类把 `{article_id}.docx`、`rawcomments.md` 和 `editormessage.md` 放入 `{Rev}/origin/`。
4. 让 Codex 运行 `$build-procedure`，生成 `{Rev}/docs/procedure.md`。
5. 让 Codex 运行 `$execute-procedure`。
6. Codex 检查当前状态，写入 `{Rev}/docs/procedure-execution.log`，然后执行下一个机器步骤，或提示人类操作。
7. 人类在 markup DOCX 中完成正文修改。
8. Codex 根据 procedure 继续生成 clean DOCX、起草 response、更新 plan，并将 response draft 转换为 DOCX。

## 开发说明

总体设计来源是 [idea/overall.md](idea/overall.md)。原始输入 idea 保存在 [idea/original-idea.md](idea/original-idea.md)。

内置 response DOCX 模板已经脱敏，位置是 `.codex/skills/convert-response-docx/assets/response-template.docx`。
