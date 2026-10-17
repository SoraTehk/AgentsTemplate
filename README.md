# Agents template

A starting point for coding-agent instructions, tuned for Claude Code. Its source of truth, `AGENTS.md`,
is also read by Codex, Cursor, Copilot and other agents.

Every repository gets the same setup, whether it stands alone, sits inside a parent repository, or
contains work repositories of its own (git submodules or nested clones). Any repository can be all three
at once, so there is one template, and the parts about containing other repositories are commented-out
sections you switch on.

Everything has a working default. A new project replaces two tokens, `{{PROJECT_NAME}}` and
`{{PROJECT_GOAL}}`, and starts working; the rest fills in as the work needs it.

## Layout

```text
AgentsTemplate/
├── README.md          this file (not copied)
└── template/          copy its contents into a repository's root
    ├── AGENTS.md                    enforcement (instructions, test-first) and the docs index
    ├── CLAUDE.md                    "@AGENTS.md", so Claude Code reads the same index
    ├── .claude/
    │   ├── settings.json            plugins and permissions; never-cd rules; hides docs/_HUMANS.md and _NOTES.md
    │   └── agents/SUBAGENTS.md      this repository's agent, for parent sessions that add it
    └── docs/
        ├── 1.PROJECT.md             purpose, milestones, prerequisites, layout
        ├── 2.INSTRUCTIONS.md        shell commands, the tool for each action, a playbook per task
        ├── 3.CONVENTIONS.md         scope, style, naming, architecture, patterns, contracts, git format
        ├── 4.TEST.md                test frameworks and layout, what each change ships with
        ├── 5.DECISIONS.md           why things are the way they are
        ├── 6.TODOS.md               deferred renames, restructures, debt
        ├── _FEATURE_TEMPLATE/       what each docs/<Feature>/ copies (not copied as a feature itself):
        │   ├── README.md                the feature's index and contract, as AGENTS.md is the repository's
        │   ├── rule.md                  becomes .claude/rules/<Feature>.md, loading the README, as CLAUDE.md does
        │   └── 1.PROJECT.md … 6.TODOS.md  what the feature adds to each root doc, copied only when it has some
        ├── _HUMANS.md               for people only: how it all works, routines, Claude Code features
        └── _NOTES.md                for people only: your scratchpad, hidden from agents
```

How the files work together, where to start an agent, and the day-to-day routines are in
[template/docs/_HUMANS.md](template/docs/_HUMANS.md). That file is copied into every repository.

## Start a project

1. **Copy the template** into the repository's root, without overwriting what's already there:

   ```sh
   git clone https://github.com/SoraTehk/AgentsTemplate.git
   cp -rn AgentsTemplate/template/. path/to/repo/                     # bash
   ```

   ```powershell
   robocopy AgentsTemplate\template path\to\repo /E /XC /XN /XO        # PowerShell: skips existing files
   ```

2. **Replace the two tokens**, from the repository's root:

   ```sh
   name='MyProject'; goal='One sentence: what it builds, for whom, and what it is not.'
   grep -rlF '{{PROJECT_' AGENTS.md docs .claude --include='*.md' --exclude-dir=_FEATURE_TEMPLATE \
     | xargs sed -i "s|{{PROJECT_NAME}}|$name|g; s|{{PROJECT_GOAL}}|$goal|g"
   ```

   ```powershell
   $name = 'MyProject'; $goal = 'One sentence: what it builds, for whom, and what it is not.'
   Get-ChildItem AGENTS.md, docs, .claude -Recurse -File -Filter *.md |
     Where-Object FullName -notmatch '_FEATURE_TEMPLATE' |
     ForEach-Object { [IO.File]::WriteAllText($_.FullName, [IO.File]::ReadAllText($_.FullName).Replace('{{PROJECT_NAME}}', $name).Replace('{{PROJECT_GOAL}}', $goal)) }
   ```

   The PowerShell version writes UTF-8 without a byte-order mark on purpose: `Set-Content -Encoding utf8`
   in Windows PowerShell adds one, which hides `SUBAGENTS.md`'s frontmatter and makes Claude Code skip it.
   In the bash version, avoid `|` and `&` in the goal, or escape them.

3. **Ignore personal files** in `.gitignore`:

   ```gitignore
   CLAUDE.local.md
   .claude/settings.local.json
   ```

That's all a new project needs. Commands and the test framework start as *not set up yet*: the first task
that needs one makes the agent stop and propose it (the gate in AGENTS.md), and you approve each line.

