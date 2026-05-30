# Prompt: Natural Language Project Connect

Use this prompt when the user wants ResearchFlow project onboarding without writing shell commands.

## User-Facing Starters

The user can say one of these in a Codex thread:

```text
I want to connect this project to ResearchFlow. You decide the safe mode and complete the standard onboarding flow.
```

```text
把当前项目接入 ResearchFlow。这个项目可以创建 .researchflow，你来完成接入、验证和记录。
```

```text
把 /abs/path/to/old-project 兼容接入 ResearchFlow。不要修改那个项目目录，用旧项目零侵入方式完成接入、验证和记录。
```

```text
我在 ResearchFlow 项目里开了这个线程，请把 /abs/path/to/project 接入我的 ResearchFlow 工作流。能写入项目目录就用原生方式，不能确定就先问我。
```

## Agent Contract

- Do not ask the user to run shell commands.
- Infer `project_root` from the current workspace when the user says "this project" or "current project".
- Use native mode only when writing `.researchflow/` into the project is allowed or clearly intended.
- Use legacy mode when the user says old project, no directory change, read-only, mounted drive, external folder, or compatible onboarding.
- Ask at most the missing facts needed for `project_id`, title, path, or write boundary.
- Run the connect script and validation script internally.
- Write skill usage and evolution records when the interface itself changes or a gap is found.

## Required Facts

- `project_root`:
- `project_id`:
- `title`:
- `mode`: native | legacy | infer
- `write_boundary`: project-local `.researchflow/` allowed | no target directory change | unknown
- `thread_context`: target project thread | ResearchFlow coordination thread

## Result Summary

Report:

- selected mode;
- adapter path;
- validation command result;
- whether target project directory was changed;
- logs or indexes written;
- next natural-language action the user can say.
