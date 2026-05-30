# Local-Public Sync Manual

**Scope:** standard process for keeping a private local ResearchFlow tree aligned with a sanitized public repository.

## 1. Boundary Labels

Use these labels when deciding what can cross the boundary:

- `PUBLIC-SYNC`: safe to keep identical in local and public repositories.
- `PUBLIC-SANITIZED`: derived from local material but stripped of private details before publication.
- `LOCAL-PRIVATE`: must remain only in the private local tree.
- `LOCAL-POINTER`: a public-safe pointer may exist, but body content remains private.

## 2. File Class Matrix

| Path class | Default label | Public handling |
| --- | --- | --- |
| `README.md` | `PUBLIC-SYNC` | keep synchronized after privacy review |
| `docs/` | `PUBLIC-SYNC` | keep synchronized after privacy review |
| `framework/` | `PUBLIC-SYNC` | publish stable rules and policies |
| `commands/` | `PUBLIC-SYNC` | publish reusable procedures |
| `skills/` | `PUBLIC-SYNC` | publish framework skills that contain no private history |
| `prompts/` | `PUBLIC-SYNC` | publish prompt contracts, not private prompt logs |
| `scripts/` | `PUBLIC-SYNC` | publish validators and deterministic helpers |
| `templates/` | `PUBLIC-SYNC` | publish reusable record formats |
| `tests/` | `PUBLIC-SYNC` | publish framework invariant tests |
| `indexes/` | `PUBLIC-SANITIZED` | publish only safe pointer or framework indexes |
| `memory/` | `LOCAL-PRIVATE` | do not publish |
| `evolution/` | `LOCAL-PRIVATE` | publish only generalized framework lessons if rewritten |
| `skills-registry/usage/` | `LOCAL-PRIVATE` | do not publish real usage logs |
| `project-interfaces/` | `LOCAL-PRIVATE` | do not publish real project adapters |
| `resources/compute/` | `LOCAL-PRIVATE` | do not publish real machine details |
| `library/sources/` | `LOCAL-POINTER` | publish empty structure or safe source cards only |

## 3. Local To Public Release Procedure

1. Record the release intent in local evolution logs.
2. Update local framework files first when the change affects private workflow behavior.
3. Copy only `PUBLIC-SYNC` files into the public export.
4. Convert `PUBLIC-SANITIZED` indexes into safe public versions.
5. Exclude `LOCAL-PRIVATE` files completely.
6. Replace absolute local paths with relative or placeholder paths.
7. Remove private emails, hardware identifiers, project names, raw conversation history, and credentials from public files.
8. Run framework validation and tests in the public export.
9. Run a privacy scan for local paths, account-specific strings, private log names, and memory paths.
10. Commit from the public export repository with the verified public commit identity.
11. Push only after validation and privacy scan pass.
12. Record the public commit, validation results, and lessons in local evolution logs and local personal GitHub memory.

## 4. Public To Local Sync Procedure

When public documentation or framework structure changes:

1. Review public changes against local private files.
2. Sync `PUBLIC-SYNC` files back to the local tree.
3. Merge `PUBLIC-SANITIZED` files carefully and preserve local private indexes.
4. Never overwrite local memory, real project adapters, hardware records, or private usage logs from the public export.
5. Run local validation after sync.
6. Record any conflict or useful lesson in local evolution logs.

## 5. Git Identity Rule

The public repository should use a verified public Git identity so repository contribution graphs can attribute commits correctly. The exact email value belongs in local private GitHub memory, not in public documentation.

If contribution attribution looks wrong, inspect the latest commit author and committer metadata, correct the local public-export Git config, amend or recommit as appropriate, and push with the least disruptive safe option.

## 6. Privacy Scan Baseline

Before public push, scan for:

- absolute home paths;
- private framework paths;
- private memory directories;
- private evolution or skill usage records;
- hardware hostnames and server names;
- email addresses not intended for public commit metadata;
- credentials, tokens, SSH aliases, or access instructions;
- raw conversation history that contains personal working style details.

The scan should be treated as a release gate, not an optional cleanup step.

## 7. Conflict Rule

If the public export and local private tree diverge:

- local private tree remains the authority for personal memory and real project operation;
- public repository remains the authority for public-facing documentation and reusable framework code;
- conflicts are resolved by classifying the file with the boundary labels above before merging.

---

# 本地-公开同步手册

**范围：** 用于保持本地私有 ResearchFlow 树和脱敏公开仓库一致的标准流程。

## 1. 边界标签

判断信息是否可以跨边界时使用这些标签：

