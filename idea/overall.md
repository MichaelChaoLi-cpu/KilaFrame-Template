# Manuscript Revision Skill System 总体设计

## 0. 设计目标

本项目不是直接处理某一篇论文，而是提供一组 Codex skills，用来注入到具体 research repo 中，帮助人类完成审稿修改流程。

核心目标：

1. 将本 repo 中维护的 Codex skills 复制或同步到目标 research repo。
2. 在目标 repo 中建立一个用于审稿修改的工作区，默认是 `Rev/`，也可以由 user 指定为 `Rev1/` 等名称。
3. 基于固定模板和少量项目化修改生成 `{Rev}/docs/procedure.md`。
4. 由执行 skill 按 procedure 检查进度、写 log、提示人类下一步，或自动执行机器可执行步骤。
5. 明确边界：agent 可以读 `markup.docx`，但不能写、改、覆盖或接受其中修订；正文替换由人类完成。

## 1. 角色分工

### User

User 是调用 skill 的人，也是最终流程控制者。

User 负责：

- 决定目标 research repo。
- 决定工作区文件夹名称。默认是 `Rev/`，也可以指定为 `Rev1/` 等名称。
- 提供论文原稿、审稿意见、编辑意见。
- 在 Word markup 文档中实际修改正文。
- 审阅 agent 生成的计划、response draft、docx 输出和 log。

### Agent

Agent 负责：

- 根据 README 中的命令获取或更新 skills。
- 根据规则初始化工作区结构。
- 根据模板和用户要求生成 procedure。
- 检查流程执行状态。
- 写入执行日志。
- 执行机器可执行任务。
- 对人类步骤给出明确提示。

Agent 不负责：

- 修改 `markup.docx`。
- 替人类在 Word 中完成正文替换。
- 假装完成人类必须检查或确认的步骤。

## 2. 目标 Repo 获取 Skills 设计

### 2.1 获取内容

目标 research repo 需要获得本 repo 中维护的 skills：

```text
.codex/skills/
  init-revision-workspace/
  build-procedure/
  execute-procedure/
  convert-origin-docx/
  make-clean-docx/
  convert-response-docx/
  build-response-draft/
```

具体 skill 名称可以后续调整，但职责应保持分离。

### 2.2 不需要 inject-revision-skills

目前不需要单独建立 `inject-revision-skills`。

原因：

1. 本 repo 会上传到 GitHub，安装或更新命令可以直接写在 README 中。
2. 注入本身是一次性或低频操作，不需要占用一个 runtime skill。
3. 目标 repo 的 `.gitignore` 更新应由 `init-revision-workspace` 完成，因为它同时知道工作区名称和需要开放给 git 的文件。

### 2.3 是否可以只下载 repo 的一部分

可以。README 可以提供命令，让 user 只下载或同步本 repo 中的 `.codex/skills/`。

可选方式：

1. 推荐使用 `git sparse-checkout` 获取指定目录。
2. 下载 GitHub archive 后只解压 `.codex/skills/`。
3. 使用 GitHub API 或专门工具下载单个目录。

这里不使用 `git clone` 把整个 repo 放进目标 repo 内部。

### 2.4 目标 repo 的 `.gitignore`

`.gitignore` 由 `init-revision-workspace` 更新，而不是由独立注入 skill 更新。

目标 repo 应避免上传注入的 skills：

```gitignore
.codex/skills/
```

同时，新建的 revision 工作区默认也应进入 `.gitignore`，只开放 `{Rev}/revision/response-draft.md` 给 git。以默认工作区 `Rev/` 为例：

```gitignore
Rev/*
!Rev/revision/
Rev/revision/*
!Rev/revision/response-draft.md
```

如果 user 指定其他工作区名称，例如 `Rev1/`，`init-revision-workspace` 应把上述规则中的 `Rev/` 替换成实际名称。

### 2.5 不应使用 `git clone` 注入

这个场景不适合把本 repo `git clone` 到目标 repo 中。

