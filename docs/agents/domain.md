# Domain Docs

How the engineering skills consume this repo's domain documentation.

## Layout

Single-context, with a full domain model:

- `GLOSSARY.md` at the repo root — canonical vocabulary.
- `05_Knowledge/concepts/` — atomic concept pages.
- `05_Knowledge/synthesis/` — cross-cutting conclusions.
- `docs/adr/` — decisions.
- `05_Knowledge/references/` — distilled source contracts and depth-one source synthesis.

Before exploring, read `GLOSSARY.md`, the ADRs in `docs/adr/`, and the concept pages relevant to the
area. If a file is absent, proceed silently.

## Consumer rules

- Use the glossary's vocabulary in issue titles, specs, test names and refactor proposals. Do not
  drift to synonyms the glossary avoids.
- If a needed concept is missing, note it for `/domain-modeling` rather than inventing a synonym.
- If proposed work contradicts an ADR, surface it explicitly:
  _Contradicts ADR-0002 (feedback event as agent boundary), but worth reopening because…_
- `05_Knowledge/references/neurosity-python-sdk-contract.md` is authoritative for SDK shapes and
  lifecycle; `06_Projects/insite-out/feedback-event-contract.md` is authoritative for the
  agent-facing shape. Do not conflate the two boundaries.
