# ResearchFlow

[![Status](https://img.shields.io/badge/status-public%20preview-2563eb)](#researchflow)
[![Docs](https://img.shields.io/badge/docs-English%20%7C%20%E4%B8%AD%E6%96%87-16a34a)](#中文说明)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](#validation)
[![Agent Workflow](https://img.shields.io/badge/agent-workflow-intent--driven-7c3aed)](#agent-philosophy)
[![Privacy](https://img.shields.io/badge/privacy-sanitized%20public%20release-0f766e)](#privacy-and-release-boundaries)
[![Index First](https://img.shields.io/badge/context-index--first-f59e0b)](#technical-characteristics)

**Language:** [English](#researchflow) | [中文](#中文说明)

ResearchFlow is an index-first workflow framework for agent-assisted research, experimentation, and project execution. It is designed for environments where long conversations, heterogeneous files, simulation artifacts, cross-project knowledge, and personal research habits can easily exceed an agent's working context.

The framework treats context as a scarce research resource. Agents first read compact indexes, then open evidence only when the task requires it. This keeps token cost low, reduces memory drift, and makes the reasoning path auditable.

## Agent Philosophy

ResearchFlow is built around a simple thesis: the human should spend attention on creative research judgment, while agents should absorb mechanical, repeated, and verifiable work after the first successful human-agent run has clarified intent.

An agent should not be reduced to a brittle sequence of point commands. It should operate from purpose, evidence, boundaries, and reusable procedures. Natural language remains the primary interface because a well-scoped intention gives the agent room to choose the right tool, while ResearchFlow's indexes, validators, and review gates keep that flexibility from becoming uncontrolled behavior.

## Project Characteristics

Functional characteristics:

- Natural-language onboarding for new and existing projects.
- Native project adapters for projects that can accept `.researchflow/` metadata.
- Legacy shadow adapters for projects that must not be modified.
- Universal, bridge, project, and external-library knowledge layers.
- Evolution inbox, issue records, journals, resolutions, and self-check paths for framework upgrades.
- Skill inventory and skill usage records, including which agent skills were useful in which project context.
- Resource and storage indexes for compute-aware research planning.
- Public/private release boundaries for publishing sanitized framework material.

Technical characteristics:

- JSONL indexes provide high-density entry points before body files are loaded.
- Read policies such as `index_only`, `on_demand`, `adapter_first`, `registry_only`, and `skip` control context loading.
- A compact state machine keeps agent runs resumable: `intake -> triage -> plan -> run -> digest -> claim -> review -> done`.
- Markdown frontmatter templates standardize claims, digests, memory proposals, procedures, evolution records, and skill usage logs.
- Lightweight Python validators check index structure, memory proposal safety, project adapter boundaries, release hygiene, and prompt loading rules.
- Public releases are generated from a sanitized export, not directly from the private local working tree.

## Topology

```mermaid
flowchart TD
    U[Human intent] --> I[Intake and triage]
    I --> IDX[Indexes]
    IDX --> P[Plan]
    P --> R[Run]
    R --> D[Digest]
    D --> C[Claim]
    C --> G[Review gate]
    G --> DONE[Done]
    G --> MEM[Memory proposal]
    G --> EVO[Evolution proposal]

    IDX --> PROJ[Project adapters]
    IDX --> LIB[External library]
    IDX --> SK[Skill registry]
    IDX --> RES[Compute and storage resources]

    PROJ --> NATIVE[Native .researchflow adapter]
    PROJ --> LEGACY[Legacy shadow adapter]

    MEM --> PM[Project memory]
    MEM --> BM[Bridge memory]
    MEM --> UM[Universal method memory]

    EVO --> INBOX[Evolution inbox]
    EVO --> JOURNAL[Journal and resolution]

    subgraph PublicRelease[Public release boundary]
        PUB[Sanitized docs, skills, commands, scripts, templates, tests, indexes]
    end

    subgraph LocalPrivate[Local private boundary]
        PRIV[Private memory, project facts, hardware records, personal logs]
    end

    PUB -.sanitized sync.-> LocalPrivate
    LocalPrivate -.filtered export.-> PUB
```

## Documentation

- [User Manual](docs/user-manual.md): natural-language workflows, project onboarding, memory capture, skill reuse, and routine use.
- [Technical Manual](docs/technical-manual.md): architecture, data model, adapter contracts, validators, indexes, and topology.
- [Local-Public Sync Manual](docs/local-public-sync.md): standard process for keeping the local framework and sanitized public repository aligned.

## Quick Start

In a Codex or agent thread, use natural language:

```text
Connect this project to ResearchFlow. Choose the safe mode, run onboarding, validate it, and report what changed.
```

The agent selects one of two adapter modes:

- **Native mode** creates `<project-root>/.researchflow/project.rf.yaml`.
- **Legacy mode** creates `project-interfaces/legacy/<safe-project-id>/project.rf.yaml` inside ResearchFlow and leaves the target project unchanged.

The user does not need to manually run shell commands during normal onboarding. Scripts remain available as deterministic internal tools and for transparent verification.

## Repository Layout

```text
commands/          operational entry points
docs/              user, technical, and sync manuals
framework/         policy, state, context, memory, and boundary rules
skills/            Codex-compatible routing skills
prompts/           on-demand prompt contracts
scripts/           lightweight validators and project adapter tools
templates/         reusable records and adapter templates
indexes/           sanitized public indexes
tests/             regression tests for framework invariants
```

## Privacy And Release Boundaries

This public repository intentionally excludes private memory, personal knowledge bases, real project history, hardware records, and local usage logs. Public material should describe the framework, not leak a specific user's research history.

The standard boundary is:

- publish sanitized framework rules, manuals, scripts, skills, commands, templates, tests, and safe indexes;
- keep private project facts, personal preferences, hardware inventory, raw logs, and local memory in the private local ResearchFlow tree;
- use local private memory only to drive release configuration, then remove sensitive values from public files before commit.

## Validation

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
```

Run the framework validator:

```bash
python3 scripts/rf_validate.py . --strict
```

Validate a connected project adapter:

```bash
python3 scripts/rf_project_validate.py \
  --framework-root . \
  --adapter /path/to/project.rf.yaml \
  --strict
```

## Current Scope

This release is a public framework skeleton, documentation set, and validation reference. It is suitable for studying, adapting, and extending the workflow, but it does not include private memories, real project history, personal knowledge-base material, or machine-specific configuration.

---

# 中文说明

[![状态](https://img.shields.io/badge/%E7%8A%B6%E6%80%81-public%20preview-2563eb)](#researchflow)
[![文档](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-English%20%7C%20%E4%B8%AD%E6%96%87-16a34a)](#researchflow)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](#validation)
[![Agent Workflow](https://img.shields.io/badge/agent-workflow-intent--driven-7c3aed)](#agent-philosophy)
[![隐私边界](https://img.shields.io/badge/privacy-sanitized%20public%20release-0f766e)](#privacy-and-release-boundaries)
[![索引优先](https://img.shields.io/badge/context-index--first-f59e0b)](#technical-characteristics)

**语言切换：** [English](#researchflow) | [中文](#中文说明)

ResearchFlow 是一个面向 agent 辅助科研、实验和项目执行的 index-first 工作流框架。它适用于长对话、复杂文件、大量模拟结果、跨项目知识和个人科研习惯容易超过 agent 工作上下文的场景。

框架把上下文视为稀缺科研资源。Agent 应先读高密度索引，再按任务需要打开证据正文，从而降低 token 消耗、减少记忆漂移，并让推理路径可复查。

## Agent 理念

ResearchFlow 的核心判断是：人应该把注意力留给创造性的科研判断，agent 应该在第一次人机协作跑通意图之后，承担机械、重复、可验证的工作。

Agent 不应该只是僵硬执行一串点对点指令。它应围绕目的、证据、边界和可复用流程工作。自然语言是主要入口，因为清晰的意图能给 agent 留出选择合适工具的空间；而 ResearchFlow 的索引、校验器和 review gate 会约束这种灵活性，避免它变成不可控行为。

## 项目特点

功能特点：

- 使用自然语言接入新项目和旧项目。
- 原生项目 adapter 适用于可以写入 `.researchflow/` 元数据的项目。
- 旧项目影子 adapter 适用于不能修改目录结构的项目。
- 通用记忆、桥接记忆、项目记忆和外部资料库分层。
- Evolution inbox、事项、日志、决议和自检路径用于框架自升级。
- Skill 清单和使用日志记录哪些 agent skill 在什么项目场景中有效。
- 算力和存储索引用于科研任务分配规划。
- 公开/本地边界用于发布脱敏后的框架材料。

技术特点：

- JSONL 索引在读取正文前提供高密度入口。
- `index_only`、`on_demand`、`adapter_first`、`registry_only`、`skip` 等读取策略控制上下文加载。
- 小型状态机让 agent 运行可恢复：`intake -> triage -> plan -> run -> digest -> claim -> review -> done`。
- Markdown frontmatter 模板统一 claim、digest、memory proposal、procedure、evolution record 和 skill usage log。
- 轻量 Python 校验器检查索引结构、记忆 proposal 安全性、项目 adapter 边界、发布卫生和 prompt 默认读取规则。
- 公开发布来自脱敏导出目录，而不是直接从本地私有工作树发布。

## 拓扑关系

```mermaid
flowchart TD
    U[人的意图] --> I[Intake 和 triage]
    I --> IDX[索引]
    IDX --> P[计划]
    P --> R[执行]
    R --> D[Digest]
    D --> C[Claim]
    C --> G[Review gate]
    G --> DONE[完成]
    G --> MEM[记忆 proposal]
    G --> EVO[演化 proposal]

    IDX --> PROJ[项目 adapter]
    IDX --> LIB[外部资料库]
    IDX --> SK[Skill registry]
    IDX --> RES[算力和存储资源]

    PROJ --> NATIVE[原生 .researchflow adapter]
    PROJ --> LEGACY[旧项目影子 adapter]

    MEM --> PM[项目记忆]
    MEM --> BM[桥接记忆]
    MEM --> UM[通用方法记忆]

    EVO --> INBOX[Evolution inbox]
    EVO --> JOURNAL[Journal 和 resolution]

    subgraph PublicRelease[公开发布边界]
        PUB[脱敏文档、skills、commands、scripts、templates、tests、indexes]
    end

    subgraph LocalPrivate[本地私有边界]
        PRIV[私人记忆、项目事实、硬件记录、个人日志]
    end

    PUB -.脱敏同步.-> LocalPrivate
    LocalPrivate -.过滤导出.-> PUB
```

## 文档

- [使用手册](docs/user-manual.md)：自然语言工作流、项目接入、记忆捕获、skill 复用和日常使用。
- [技术手册](docs/technical-manual.md)：架构、数据模型、adapter contract、校验器、索引和拓扑。
- [本地-公开同步手册](docs/local-public-sync.md)：保持本地框架和脱敏公开仓库一致的标准流程。

## 快速开始

在 Codex 或其他 agent 线程中直接使用自然语言：

```text
把当前项目接入 ResearchFlow。你来判断安全模式、完成接入、验证并汇报变化。
```

Agent 会选择两种 adapter 模式之一：

- **原生模式**：在项目内创建 `<project-root>/.researchflow/project.rf.yaml`。
- **旧项目兼容模式**：在 ResearchFlow 内创建 `project-interfaces/legacy/<safe-project-id>/project.rf.yaml`，不修改目标项目目录。

用户正常使用时不需要手动运行命令。脚本仍作为 agent 内部的确定性执行工具，也可用于透明验证。

## 仓库结构

```text
commands/          操作入口
docs/              使用手册、技术手册和同步手册
framework/         策略、状态、上下文、记忆和边界规则
skills/            Codex 兼容的路由 skill
prompts/           按需读取的 prompt contract
scripts/           轻量校验器和项目 adapter 工具
templates/         标准记录模板
indexes/           脱敏后的公开索引
tests/             框架不变量回归测试
```

## 隐私与发布边界

此公开仓库刻意排除了私人记忆、个人知识库、真实项目历史、硬件记录和本地使用日志。公开材料只描述框架，不泄露某个具体用户的研究历史。

标准边界是：

- 可以发布脱敏后的框架规则、手册、脚本、skills、commands、templates、tests 和安全索引；
- 私人项目事实、个人偏好、硬件清单、原始日志和本地记忆保留在本地私有 ResearchFlow 树；
- 本地私有记忆只用于驱动发布配置，提交公开仓库前必须移除敏感值。

## 校验

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

运行框架校验：

```bash
python3 scripts/rf_validate.py . --strict
```

校验某个项目 adapter：

```bash
python3 scripts/rf_project_validate.py \
  --framework-root . \
  --adapter /path/to/project.rf.yaml \
  --strict
```

## 当前范围

这个版本是公开的框架骨架、文档集和校验参考，适合学习、改造和扩展工作流；它不包含私人记忆、真实项目历史、个人知识库内容或本机配置。