原因：

1. `git clone` 会带入独立 `.git/`、remote、历史和仓库边界，不适合做轻量注入。
2. 目标 repo 只需要 skills 文件，不需要本 repo 的完整历史。
3. clone 到目标 repo 内部容易形成嵌套 repo，增加同步和提交风险。
4. 获取后的 skills 按设计应被 `.gitignore` 忽略，不属于目标 repo 要上传的研究内容。

推荐方式是复制或同步本 repo 中的 skill 目录到目标 repo 的 `.codex/skills/`。如果需要版本管理，应在本 repo 中管理模板和 skills，而不是在每个目标 research repo 中 clone 一份。

## 3. Rev 工作区设计

### 3.1 工作区根目录

在目标 repo 中创建一个 revision 工作区。默认名为：

```text
Rev/
```

这个名称可以由 user 改写，例如 `Rev1/`。后文用 `{Rev}/` 表示最终确定的工作区根目录。

### 3.2 基础结构

初始化时建立目录，并在缺失时创建两个空的评论输入文件：

```text
Rev/
  origin/
    rawcomments.md
    editormessage.md
  revision/
  docs/
```

`etc/` 是 optional，不强制建立。

如果 `{Rev}/origin/rawcomments.md` 或 `{Rev}/origin/editormessage.md` 已存在，初始化过程不得写入或覆盖它们，而应提醒 human 检查已有内容。

### 3.3 目录职责

`origin/` 是输入区。

用于存放：

- 论文原稿，命名为 `{article_id}.docx`。
- 原稿转换后的可读 Markdown，命名为 `origin.md`。
- 原稿转换产生的图片目录，命名为 `originsrc/`。
- 原始审稿意见。
- 编辑意见。

这些内容主要由人类放入或粘贴。

`revision/` 是输出和修订区。

用于存放：

- `markup.docx` 或 `{article_id}.rev.markup.docx`。
- `clean.docx` 或 `{article_id}.rev.clean.docx`。
- `response-draft.md`。
- `response-draft.docx`。

边界：

- Agent 可以读 `markup.docx`。
- Agent 不能写、改、覆盖、移动、删除 `markup.docx`。
- Agent 运行时自动从 markup 生成 clean 版本，但必须输出为独立 clean 文件，不能改变 markup 文件。
- `response-draft.md` 固定放在 `{Rev}/revision/response-draft.md`，可由 agent 生成初稿，并由人类逐步修改。
- `response-draft.docx` 可由 skill 从 `response-draft.md` 转换生成，之后由人类审阅。
- `{article_id}` 来自 `{Rev}/origin/{article_id}.docx` 的文件名。

`docs/` 是流程和记录区。

用于存放：

- `procedure.md`
- `structuredcomments.md`
- `revisionplan.md`
- `procedure-execution.log`
- 其他流程记录、检查结果、规则化文档

这个文件夹主要由 agent 处理，但人类可以审阅和修正。

## 4. Procedure 构建设计

### 4.1 build-procedure skill

`build-procedure` 的职责是基于固定模板生成：

```text
{Rev}/docs/procedure.md
```

它不直接执行 revision 流程，只负责把固定模板复制为项目 procedure，并根据 user 的少量项目化要求修改。

### 4.2 模板是否放入 skill

procedure 使用固定模板，再做少量项目化修改。可以把 procedure 模板融合在 skill 中。

建议方式：

- 如果模板很短，直接写在 `build-procedure/SKILL.md` 中。
- 如果模板较长，放在 `build-procedure/references/procedure-template.md`。
- 如果需要生成固定文件结构或样板文件，可以放在 `build-procedure/assets/`。

这样目标 repo 不需要预先存在 `etc/procedure.md`。目标 repo 的正式流程文件应是 `{Rev}/docs/procedure.md`。

Response template 不放在 `build-procedure` 中；它应由 `build-response-draft` 提供或引用。

### 4.3 Procedure 的内容边界

