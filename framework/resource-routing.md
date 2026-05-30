# Resource Routing

Resource routing records compute resources, storage locations, and task-route suggestions for research work across laptops, servers, disks, and mounted storage.

It is recommendation-only.

## Resource Types

- `compute-resource`: computer, workstation, server, cluster login, or remote machine.
- `storage-location`: internal disk, external disk, NAS, mounted server path, archive location, or scratch area.
- `task-route`: reusable rule that says which kinds of tasks fit which resources.

## Routing Output

When planning a task, output:

- recommended resource;
- recommended storage;
- reason;
- risks;
- paths that must be confirmed;
- whether data transfer is needed.

Do not auto-run SSH commands, submit jobs, move large files, or write to a mounted disk without explicit user confirmation.

Do not store passwords, tokens, private keys, or secret connection material.
