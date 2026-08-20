# claude-skills

Personal skills for [Claude Code](https://claude.com/claude-code), consolidated from
patterns observed across real working sessions. Each one is a self-contained
`SKILL.md` that Claude Code loads automatically when the task matches its
description — nothing to configure beyond placing the directory in your
skills folder.

## Skills

- **[execute-external-setup](execute-external-setup/)** — methodology for
  running externally-authored setup/install instructions (a tutorial, a
  forwarded "install these" list, an MCP/plugin install guide) without
  running commands blind: audit current state first, verify identifiers
  against their source, surface OAuth/TTY boundaries before starting, verify
  behaviour rather than trusting a green preflight, and attempt an action
  instead of polling an ambiguous status probe.
- **[frontend-verification-loop](frontend-verification-loop/)** — verify
  what a browser-automation or preview tool actually shows you before
  trusting its report: recover a page/tab it can't see, prove a render
  surface renders anything before debugging app code, and instrument a UI
  pipeline stage-by-stage instead of guessing at the last one.
- **[shell-command-verification](shell-command-verification/)** — running a
  shell command isn't the same as knowing what it did: don't let a
  readability filter (`| tail`, `| Select-Object -Last N`) hide progress or
  the real exit code, match your progress probe to how the tool actually
  writes, and verify the postcondition rather than the report.
- **[extracting-documents-from-web-uis](extracting-documents-from-web-uis/)**
  — pull a source document out of a web UI (Notion, a wiki, a docs site)
  without losing content to invisible truncation, via an
  expand-then-inventory-then-window pass, and match how you relay a
  sourced command to where it will actually execute.

## Install

Copy (or clone and symlink) the skill directory you want into your Claude
Code skills folder:

```
cp -r execute-external-setup "$HOME/.claude/skills/"
```

Claude Code picks it up automatically on the next session — no restart or
registration step needed.

## License

MIT — see each skill's frontmatter. Use, adapt, and redistribute freely.