`procedure.md` 应明确：

- 哪些步骤由人类执行。
- 哪些步骤由 agent 执行。
- 哪些步骤需要人类确认后 agent 才能继续。
- 每一步的输入文件。
- 每一步的输出文件。
- 每一步完成后写入哪个 log 或更新哪个计划文件。
- `markup.docx` 禁止写入规则。
- `{article_id}` 从 `{Rev}/origin/{article_id}.docx` 识别。
- Agent 可以检查 `{Rev}/` 之外的 repo 代码、数据、脚本和结果文件来构思修改方案，但不得把这些目录假定为固定名称。

## 5. 流程执行设计

### 5.1 execute-procedure skill

`execute-procedure` 是流程调度器，不直接承载格式转换逻辑。它的职责是：

1. 读取 `{Rev}/docs/procedure.md`。
2. 检查 `{Rev}/` 当前文件状态。
3. 判断当前处于哪一步。
4. 如果下一步是机器任务，则执行或调用对应子 skill。
5. 如果下一步是人类任务，则提示 user 操作。
6. 每一步完成后写 log。
7. 必要时更新 `{Rev}/docs/revisionplan.md` 或相关文档。

它调用的子 skill 包括：

- `convert-origin-docx`: `{Rev}/origin/{article_id}.docx` -> `{Rev}/origin/origin.md` 和 `{Rev}/origin/originsrc/`。
- `make-clean-docx`: `{Rev}/revision/{article_id}.rev.markup.docx` -> `{Rev}/revision/{article_id}.rev.clean.docx`，禁止修改 markup。
- `convert-response-docx`: `{Rev}/revision/response-draft.md` -> `{Rev}/revision/response-draft.docx`，格式规则放在该 skill 中，作为个人风格固化。
- `build-response-draft`: 根据 structured comments、editor message 和 response template 生成 response draft 初稿或 response 文本。

### 5.2 Logging 规则

主执行日志写入：

```text
{Rev}/docs/procedure-execution.log
```

每次执行至少记录：

- 时间。
- user 请求。
- 检查了哪些文件。
- 当前 procedure step。
- 执行了什么。
- 验证了什么。
- 是否修改文件。
- 下一步是谁执行。
- `markup.docx` 是否保持未修改。

### 5.3 自动执行和提示边界

Agent 可以自动执行：

- 生成 structured comments。
- 校验 structured comments 是否忠实于 raw comments。
- 生成 revision plan。
- 调用 `build-response-draft` 生成 response draft 初稿。
- 调用 `make-clean-docx` 从 markup 自动生成 clean docx，但不得修改 markup docx。
- 调用 `convert-origin-docx` 转换原稿。
- 调用 `convert-response-docx` 将 response draft 转换为 docx。
- 检查 clean docx 或 response docx 并提出意见。
- 检查 `{Rev}/` 之外的 repo 代码、数据和分析材料，用于制定对 comment 的修改方案。

Agent 默认不得直接写入 `{Rev}/revision/response-draft.md` 的逐条 response 修改内容。逐条 response 应先输出为方便 human 复制的文本，由 human 粘贴进 `response-draft.md`。只有 human 在当次请求中明确授权写入时，agent 才能写入；授权每次都要重新获得。

Agent 只提示人类执行：

- 保存或移动原始 Word 文件。
- 粘贴审稿意见和编辑意见。
- 检查 comment 数量和分条是否合理。
- 在 `markup.docx` 中做正文修改。
- 在 response 中粘贴引文、页码、行号。
- 审阅最终 docx。

## 6. Skill 数量设计

建议最小可维护版本为 7 个 skills：