**When it applies:**

- **Repositories inside this one:** uncomment "Work repositories" in AGENTS.md and 1.PROJECT and list
  each one. Start Claude Code with `claude --add-dir ChildA --add-dir ChildB`.
- **Never a work repository itself:** delete `.claude/agents/SUBAGENTS.md`.
- **Code in a language with an official LSP plugin:** enable it in `.claude/settings.json` (such as
  `"clangd-lsp@claude-plugins-official": true`), and list its language server in 1.PROJECT Prerequisites.
- **Commands in PowerShell, not Bash:** swap in the PowerShell blocks from `_HUMANS.md` "Commands in
  PowerShell".
- **No tests yet, on purpose:** log it in 5.DECISIONS with a "Revisit when", and add the exemption shown at
  the bottom of 4.TEST, naming the commands that check a change by hand.
- **Adopting into an existing project:** have the agent fill in what the code already shows:

  > This repository was just given the agent-docs template, and setting it up is the task: the "Always"
  > rules in AGENTS.md don't apply until it's done. Replace every *not set up yet* and default in AGENTS.md
  > and docs/ that the build files, CI, configs, README or git log contradict or can fill, and merge any
  > existing CLAUDE.md or docs instead of replacing them, asking before moving content. If most of the code
  > predates the conventions you write, propose narrowing 3.CONVENTIONS Scope to the branch files, with the
  > legacy files that keep their own style. Never invent commands, versions or rules; list what you couldn't
  > verify as questions for me.

## Design choices, and why

- **Working defaults, two tokens.** A template full of blanks either stays blank or gets filled with
  guesses. Defaults that suit most projects, plus *not set up yet* where nothing generic fits, keep a new
  project usable from the first prompt, and the gate turns each gap into a question when it matters.
- **AGENTS.md enforces, docs instruct.** In Vercel's evals, a compact docs index kept in AGENTS.md
  passed 100% of tasks. The same docs packaged as a skill passed at most 79%, because agents often
  didn't think to load it. So the rules that must always hold (follow 2.INSTRUCTIONS, ask when it has
  no answer, test first) sit in the always-loaded file. Everything else is one indexed hop away.
- **One home per kind of content.** Commands and procedures live in 2.INSTRUCTIONS, facts in 1.PROJECT,
  code shape in 3.CONVENTIONS, tests in 4.TEST. A fact kept in two places drifts.
- **Features mirror the repository, one level down.** A feature's README is its index, a path rule loads it,
  and its numbered docs add to the root doc with the same number, created only when there's something of its
  own to say. Agents navigate both levels the same way, and a small feature costs one README.
- **Commands run as pasted and say what success looks like.** An agent's shell keeps nothing between calls,
  so each block stands alone, with `# edit` marking the only lines to change. A stated "Passes when" lets
  the agent check the result instead of guessing.
- **Short, human-curated, no restating defaults or code.** Claude Code's docs recommend under 200
  lines per instruction file, because adherence drops as files grow. An ETH Zurich study found
  LLM-generated context files lowered agents' success and raised cost by more than 20%. Hence the line
  budgets, and the Claude Code defaults kept out of agent docs and recorded in `_HUMANS.md` instead.
- **`CLAUDE.md` is a one-line import.** Claude Code reads `AGENTS.md` natively only when no `CLAUDE.md`
  exists in the folder or any parent, and not at all on older versions or some providers. One stray
  `CLAUDE.md` higher up would make it skip every `AGENTS.md` below it. Using `@AGENTS.md` everywhere
  works in all cases.
- **Specific, with exact commands and firm limits.** GitHub's study of more than 2,500 agents.md files
  found most fail by being vague.
- **Numbered names have no spaces** (`2.INSTRUCTIONS.md`). The number keeps reading order in file
  listings. Paths with spaces need escaping in links and `@` imports.

## Sources

- Claude Code docs: [memory and AGENTS.md](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings), [permissions](https://code.claude.com/docs/en/permissions), [monorepos and large codebases](https://code.claude.com/docs/en/large-codebases), [subagents](https://code.claude.com/docs/en/sub-agents)
- [agents.md](https://agents.md/) and [Codex: AGENTS.md discovery](https://developers.openai.com/codex/guides/agents-md)
- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [GitHub: How to write a great agents.md, lessons from over 2,500 repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv 2602.11988 (2026)
