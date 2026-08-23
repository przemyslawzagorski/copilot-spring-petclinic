# CLI training kit — run the demo, read the numbers

> A presenter's supplement. [Context economy](context-economy.md) holds the
> evidence and [Optimizer playbook](optimizer-playbook.md) the procedure; this
> page is the **running order**: which command to type on stage, what the
> audience should see, which number to read afterwards, and where the platform
> comes in at the end.
>
> Every figure below was measured on `auggie 0.32.0`. Where a claim depends on
> the execution mode, the mode is named — most of the confusion in this area
> comes from a flag that works in one mode and is silently ignored in another.

## 1. The one-sentence model

```
cost ≈ turns × (system prompt + tool definitions + history + your message)
```

Two of the four terms are fixed and identical on every call: **24 269
tokens/call = 26.2%** of everything billed (245 sessions, 23 624 calls). Your
actual message is 0.5%. So there are exactly two levers — **make each call
cheaper** (fixed prefix) and **make fewer calls** (turns). Everything on stage
is one of the two.

## 2. The four execution modes — and why the flag table differs

`auggie` is one binary with four ways in. They do not share a control surface,
and that is the single most misleading thing about the CLI documentation.

| Mode | How it starts | Loop | Who drives it |
|---|---|---|---|
| **Interactive** | `auggie` | until you exit | a human at a TTY |
| **Print** (`--print` / `-p`) | `auggie -p "task"` | one shot, agent loops internally, then exits | a script |
| **ACP** (`--acp`) | `auggie --acp` | long-lived process, JSON-RPC over stdio | an SDK client |
| **MCP** (`--mcp`) | `auggie --mcp` | server; the model calls *it* | another agent |

Print mode is the one people mean by "automation": stdin is not a terminal, no
consent banner, one instruction in, final message out (`-q` strips the
reasoning log). `--output-format json` adds a machine-readable envelope, and
**only exists in print mode**.

ACP is what this platform uses (`AGENT_PROVIDER=auggie-acp`, the default). The
gain is that a client is a *pooled long-running process*: a message costs a
round-trip instead of a cold start. The cost is that the child's flags are
fixed when the client is constructed — a per-call flag list cannot reach a
process that is already running, so `concierge/providers/auggie_acp.py`
discards `extra_cli` outright and passes only what the SDK constructor accepts
(`model`, `workspace_root`, `removed_tools`, `cli_args` at construction).

### What binds where

| Lever | Interactive | Print | ACP | Notes |
|---|:--:|:--:|:--:|---|
| `--model` | ✅ | ✅ | ✅ | SDK constructor arg over ACP |
| `--remove-tool` | ✅ | ✅ | ✅ | `removed_tools=[…]` over ACP — **the lever that really restricts** |
| `--max-turns` | — | ✅ | ❌ | *measured below* |
| `--ask` | ✅ | ✅ | ❌ | over ACP it does not prevent writes — pinned by a live test |
| `--output-format json` | — | ✅ | — | print-only by design |
| `--rules <path>` | ✅ | ✅ | ✅ | extra rules file |
| `.augment/` in the repo | ✅ | ✅ | ✅ | discovered from the workspace root in every mode |

## 3. Measured: `--max-turns` binds in print, is ignored over ACP

Same task ("read three files one at a time with `view`, then summarise"), same
model (`haiku4.5`), same workspace. Turns are counted from the session file
the run itself wrote — one `token_usage` node per billed round.

**Print mode** (`auggie --print --quiet --model haiku4.5 …`):

| Arm | Turns | Exit | Output |
|---|---:|:--:|---|
| no flag | 2 | 0 | full summary, 1 172 B |
| `--max-turns 2` | 2 | 0 | full summary, 889 B |
| `--max-turns 1` | **1** | **0** | `⚠️ The conversation has been paused because maximum iterations reached (1).` |

