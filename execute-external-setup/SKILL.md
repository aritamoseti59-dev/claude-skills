---
name: execute-external-setup
description: Methodology for executing externally-authored setup, install, or connection instructions — a written tutorial, a forwarded DM or doc listing "install these" links, an MCP server / plugin / skill install guide, a course's setup steps — instead of running them top to bottom on trust. Covers auditing what's already installed before running anything, verifying every named identifier (repo handles, package names, endpoints, exact commands) against its authoritative source before executing, diagnosing a capability that ships through multiple delivery channels so a partial success doesn't read as total failure, surfacing OAuth- and TTY-gated steps as part of the plan before starting rather than after the work looks done, and attempting the real action instead of polling an ambiguous status probe when a step seems stuck. Use this whenever asked to install a tool, connect an MCP server, follow a tutorial's setup steps, work through a forwarded list of install links, set up a plugin or marketplace, or complete any multi-step external instructions — even if the request never uses the word "install."
license: MIT
---

# Execute External Setup

A setup document written by someone else is a claim about the world at the time
they wrote it, not a live description of it. A list of "install these" items
describes desired end states, not a sequence of commands to run blind. Both
assumptions break in specific, recurring ways — this skill is the checklist for
catching them before they cost a round trip.

## Step 1: Audit before you run anything

Enumerate current state before touching the list: package manifests, lock
files, config files, the agent's own loaded-capability listing (skills
directory, registered plugin marketplaces, connected MCP servers). Classify
every item as already-present / installable / not-actually-installable — and
separately classify it by *what it is* (an MCP server, a skill, a plugin, a
plain reference document to copy), because each has a different definition of
"done."

Real case: a forwarded six-item list had item 1 already fully installed — a
lock file from a prior session proved it — and item 6 wasn't an installable
artefact at all, just a reference library meant to be copied into each
project. Running the list top to bottom would have produced a redundant
reinstall and a meaningless "installed" claim for the item that was never
going to be installed.

## Step 2: Resolve every identifier before running a single step

Extract every named identifier from the source — repo handles, package names,
endpoints, exact command syntax — and verify each against its authoritative
source in one batch, before executing anything. Where the document itself
hedges on an identifier ("double check his handle on his site first"), treat
that as a hard verification gate, not a footnote to skip.

Real case: three of five install commands in a tutorial were wrong — two
referenced repositories that didn't exist under the names given, and one
connector command omitted a required transport and URL. Each wrong identifier
cost a failed run plus a recovery search, and those failures interleaved with
genuine, unrelated network errors on the same machine — which made it briefly
unclear whether a given failure was a bad identifier or a real outage.

When you find and fix a wrong identifier, report the correction back to the
user as a diff against their source document. It's usually their saved
reference, and it stays wrong for the next reader otherwise.

## Step 3: Surface capability boundaries before you start, not after

Some steps in a setup flow are ones you cannot complete alone. Find these
while planning, not at the point the work already looks finished — a
capability gap disclosed up front reads as an accurate division of labour; the
same gap disclosed after everything else is done reads as a failure.

**OAuth-gated remote servers and plugin installs.** Inspect the manifest for
remote or OAuth-gated components before running the install, and state the
interactive-only step as part of the plan from the start. Verify actual auth
status with the tool's own status command rather than inferring it from an
install-success message — a plugin's reported component inventory frequently
doesn't count servers declared inline in its manifest, so "install succeeded"
and "server is authenticated" are different claims.

**TTY-required CLI steps** (an OAuth login command that needs a real
terminal). Don't fall back to asking the user to relay tokens or callback
URLs through chat — a consumed or expired authorize URL can't be reused, and
it also hands you something you shouldn't be handling. Instead spawn a
genuine interactive terminal on the user's desktop with the command
pre-loaded, tell them exactly what the window should print and warn them not
to close it before the callback lands (closing it kills the local listener),
then verify afterwards with a status command.

