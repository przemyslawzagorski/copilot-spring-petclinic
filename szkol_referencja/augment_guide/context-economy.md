# Context economy — a measured cheatsheet

> Every number here was measured on 226 local session files (292 MB, 23 155
> LLM calls, 5 455 543 credits) and on controlled `auggie 0.32.0` runs where a
> single variable changed. Where a figure is inferred rather than measured, it
> says so. Re-run any measurement yourself with the commands in
> [Verify it yourself](#verify-it-yourself).
>
> If you read one section, make it
> [the worked example](#worked-example--the-same-task-sixteen-ways): sixteen
> configurations against the same graded task, where the cheapest options score
> zero.

## Where the money actually goes

Each LLM call assembles a context from five parts. Averaged over 23 155 calls:

| Component | Share | Mean per call | Can you control it? |
|---|---:|---:|---|
| Conversation history | 71.8% | 67 754 | Barely — see [History](#history-the-big-one-you-mostly-cannot-fix) |
| **Tool definitions** | **18.7%** | **17 662** | **Yes — biggest real lever** |
| **System prompt** | **7.1%** | **6 665** | **Yes — rules and skills live here** |
| Tool results | 1.1% | 1 041 | Yes, indirectly |
| Your actual message | 0.5% | 438 | — |

The headline: **25.7% of everything you pay is identical on every call.** It is
the price of being *able* to act, paid before you act. Your prompt is 0.5%.

### Not every token costs the same

Those shares are *nominal* volume. Across the same 23 357 calls, the billing
tier breaks down as:

| Tier | Volume | Share |
|---|---:|---:|
| Cache read | 2 819 000 630 | 94.5% |
| Cache creation | 163 199 923 | 5.5% |
| Fresh input | 141 690 | 0.005% |

Weighted at the usual cache rates (read ≈0.1×, write ≈1.25×), 2.98 billion
nominal tokens behave like **486 million** — 16.3% of the headline figure.

Two consequences, and they pull in opposite directions:

- **History is cheaper than its 72% suggests.** It is almost entirely
  cache-read, and the cached share *rises* with session length (75.8% in the
  first 10 turns, 93–96% after 30). Long sessions are not the problem.
- **Fixed cost is worse than its 25.7% suggests.** Tool definitions and the
  system prompt sit at the *front* of the prompt, so every change to them
  invalidates the cache for everything after. That is why the levers below are
  worth more than a naive reading of the table implies.

## The golden rules

**1. Pay for capability you use, not capability you might use.**
The default catalog is 30 tools costing 17 219 tokens per call. Sub-agents cost
3 805 of that and were invoked in 0.83% of 27 112 calls.

**2. An attached MCP server is a per-call tax, not a per-use cost.**
Attaching `<serwer-mcp-A>` (~50 tools) added ~46 152 tokens to *every* call in
that session. Four sessions had it attached and never called it once:
14.6 million tokens for nothing.

**3. Ask for fewer iterations; cap them only as a runaway guard.**
A 140-token rule asking the agent to batch calls and not re-verify finished
work cut a task by **31.5%** at an unchanged 3/3. The turn cap, swept from 2 to
uncapped, changed nothing above 2 — it never binds when the agent stops on its
own, and below the task's needs it fails *silently* (0/3 twice, exit code 0).
Real tasks need a median of 9 turns and a p95 of 100, so set the ceiling around
60 to bound the tail, and put the frugality where it works: in the prompt.

**4. Rules are cheap unless `always_apply`.**
A 60 KB rule as `agent_requested` costs **66 tokens**. The same file as
`always_apply` costs **23 145**. A 350× difference decided by one frontmatter
line.

**5. Skills are cheap by construction.**
A 123 KB skill added 66 tokens. Progressive disclosure works — the body loads
only when triggered. Write skills freely; write `always_apply` rules sparingly.

**6. Ask mode is a safety belt, not a discount.**
`--ask` produced byte-identical token counts. It restricts edits by
*instruction*, not by removing tools. Use it for safety; expect no savings.

**7. A weaker model is not a cheaper model.**
On the same graded task `haiku4.5` cost **14.2% more** than `sonnet4.6`, and
`gemini-3.1-pro-preview` cost 89% more — both because they took more turns, not
because their tokens cost more. Cost is *turns × fixed cost*. Pick the model
that finishes in fewest turns.

**8. Measure before you optimise.**
This repo's `.augment/` costs 6 302 tokens per call — real, but 8× smaller than
the MCP attachment that nobody noticed. Intuition ranked these backwards.

## The levers, with commands

| Lever | Measured cost | Command | Safe to trade away when |
|---|---:|---|---|
| Sub-agents (7) | 3 805 tok/call | `auggie tools remove sub-agent-validate` | You are not delegating. `sub-agent-validate` was never used in 226 sessions. |
| MCP server | ~46 152 tok/call *(inferred)* | `auggie mcp remove <name>` | The task touches no Jira/GitLab/Wiki. |
| MCP, keep but hide | see below | `auggie --enable-tool-search` | You need it occasionally — exposes `find-tool` instead of 50 schemas. |
| Task tools (4) | 1 869 tok/call | `auggie tools remove add_tasks` | One-shot scripted runs. **Keep for interactive work** — 5.3% real use. |
| Frugality rule | −31.5% for 140 tok/call | `always_apply` rule: batch calls, read once, don't re-verify | Always — it removed turn *variance* too. |
| Turn cap | 0% above the task's need | `auggie -p --max-turns 60 "…"` | Runaway guard only. Only works with `--print`. |
| `always_apply` rule | full body, every call | `type: agent_requested` + `description:` | Almost always. Reserve `always_apply` for genuine invariants. |
| Single tool, one run | 145–1 631 tok | `auggie --remove-tool web-fetch` | Per-run experiments. |
| Never-used tools | ~1 000 tok/call | `auggie tools remove codebase-retrieval-raw` | Always — see below. |

### Never used in 226 sessions

Zero invocations, still paid for on every call:

```bash
auggie tools remove sub-agent-validate
auggie tools remove codebase-retrieval-raw
auggie tools remove view-session
```

Persists to `~/.augment/settings.json` (`removedTools`). Undo with
`auggie tools add <name>`.

### Measured differential cost per tool

Removing one tool and re-measuring the fixed cost:

| Tool | Fixed cost |
|---|---:|
| `str-replace-editor` | 1 631 |
| `view` | 1 493 |
| `launch-process` | 1 092 |
| `codebase-retrieval` | 332 |
| `save-file` | 322 |
| `web-fetch` | 173 |
| `ask-user` | below measurement threshold |

Removing all 7 sub-agents **and** the 4 task tools drops the fixed cost from
17 219 to 11 545 — a 33% cut. Read-only minimum (18 tools removed) reaches
9 045, a 47.5% cut.

Note the side effect: removing task tools also shrank the *system prompt*
(5 587 → 4 782). A tool's cost includes the instructions that explain it.

## Worked example — the same task, sixteen ways

The tables above price *availability*. This one prices *outcomes*: one fixed
task, sixteen configurations, and a grader that does not care how convincing
the answer sounded.

**The task.** A `stats.py` with three real bugs — `median` ignores even-length
lists, `clamp` swaps its bounds, `normalise` divides by zero on a constant
series — plus two correct functions the agent must not break. Scoring is
mechanical: 0–3, one point per bug genuinely fixed.

**Held constant.** Same prompt, same fixture, a fresh copy per run, no
`.augment/` config. `sonnet4.6` unless the row names another model.
Percentages are against the default full-catalog uncapped run (83 313 tokens).

| Variant | Turns | Tokens | vs default | Score |
|---|---:|---:|---:|:---:|
| All 32 tools removed, `--max-turns 1` | 1 | 4 571 | **−94.5%** | **0/3** |
| All 32 tools removed, `--max-turns 2` | 1 | 4 571 | −94.5% | **0/3** |
| All 32 tools removed, uncapped | 1 | 4 574 | −94.5% | **0/3** |
| 2 tools, `--max-turns 2` | 2 | 18 854 | −77.4% | **0/3** |
| 2 tools, `--max-turns 2` (repeat) | 2 | 18 882 | −77.3% | **0/3** |
| **`gpt5.6-luna`, 2 tools, `--max-turns 4`** | 4 | **23 033** | **−72.4%** | **3/3** |
| **2 tools, uncapped** | 3 | **29 830** | **−64.2%** | **3/3** |
| 2 tools, `--max-turns 4` | 4 | 39 988 | −52.0% | 3/3 |
| Full catalog, `--max-turns 2` | 2 | 40 245 | −51.7% | 3/3 |
| `gpt5.6-luna`, full catalog | 6 | 72 333 | −13.2% | 3/3 |
| Full catalog, uncapped *(default)* | 4 | 83 313 | — | 3/3 |
| `haiku4.5`, full catalog | 6 | 95 136 | +14.2% | 3/3 |
| `opus5`, full catalog | 5 | 101 567 | +21.9% | 3/3 |
| `glm-5.2`, full catalog | 10 | 117 187 | +40.7% | 3/3 |
| `sonnet5-high`, full catalog | 6 | 125 037 | +50.1% | 3/3 |
| `gemini-3.1-pro-preview`, full catalog | 11 | 157 594 | +89.2% | 3/3 |

### What this actually shows

**Removing every tool is 94.5% cheaper and worth nothing.** Three runs, three
scores of zero. Without `view` and an editor the model cannot read the file or
write the fix, so it produces a confident description of a patch it never
applied. An agent with no tools is a chatbot. This is the control, not a
recommendation.

**A turn cap below what the task needs fails silently.** `2 tools /
--max-turns 2` scored 0/3 **twice** — the agent spends one turn reading and is
cut off mid-edit. Nothing warns you: the exit code is 0 and the run looks
finished. The same configuration at 4 turns scored 3/3. Cap turns to bound
runaway loops, not to squeeze a task into fewer steps than it has.

**The sweet spot is a small catalog, not a small budget.** Two tools uncapped:
**−64.2% for an identical 3/3**. The saving comes from fewer tool definitions
in *every* call, not from stopping early — which is why it costs nothing in
quality. Best overall was `gpt5.6-luna` with those same two tools: **−72.4%**.

**Model choice moves cost more than any flag, and not the way you would
guess.** All models solved it, with a 4.3× spread between `gpt5.6-luna`
(72 333) and `gemini-3.1-pro-preview` (157 594). The driver is *turns taken*,
not price per token: Gemini used 11 turns and 10 tool calls where Luna used 6.
Note that `haiku4.5` — the "cheap" model — cost **more** than `sonnet4.6`
(+14.2%) because it needed two extra turns. A weaker model is not a cheaper
model.

**The same effect in production data.** Across the 226 real sessions, cost per
call is nearly flat regardless of model (~128 000 tokens for
`claude-opus-4-7`, `-4-8` and `fable-5`; 142 815 for `opus-5`). What separates
a cheap session from an expensive one is the median turn count — 1 for
`sonnet-4-5` sessions, 400+ for `opus-4-8`. **Cost is turns × fixed cost.**
Both factors are yours to set; the per-token price is not.

### Asking for fewer iterations beats capping them

A turn cap is a hard stop applied from outside; an instruction is a change in
how the agent works. Only the second one saved anything here.

Six runs, full catalog, uncapped, identical task — three with a 398-byte
`always_apply` rule asking the agent to batch independent tool calls, read a
file once in full, group edits, and not re-verify finished work:

| Variant | Turns | Tokens (mean of 3) | vs no rule | Score |
|---|---|---:|---:|:---:|
| No rule | 4, 4, 5 | 90 668 | — | 3/3, 3/3, 3/3 |
| **Frugality rule** | **3, 3, 3** | **62 066** | **−31.5%** | **3/3, 3/3, 3/3** |

The rule adds **140 tokens** to the system prompt on every call and removes
roughly 28 600. It also removed the *variance*: uncapped runs wandered between
3 and 6 turns, every rule-on run took exactly 3.

The rule that produced those numbers is committed in this repository at
`.augment/rules/frugal.md`, byte-identical to the benchmarked one — and served
verbatim by `GET /api/v1/workshop/context-budget`, so the Workshop panel offers
it with a copy button (a test asserts the served text and the file never
diverge). Copy it into
your repository's `.augment/rules/` and the stock CLI picks it up — nothing
else is needed. To hand it to a whole team, put it in the GitLab skills repo
(`GITLAB_SKILLS_REPO_URL`): after `POST /api/v1/skills/sync` it appears under
**Resources → Browse**, where anyone can download a ZIP with a valid
`.augment/` tree or install it into their active clone.

It is `always_apply`, so those 140 tokens are paid on every call whether or not
the rule changes anything — the measurement above is what justifies the price.
Verify it against your own work before adopting it team-wide; a task profile
unlike this benchmark may not respond the same way.

The turn cap, tested the same way, did nothing:

| Cap | Turns taken (2 runs) | Score |
|---|---|:---:|
| 2 | 2, 2 | 3/3, 3/3 |
| 4 | 4, 4 | 3/3, 3/3 |
| 6 | 4, 3 | 3/3, 3/3 |
| 8 | 3, 4 | 3/3, 3/3 |
| 12 | 4, 4 | 3/3, 3/3 |
| uncapped | 4, 6 | 3/3, 3/3 |

Above 2 the cap never binds — the agent stops when it is done, so the limit is
not what determines the turn count. It only changes the outcome when it cuts
in below what the task needs, and then it does so silently (the 0/3 rows
above). **Set the cap as a runaway guard; ask for frugality in the prompt.**

### How many turns does real work actually take?

Segmenting 227 local sessions by user request gives **988 tasks / 23 490 LLM
calls**. Per task:

| p50 | p75 | p90 | p95 | p99 | max |
|---:|---:|---:|---:|---:|---:|
| 9 | 26 | 68 | 100 | 194 | 424 |

A cap of 2 would truncate 74% of real tasks. The distribution is heavily
skewed: the 22% of tasks needing over 30 turns burn **72.8%** of all tokens.
A cap around **60** leaves 88.7% of tasks untouched while bounding the tail
that costs half the budget — a guard rail, not a schedule.

### The honest caveat

These are single runs on one small task. Token counts were stable on repeat
(18 854 vs 18 882 — 0.15% apart), so the *cost* figures are reliable; the
*scores* are one sample each, and a harder task would separate the models
differently. Treat the ranking as a method to copy, not a league table to
cite. The harness is about 60 lines — rebuild it around a task that resembles
your own work.

## History — big in volume, small in bill

History is 72% of context volume and there is no client-side flag for it — but
it is also the *cheapest* 72% you will ever pay for. What the data shows:

- It **plateaus**, it does not grow forever: median 23 262 tokens over the
  first 25 calls, ~64 000 from call 50 onward. A sliding window is in effect.
- Not one of the 226 sessions was auto-compacted (`isHistorySummary`: 0).
- Only 3 calls out of 23 165 exceeded the 200 000-token window.
- It is almost entirely cache-read, and **the cached share grows with session
  length** — 75.8% in the first 10 turns, 93–96% after 30.

So "end your session early" is **actively wrong**: a long session has *better*
cache economics than a fresh one, and a restart re-pays the cache-creation
premium on the whole prefix. What *is* supported: fewer turns per task, because
each turn re-pays the fixed prefix at full rate. That is rule 3 — a statement
about task shape, not session hygiene.

> **Reconciliation with `optymalizacja-zuzycia.md`.** That document advises
> *always* resetting the session (`/new`) rather than correcting inside a bloated
> one — the opposite of the paragraph above. Both are right about different
> things. Cache read is cheap **per token**, but 100 000 tokens × 30 turns is
> still 3 million cache-read tokens; a session stuffed with failed searches is
> expensive on *every* turn. The resolution is not about session length but
> about session **contents**: restarting while carrying the same context loses
> (you re-pay cache creation), restarting with a **condensed handoff** wins
> (100k → 5k). The saving comes from the condensation, not from the restart.
> Decision table: [`optymalizacja-zuzycia.md` § C](optymalizacja-zuzycia.md).

## Hooks

Per the [CLI docs](https://docs.augmentcode.com/cli/hooks.md), `SessionStart`
and `PostToolUse` hooks can inject text into the model context (via stdout or
`additionalContext`). That text is billed like any other context on every
subsequent call. `PreToolUse`, `SessionEnd` and `Stop` do not inject.

No hooks were configured on this machine, so there is **no measurement** here —
only the documented contract. Treat injected hook output with the same
suspicion as an `always_apply` rule.

## Verify it yourself

Fixed cost of your current configuration, in any repository:

```bash
auggie -p -q --max-turns 1 "Say OK." >/dev/null
python3 - <<'PY'
import json, pathlib
f = max(pathlib.Path.home().joinpath(".augment/sessions").glob("*.json"),
        key=lambda p: p.stat().st_mtime)
for e in json.loads(f.read_text())["chatHistory"]:
    for n in e["exchange"]["response_nodes"]:
        u = n.get("token_usage")
        if u and u.get("tool_definitions_tokens"):
            print(f"system_prompt={u['system_prompt_tokens']:,}  "
                  f"tool_definitions={u['tool_definitions_tokens']:,}")
            raise SystemExit
PY
```

Run it once as-is, then again after `auggie tools remove <name>`. The
difference is that tool's true price. Interactively, `/context` shows the same
breakdown.

### Or let the platform do it

The manual measurement above is what
`GET /api/v1/workshop/context-budget` automates over your whole local session
corpus — and what the **Workshop › Stały koszt kontekstu** panel renders. It is
free: SQL over the indexed session files plus one read of
`~/.augment/settings.json` (server and tool *names* only — never `env`,
`command` or `args`). It issues no model call and writes nothing.

Each finding arrives with the command that acts on it and a confidence label:
`measured` when the figure came from removing the subject and re-running,
`inferred` when it came from comparing groups of sessions. On this repository's
corpus (293 files, 245 measured sessions, 23 624 calls):

| Fact | Value |
|---|---:|
| Fixed cost per call | 24 269 tokens |
| Share of everything paid for | 26.2% |
| Sub-agent group, invoked under 1% of calls | 3 805 tokens/call, `measured` |
| `<serwer-mcp-A>`, attached and never invoked | 46 152 tokens/call, `inferred` |

Sessions indexed before the parser read the decomposition report as
`unmeasured` rather than as zero. Back-fill them with a forced re-parse:

```bash
curl -X POST "http://localhost:8770/api/v1/admin/sessions/sync?force=true"
```

A scope with no measured call returns `status: "no local sessions"` and no
findings at all — an absence of measurement is never rendered as a clean bill
of health.

### Reproducing the worked example

The benchmark needs three pieces: a fixture with bugs a grader can check, a
grader that imports the result and asserts behaviour, and a runner that copies
the fixture fresh, invokes `auggie` once, then grades and reads `token_usage`
from the session file written by that run. Restrict the session search to files
modified after the run started — otherwise a failed run silently reports the
previous run's numbers.

Vary exactly one thing per run:

```bash
# tool catalog: keep only what the task needs
auggie -p -q --remove-tool web-search --remove-tool sub-agent-code … "$TASK"

# turn cap
auggie -p -q --max-turns 4 "$TASK"

# model
auggie -p -q -m gpt5.6-luna "$TASK"
```

Always pair a cost number with a correctness score. Cost alone ranks "do
nothing" first.

## Related

- [Optimizer playbook](optimizer-playbook.md) — the same findings as a
  step-by-step procedure: which flag, file or frontmatter line achieves each
  saving, in the order worth doing them.
- [CLI training kit](cli-training-kit.md) — the presenter's running order:
  which command to type live, what the audience should see, and which flag
  binds in which execution mode.
- progressive disclosure (mechanizm opisany w [skills docs](https://docs.augmentcode.com/cli/skills)) — the mechanism
  that makes skills cheap.
- konwencje autorskie reguł (patrz [rules docs](https://docs.augmentcode.com/cli/rules)) — rule authoring conventions.
