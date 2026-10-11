# Agents template

A starting point for coding-agent instructions, tuned for Claude Code. Its source of truth, `AGENTS.md`,
is also read by Codex, Cursor, Copilot and other agents.

Every repository gets the same setup, whether it stands alone, sits inside a parent repository, or
contains work repositories of its own (git submodules or nested clones). Any repository can be all three
at once, so there is one template, and the parts about containing other repositories are optional
sections.

## Layout

```text
AGENTS_TEMPLATE/
├── README.md          this file (not copied)
└── template/          copy its contents into a repository's root
    ├── AGENTS.md                    enforcement (instructions, test-first) and the docs index
    ├── CLAUDE.md                    "@AGENTS.md", so Claude Code reads the same index
    ├── .claude/
    │   ├── settings.json            plugins and permissions; hides docs/_HUMANS.md from Claude
    │   ├── agents/SUBAGENTS.md      this repository's agent, for parent sessions that add it
    │   └── rules/FeatureName.md     loads a feature's doc when Claude touches that feature's code
    └── docs/
        ├── 1.PROJECT.md             purpose, milestones, prerequisites, layout
        ├── 2.INSTRUCTIONS.md        shell commands, the tool for each action, a playbook per task
        ├── 3.CONVENTIONS.md         style, naming, architecture, patterns, contracts, git format
        ├── 4.TEST.md                test frameworks and layout, what each change ships with
        ├── 5.DECISIONS.md           why things are the way they are
        ├── 6.TODOS.md               deferred renames, restructures, debt
        ├── FeatureName/README.md    one folder per feature, e.g. docs/HttpServer/, docs/Ocr/
        └── _HUMANS.md               for people only: how it all works, routines, Claude Code features
```

How the files work together, where to start an agent, and the day-to-day routines are in
[template/docs/_HUMANS.md](template/docs/_HUMANS.md). That file is copied into every repository.

## Apply it

1. **Copy without overwriting** what the repository already has:

   ```sh
   cp -rn AGENTS_TEMPLATE/template/. path/to/repo/                  # bash
   ```

   ```powershell
   robocopy AGENTS_TEMPLATE\template path\to\repo /E /XC /XN /XO     # PowerShell: skips existing files
   ```

2. **Have the agent fill it in.** Until 2.INSTRUCTIONS is filled in, the gate in AGENTS.md will stop the
   agent, so say that this task is the exception. Start Claude Code in the repository and give it this prompt:

   > This repository was just given the agent-docs template, and filling it in is the task: the
   > "Always" rules in AGENTS.md don't apply until it's done. Fill in the `{{...}}` placeholders in
   > AGENTS.md and docs/ from the build files, CI, configs, README and git log. Merge with any existing
   > CLAUDE.md or docs instead of replacing them, and ask before moving content. Delete optional sections
   > that don't apply. For each language the code uses, enable its official LSP plugin in
   > `.claude/settings.json` (such as `clangd-lsp`, `csharp-lsp`, `pyright-lsp`, `typescript-lsp`, all
   > `@claude-plugins-official`) and list its language server in 1.PROJECT Prerequisites. Never invent commands, versions or rules: leave
   > `{{TODO: question}}` for anything you can't verify, then list those questions for me. Rename or delete
   > the FeatureName examples. Fill in `.claude/agents/SUBAGENTS.md`, keeping its
   > frontmatter valid YAML. If this repository contains work repositories, list each one, with its agent's name, in
   > AGENTS.md "Work repositories".

3. **Review 2.INSTRUCTIONS and 4.TEST line by line.** Together they decide what the agent may do and
   when it must write tests first.
4. **Ignore personal files** in `.gitignore`:

   ```gitignore
   CLAUDE.local.md
   .claude/settings.local.json
   ```

## Design choices, and why

- **AGENTS.md enforces, docs instruct.** In Vercel's evals, a compact docs index kept in AGENTS.md
  passed 100% of tasks. The same docs packaged as a skill passed at most 79%, because agents often
  didn't think to load it. So the rules that must always hold (follow 2.INSTRUCTIONS, ask when it has
  no answer, test first) sit in the always-loaded file. Everything else is one indexed hop away.
- **One home per kind of content.** Commands and procedures live in 2.INSTRUCTIONS, facts in 1.PROJECT,
  code shape in 3.CONVENTIONS, tests in 4.TEST. A fact kept in two places drifts.
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

- Claude Code docs: [memory and AGENTS.md](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings), [permissions](https://code.claude.com/docs/en/permissions), [monorepos and large codebases](https://code.claude.com/docs/en/large-codebases)
- [agents.md](https://agents.md/) and [Codex: AGENTS.md discovery](https://developers.openai.com/codex/guides/agents-md)
- [Vercel: AGENTS.md outperforms skills in our agent evals](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [GitHub: How to write a great agents.md, lessons from over 2,500 repositories](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
- Gloaguen et al., *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*, arXiv 2602.11988 (2026)