Say plainly, up front: which parts you can complete, which only the user can,
and why.

Real case: a plugin install completed fully via the CLI, but its bundled MCP
server needed OAuth, which the non-interactive session couldn't run. The
blocker surfaced only after the install had already finished, so the user
reasonably expected a client restart to hand the remaining step back to the
agent — it never could. Separately, an OAuth login command failed with
"stdin isn't a terminal," including when backgrounded, since backgrounding
never creates one; its non-interactive fallback needed a redirect URL pasted
back, which is exactly the kind of value not to solicit. Spawning a real
terminal with the login command pre-loaded let the user complete it in their
own browser without the agent ever touching the credential.

## Step 4: Execute, then verify behaviour — not presence

A preflight that confirms a binary or file exists has not confirmed the tool
works on this machine. End any install with a minimum-cost end-to-end smoke
test on trivial input — a few-second file, a one-line script — rather than
trusting a green preflight and moving on.

Two things go wrong specifically because the source material ages:

- **The tool assumes a different OS or toolchain than this one.** A skill or
  installer authored and tested on one platform may only auto-install
  dependencies there, silently degrading to "print the command" everywhere
  else — which can look like success in a preflight that only checks whether
  a step ran, not what it produced.
- **CLI flags it passes go stale.** When a step that shells out to a
  fast-moving CLI breaks, read the actual invocation for a deprecated flag
  before blaming the environment, and patch at the modern equivalent rather
  than downgrading the dependency to match old documentation.

Real case: a skill's installer auto-installed its binaries only on
macOS/Homebrew; on Windows it just printed commands, so its own preflight
reported success criteria the installer could never itself satisfy there. The
same skill passed ffmpeg a flag removed several versions ago — the
*freshly-installed, current* binary was what broke it, because the preflight
had checked presence, never version compatibility.

When something reports as missing, check whether the capability actually
ships through more than one delivery channel before re-running anything. An
installer script and a separate marketplace or registration step frequently
fail independently, and the more visible channel failing silently can make a
partial success read as total failure. Enumerate every channel on disk, then
tell the user precisely which piece is actually missing and whether they need
it — an alias or command-registration channel is often optional even when the
underlying engine already works fine.

Real case: a tool shipped through two channels — an installer that wrote the
skill files, and a separate marketplace step that registered its slash
command. The installer succeeded and wrote 147 files; the marketplace step
failed silently on a network reset. The user's only visible signal was the
missing slash command, from which the reasonable inference was "nothing
installed" — but the entire engine was present and directly invocable by
name. The obvious next move, re-running the whole install, would have been
wasted effort on the part that had already worked.

## Step 5: When a step seems stuck, attempt the action instead of polling for permission to try it

A read-only status probe — has the user pressed the button yet, did the
webhook fire — can return an empty result that is genuinely ambiguous: it
cannot distinguish "this hasn't happened" from "this probe can't see it."
Attempting the real action directly is usually available without any extra
round trip, and its failure is specific — it names its own cause instead of
staying silent.

After two identical empty reads from the same probe, stop re-instructing the
user and start suspecting the probe itself. And before deriving a needed value
from scratch, check whether it already exists in a working sibling
configuration — a second account or integration set up the same way — since
it's frequently sitting there already.

Real case: connecting a bot integration needed its chat ID. The documented
route — have the user trigger it, then poll for the result — came back empty
four times across three rounds of re-instructing the user, including once
suspecting they'd triggered the wrong thing. The actual fix took one call:
attempting to send a message directly returned a specific, named error that
revealed the real missing step in one shot, something the empty poll was
never going to produce no matter how many times it ran.

## Closing check

Before calling a setup complete, confirm: every item was classified against
actual current state, not assumed from the list; every identifier that
mattered was verified against its source, not trusted from the document; any
step only the user can finish was named as such before you started, not
discovered at the end; and completion was proven by one real, working action —
not by a preflight, an install-success message, or a status field that was
never independently checked.
