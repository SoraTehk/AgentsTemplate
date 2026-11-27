# Agents template

A starting point for Claude Code and Codex in Windows Unreal Engine C++ projects. Both follow `AGENTS.md` and the same project docs. Shared skills live under `.agents/skills/`. The repository root guides template maintainers; `template/` contains the files installed in a project.

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
    ├── AGENTS.md                    shared session rules and paths to the two required docs
    ├── CLAUDE.md                    Claude imports for AGENTS.md and both startup docs
    ├── Tools/
    │   ├── Link-AgentSkills.ps1     links a shared skill into this checkout's Claude skills folder
    │   ├── python.cmd               runs a script with the engine's Python, by a fixed path Claude Code can approve
    │   └── ue.py                    the engine commands: build, clang-db, test, editor-python, engine
    ├── .agents/skills/agent-docs/
    │   ├── SKILL.md                 shared editing rules and feature setup
    │   ├── references/              doc formats, audit and work-repository sections
    │   └── assets/                  templates used when creating feature docs, rules and TODOs
    ├── .claude/
    │   ├── settings.json            clangd-lsp and rider-skills plugins, never-cd rules; hides docs/_HUMANS.md
    │   ├── agents/SUBAGENTS.md      this repository's agent, for parent sessions that add it
    │   └── skills/.gitignore        excludes the checkout-local agent-docs junction
    └── docs/
        ├── 1_{{PROJECT_NAME_CAPS}}.md the project index; purpose, milestones, prerequisites, variables, SESSION_FILES, layout
        ├── 2_INSTRUCTIONS.md        one table: what you want to do, how, done when; Unreal commands filled in
        ├── 3_CONVENTIONS.md         Epic's coding standard, vocabulary, architecture, contracts
        ├── 4_TEST.md                Automation Spec, where tests live, naming
        ├── 5_DECISIONS.md           why things are the way they are, edited in place
        └── _HUMANS.md               for people only: how it all works, permissions, routines, your notes
