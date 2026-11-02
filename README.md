# Agents template

A starting point for coding-agent instructions in Unreal Engine C++ projects, for Claude Code. Its rules live in
`AGENTS.md`, the cross-tool file, so other agents can be added later without restructuring.

Every repository gets the same setup, whether it stands alone, sits inside a parent repository, or
contains work repositories of its own. Any repository can be all three at once, so there is one template,
and the sections a parent needs are in the agent-docs skill, added when you ask.

Everything has a working default. A new project replaces four tokens, `{{PROJECT_NAME}}` (and its ALL_CAPS `{{PROJECT_NAME_CAPS}}`), `{{MODULE_NAME}}` and
`{{PROJECT_GOAL}}`, sets nothing per machine, and starts working; the rest fills in as the work needs it.

## Layout

```text
AgentsTemplate/
├── README.md          this file (not copied)
└── template/          copied into a repository's root
    ├── AGENTS.md                    keywords and the rules every turn needs; imports the project index and 2.INSTRUCTIONS
    ├── CLAUDE.md                    "@AGENTS.md", so Claude Code reads it
    ├── Tools/
    │   ├── python.cmd               runs a script with the engine's Python, by a fixed path Claude Code can approve
    │   └── ue.py                    the engine commands: build, clang-db, test, editor-python, engine
    ├── .claude/
    │   ├── settings.json            clangd-lsp and rider-skills plugins, never-cd rules; hides docs/_HUMANS.md
    │   ├── agents/SUBAGENTS.md      this repository's agent, for parent sessions that add it
    │   └── skills/agent-docs/       how to change, start and check the agent docs:
    │       ├── SKILL.md                 the shared editing rules; starting a feature
    │       ├── references/              each doc's rules and formats, the check, work-repository sections
    │       └── assets/                  docs created when first needed: feature/ (1.{{FEATURE_NAME_CAPS}}.md, 2…6,
    │                                    rule.md) and root/ (6.TODOS.md)
    └── docs/
        ├── 1.{{PROJECT_NAME_CAPS}}.md the project index; purpose, milestones, prerequisites, variables, SESSION_FILES, layout
        ├── 2.INSTRUCTIONS.md        one table: what you want to do, how, done when; Unreal commands filled in
        ├── 3.CONVENTIONS.md         Epic's coding standard, vocabulary, architecture, contracts
        ├── 4.TEST.md                Automation Spec, where tests live, naming
        ├── 5.DECISIONS.md           why things are the way they are, edited in place
        └── _HUMANS.md               for people only: how it all works, permissions, routines, your notes
```

How the files work together, where to start an agent, and the day-to-day routines are in
[template/docs/_HUMANS.md](template/docs/_HUMANS.md). That file is copied into every repository.

## Start a project

Open Claude Code in the new repository and give it this:

> Copy everything in `template/` of https://github.com/SoraTehk/AgentsTemplate into this repository's root,
> keeping any file that already exists, with `.claude/skills/agent-docs/` copied as it is. In every other copied
> file, and in the name `docs/1.{{PROJECT_NAME_CAPS}}.md`, replace `{{PROJECT_NAME}}` with `<Name>` (the `.uproject`'s
> name), `{{PROJECT_NAME_CAPS}}` with that name in ALL_CAPS, words split by underscores (`LyraStarterGame` →
> `LYRA_STARTER_GAME`), `{{MODULE_NAME}}` with `<Module>` (the game module, the `Source/` folder the `.uproject`'s first module
> names), and `{{PROJECT_GOAL}}` with "<one sentence: what it builds, for whom, and what it is not>". Write
> UTF-8 without a byte-order mark: one hides `SUBAGENTS.md`'s frontmatter from Claude Code. In 2.INSTRUCTIONS, keep
> the version control and SESSION_FILES commands for the system this repository uses, git or Perforce, and delete
> the other's. Then run `Tools/python.cmd Tools/ue.py engine`; if it finds no engine, ask me for the engine's folder
> and set it as `UE_ENGINE_DIR` in `.claude/settings.local.json`.

Keep `CLAUDE.local.md`, `.claude/settings.local.json` and `compile_commands.json` out of version control.
Start a new session after setting any variable, so it applies.

That's all a new project needs. Build, tests, the C++ database, editor Python scripts and version control work from
the first prompt. Lint, running the game and the SESSION_FILES base start as *not set up yet*: the first task that
needs one makes the agent stop and propose it (the gate in AGENTS.md), and you approve each line.

**When it applies:**

- **Repositories inside this one:** ask the agent to "add the work repositories ChildA and ChildB"; the agent-docs
  skill holds the sections to add. Start Claude Code with `claude --add-dir ChildA --add-dir ChildB`, and set any
  override in this repository's `.claude/settings.local.json`.
- **Never a work repository itself:** delete `.claude/agents/SUBAGENTS.md`.
- **No automated tests yet, on purpose:** record it as a decision (how every change is still tested
  meanwhile, and when to revisit), and say so in 4.TEST.
- **Adopting into an existing project:** have the agent fill in what the project already shows:

  > This repository was just given the agent-docs template, and setting it up is the task: the rules in
  > AGENTS.md don't apply until it's done, except that every doc edit follows the agent-docs skill. Replace every
  > *not set up yet* and default in AGENTS.md and docs/ that the `.uproject`, `.Build.cs` and `.Target.cs` files,
  > configs, README or history contradict or can fill, and merge any existing CLAUDE.md or docs instead of
  > replacing them, asking before moving content.
  > If most of the code predates the conventions, propose narrowing the conventions' Scope to SESSION_FILES, with
  > the legacy files that keep their own style. Never invent commands, versions or rules; list what you couldn't
  > verify as questions for me.

