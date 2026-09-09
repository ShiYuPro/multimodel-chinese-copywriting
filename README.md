# Multimodel Chinese Copywriting

Draft Chinese copy with Kimi, Doubao or DeepSeek, then verify facts before shipping. A skill for Codex and Claude Code with explicit API configuration and offline dry runs.

## Install

From your project directory, choose the command for your agent. Existing destinations
are not overwritten by `git clone`.

**Codex:**

```sh
git clone https://github.com/ShiYuPro/multimodel-chinese-copywriting.git .agents/skills/multimodel-chinese-copywriting
```

**Claude Code:**

```sh
git clone https://github.com/ShiYuPro/multimodel-chinese-copywriting.git .claude/skills/multimodel-chinese-copywriting
```

Invoke `$multimodel-chinese-copywriting` in a new task. Discovery depends on your host's support for
`SKILL.md`; installation does not change project policy or grant external permissions.

## First use

```sh
python3 scripts/multimodel_copywriting.py --provider kimi --prompt-file examples/copy-brief.txt --dry-run
```

Run helper commands from the installed skill directory or this repository root.
See [setup and examples](references/setup.md) and the [full skill](SKILL.md).

## Requirements

Python 3.9+, standard library only. Live drafting requires an authorized provider account and may incur API costs.

## Verify locally

```sh
python3 scripts/check.py
```

Tests use temporary fixtures and mocked responses. They do not clean your project,
call paid model APIs, or deploy a production service.

## Boundaries

Dry run sends no request and needs no credentials. Live requests require an approved brief, explicit provider configuration and authorization for costs and disclosure. Tests use mocked responses; real provider availability is not guaranteed.

## Sources and license

See [SOURCES.md](SOURCES.md) for reviewed alternatives and adaptation decisions,
and [LICENSE](LICENSE) for terms. This standalone repository was split from
[Agent Workflow Skills](https://github.com/ShiYuPro/agent-workflow-skills).
Future changes for this skill belong here.
