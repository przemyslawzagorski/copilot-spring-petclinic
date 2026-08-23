# Optimizer playbook — how to actually cut the bill

> An engineering tutorial: what we measured, what we recommend, and **by which
> flag, file or frontmatter line** each saving is achieved. The numbers behind
> every claim live in [Context economy](context-economy.md); this page is the
> procedure.

## 0. The one-sentence model

```
cost ≈ turns × (system prompt + tool definitions + history + your message)
```

Two of those four terms are fixed, identical on every call, and paid before the
model reads your task. Together they are **24 269 tokens/call = 26.2%** of
everything billed (245 sessions, 23 624 calls). Your actual message is 0.5%.

So there are exactly two things to optimise: **the fixed prefix** (make each
call cheaper) and **the turn count** (make fewer calls). Everything below is
one of those two.

## 1. What came out of the tests

Every row is a controlled run — one variable changed, same task, same fixture,
graded 0–3 by a script that imports the result and asserts behaviour.

| # | Change | Effect | Correctness | Verdict |
|---|---|---:|:---:|---|
| 1 | Catalog cut to the 2 tools the task needs | **−64.2%** | 3/3 | **Adopt** |
| 2 | Same, on `gpt5.6-luna` | **−72.4%** | 3/3 | **Adopt** |
| 3 | 140-token `always_apply` frugality rule | **−31.5%** | 3/3 ×3 | **Adopt** |
| 4 | Drop 7 sub-agents (used in 0.83% of calls) | −3 805 tok/call | unchanged | **Adopt** |
| 5 | Detach an idle MCP server | −46 152 tok/call *(inferred)* | unchanged | **Adopt** |
| 6 | `always_apply` → `agent_requested` on a 60 KB rule | 23 145 → **66** tok | unchanged | **Adopt** |
| 7 | `--max-turns` above the task's need | **0%** | 3/3 | Guard rail only |
| 8 | `--max-turns` below the task's need | −77% | **0/3, silently** | **Never** |
| 9 | Remove all tools | −94.5% | **0/3 ×3** | Control, not advice |
| 10 | `haiku4.5` instead of `sonnet4.6` | **+14.2%** | 3/3 | Reject |
| 11 | `--ask` mode | 0 tokens | — | Safety, not savings |
| 12 | Ending sessions early | worse | — | **Reject** |

Three results are counter-intuitive enough to state plainly:

- **The cheap model was the expensive one.** `haiku4.5` cost 14.2% *more* than
  `sonnet4.6` because it needed two extra turns. Cost is turns × fixed cost —
  price per token barely matters.
- **A turn cap saves nothing and fails silently.** Swept 2 → uncapped, the cap
  never bound above 2; below the task's need it produced 0/3 twice with **exit
  code 0**. It is a runaway guard, not a budget.
- **Long sessions are fine.** 94.5% of input volume is cache-read, and the
  cached share *rises* with session length (75.8% in the first 10 turns, 93–96%
  after 30). Restarting re-pays the cache-creation premium on the whole prefix.

## 2. The recommended order

Do these top-down. Each step is measurable on its own; stop when the remaining
work costs more than it returns.

### Step 1 — Measure before you touch anything

```bash
auggie -p -q --max-turns 1 "Say OK." >/dev/null
```

