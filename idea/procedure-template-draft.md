# Revision Procedure Template Draft

> 这是 `build-procedure` 将来要固化的模板草案。实际生成时，`{Rev}` 替换为 user 选定的工作区名称，默认 `Rev`；`{article_id}` 从 `{Rev}/origin/{article_id}.docx` 的文件名识别。

## 0. 全局规则

1. `{Rev}/` 是本次 revision 工作区。
2. `{Rev}/origin/` 是输入区，存放人类提供的原稿、原始审稿意见、编辑意见，以及 agent 从原稿转换出的可读材料。
3. `{Rev}/revision/` 是修订输出区，存放 markup docx、clean docx、`response-draft.md` 和 `response-draft.docx`。
4. `{Rev}/docs/` 是流程记录区，存放 procedure、structured comments、revision plan、执行 log 和检查记录。
5. Agent 不得修改、覆盖、移动、删除 `*.rev.markup.docx` 或任何 user 指定的 markup Word 文件。
6. 正文替换由 human 在 markup Word 文档中完成。
7. Agent 可以从 markup Word 文件生成独立 clean docx，但不得改变 markup Word 文件。
8. 每一步执行后，`execute-procedure` 应写入 `{Rev}/docs/procedure-execution.log`。
9. Agent 可以检查 `{Rev}/` 外的 repo 代码、数据、脚本和结果文件来构思修改方案；这些目录名称不固定，不应假定一定叫 `code/` 或 `data/`。
10. 不要用记忆中的文档替代当前 repo 文件。检查必须基于当前文件。

## 1. Human: 放入初始输入文件

Human 负责准备：

- `{Rev}/origin/{article_id}.docx`
- `{Rev}/origin/rawcomments.md`
- `{Rev}/origin/editormessage.md`
- `{Rev}/revision/{article_id}.rev.markup.docx`

规则：

- `{article_id}` 来自 `{Rev}/origin/{article_id}.docx` 的文件名。
- `rawcomments.md` 存放从邮件或审稿系统复制出的原始 reviewer comments。
- `editormessage.md` 存放 editor message；如果没有 editor message，可以保持为空。
- `rawcomments.md` 和 `editormessage.md` 只应在缺失时由初始化步骤创建为空文件；如果已存在，Agent 不得覆盖，必须提醒 human 检查已有内容。
- `{article_id}.rev.markup.docx` 是 human 后续直接修改的 Word markup 文件。
- Agent 不得替 human 移动、另存或修改 markup 文件。

完成后：

- `execute-procedure` 记录 human input 是否存在。
- 如果缺文件，只提示 human 补充，不假装完成。

## 2. Agent: 转换原稿为可读 Markdown

输入：

- `{Rev}/origin/{article_id}.docx`

输出：

- `{Rev}/origin/origin.md`
- `{Rev}/origin/originsrc/`

规则：

- `origin.md` 是 agent 为阅读和定位修改建议生成的可读转换版。
- `originsrc/` 存放转换产生的图片或资源。
- 如果转换工具不可用，记录 blocker，并提示 human 或后续 agent 安装/提供工具。

完成后：

- `execute-procedure` 写入转换结果和验证范围。

## 3. Agent: 结构化 raw comments

输入：

- `{Rev}/origin/rawcomments.md`

输出：

- `{Rev}/docs/structuredcomments.md`

规则：

- 只重新分条，不改写 comment 内容。
- Reviewer 用一级标题，例如 `# Reviewer 1`。
- Comment 用二级标题，例如 `## Comment 1`。
- 如果 reviewer 有 overall comment，放在 `## Overall Comment`。
- reviewer 原报告中的编号可以作为理解依据，但最终应按实际 comment 重新分条和编号。
- 必须保留原始 comment 文本，不得新增、删减或改写实质内容。

完成后：

- `execute-procedure` 写入生成结果。

## 4. Human: 检查 comment 数量和分条

输入：

- `{Rev}/origin/rawcomments.md`
- `{Rev}/docs/structuredcomments.md`

Human 负责检查：

- comment 数量是否正确。
- 分条是否合理。
- overall comment 是否处理正确。

规则：

- 这是 human-only 步骤。
- Agent 只能提示 human 检查，不得自动标记 human 已确认。

完成后：

- Human 告诉 agent 是否通过。
- `execute-procedure` 记录 human 确认结果。

