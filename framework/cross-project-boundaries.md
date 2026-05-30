# Cross-Project Boundaries

ResearchFlow can work from many project folders. The main framework stays in one root, while each project can expose either a native adapter:

```text
<project-root>/.researchflow/project.rf.yaml
```

or a legacy shadow adapter:

```text
agent-framework/researchflow/project-interfaces/legacy/<safe-project-id>/project.rf.yaml
```

The adapter is a pointer and local read policy. It does not transfer project facts into the global framework.

## Authority Order

```text
current user instruction
> current project evidence
> current project adapter
> current project memory
> global project/resource/link indexes
> other project memory as external evidence
> universal memory
> library/RSS/evolution pointers
> model prior
```

## Link Rules

- `project-link` entries are weak links: related projects, shared methods, datasets, dependencies, conflicts, or resource relationships.
- Other project memory is external evidence until current-project evidence confirms it.
- Reusable project experience must pass through `MemoryBridge` before becoming universal memory.
- Conflicting project claims should be linked with `conflicts_with`, not merged.
