---
name: shell-command-verification
description: Verification discipline for running and monitoring shell commands — especially long-running, backgrounded, or piped ones — where a readability filter or a convenient-but-wrong signal can silently hide a real failure. Covers why piping a command through `tail` / `head` / `Select-Object -Last N` can erase both progress visibility (buffering filters emit nothing until the upstream command exits) and the real exit code (only the last command in a pipe sets `$?` / `&&`), why directory listings and intermediate caches report stale sizes for files actively being written, and why the actual postcondition — does the file, binary, or directory exist — is the one signal that can't lie. Use this whenever running an install, build, download, or any command being backgrounded or piped through an output-reducing filter, or when checking whether a long-running process has stalled or a command actually succeeded — even if the exit code says 0.
license: MIT
---

# Shell Command Verification

Running a long or important shell command is not the same as knowing what it
did. Two things get lost the same way, quietly: piping raw output through a
filter for readability, and trusting one convenient signal — an exit code, a
directory listing — instead of verifying what actually happened.

## Step 1: Don't let a readability filter erase your only signal

Two specific failure shapes come from the same instinct: keep output short.

**Progress signal.** Piping a long-running command through a buffering
filter (`| Select-Object -Last N`, or piping streaming progress output
through `| tail`) to keep it readable seems harmless — until the command is
backgrounded. Buffering filters typically emit nothing until the upstream
command exits, so a backgrounded process's output file can sit completely
empty while the process itself is perfectly healthy. Reduce at read time, not
write time: let raw output stream unfiltered to a file, and sample the tail
of that file when you check on it, rather than filtering at the source.

**Exit-code signal.** In a pipeline, `$?` and `&&` only see the *last*
command's status. `cmd | tail && echo done` reports success even when `cmd`
itself failed — the pipe swallows the real status. Combined with a background
task's own "exit 0" notification, a genuine failure can end up doubly
confirmed as a success, with no signal anywhere that anything went wrong.

Real case: `yarn install --silent 2>&1 | tail -20 && echo "INSTALL DONE"` ran
as a background task. `yarn` wasn't on PATH, so the install never actually
ran — but `tail` exited 0, `&&` fired, "INSTALL DONE" printed, and the
background task itself reported exit code 0. The failure only surfaced steps
later, when the expected output didn't exist, after the user had already
been told the install succeeded.

What to do: when piping a command whose success matters, capture and print
the real status of the command you actually care about — e.g.
`cmd 2>&1 | tail -20; echo "exit: ${PIPESTATUS[0]}"` in bash — never
`cmd | tail && echo OK`. Better still, don't rely on the exit code at all:
see Step 3.

## Step 2: Match your progress probe to how the tool actually writes

Not every "is it stuck?" check reads what it thinks it reads.

- **Discrete-jump caches read as stalled between jumps.** An intermediate
  artefact that's only written when a stage completes — a download tool's
  HTTP cache, a staged build's manifest — will look frozen for the entire
  duration of that stage even while the underlying transfer is healthy.
  Judge staleness against a monotonically increasing counter the process
  must actually advance to make progress, not against a value that only
  updates in jumps.
- **Directory-entry size is stale for files still being written.** A
  directory listing's cached size for an open file can lag the real size by
  a wide margin, and for a long time — filesystems commonly don't flush a
  file's directory entry while a write handle stays open. A coincidentally
  repeated stale reading can look like corroborated evidence of a stall
  rather than the artefact it actually is. Recursive folder-size totals
  inherit this staleness for every file inside that's currently being
  written.

Real case: the same in-progress file reported 86.8 MB via a directory
listing and 1483 MB when stat'd directly, in the same command — the
directory entry hadn't been flushed in 15 minutes. That stale figure
happened to exactly match the previous poll too, which made it look
confirmed rather than simply frozen.

What to do: stat the file path directly rather than reading its size from a
parent-directory listing or a recursive tree sum. Treat a poll value
identical to the previous poll as suspect, and re-derive it through a
different mechanism before concluding "no progress" — agreement between two
reads of the same stale source is not confirmation. Prefer one cheap
cumulative counter sampled twice over several one-shot instantaneous checks.

## Step 3: Verify the postcondition, not the report

An exit code — even an accurate one — only tells you the command finished; it
does not by itself prove the command produced what you needed. And a
project's own documentation or lockfile naming a tool doesn't prove that tool
is actually installed on this machine — a `yarn.lock` means the project was
*authored* with yarn, not that yarn is on PATH here.

After anything a later step depends on, check for the actual artefact: the
file exists, the binary is on PATH, the directory was created, the expected
count changed. This one check catches every failure mode above at once — a
masked exit code, a stale progress reading, an assumed-but-missing
dependency — because it doesn't rely on any of the signals that can lie.

## Closing check

Before reporting a shell command as done, ask: did anything sit between the
command and my read of it that could have hidden a failure — a pipe, a
filter, a backgrounded process? And did I confirm the actual output — the
file, the binary, the count — rather than trusting an exit code or a
convenient-looking status line?