## Design choices, and why

- **Working defaults, four tokens.** A template full of blanks either stays blank or gets filled with
  guesses. Defaults that suit every Unreal C++ project, plus *not set up yet* where nothing generic fits,
  keep a new project usable from the first prompt, and the gate turns each gap into a question when it matters.
- **AGENTS.md enforces and loads the index.** In Vercel's evals, a compact docs index embedded in AGENTS.md
  passed 100% of tasks; the same docs packaged as a skill passed at most 79%, because agents often didn't
  think to load it. So the rules that must always hold sit in the always-loaded file, and it imports the project
  index and 2.INSTRUCTIONS, which every session needs. Everything else is one indexed hop away.
- **The index is `1.<PROJECT>.md`, not AGENTS.md,** so a feature's index, `1.<FEATURE>.md`, is built the same
  way, and a feature can become a project of its own.
- **One index, no cross-references.** Only the project index names or links other docs; each numbered doc refers
  to content by what it is. Renaming, splitting or adding a doc touches one table, and an agent always finds its
  way from the same place.
- **One home per kind of content.** What to do and how lives in 2.INSTRUCTIONS, facts in the project index, code
  shape in 3.CONVENTIONS, tests in 4.TEST. A fact kept in two places drifts.
- **Editing rules are a skill.** Only an edit needs them, and every session used to pay for them. The
  agent-docs skill holds them, each doc's formats and fill-in hints, the feature templates and the docs check,
  and AGENTS.md sends Claude there before a doc changes. It holds no project facts, so updating the template
  replaces it whole.
- **Three rule keywords.** Every rule starts with Always, Ask first or Never, defined once in AGENTS.md, and
  sits in the doc for its kind: the three tiers other agents.md templates use. One spelling everywhere makes a
  rule easy to spot, and something to do only on request is Ask first.
- **No HTML comments.** Claude Code strips them from the files it loads at start, but not from docs it opens
  with a tool, and one holding a code fence leaks. Hints and optional sections live in the skill.
- **Docs describe the present.** A decision that changes is edited in place with a "revised" date, merged
  with any that decide the same thing, never superseded. Version control keeps the history, so agents never
  have to work out which of two entries still holds.
- **Features mirror the repository, one level down.** A feature's `1.<FEATURE>.md` is its index, a path rule
  loads it, and its other numbered docs add to the root doc with the same number, created only when there's
  something of its own to say. Agents navigate both levels the same way, and a small feature costs one file.
- **No version control in the docs; the engine is found, not set.** Nothing assumes git: SESSION_FILES names
  the current work's files and base, and the version control rows ship for both git and Perforce, the one
  not in use deleted at setup. Our scripts find the engine the way Unreal's own tools do, from the `.uproject`'s `EngineAssociation` in the
  registry, so every tool uses the same one and nothing is kept in sync; `UE_ENGINE_DIR` only overrides it.
- **Commands are fixed text.** Claude Code can't save an approval for a command whose program is a variable, so
  every engine command is a `Tools/ue.py` subcommand run through `Tools/python.cmd`. Commands prompt as usual, and a
  developer's "don't ask again" approvals match them.
- **Shared skills ship as plugins, not copies.** `rider-skills` is declared in `.claude/settings.json`, its
  marketplace and the plugin, so every developer is offered it and its updates; copying its skills in would freeze
  them. Rider's MCP server, which the skills call, is set up per machine, since Rider picks its port.
- **Index files are ALL_CAPS**, like the numbered docs: `1.LYRA_STARTER_GAME.md`, `1.BUILDING_SYSTEM.md`.
- **Code paths use the module, not the project.** Lyra's project is `LyraStarterGame`, its code `Source/LyraGame`
  and its editor target `LyraEditor`, so paths take `{{MODULE_NAME}}` and `ue.py` finds the target in `Source/`.
- **Commands say what success looks like.** Each ends with `exit <code>`, and its "Done when" says what success
  prints, so the agent checks the result instead of guessing. Scripts we write ourselves are Python, run with the
  engine's own interpreter.
- **Only the test-first test runs unasked.** A small change shouldn't cost a long run when it isn't the final
  state; other tests and lint are Ask first.
- **Short, human-curated, no restating defaults or code.** Claude Code's docs recommend under 200
  lines per instruction file, because adherence drops as files grow. An ETH Zurich study found
  LLM-generated context files lowered agents' success and raised cost by more than 20%. Hence the line
  budgets, and the Claude Code defaults kept out of agent docs and recorded in `_HUMANS.md` instead.
- **`CLAUDE.md` is a one-line import.** Claude Code reads `AGENTS.md` natively only from 2.1.277, and only
  when no `CLAUDE.md` or `CLAUDE.local.md` exists in the folder or any parent. One stray `CLAUDE.md` higher
  up, or a personal `CLAUDE.local.md`, would make it skip every `AGENTS.md`. Using `@AGENTS.md` everywhere
  works in all cases, and never loads it twice.
- **Specific, with exact commands and firm limits.** GitHub's study of more than 2,500 agents.md files
  found most fail by being vague.
- **Numbered names have no spaces** (`2.INSTRUCTIONS.md`). The number keeps reading order in file
  listings. Paths with spaces need escaping in links and `@` imports.

## Sources

- Claude Code docs: [memory and AGENTS.md](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings), [permissions](https://code.claude.com/docs/en/permissions), [monorepos and large codebases](https://code.claude.com/docs/en/large-codebases), [subagents](https://code.claude.com/docs/en/sub-agents)
- [agents.md](https://agents.md/)
- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [GitHub: How to write a great agents.md, lessons from over 2,500 repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [Epic's C++ Coding Standard for Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine)
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv 2602.11988 (2026)