Then read the decomposition the run wrote to `~/.augment/sessions/<id>.json`
(script in [Verify it yourself](context-economy.md#verify-it-yourself)), or
interactively type `/context`. You need two numbers: `system_prompt_tokens` and
`tool_definitions_tokens`. Everything below is judged against them.

Platform shortcut: **Workshop › Stały koszt kontekstu**
(`GET /api/v1/workshop/context-budget`) does this over your whole local session
corpus for free — no LLM call, no write.

### Step 2 — Detach MCP servers you are not calling

The single largest item, and the one nobody notices: an attached server is a
**per-call tax, not a per-use cost**. Its ~50 tool schemas are serialised into
every prompt whether or not you invoke it. Four sessions in the corpus had
`<serwer-mcp-A>` attached and never called it once — 14.6 million tokens for
nothing.

```bash
auggie mcp remove <name>          # detach entirely
auggie --enable-tool-search       # or: keep it, expose `find-tool` instead of 50 schemas
```

`--enable-tool-search` is the compromise when you need the server occasionally:
the model gets one search tool instead of the full schema dump.

### Step 3 — Remove tool groups you do not use

```bash
auggie tools remove sub-agent-validate    # persists to ~/.augment/settings.json
auggie tools add sub-agent-validate       # undo
auggie --remove-tool web-fetch "…"        # one run only, nothing persisted
```

`auggie tools remove` writes `removedTools` in `~/.augment/settings.json` and
applies to every future run. `--remove-tool` is per-invocation and is what the
Workshop's variant comparison sends on your behalf.

Measured differential prices (remove the subject, re-measure the prefix):

| Subject | Fixed cost | Real usage |
|---|---:|---|
| sub-agents (7 tools) | **3 805** tok/call | 0.83% of calls |
| task management (4 tools) | 1 869 tok/call | 5.3% — **keep for interactive work** |
| `str-replace-editor` | 1 631 | essential for editing |
| `view` | 1 493 | essential for reading |
| `sub-agent-validate`, `codebase-retrieval-raw`, `view-session` | ~1 000 combined | **0 invocations in 226 sessions** |

A tool's price includes the prose that explains it: removing the task tools
also shrank the *system prompt* (5 587 → 4 782). That is why removals are
measured per group, never divided into a per-tool figure nobody observed.

### Step 4 — Fix your rule frontmatter

This is free and the highest ratio on the page. One line decides whether a rule
body is prepended to **every** prompt or offered on demand:

```yaml
---
type: agent_requested                        # body loads only when the description matches
description: Use when editing CI pipelines.  # mandatory — this text is what gets loaded
---
```

| `type` | `description` | What the CLI does | Cost of a 60 KB rule |
|---|---|---|---:|
| `always_apply` | any | Body prepended to every prompt | **23 145** tok/call |
| `agent_requested` | present | Offered by description, body on demand | **66** tok/call |
| `manual` | any | Never loaded automatically | 0 |
| unusable / missing | present | Degrades to `agent_requested` | 66 |
| unusable / missing | **absent** | Body prepended to **every** prompt | 23 145 |

A 350× difference decided by one frontmatter line — and the failure is silent.
An invalid `type` (`auto`, `always`, `agent`) is reinterpreted, never rejected.
This repository had four such rules and one command with unquoted YAML, all
silently degraded from the day they were written. Audit yours: **Workshop ›
Audit** flags them as `invalid_type` / `missing_description`.

Skills are cheap by construction — a 123 KB skill added **66 tokens**, because
progressive disclosure loads the body only on trigger. Write skills freely;
write `always_apply` rules sparingly.

### Step 5 — Ask for fewer turns; do not cap them

The one lever that acts on the prompt rather than the catalog. Save this as
`.augment/rules/frugal.md` — the stock CLI picks it up with no other setup:

```markdown
---
type: always_apply
---
# Work in as few iterations as possible

Prefer one broad read over several narrow ones: batch independent tool calls
into a single step rather than issuing them one at a time. Read a file once,
in full, instead of re-reading fragments. Make all related edits to a file in
one edit call. Do not re-verify work you have already verified. Stop as soon
as the task is done.
```

It costs **140 tokens** on every call and removed roughly 28 600 — **−31.5%**
across three runs at an unchanged 3/3. It also removed the *variance*: without
it, runs wandered between 3 and 6 turns; with it, every run took exactly 3.

The Workshop serves this file verbatim with a copy button (a test asserts the
served text and `.augment/rules/frugal.md` never diverge). To hand it to a
team, put it in the GitLab skills repo → `POST /api/v1/skills/sync` →
**Resources → Browse**.

Set the cap as a guard rail only:

```bash
auggie -p --max-turns 60 "…"   # only works with --print
```

Real tasks need a median of **9** turns and a p95 of **100** (988 segmented
tasks, 23 490 calls). A cap of 2 would truncate 74% of them. A cap of 60 leaves
88.7% untouched while bounding the tail — the 22% of tasks over 30 turns burn
**72.8%** of all tokens.

### Step 6 — Pick the model that finishes, not the one that is cheap

All benchmarked models solved the task, with a **4.3× spread** driven entirely
by turns taken: `gpt5.6-luna` 6 turns / 72 333 tokens vs
`gemini-3.1-pro-preview` 11 turns / 157 594. In production data, cost per call
is nearly flat across models (~128 000 tokens); what separates a cheap session
from an expensive one is the median turn count.

```bash
auggie -p -q -m gpt5.6-luna "$TASK"
```

## 3. Prove it on your own work

Change exactly one thing per run and always pair the cost with a correctness
score — cost alone ranks "do nothing" first.

```bash
auggie -p -q --remove-tool sub-agent-code --remove-tool web-search "$TASK"   # catalog
auggie -p -q --max-turns 4 "$TASK"                                          # cap
auggie -p -q -m gpt5.6-luna "$TASK"                                         # model
```

Restrict the session-file search to files modified **after** the run started —
otherwise a failed run silently reports the previous run's numbers.

The platform automates the comparison: **Workshop › variant comparison**
(`POST /api/v1/workshop/variants`) runs one constant probe across 2–5
configurations and ranks them by measured cost. Each result reports
`tool_definitions_tokens` **per call**, with `fixed_context_source` =
`session_file` (measured) or `unverified` (the run reported no decomposition —
never rendered as a zero saving).

Verified end to end: baseline **11 631** tok/call → withholding `sub-agents`
**7 826** tok/call, a delta of **3 805** — the audited figure to the token.

!!! warning "A trimmed variant costs more on a single probe"
    A variant with `removed_tools` runs on a dedicated one-shot ACP client
    (no pooled warm start): 58.9 s / 338 credits vs 26.8 s / 247 for the
    baseline. The saving is fixed context **per call**, realised across a
    working session — not in the single measurement probe.

## 4. What not to bother with

| Idea | Why it fails |
|---|---|
| Capping turns to save money | 0% above the task's need; 0/3 silently below it |
| Ending sessions early to "reset" context | History is 94.5% cache-read and gets *cheaper* per turn; a restart re-pays the cache-creation premium. **But see the note below** — this holds for a session whose history you still need |
| Switching to a cheaper model | `haiku4.5` cost +14.2% — it took two more turns |
| `--ask` mode for savings | Byte-identical token counts; it restricts by instruction, not by removing tools |
| Removing tools "to be safe" | Without `view` and an editor the agent describes a patch it never applied: −94.5% for 0/3 |
| Trimming your prompt | It is 0.5% of the bill |
| Optimising by intuition | This repo's `.augment/` costs 6 302 tok/call — real, but 8× smaller than the MCP attachment nobody noticed |

> **Note on "ending sessions early".** The row above is measured against a
> session whose history is still doing work. It is **not** an argument for
> staying in a session stuffed with failed searches: cache read is cheap per
> token, but 100 000 tokens × 30 turns is 3 million cache-read tokens.
> The distinction is contents, not length — restarting while carrying the same
> context loses, restarting with a **condensed handoff file** (100k → 5k) wins.
> Full decision table in
> [`optymalizacja-zuzycia.md` § C](optymalizacja-zuzycia.md).

## 5. Caveats

Cost figures are stable on repeat (18 854 vs 18 882 — 0.15% apart) and safe to
rely on. Correctness **scores are one sample each** on one small task; a harder
task would separate the models differently. Treat the ranking as a method to
copy, not a league table to cite. The harness is about 60 lines — rebuild it
around a task that resembles your own work.

## Related

- [Context economy](context-economy.md) — the measured evidence, corpus
  statistics and the full 16-variant benchmark.
- [CLI training kit](cli-training-kit.md) — this procedure as a live demo
  script, plus the mode-by-mode table of which flag actually binds.
- progressive disclosure (mechanizm opisany w [skills docs](https://docs.augmentcode.com/cli/skills)) — why skills
  cost 66 tokens.
- konwencje autorskie reguł (patrz [rules docs](https://docs.augmentcode.com/cli/rules)) — rule authoring conventions.
