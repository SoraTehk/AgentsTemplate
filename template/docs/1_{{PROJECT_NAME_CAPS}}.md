# 1_{{PROJECT_NAME}}

## What and why

{{PROJECT_GOAL}}

**Not in scope:** nothing ruled out yet.

## Docs

AGENTS.md directs each session here and to the instructions. Read the other docs your task needs by "Read when".

| Doc | Holds | Read when |
| --- | --- | --- |
| [2_INSTRUCTIONS](2_INSTRUCTIONS.md) | What to do for each task or action, and how: commands, tools, procedures | Every session |
| [3_CONVENTIONS](3_CONVENTIONS.md) | What code looks like: coding standard, vocabulary, architecture, contracts | Before writing or reviewing code |
| [4_TEST](4_TEST.md) | How tests are written: framework, where they live, naming | Before changing behaviour |
| [5_DECISIONS](5_DECISIONS.md) | Why things are the way they are | Before reversing a choice or changing architecture |

### Features

A feature's docs live in `docs/<Feature>/`, and its index, `1_<FEATURE>.md`, is built like this file. Its other
numbered docs add to the root doc with the same number. **Never** pick one side of a conflict between the two: it is
two instructions conflicting, so the gate applies.

| Feature | Index | Code | Tests |
| --- | --- | --- | --- |

## Milestones

| # | Milestone | Outcome that proves it | Status |
| --- | --- | --- | --- |
| 1 | Project set up | A fresh copy builds using only the instructions | in progress |

**Now:** milestone 1.

## Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| Unreal Engine | *not set up yet*: the one the `.uproject`'s `EngineAssociation` names, registered on the machine (a launcher install, or a source build registered with UnrealVersionSelector) | Builds, runs and tests the project, and its Python runs our scripts |
| MSVC toolset and Windows SDK | *not set up yet*: the ones that engine version asks for | Unreal Build Tool compiles with them; a wrong toolset fails the Build in its first seconds |
| JetBrains Rider (optional) | A version with an MCP server, connected to your agent with the solution open | Symbol lookup, diagnostics and refactoring |
| clangd (optional) | A version supported by your agent's language-server integration | C++ symbol lookup using the project's compilation database |

## Variables

None is needed: our scripts find the engine the way Unreal's own tools do, from the `.uproject`'s `EngineAssociation`
in the registry. Set an override in the environment that launches your agent. If the scripts cannot find an
engine, ask the user to register it or set `UE_ENGINE_DIR`.

| Variable | Holds | Example |
| --- | --- | --- |
| `UE_ENGINE_DIR` | Optional: the engine's root folder, the one holding `Engine\`, when the registry doesn't name it | `C:\Program Files\Epic Games\UE_5.8` |
| `UE_PROJECT_FILE` | Optional: the `.uproject` to use when neither this repository's root nor one folder below it holds exactly one | `C:\Projects\{{PROJECT_NAME}}\{{PROJECT_NAME}}.uproject` |
| `UE_EDITOR_TARGET` | Optional: the editor target to build when `Source/` has neither `<Project>Editor.Target.cs` nor exactly one `*Editor.Target.cs` | `{{PROJECT_NAME}}Editor` |

## SESSION_FILES

The files the current piece of work has changed or added since its base, saved or not. The conventions apply to
them first, and lint runs on them. How to list them is in the instructions.

**Base:** *not set up yet*.

## Layout

```text
Source/{{MODULE_NAME}}/    the game module
Plugins/                   project plugins, each with its own Source/
Config/                    Default*.ini
Content/                   assets, changed only through the editor
Tools/                     our own scripts, in Python, run through Tools/python.cmd
docs/                      agent docs; start at AGENTS.md
.agents/skills/            shared agent skills
.claude/                   Claude Code settings and adapters
```