- `PUBLIC-SYNC`：本地和公开仓库可以保持一致。
- `PUBLIC-SANITIZED`：来自本地材料，但公开前必须脱敏。
- `LOCAL-PRIVATE`：只能保留在本地私有树。
- `LOCAL-POINTER`：可以有公开安全指针，但正文仍留在本地。

## 2. 文件类别矩阵

| 路径类别 | 默认标签 | 公开处理 |
| --- | --- | --- |
| `README.md` | `PUBLIC-SYNC` | 隐私检查后同步 |
| `docs/` | `PUBLIC-SYNC` | 隐私检查后同步 |
| `framework/` | `PUBLIC-SYNC` | 发布稳定规则和策略 |
| `commands/` | `PUBLIC-SYNC` | 发布可复用流程 |
| `skills/` | `PUBLIC-SYNC` | 发布不含私人历史的框架 skills |
| `prompts/` | `PUBLIC-SYNC` | 发布 prompt contract，不发布私人 prompt 记录 |
| `scripts/` | `PUBLIC-SYNC` | 发布校验器和确定性辅助工具 |
| `templates/` | `PUBLIC-SYNC` | 发布标准记录格式 |
| `tests/` | `PUBLIC-SYNC` | 发布框架不变量测试 |
| `indexes/` | `PUBLIC-SANITIZED` | 只发布安全指针或框架索引 |
| `memory/` | `LOCAL-PRIVATE` | 不发布 |
| `evolution/` | `LOCAL-PRIVATE` | 只在重写为通用框架经验后发布 |
| `skills-registry/usage/` | `LOCAL-PRIVATE` | 不发布真实使用日志 |
| `project-interfaces/` | `LOCAL-PRIVATE` | 不发布真实项目 adapter |
| `resources/compute/` | `LOCAL-PRIVATE` | 不发布真实机器细节 |
| `library/sources/` | `LOCAL-POINTER` | 只发布空结构或安全来源卡片 |

## 3. 本地到公开发布流程

1. 在本地 evolution logs 中记录发布意图。
2. 如果变更影响私有工作流行为，先更新本地框架文件。
3. 只把 `PUBLIC-SYNC` 文件复制到公开导出目录。
4. 把 `PUBLIC-SANITIZED` 索引转换为安全公开版本。
5. 完全排除 `LOCAL-PRIVATE` 文件。
6. 把绝对本地路径替换为相对路径或占位路径。
7. 从公开文件中移除私人邮箱、硬件标识、项目名称、原始对话历史和凭证。
8. 在公开导出目录运行框架校验和测试。
9. 对本地路径、账号特定字符串、私有日志名和 memory 路径做隐私扫描。
10. 使用已验证的公开提交身份，从公开导出仓库提交。
11. 只有校验和隐私扫描通过后才推送。
12. 在本地 evolution logs 和本地个人 GitHub 记忆中记录公开 commit、校验结果和经验。

## 4. 公开到本地同步流程

当公开文档或框架结构发生变化时：

1. 对照本地私有文件审查公开变更。
2. 把 `PUBLIC-SYNC` 文件同步回本地树。
3. 谨慎合并 `PUBLIC-SANITIZED` 文件，并保留本地私有索引。
4. 不要用公开导出覆盖本地 memory、真实项目 adapter、硬件记录或私有 usage logs。
5. 同步后运行本地校验。
6. 把冲突或经验记录进本地 evolution logs。

## 5. Git 身份规则

公开仓库应使用已验证的公开 Git 身份，确保贡献图能正确归属 commit。具体邮箱值属于本地私有 GitHub 记忆，不应写入公开文档。

如果贡献归属不正确，先检查最新 commit 的 author 和 committer 元数据，修正公开导出仓库的 Git config，按需要 amend 或重新提交，再用最小破坏的安全方式推送。

## 6. 隐私扫描基线

公开推送前扫描：

- 绝对 home 路径；
- 私有框架路径；
- 私有 memory 目录；
- 私有 evolution 或 skill usage records；
- 硬件主机名和服务器名；
- 不打算作为公开 commit metadata 的邮箱地址；
- 凭证、token、SSH alias 或访问说明；
- 包含个人工作习惯细节的原始对话历史。

这个扫描是发布 gate，不是可选清理。

## 7. 冲突规则

如果公开导出和本地私有树发生分歧：

- 本地私有树对个人记忆和真实项目运行保持权威；
- 公开仓库对公开文档和可复用框架代码保持权威；
- 合并前先用上面的边界标签给文件分类，再解决冲突。