The cap binds — and note the third row: **exit code 0**. A truncated run looks
exactly like a finished one to a CI pipeline. That is the whole reason the
worked example in [Context economy](context-economy.md#worked-example--the-same-task-sixteen-ways)
scored 0/3 twice without any warning.

**ACP mode**, the same flag passed through `cli_args`:

| Arm | Turns |
|---|---:|
| no flag | 4 |
| `--max-turns 3` | **5** |

Not capped — the run came out *longer*. This is pinned as a characterisation
test (`test_auggie_acp_capabilities_live.test_max_turns_is_ignored_in_acp_mode`),
so an SDK upgrade that starts honouring the flag fails loudly instead of
quietly changing our safety assumptions.

**Consequence for the demo.** If you show `--max-turns` on stage, show it in
print mode and show the truncation warning. If someone asks "so can I cap my
IDE / SDK agent the same way?" — the honest answer is no, and section 4 is what
to do instead.

## 4. The turn budget that does work: put it in the prompt

Since the transport will not cap the loop, state the budget as an instruction.
This is what the Workshop injects ahead of the probe (`{n}` = chosen budget):

```text
Turn budget for this task: at most {n} turns (model calls).
- Gather information in batches: call several tools in one turn instead of one file per turn.
- On turn {n} you must deliver the final answer, even if incomplete, marking what you could not confirm.
- Do not begin a new search when only the last turn remains.
```

Measured over one repository probe demanding cited file paths, four variants,
`comparison_id=budget1`:

| Variant | Budget | Turns | Tokens | USD | Cited paths that exist |
|---|:--:|---:|---:|---:|:--:|
| `sonnet4.6` | — | 8 | 171 176 | $0.223 | 8/8 |
| `sonnet4.6` | 2 | **4** | **81 447** | **$0.100** | 7/8 |
| `haiku4.5` | — | 16 | 756 639 | $0.130 | 8/8 |
| `haiku4.5` | 2 | **8** | **379 037** | **$0.072** | 9/9 |

Both models halved their turns, their tokens and their spend without losing
the grounding the probe demanded. **Neither reached the stated 2.** The budget
compresses the loop; it does not close it — which is why the Workshop reports
`turn_budget_respected` as a verdict (`true` / `false` / `null` when unasked or
unmeasured) instead of promising a cap.

It costs about **90 tokens** of prompt on every turn. On a task that would have
taken two turns anyway, that is pure overhead; the saving appears when the
uninstructed run would have wandered.

### The same idea, permanently: the frugality rule

The budget is per-run. The standing version is a 140-token `always_apply` rule
committed at `.augment/rules/frugal.md` — batch independent calls, read a file
once, group edits, do not re-verify finished work. Over six runs of one graded
task it cut billed tokens **−31.5%** at an unchanged 3/3, and removed the
*variance*: uncapped runs wandered between 3 and 6 turns, every rule-on run
took exactly 3.

Two levers, one mechanism: **ask for fewer turns, never cap them.**

## 5. Rules: one frontmatter line, a 350× difference

| `type` | `description` | What the CLI does | Cost of a 60 KB rule |
|---|---|---|---:|
| `always_apply` | any | Body prepended to **every** prompt | **23 145** tok/call |
| `agent_requested` | present | Offered by description; body on demand | **66** tok/call |
| `manual` | any | Never loaded automatically | 0 |
| unusable / missing | present | Degrades to `agent_requested` | 66 |
| unusable / missing | **absent** | Body prepended to **every** prompt | 23 145 |

The failure is silent. An invalid `type` (`auto`, `always`, `agent`) is
reinterpreted, never rejected — nothing is logged, so the author never learns.
This repository's first audit found four such rules and one command with
unquoted YAML, all silently degraded from the day they were written; `.augment/rules/`
here is now clean (3 `always_apply`, 10 `agent_requested`).

Skills are cheap by construction — a 123 KB skill added **66 tokens**, because
progressive disclosure loads the body only on trigger. Write skills freely;
write `always_apply` rules sparingly.

## 6. The catalog: pay for capability you use

The default catalog is 30 tools costing **17 219** tokens on every call.
Measured differentially — remove the group, re-measure the prefix:

| Subject | Fixed cost | Real usage |
|---|---:|---|
| sub-agents (7 tools) | **3 805** tok/call | 0.83% of 27 112 calls |
| task management (4) | 1 869 tok/call | 5.3% — keep for interactive work |
| `str-replace-editor` | 1 631 | essential for editing |
| `view` | 1 493 | essential for reading |
| `sub-agent-validate`, `codebase-retrieval-raw`, `view-session` | ~1 000 combined | **0 invocations in 226 sessions** |

An **attached MCP server is a per-call tax, not a per-use cost**: `<serwer-mcp-A>`
(~50 tools) added ~46 152 tokens to every call in its sessions, and four
sessions had it attached and never invoked it — 14.6 million tokens for
nothing. `--enable-tool-search` is the compromise: one search tool instead of
50 schemas.

Removing every tool is **−94.5% and worth nothing**: three runs, three scores
of 0/3. Without `view` and an editor the model produces a confident description
of a patch it never applied. Show this arm — it is the control that stops the
audience over-trimming.

## 7. The snowball: why turns dominate

Every turn is one call to the model that re-sends the system prompt, the whole
tool catalog and the history so far. Occupancy therefore climbs monotonically
across a run, which neither the total nor the peak can show. Measured on one
probe (`comparison_id=snowball1`, occupancy in tokens per turn):

| Model | Turns | Occupancy, turn by turn |
|---|---:|---|
| `haiku4.5` | 4 | 20 284 → 29 343 → 38 260 → 45 335 |
| `sonnet4.6` | 7 | 20 284 → 22 592 → 26 031 → 29 086 → 31 251 → 32 231 → 32 673 |

Both start at the identical **20 284** — the fixed prefix, paid before either
did any work — and diverge only by what each turn accumulated.

Two corollaries worth stating on stage:

- **A weaker model is not a cheaper model.** `haiku4.5` cost **+14.2%** against
  `sonnet4.6` on the same graded task, because it needed two more turns.
- **Long sessions are fine.** 94.5% of input volume is cache-read and the
  cached share *rises* with session length (75.8% in the first 10 turns, 93–96%
  after 30). Restarting re-pays the cache-creation premium on the whole prefix.
  "End your session early to reset context" is actively wrong.

A caveat to keep the claim honest: a **turn** is one *billed round*. Across 214
exchanges on disk, every exchange carries exactly one `token_usage` and one
`billing_metadata` node while up to four `tool_use` nodes sit inside it. The
tool-call loop within a round is not separately priced by the vendor and cannot
be separately counted — the two figures differ by up to 4×.

## 8. The live demo — running order

Work in a scratch clone, not the repository you care about. Each step is one
command and one number; the whole set runs in about ten minutes.

### Step 0 — the reader (paste once)

Every step below reads the same two numbers from the session file the run just
wrote. Restrict the search to files modified **after** the run started —
otherwise a failed run silently reports the previous run's figures.

```bash
cat > /tmp/fixed.py <<'PY'
import json, pathlib, sys, time
since = float(sys.argv[1])
d = pathlib.Path.home() / ".augment/sessions"
files = [p for p in d.glob("*.json") if p.stat().st_mtime > since]
if not files:
    raise SystemExit("no session file written after the run started")
f = max(files, key=lambda p: p.stat().st_mtime)
turns = 0
fixed = None
for e in json.loads(f.read_text())["chatHistory"]:
    for n in e["exchange"]["response_nodes"]:
        u = n.get("token_usage")
        if not u:
            continue
        turns += 1
        if fixed is None and u.get("tool_definitions_tokens"):
            fixed = (u["system_prompt_tokens"], u["tool_definitions_tokens"])
sp, td = fixed or (0, 0)
print(f"turns={turns}  system_prompt={sp:,}  tool_definitions={td:,}  fixed/call={sp+td:,}")
PY
```

### Step 1 — what a call costs before it does anything

```bash
T0=$(date +%s); auggie -p -q --max-turns 1 "Say OK." >/dev/null
python3 /tmp/fixed.py $T0
```

Read out `fixed/call`. Everything that follows is judged against it.
Interactively, `/context` shows the same breakdown.

### Step 2 — the catalog is most of it

```bash
T0=$(date +%s); auggie -p -q --max-turns 1 \
  --remove-tool sub-agent-explore --remove-tool sub-agent-plan \
  --remove-tool sub-agent-auggie-guide --remove-tool sub-agent-general-purpose \
  --remove-tool sub-agent-research --remove-tool sub-agent-code \
  --remove-tool sub-agent-validate "Say OK." >/dev/null
python3 /tmp/fixed.py $T0
```

Expect roughly **−3 805** tokens per call. Point out that it is per call, so
its real value is that figure × the turns of a working session. Mention the
side effect: removing the task tools also shrank the *system prompt*
(5 587 → 4 782) — a tool's price includes the prose that explains it.

`--remove-tool` is per-invocation. `auggie tools remove <name>` persists to
`~/.augment/settings.json` (`removedTools`); undo with `auggie tools add`.

### Step 3 — the frontmatter line

Two runs, one file, one word changed:

```bash
mkdir -p .augment/rules
printf -- '---\ntype: always_apply\n---\n' > .augment/rules/big.md
head -c 60000 /dev/urandom | base64 >> .augment/rules/big.md
T0=$(date +%s); auggie -p -q --max-turns 1 "Say OK." >/dev/null; python3 /tmp/fixed.py $T0

sed -i '2s/.*/type: agent_requested\ndescription: Use when editing CI pipelines./' .augment/rules/big.md
T0=$(date +%s); auggie -p -q --max-turns 1 "Say OK." >/dev/null; python3 /tmp/fixed.py $T0
```

`system_prompt` moves by roughly **23 000 tokens**. This is the highest-ratio
change on the page and it is free.

### Step 4 — the cap binds only in print, and it lies quietly

```bash
auggie -p -q --max-turns 1 --model haiku4.5 \
  "Read README.md, then CHANGELOG.md, one at a time with view, then summarise."
echo "exit=$?"
```

The output is the truncation warning; the exit code is **0**. Then contrast
with `--max-turns 4` on the same task. Say plainly: cap as a runaway guard
(around 60 — real tasks need a median of 9 turns and a p95 of 100), never as a
budget.

### Step 5 — ask instead of capping

```bash
cp /path/to/agentic-platform/.augment/rules/frugal.md .augment/rules/
T0=$(date +%s); auggie -p -q "<a task that takes several turns>" >/dev/null
python3 /tmp/fixed.py $T0
```

Compare `turns` with and without the file. In the benchmark: 4/4/5 turns → a
flat 3/3/3, **−31.5%** tokens, unchanged correctness.

### What to say if a step lands differently

Cost figures repeat within about 0.15% (18 854 vs 18 882 on the same
configuration), so a token count that moves by a few percent is noise, not a
finding. Correctness scores are one sample each — a live run that solves the
task differently is a different sample, not a contradiction. The method is
what transfers; the league table is not.

## 9. After the demo — reading the statistics

Everything above reads one session file at a time. The interesting questions
are about the corpus: which repository burns the budget, which tool is paid for
and never called, did adopting a rule actually change anything.

The vendor's own dashboard (`app.augmentcode.com`) answers the spend question
per user and enforces budgets. What it does not break down is *where inside a
call* the tokens went — and that decomposition is what every lever above acts
on. It sits in `~/.augment/sessions/*.json`, one file per session, written by
the CLI itself.

Whatever tool you point at that corpus, these are the four questions worth
asking of it:

| Question | Where the answer lives in the session file |
|---|---|
| What does a call cost before any work? | `token_usage.system_prompt_tokens` + `tool_definitions_tokens` |
| Which tools am I paying for and not calling? | tool-call nodes, counted against the catalog |
| Is an MCP server attached and idle? | server names in `~/.augment/settings.json` vs invocations |
| How long are my tasks, really? | count of `token_usage` nodes per user request |

That last one decides where a guard rail belongs. Segmenting 227 local sessions
by user request gives 988 tasks / 23 490 calls:

| p50 | p75 | p90 | p95 | p99 | max |
|---:|---:|---:|---:|---:|---:|
| 9 | 26 | 68 | 100 | 194 | 424 |

A cap of 2 would truncate 74% of real tasks. A cap of 60 leaves 88.7%
untouched while bounding the tail — the 22% of tasks over 30 turns burn
**72.8%** of all tokens.

## 10. Where the platform fits

The manual reader in Step 0 is one file, one number, one run. This platform
runs the same reads over the whole corpus and turns them into a decision.

| Surface | What it does | Cost |
|---|---|---|
| **Workshop › Stały koszt kontekstu** (`GET /api/v1/workshop/context-budget`) | The Step 1–2 measurement over every indexed session, plus the findings: an underused tool group, an idle MCP server — each with the `auggie` command that removes it, labelled `measured` or `inferred` | free — SQL + one settings read, no model call |
| **Workshop › Audit** | The Step 3 frontmatter check over your repository's whole `.augment/` tree, including the degradations the CLI applies silently | free |
| **Workshop › Porównanie wariantów** (`POST /api/v1/workshop/variants`) | Steps 2, 4 and 5 as one experiment: 2–5 configurations against one probe, ranked by measured USD, with turns, per-turn occupancy and the turn budget of section 4 | paid — one call per variant, projected before it runs |
| **Admin › Sessions › Diagnosis** (`GET /api/v1/admin/sessions/analytics`) | Section 9's four questions in SQL: usage, tools, repeat reads, loop-length distribution — per repository, with a before/after window around an adoption date | free |
| **Resources › Browse** | Ships the artefacts as a ZIP with a valid `.augment/` tree, or installs them into your active clone | free |

Two properties worth stating when you show it:

- **It measures, it does not estimate.** Every variant's fixed cost is read
  from the session file that run wrote. A run that reported no decomposition is
  labelled `unverified` and left off the chart — never drawn as a zero saving,
  because "unmeasured" and "nothing to save" must not look the same.
- **It produces files, not lock-in.** The output is a `.augment/` tree the
  stock CLI honours with no platform involvement afterwards. The frugality
  rule the panel serves is byte-identical to `.augment/rules/frugal.md` in this
  repository, and a test asserts the two never diverge.

Back-fill sessions indexed before the parser read the decomposition — they show
as `unmeasured`, not as zero:

```bash
curl -X POST "http://localhost:8770/api/v1/admin/sessions/sync?force=true"
```

## Related

- [Context economy](context-economy.md) — the corpus statistics and the full
  16-variant benchmark behind every number here.
- [Optimizer playbook](optimizer-playbook.md) — the same findings as an ordered
  procedure, with the flag or frontmatter line behind each saving.
- progressive disclosure (mechanizm opisany w [skills docs](https://docs.augmentcode.com/cli/skills)) — why a 123 KB
  skill costs 66 tokens.
