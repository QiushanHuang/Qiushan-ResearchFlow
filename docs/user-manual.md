# ResearchFlow User Manual

**Scope:** public-sanitized operational manual. It describes how to use the framework without exposing private memory or real project history.

## 1. Operating Model

ResearchFlow is normally used through natural language in an agent thread. The user states an intention, the agent loads the smallest relevant indexes, chooses the proper workflow, runs deterministic scripts where useful, and reports evidence-backed results.

The user does not need to remember shell commands for ordinary use. Commands and scripts are part of the agent's internal execution surface and can be shown for transparency when requested.

## 2. First Contact Prompt

Use this when opening a project thread:

```text
Use ResearchFlow for this project. Load the framework indexes first, choose the safest connection mode, connect the project, validate the adapter, and report what changed.
```

Expected agent behavior:

- read `rf.yaml`, `indexes/project.index.jsonl`, and `indexes/project-interface.index.jsonl`;
- inspect the project root without scanning heavy artifacts by default;
- choose native mode only when adding `.researchflow/` metadata is acceptable;
- choose legacy shadow mode when the target project should not be modified;
- run validation and summarize created files, skipped files, and residual risk.

## 3. Connecting A New Native Project

Use native mode when the project can carry its own ResearchFlow metadata.

Natural language prompt:

```text
Connect this as a native ResearchFlow project. Create the local adapter, set up the project indexes, validate it, and give me the next operating prompt.
```

Expected result:

- `<project-root>/.researchflow/project.rf.yaml`;
- project-local indexes for memory, procedures, skill usage, and artifacts when needed;
- a pointer entry in the framework project index;
- a validation report.

## 4. Connecting An Existing Legacy Project

Use legacy mode when the project directory should remain untouched.

Natural language prompt:

```text
Connect this old project to ResearchFlow without changing its folder. Use a shadow adapter inside ResearchFlow, validate it, and explain the boundary.
```

Expected result:

- a shadow adapter under `project-interfaces/legacy/<safe-project-id>/`;
- no file writes inside the target project;
- a framework-level pointer to the adapter;
- a clear note that the adapter is the ResearchFlow authority, while the target project remains structurally unchanged.

## 5. Daily Research Run

Use this when starting a normal work session:

```text
Start a ResearchFlow run for this task. Load only the relevant indexes first, make a compact plan, execute the verifiable steps, write a digest, propose any claims, and record anything that should become a future workflow improvement.
```

The standard run path is:

```text
intake -> triage -> plan -> run -> digest -> claim -> review -> done
```

The agent should branch to `needs_user` for creative judgment, permission, unclear external commitments, or safety-sensitive decisions.

## 6. Capturing Knowledge

ResearchFlow separates three common knowledge destinations:

- **Project memory:** exact project implementation details, parameters, local decisions, and run-specific evidence.
- **Universal or bridge memory:** reusable methods, common failure modes, transferable heuristics, and conditions under which a method works.
- **External library:** research notes, articles, papers, parameter explanations, theorem notes, RSS summaries, and study materials that should be indexed for later retrieval but not loaded by agents by default.

Natural language prompt:

```text
Record this answer in the right ResearchFlow knowledge layer. If it is project-specific, keep it local. If it is reusable, propose bridge or universal memory. If it is study material, index it as library knowledge and avoid adding it to default agent memory.
```

The agent should not promote a single observation into universal memory without evidence, scope, confidence, and invalidation conditions.

## 7. Capturing Problems And Framework Upgrades

Use the evolution system when you notice friction, bugs, missing modules, or agent behavior that should improve.

Natural language prompt:

```text
Record this as a ResearchFlow evolution signal. Normalize my wording, keep the raw signal, classify it, and turn it into an upgrade item if it is actionable.
```

Expected records:

- inbox signal with raw and normalized intent;
- evolution item for actionable work;
- journal for implementation;
- resolution after validation;
- knowledge movement note if the lesson enters memory, documentation, or skill guidance.

## 8. Skill Reuse

ResearchFlow records both skill inventory and skill usage. This helps future agents know which skills were effective in which context.

Typical prompt:

```text
Before solving this, check the ResearchFlow skill registry. Select relevant skills, use them, and record skill usage with project context and outcome.
```

Reusable actions can be named. For example, a project may define a named action for multi-agent review, repeated iteration, or a standard validation pass. The action name should point to a command document rather than forcing the user to repeat a long instruction every time.

## 9. Agent Reporting Style

A good ResearchFlow report should include:

- what was changed;
- what evidence was checked;
- what was not changed;
- validation results;
- residual risk;
- whether anything was written to memory, library, evolution logs, or skill usage records.

The report should not force the user to inspect logs to understand whether the issue was resolved.

## 10. What Agents Should Avoid Loading By Default

Agents should avoid default scanning of:

- raw simulation outputs;
- logs;
- checkpoints;
- binary artifacts;
- large arrays and model files;
- private memory;
- personal hardware records;
- project bodies that are not referenced by a relevant index.

Open body files only after the index shows why the file is relevant.

---

# ResearchFlow 使用手册

**范围：** 公开脱敏操作手册。它说明如何使用框架，但不包含私人记忆或真实项目历史。