## 5. Agent: 验证 structured comments 没有编造内容

输入：

- `{Rev}/origin/rawcomments.md`
- `{Rev}/docs/structuredcomments.md`

输出：

- 验证结果写入 `{Rev}/docs/procedure-execution.log`

规则：

- 检查 structured comments 是否只改变标题和结构。
- 检查是否出现 raw comments 中不存在的 comment 内容。
- 检查是否遗漏 raw comments 中的实质内容。

如果发现问题：

- 说明具体问题。
- 不继续构建 revision plan。

## 6. Agent: 构建 revision plan

输入：

- `{Rev}/docs/structuredcomments.md`

输出：

- `{Rev}/docs/revisionplan.md`

表格列：

- reviewer id
- comment id
- 修改序号
- 问题简述
- 风险等级
- 影响的章节
- 修改计划
- 是否搞定

排序原则：

1. 与其他 comment 无耦合的优先。
2. 文字性修改优先，需要增补计算或分析的后排。
3. 局部修改优先，全局修改后排。
4. overall comment 放在最后，因为细节修改完成后整体回复更容易确定。

完成后：

- `execute-procedure` 写入 plan 生成结果。

## 7. Agent: 生成 response draft

输入：

- `{Rev}/docs/structuredcomments.md`
- `{Rev}/origin/editormessage.md`
- response template 规则

输出：

- `{Rev}/revision/response-draft.md`

规则：

- Response template 不由 `build-procedure` 提供。
- Response template 应由 `execute-procedure` 调用的其他 skill 提供，具体 skill 名称待定。
- 按 reviewer/comment 顺序复制 comment content。
- 不得修改 reviewer comment 原文。
- editor message 如需回应，则放入 editor 部分；如果不需要具体答复，可以只作为记录。
- 为每个 response 留出后续 human 粘贴引文、页码、行号的位置。

完成后：

- 复查 comment 数量。
- 复查 comment 内容是否与 structured comments 严格一致。
- `execute-procedure` 写入生成和复查结果。

## 8. Iterative Revision Loop: 按 comment 修改

每条 comment 的循环：

1. Human 询问当前最高优先级且未完成的 comment。
2. Agent 读取 `{Rev}/docs/revisionplan.md`，选择排序最高且未完成的一条。
3. Agent 可读取 `{Rev}/origin/origin.md`、clean docx、相关代码、数据、脚本、结果文件，构思修改方案。
4. Agent 给出原文修改建议、分析补充建议或需要 human 执行的操作。
5. Human 在 `{Rev}/revision/{article_id}.rev.markup.docx` 中实际修改正文。
6. Agent 从 markup 生成 `{Rev}/revision/{article_id}.rev.clean.docx`，但不得修改 markup。
7. Agent 读取 clean docx，检查 human 修改是否支持回复该 comment。
8. Agent 起草该 comment 的 response 段落，写入或建议写入 `{Rev}/revision/response-draft.md`。
9. Human 审阅 response。
10. 如果 human 确认通过，Agent 更新 `{Rev}/docs/revisionplan.md` 的完成状态，并写 log。

Response 段落模式：

- 感谢 reviewer。
- 说明修改了哪个章节或部分。
- 用一句话概述如何修改。
- 保留 human 后续粘贴引文、页码、行号的位置。

如果 Agent 判断 response 或修改不充分：

- 只说明问题和建议下一步。
- 如果 user 明确要求不要动 md，则不得修改 `response-draft.md`。

## 9. Agent: 转换 response draft 为 docx

输入：

- `{Rev}/revision/response-draft.md`

输出：

- `{Rev}/revision/response-draft.docx`

规则：

- 使用 response docx 格式规则或相关 skill。
- 转换后检查结构和明显格式问题。
- 不修改 markup docx。

完成后：

- `execute-procedure` 写入转换和检查结果。

## 10. Human: 最终审阅

Human 审阅：

- `{Rev}/revision/response-draft.docx`
- `{Rev}/revision/{article_id}.rev.markup.docx`
- `{Rev}/revision/{article_id}.rev.clean.docx`
- 其他需要提交的 supplement 或 revision 文件

Agent 可以：

- 检查 clean docx、response docx、supplement 文件并提出意见。
- 只提意见，不修改 docx，除非 user 明确要求生成新的非 markup 输出文件。

Agent 不得：

- 修改 markup docx。
- 替 human 完成最终审阅。