1. `init-revision-workspace`
   - 在目标 repo 中创建 `{Rev}/`，默认是 `Rev/`，也可由 user 指定为 `Rev1/` 等名称。
   - 建立 `origin/`、`revision/`、`docs/`。
   - 在缺失时创建空文件 `{Rev}/origin/rawcomments.md` 和 `{Rev}/origin/editormessage.md`；如果已存在则不覆盖，并提醒 human 检查。
   - 更新目标 repo `.gitignore`。
   - 忽略注入的 `.codex/skills/`。
   - 忽略新建的 revision 工作区，只开放 `{Rev}/revision/response-draft.md` 给 git。
   - 不填充具体论文内容。

2. `build-procedure`
   - 从固定模板生成 `{Rev}/docs/procedure.md`，并根据 user 要求少量修改。
   - 明确人类步骤、agent 步骤、输入、输出、日志位置和禁止修改 markup 的规则。

3. `execute-procedure`
   - 按 `{Rev}/docs/procedure.md` 执行流程。
   - 自动执行机器步骤或调度子 skill。
   - 提示人类步骤。
   - 写入 `{Rev}/docs/procedure-execution.log`。

4. `convert-origin-docx`
   - 将 `{Rev}/origin/{article_id}.docx` 转换为 `{Rev}/origin/origin.md`。
   - 将图片和资源输出到 `{Rev}/origin/originsrc/`。

5. `make-clean-docx`
   - 复制 `{Rev}/revision/{article_id}.rev.markup.docx` 为 clean docx。
   - 在 clean docx 中接受全部修订。
   - 禁止修改 markup docx。

6. `convert-response-docx`
   - 将 `{Rev}/revision/response-draft.md` 转换为 `{Rev}/revision/response-draft.docx`。
   - 格式规则放在该 skill 中，用于固化个人文档风格。

7. `build-response-draft`
   - 根据 `{Rev}/docs/structuredcomments.md`、`{Rev}/origin/editormessage.md` 和 response template 生成 response draft 初稿或逐条 response 文本。
   - 默认逐条 response 只输出给 human 复制，不直接写入 `response-draft.md`。
   - 只有 human 在当次请求明确授权时才可写入 `response-draft.md`。

## 7. 推荐调用顺序

在目标 research repo 中，user 的使用顺序是：

```text
1. 按 README 命令把本 repo 的 skills 获取到目标 repo 的 .codex/skills/
2. 使用 init-revision-workspace 初始化 {Rev}/ 并更新 .gitignore
3. 人类把原稿、审稿意见、编辑意见放入 {Rev}/origin/
4. 使用 build-procedure 生成 {Rev}/docs/procedure.md
5. 使用 execute-procedure 检查当前状态并推进流程
6. 人类根据提示在 markup.docx 中修改正文
7. execute-procedure 继续检查、写 response、更新 log 和计划
```

## 8. 已确认设计决策

以下为已确认决策：

1. 工作区默认使用 `Rev/`，但 user 可以指定其他名称，例如 `Rev1/`。
2. `response-draft.md` 固定放在 `{Rev}/revision/response-draft.md`。
3. `clean.docx` 由 agent 自动从 markup 生成，但 agent 不得修改 markup 文件。
4. `procedure.md` 从固定模板复制后做少量项目化修改。
5. README 中推荐使用 `git sparse-checkout` 获取本 repo 的 `.codex/skills/`。
6. `{article_id}` 来自 `{Rev}/origin/{article_id}.docx`。
7. `origin.md` 放在 `{Rev}/origin/origin.md`。
8. 原稿图片目录放在 `{Rev}/origin/originsrc/`。
9. `structuredcomments.md` 放在 `{Rev}/docs/structuredcomments.md`。
10. `response-template` 不放进 `build-procedure`，由 `execute-procedure` 调用的其他 skill 提供。
11. convert 类能力拆为独立 skills：`convert-origin-docx`、`make-clean-docx`、`convert-response-docx`。
12. response draft 生成拆为独立 skill：`build-response-draft`。
13. `convert-response-docx` 的格式规则放入该 skill，用于固化个人文档风格。
14. Agent 默认不得直接写入逐条 response 到 `{Rev}/revision/response-draft.md`；必须每次获得 human 明确授权。
