# Triage labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the label
strings chosen for `reallife-spark/insite-out`: the Home standard set
`needs-triage`, `ready-for-human`, `priority: critical`.

| Label in mattpocock/skills | Label in our tracker | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | Maintainer needs to evaluate this issue |
| `needs-info` | `needs-triage` | No dedicated label here; treat as awaiting triage |
| `ready-for-agent` | `ready-for-human` | No AFK-ready label here; a human owns implementation |
| `ready-for-human` | `ready-for-human` | Requires human implementation |
| `wontfix` | — | No label; close with an explanatory comment |

`priority: critical` is an additional severity label, not a triage role. Apply it alongside a role
label when work is blocking.

When a skill names a role, use the corresponding string from this table. To change the vocabulary,
edit this file and update the labels in the GitHub repo.