## 1. 使用模型

ResearchFlow 通常通过 agent 线程中的自然语言使用。用户表达意图，agent 先加载最小相关索引，再选择合适工作流，在需要时调用确定性脚本，并用证据支撑结果汇报。

日常使用不要求用户记住 shell 命令。命令和脚本是 agent 的内部执行面，用户需要透明性时再展示。

## 2. 初次接入 Prompt

打开项目线程时可以这样说：

```text
在这个项目中使用 ResearchFlow。先加载框架索引，选择最安全的接入模式，完成项目接入，验证 adapter，并汇报修改了什么。
```

Agent 应该：

- 读取 `rf.yaml`、`indexes/project.index.jsonl` 和 `indexes/project-interface.index.jsonl`；
- 检查项目根目录，但默认不扫描大型产物；
- 只有在允许写入 `.researchflow/` 元数据时选择原生模式；
- 当目标项目不应被修改时选择旧项目影子模式；
- 运行校验，并总结创建文件、跳过文件和剩余风险。

## 3. 接入新原生项目

当项目可以保存自己的 ResearchFlow 元数据时，使用原生模式。

自然语言 prompt：

```text
把这个项目作为原生 ResearchFlow 项目接入。创建本地 adapter，建立项目索引，完成校验，并给我下一步操作 prompt。
```

预期结果：

- `<project-root>/.researchflow/project.rf.yaml`；
- 需要时创建项目本地 memory、procedure、skill usage 和 artifact 索引；
- 在框架项目索引中写入指针；
- 给出校验报告。

## 4. 接入旧项目

当项目目录不能被修改时，使用旧项目兼容模式。

自然语言 prompt：

```text
在不修改旧项目文件夹的情况下，把它接入 ResearchFlow。使用 ResearchFlow 内部的影子 adapter，完成校验，并解释边界。
```

预期结果：

- 在 `project-interfaces/legacy/<safe-project-id>/` 下创建影子 adapter；
- 不在目标项目内写入文件；
- 在框架层保存指向 adapter 的指针；
- 明确说明 adapter 是 ResearchFlow 侧的权威记录，目标项目结构保持不变。

## 5. 日常科研运行

普通工作会话可以这样开始：

```text
为这个任务启动 ResearchFlow run。先只加载相关索引，制定紧凑计划，执行可验证步骤，写 digest，提出必要 claim，并记录可能需要升级成未来流程的内容。
```

标准路径是：

```text
intake -> triage -> plan -> run -> digest -> claim -> review -> done
```

当任务需要创造性判断、权限、不清楚的外部承诺或安全敏感决策时，agent 应进入 `needs_user`。

## 6. 知识捕获

ResearchFlow 区分三类知识去向：

- **项目记忆：** 具体项目实现、参数、本地决策和运行证据。
- **通用或桥接记忆：** 可复用方法、常见失败模式、可迁移经验和方法适用条件。
- **外部资料库：** 研究笔记、论文、参数解释、定理记录、RSS 摘要和学习材料。它们应被索引方便检索，但不应默认进入 agent 记忆。

自然语言 prompt：

```text
把这个回答记录到合适的 ResearchFlow 知识层。如果是项目特定内容，留在项目本地；如果可复用，提出桥接或通用记忆 proposal；如果是学习资料，进入 library 索引，不加入默认 agent 记忆。
```

Agent 不应把单次观察直接提升为通用记忆，除非同时记录证据、适用范围、置信度和失效条件。

## 7. 问题记录和框架升级

当发现摩擦、bug、缺失模块或 agent 行为需要改进时，使用 evolution 系统。

自然语言 prompt：

```text
把这件事记录为 ResearchFlow evolution 信号。保留原始表达，优化成准确简洁的意图，分类，并在可执行时转成升级事项。
```

预期记录：

- inbox signal，包含原始输入和归一化意图；
- actionable evolution item；
- 实施 journal；
- 校验后的 resolution；
- 如果经验进入 memory、文档或 skill 指南，记录知识流向。

## 8. Skill 复用

ResearchFlow 同时记录 skill 清单和 skill 使用历史，帮助未来 agent 判断什么场景适合使用哪些 skill。

常用 prompt：

```text
解决这个任务前先检查 ResearchFlow skill registry。选择相关 skill，使用它们，并记录 skill usage，包括项目上下文和结果。
```

可复用动作可以被命名。例如，一个项目可以定义多 agent review、重复迭代或标准校验的动作名。动作名应指向 command 文档，而不是要求用户每次重复一大段长指令。

## 9. Agent 汇报规范

好的 ResearchFlow 汇报应包含：

- 修改了什么；
- 检查了什么证据；
- 没有修改什么；
- 校验结果；
- 剩余风险；
- 是否写入 memory、library、evolution log 或 skill usage record。

用户不应该必须翻日志才能知道问题是否被解决。

## 10. 默认不应读取的内容

Agent 默认应避免扫描：

- 原始模拟输出；
- 日志；
- checkpoint；
- 二进制产物；
- 大型数组和模型文件；
- 私人记忆；
- 个人硬件记录；
- 未被相关索引指向的项目正文。

只有索引说明文件相关时，再按需打开正文。
