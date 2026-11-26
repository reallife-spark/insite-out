# Issue tracker: GitHub

Issues and specs for this repo live in GitHub Issues on `reallife-spark/insite-out`. Use the `gh`
CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments` with
  appropriate `--label` and `--state` filters.
- **Sub-issues and blocking**: prefer GitHub native sub-issues and issue dependencies via
  `gh issue create --parent`, `gh issue edit --add-sub-issue` and `--add-blocked-by`. Where the CLI
  version lacks them, put `Part of #<parent>` or `Blocked by: #<n>` at the top of the child body.
- **Comment and close**: post the explanation with `gh issue comment <number> --body "..."`, then
  `gh issue close <number>`.
- **Label**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`. The label
  vocabulary is in `docs/agents/triage-labels.md`.

Infer the repo from `git remote -v`; `gh` does this automatically inside the clone. File issues
only into `reallife-spark/insite-out`, never into the vendored `mattpocock/skills` upstream.

## Pull requests as a triage surface

**PRs as a request surface: no.** External PRs are not part of the triage queue; flip this flag in
the file later if that changes.

## Wayfinding operations

A wayfinder map is a single issue labelled `wayfinder:map` with child tickets labelled
`wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling` or `wayfinder:task`. Claim a
ticket by assigning it to the driving dev; resolve it with a comment, then close it.