```

How the files work together, where to start an agent, and the day-to-day routines are in
[template/docs/_HUMANS.md](template/docs/_HUMANS.md). That file is copied into every repository.

For template maintenance, open this repository's root. The maintainer instructions use
[`fixture`](.agents/skills/fixture/SKILL.md) for fixture checks. The placeholder heading in
`template/AGENTS.md` distinguishes the template source from an installed project's instructions.

## Shared skill paths on Windows

The directory containing the installed AGENTS.md anchors startup reads. Codex discovers skills under `.agents/skills/`. Both agents can read them there directly. To expose a shared skill in Claude's skill menu, run the applicable command once per checkout.

- Installed project: `.\Tools\Link-AgentSkills.ps1 agent-docs`
- Template maintainer, from this repository root: `.\template\Tools\Link-AgentSkills.ps1 fixture -ProjectRoot .`

The helper links the selected directory, including its assets. Run it at the destination after copying the template. A Windows junction contains an absolute target. After moving a checkout, inspect the old junction, remove only the junction itself, and rerun the helper. Git ignore entries ship for both names. For Perforce, exclude the generated junction in your workspace ignore rules.

## Start a project

Open Claude Code or Codex in the new repository and give it this:

> Copy everything in `template/` of https://github.com/SoraTehk/AgentsTemplate into this repository's root,
> including hidden folders and keeping any file that already exists. Copy `.agents/skills/agent-docs/` unchanged,
> preserving all placeholders in that skill and its assets for future use. In every other newly copied
> file, and in the name `docs/1_{{PROJECT_NAME_CAPS}}.md`, replace `{{PROJECT_NAME}}` with `<Name>` (the `.uproject`'s
> name), `{{PROJECT_NAME_CAPS}}` with that name in ALL_CAPS, words split by underscores (`LyraStarterGame` →
> `LYRA_STARTER_GAME`), `{{MODULE_NAME}}` with `<Module>` (the game module, the `Source/` folder the `.uproject`'s first module
> names), and `{{PROJECT_GOAL}}` with "<one sentence: what it builds, for whom, and what it is not>". Write
> UTF-8 without a byte-order mark: one hides `SUBAGENTS.md`'s frontmatter from Claude Code. In 2_INSTRUCTIONS, keep
> the version control and SESSION_FILES commands for the system this repository uses, git or Perforce, and delete
> the other's. For a fresh Claude installation on Windows, enable the shared skill using the command under
> “Shared skill paths on Windows”. Then run `Tools/python.cmd Tools/ue.py engine`; if it finds no engine, ask me for the engine's folder
> and set it as `UE_ENGINE_DIR` in the agent process environment.

Keep `CLAUDE.local.md`, `.claude/settings.local.json` and `compile_commands.json` out of version control.
Start a new session after setting any variable, so it applies.

That's all a new project needs. Build, tests, the C++ database, editor Python scripts and version control work from
the first prompt. Lint, running the game and the SESSION_FILES base start as *not set up yet*: the first task that
needs one makes the agent stop and propose it (the gate in AGENTS.md), and you approve each line.

**When it applies:**

- **Repositories inside this one:** ask the agent to "add the work repositories ChildA and ChildB"; the agent-docs
  skill holds the sections to add. Start a session in the child for work there, or follow the child repository's
  entry point from an authorized parent session. Claude Code can attach children with `claude --add-dir ChildA --add-dir ChildB`.
- **Never a work repository itself:** delete `.claude/agents/SUBAGENTS.md`.
- **No automated tests yet, on purpose:** record it as a decision (how every change is still tested
  meanwhile, and when to revisit), and say so in 4_TEST.
- **Adopting into an existing project:** have the agent fill in what the project already shows:

  > This repository was just given the agent-docs template, and setting it up is the task: the rules in
  > AGENTS.md don't apply until it's done, except that every doc edit follows the agent-docs skill. Replace every
  > *not set up yet* and default in AGENTS.md and docs/ that the `.uproject`, `.Build.cs` and `.Target.cs` files,
  > configs, README or history contradict or can fill, and merge any existing CLAUDE.md or docs instead of
  > replacing them, asking before moving content.
  > If most of the code predates the conventions, propose narrowing the conventions' Scope to SESSION_FILES, with
  > the legacy files that keep their own style. Never invent commands, versions or rules; list what you couldn't
  > verify as questions for me.

## Upgrade an existing installation

1. Compare your installed `.claude/skills/agent-docs/` with the new shared skill under `.agents/skills/agent-docs/`.
   Merge local skill edits into the shared copy before retiring the old tracked Claude directory. Record its removal in version control before creating a local junction there.
2. Merge the new startup paths and workflow rows into your existing project docs. Preserve project facts, test filters,
   commands and decisions. For each feature, copy its code and test path globs into the project index so Codex can
   find the same docs as a Claude path rule. Update the Claude imports to use your project's actual index filename.
3. Open a fresh session **at the project's root**. Ask it to name the required startup docs and the doc-editing skill,
   then give the command for one of your named tests without running it. Check the answer against the project files.

## Design choices, and why

- **Working defaults, four tokens.** A template full of blanks either stays blank or gets filled with
  guesses. Defaults that suit every Unreal C++ project, plus *not set up yet* where nothing generic fits,
  keep a new project usable from the first prompt, and the gate turns each gap into a question when it matters.
- **AGENTS.md enforces and loads the index.** In Vercel's evals, a compact docs index embedded in AGENTS.md
  passed 100% of tasks; the same docs packaged as a skill passed at most 79%, because agents often didn't
  think to load it. The shared entry point tells Codex to read the project index and 2_INSTRUCTIONS.
  Claude imports those files in its adapter. Everything else is one indexed hop away.
- **The index is `1_<PROJECT>.md`, not AGENTS.md,** so a feature's index, `1_<FEATURE>.md`, is built the same
  way, and a feature can become a project of its own.
- **One index, no cross-references.** Only the project index names or links other docs; each numbered doc refers
  to content by what it is. Renaming, splitting or adding a doc touches one table, and an agent always finds its
  way from the same place.
- **One home per kind of content.** What to do and how lives in 2_INSTRUCTIONS, facts in the project index, code
  shape in 3_CONVENTIONS, tests in 4_TEST. A fact kept in two places drifts.
- **Editing rules are a skill.** Only an edit needs them, and every session used to pay for them. The
  agent-docs skill holds them, each doc's formats and fill-in hints, the feature templates and the docs check,
  and AGENTS.md sends every agent there before a doc changes. It holds no project facts, so updating the template
  replaces it whole.
- **Three rule keywords.** Every rule starts with Always, Ask first or Never, defined once in AGENTS.md, and
  sits in the doc for its kind: the three tiers other agents.md templates use. One spelling everywhere makes a
  rule easy to spot, and something to do only on request is Ask first.
- **No HTML comments.** Claude Code strips them from the files it loads at start, but not from docs it opens
  with a tool, and one holding a code fence leaks. Hints and optional sections live in the skill.
- **Docs describe the present.** A decision that changes is edited in place with a "revised" date, merged
  with any that decide the same thing, never superseded. Version control keeps the history, so agents never
  have to work out which of two entries still holds.
- **Features mirror the repository, one level down.** A feature's `1_<FEATURE>.md` is its index. The project index
  maps code and test paths to features; Claude path rules can also point there. Feature docs add to the root doc with the same number, created only when there's
  something of its own to say. Agents navigate both levels the same way, and a small feature costs one file.
- **No version control in the docs; the engine is found, not set.** Nothing assumes git: SESSION_FILES names
  the current work's files and base, and the version control rows ship for both git and Perforce, the one
  not in use deleted at setup. Our scripts find the engine the way Unreal's own tools do, from the `.uproject`'s `EngineAssociation` in the
  registry, so every tool uses the same one and nothing is kept in sync; `UE_ENGINE_DIR` only overrides it.
- **Commands are fixed text.** Claude Code can't save an approval for a command whose program is a variable, so
  every engine command is a `Tools/ue.py` subcommand run through `Tools/python.cmd`. Commands prompt as usual, and a
  developer's "don't ask again" approvals match them.
- **Rider is optional.** Claude's settings declare the `rider-skills` plugin. The shared workflow uses the IDE or
  language server available in the session and falls back to searching and checking source.
- **Index files are ALL_CAPS**, like the numbered docs: `1_LYRA_STARTER_GAME.md`, `1_BUILDING_SYSTEM.md`.
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
- **Claude imports live in CLAUDE.md.** Keeping the imports in the Claude adapter lets agents that read plain
  Markdown follow the paths in AGENTS.md without interpreting Claude syntax.
- **Specific, with exact commands and firm limits.** GitHub's study of more than 2,500 agents.md files
  found most fail by being vague.
- **Document prefixes** use a number and an underscore, as in `1_PROJECT.md`. Subdocuments append an uppercase
  letter to the parent number, as in `1A_OVERVIEW.md` and `1B_TERMS.md`.

## Sources

- Codex docs: [project instructions](https://developers.openai.com/codex/guides/agents-md/), [repository skills](https://developers.openai.com/codex/skills/)
- Claude Code docs: [memory and AGENTS.md](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings), [permissions](https://code.claude.com/docs/en/permissions), [monorepos and large codebases](https://code.claude.com/docs/en/large-codebases), [subagents](https://code.claude.com/docs/en/sub-agents)
- [agents.md](https://agents.md/)
- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [GitHub: How to write a great agents.md, lessons from over 2,500 repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- [Epic's C++ Coding Standard for Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine)
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv 2602.11988 (2026)
