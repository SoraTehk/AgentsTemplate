<!--
  Template for one feature's index, not a feature itself. 2.INSTRUCTIONS "Add or change a feature" copies it to
  docs/<Feature>/README.md. This README is to its feature what AGENTS.md is to the repository: the index every agent
  reads first, plus the feature's contract. Budget: ~150 lines; past that, move detail into a numbered doc or a file
  listed under Related. Features don't nest: split a big one into sibling features (5.DECISIONS D-002).
-->
# {{FEATURE_NAME}}

{{One sentence: what this feature does for the user.}}

**Status:** planned · **Code:** `src/{{FEATURE_NAME}}/` · **Tests:** `tests/{{FEATURE_NAME}}/`
<!-- List every folder the feature owns; .claude/rules/{{FEATURE_NAME}}.md `paths` must match them. -->

## Docs

Each doc here adds to the root doc with the same number, which still applies. Neither overrides the other: if they
conflict, that is two instructions conflicting (AGENTS.md rule 2). A number missing here has nothing of its own yet.

None yet: the root docs cover everything.
<!-- Replace "None yet..." with a table, one row per numbered doc in this folder, in number order:
| Doc | Holds | Read when |
| --- | --- | --- |
| [1.PROJECT](1.PROJECT.md) | Its purpose, milestones, layout | Starting work on it, or asked about its scope or status |
| [2.INSTRUCTIONS](2.INSTRUCTIONS.md) | Its own commands and playbooks | Before your first action in it |
| [3.CONVENTIONS](3.CONVENTIONS.md) | Rules that apply only to its code | Before writing or reviewing its code |
| [4.TEST](4.TEST.md) | Its own test layout and exemptions | Before writing any of its code |
| [5.DECISIONS](5.DECISIONS.md) | Why it works the way it does | Before reversing a choice in it |
| [6.TODOS](6.TODOS.md) | Its deferred work and known gaps | Before refactoring it, or when you defer something in it |
-->

## Contract

<!-- What other code, and other features, may rely on: public types, endpoints, messages, file formats. The part
     that must not drift. Another feature relies on this section only, never on the feature's internals. -->
Not defined yet.

## How it works

Not written yet. <!-- A short paragraph or a diagram of the flow. Name the entry point a reader should open first. -->

<!-- Once the feature has terms of its own, add:
## Vocabulary

| Term | In the code | Meaning |
| --- | --- | --- |
-->

## Gotchas

None recorded yet.

## Related

None yet. <!-- Specs, protocols, diagrams or sample data beside this README; other features' READMEs; external specs. -->
