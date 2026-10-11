<!--
  One folder per feature: docs/<FeatureName>/README.md is the entry point. Add more files beside it
  only when this one passes ~150 lines (specs, protocols, diagrams, sample data).
  Register the folder in AGENTS.md "Feature docs" and add .claude/rules/<FeatureName>.md.
-->
# {{FeatureName}}

{{One sentence: what this feature does for the user.}}

**Status:** {{planned | in progress | done}} · **Code:** `{{src/FeatureName/}}` · **Tests:** `{{tests/FeatureName/}}`

## Contract

<!-- What other code may rely on: public types, endpoints, messages, file formats. The part that must not drift. -->
- {{signature / endpoint / schema}}: {{meaning, units, error cases}}.

## How it works

{{A short paragraph or a diagram of the flow. Name the entry point a reader should open first.}}

## Gotchas

- {{The non-obvious thing that has bitten someone, and how to avoid it}}.

## Related

- {{Other feature docs, decisions (5.DECISIONS D-00x) or external specs}}.
