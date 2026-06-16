# 基本设计
这是一次思路重构
user调用skill的人

## 1 注入启动
1. 将本repo的codex skills注入到另一个research repo中，
2. 更改被注入的repo的.gitignore保持这些skill不会上传
3. 我确认一点，这样是不是不应该使用git clone

## 2 使用skill基于规则构建一个修改用的文件夹
1. 这应该建立一个skill固化当前的文件机构
在被注入的文件夹中，应该新增一个Rev（在这里我们就用Rev）文件夹，这个由user决定
2. 这个Rev中，应该包括origin/，revision/，docs/
3. 以下为各个文件夹的使用说明。在初始化的时候不需要构建这些内容。具体内容注入应该在procdure决定后执行。
origin存储论文原稿，原始的审稿意见，编辑意见。这是由人类粘贴进来的。
docs存log，procedure，revisionplan等内容，这个文件夹主要有agent来处理
revision存markup.docx，这部分ai可以读，但是不能写入。clean.docx也在这里可以由skill控制生成。但是skill不能改。response-draft.md 这个有skill生成原始稿件，根据规则构建，把审稿人意见和编辑意见贴入，并占位，之后由人类逐步修改。在修改完抽，response-draft.docx通过skill由response-draft.md转化而成response-draft.docx。之后由人类审阅。
etc/这个是optional不强制建立。

4. 本质上，origin/就是输入，revision就是输出，docs就是执行的日志计划等文档的记录。

## 3 在docs中构建procedure
应该启动build-procedure skill来构建docs/procedure.md
是不是可以把模版融合在skill中

## 4 流程执行skill
这个skill应该执行，提示，和logging
如果应该机器执行的任务，就执行
如果是人应该执行的任务，就提示操作
具体步骤执行完就往对应的文档中log。


## 我关注的问题：
1. skill的数量
2. 怎么把skill加入到目标repo中

## 总体设计
能不能帮我在idea中写一个总体设计。

不要猜测我的意图。
有任何不懂都要问我。
用中文问我
