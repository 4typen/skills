---
name: monte-carlo-forecasting
description: Probabilistic delivery forecasts (P50/P85/P95) from historical throughput and cycle time via Monte Carlo simulation, for Scrum (sprints) and Kanban (continuous flow). Use whenever someone asks when an epic, feature, release, or backlog will be done, how many items fit until a date, the probability of hitting a deadline, how long a single ticket takes (SLE, aging items), or wants to replace story points/velocity with data-driven forecasts, even without saying "Monte Carlo" (e.g. "wann ist das Epic fertig?", "was schaffen wir bis zum Release?", "Prognose ohne Sprints", "Roadmap realistisch?").
metadata:
  author: "André Schubert"
  date: "2026-10-15"
  updated: "2026-10-15"
---

# Monte Carlo forecasting

Answer "when?" and "how many?" questions with a **probability distribution**, never a single date. The method: resample the team's real historical **throughput** (finished items per period) thousands of times and read percentiles off the simulated outcomes. Item counts replace story points: you forecast from what the delivery system actually finished, not from estimates fed back into a prediction.

The method does not depend on the process. A **period** is only a sampling bucket. In Scrum it is a sprint. In Kanban it is a workday or a week. Kanban adds one forecast that Scrum rarely uses: **cycle time** per item, which drives the SLE and the treatment of aging items.

The simulation lives in `scripts/mc_forecast.py` (Python 3, stdlib only). Always run it rather than computing by hand: percentile direction differs per mode and is easy to invert.

## Steps

### 1. Pin the question and the cadence

Map the request to a mode:

| Question | Mode | Fixed | Forecast |
|---|---|---|---|
| "When is epic X done?" | `when` | remaining items | periods / date |
| "What do we get done by the release?" | `how-many` | horizon / end date | items (at least) |
| "When will each roadmap epic land?" | `roadmap` | ordered epics | date per epic |
| "Will we make the deadline?" | `when --target-date` / `how-many --target-items` | both | probability |
| "How long does a ticket take? Is this one stuck?" | `cycle-time` | finished items' start/end | single-item percentiles, SLE |

Then determine the team's **cadence**. It sets the period and the history window:

| | Scrum | Kanban | Transition (Scrum → Kanban) |
|---|---|---|---|
| Period | sprint: `--period-days 14 --period-label sprints` | workday: `--workdays-only` (+ `--holidays`); week (`--period-days 7`) if items close in batches | week: `--period-days 7` |
| History window | last 8–20 sprints | last 40–90 workdays / 8–20 weeks | see *Transition* below |
| `--start-date` | first day of the next sprint | today | today |
| Result reads as | "within N sprints" (= sprint end date) | calendar date | calendar date |
| Extras | — | `cycle-time` SLE, aging items, `--parallel` = epic WIP limit | re-forecast weekly |

Ask only if mode or cadence is truly unclear. Done when you know the mode, cadence, scope (item count or ordered epics), and the horizon or target, if one exists.

### 2. Get flow history

Prefer an **export of completion dates**, plus start dates when you need cycle times, over per-sprint counts. Dates do not depend on cadence: the same data works for sprints, weeks, and workdays. They also survive a process change. Sources, in order:

1. Data the user provided.
2. The issue tracker through whatever access exists (CLI, MCP, API). Per-tracker queries: [`references/data-sources.md`](references/data-sources.md).
3. Ask for per-sprint/week counts as a last resort.

Rules that keep the history representative:

- **Same unit on both sides.** Count the same item types (e.g. stories and bugs, not sub-tasks) in the history and in the remaining scope.
- **Include zero periods.** `--dates-file` creates them automatically; a hand-written list must include them.
- **Daily sampling needs continuous closing.** If items pile up on sprint-end days, the script warns about batch closing. Switch to weekly or sprint periods.
- **Cut history from before team or process changes** with `--history-from` or `--last N`.

**Transition (Scrum → Kanban):** Old sprint-era data shows batch closing and sprint-shaped flow.

- With **≥ 6 weeks** of Kanban data: forecast from the Kanban data only (`--history-from <switch date>`). Use weekly periods until ~40 workdays exist, then workdays.
- With **less**: use the full history at weekly granularity. Check for a trend warning, and state that the forecast still reflects the old process.

Run both variants if the difference matters, and report the gap.

Done when you have ≥ 6 samples (ideally 10+ weeks/sprints or 40+ workdays), the counting rule is stated, and the period is chosen.

### 3. Get remaining scope

Count open items under the epic(s), using the same counting rule. Unrefined epics grow: stories get split and new ones get discovered. Model this with `--split-factor LOW HIGH`, which multiplies scope per trial:

- Fully refined, stable scope: omit it.
- Partially refined: `1.0 1.3`
- Only a rough outline: `1.2 2.0`. Also say clearly that scope is the main uncertainty.

If past epics' initial vs. final item counts are available, derive the range from them and say so. For roadmaps, ask how many epics the team works on at once. That number becomes `--parallel K`: sequential (`1`) is typical for Scrum sprint goals, and Kanban teams often limit epic WIP to 2–3.

Done when every epic has a remaining count, a split decision, and the parallelism is known.

### 4. Run the simulation

```bash
S=<skill-dir>/scripts/mc_forecast.py
# Scrum: 18 stories, 2-week sprints, deadline check
python3 $S when --throughput "7,5,8,4,6,9,5,7,3,8,6,5" --remaining 18 \
  --period-days 14 --period-label sprints --start-date 2025-10-06 --target-date 2025-11-30
# Kanban: completion dates sampled per workday, holidays excluded, from today
python3 $S when --dates-file done.csv --date-column Done --workdays-only --history-from 2025-07-28 \
  --holidays 2025-12-24,2025-12-25,2025-12-26 --remaining 30 --start-date 2025-10-06 --target-date 2025-11-14
# How many by the release (weekly periods work for both cadences)
python3 $S how-many --dates-file done.csv --date-column Done --period-days 7 \
  --start-date 2025-10-06 --until 2025-12-19 --target-items 75
# Roadmap: priority order, 2 epics in progress at a time
python3 $S roadmap --dates-file done.csv --date-column Done --workdays-only --history-from 2025-07-28 --start-date 2025-10-06 \
  --epic "Checkout=12@2025-11-30" --epic "Search=24" --epic "Profile=9" --parallel 2 --split-factor 1.0 1.3
# Kanban single item: SLE + forecast for an item in progress since 2025-09-22
python3 $S cycle-time --items-file done.csv --start-column Started --end-column Done --workdays-only \
  --history-from 2025-07-28 --started 2025-09-22
```

Defaults: 10,000 trials, percentiles 50/70/85/95. Add `--seed` for reproducible reports and `--json` for tool consumption. `-h` on each mode lists all options.

Done when the script ran without errors and you read every `Data warnings` line.

### 5. Report

Write in the user's language. Use this structure:

1. **Headline sentence** at P85, framed as probability:
   - Scrum: *"Based on our last 12 sprints, there is an 85% probability that epic X is done within 4 sprints (by Nov 30)."*
   - Kanban: *"Based on the last 50 workdays, there is an 85% probability that epic X is done by Nov 4."*
   - How-many: *"With 85% probability we finish **at least** 70 items by Dec 19."*
   - Cycle time: *"85% of our items finish within 6 workdays."* That sentence is the SLE.
2. **Percentile table** (P50/P70/P85/P95) with dates.
3. **Target probability**, if a deadline or target exists, plus what would raise it (cut scope, move date, protect throughput, lower WIP).
4. **Assumptions:** cadence and period, history window, counting rule, split factor, epic order and parallelism, holidays.
5. **Caveats:** relay each script warning in plain words and add any listed under Interpretation below that apply.
6. **Next step:** re-forecast continuously. In Scrum, do it after each sprint. In Kanban, do it at least weekly or whenever an item finishes. The forecast updates the way a navigation app updates its arrival time.

Use P85 for commitments. Present P50 explicitly as a coin flip, never as "the estimate". If the naive average looks rosier than P85, show both. The gap is why this method exists. In Kanban, forecasts replace sprint commitments: make clear that the date is a probability, not a promise to fill.

Done when every number in the report traces to script output and every assumption is stated.

## Interpretation

- **Percentile direction differs by mode.** `when`/`roadmap`/`cycle-time`: P85 = done **within** N in 85% of cases (higher percentile → later). `how-many`: P85 = **at least** N items (higher percentile → fewer items). The script handles this; keep the wording correct.
- **Sprint results are sprint-granular.** "Within 4 sprints" means by the end date of sprint 4, even if the work finishes mid-sprint. Kanban workday results have no such rounding.
- **Throughput vs. cycle time:** use throughput simulations for *multiple items* (epics, releases). Use cycle time only for *single items*. Never add up cycle times to forecast an epic: parallel work makes the sum meaningless.
- **Aging items:** an in-progress item older than the SLE needs action (swarm, split, unblock), not a forecast. The `cycle-time` conditional forecast shows how much longer such items usually took.
- **WIP drives cycle time (Little's Law).** If WIP limits change, cycle-time history from before the change is stale; throughput usually changes less.
- **Parallel epics:** `--parallel K` deals finished items round-robin across the first K unfinished epics. If epics are staffed by separate sub-teams, forecast each with its own sub-team's history instead.
- **Right-sizing beats precision.** Item count works when items are sized *roughly* consistently. A long cycle-time tail (script warning) means oversized items, so recommend slicing before relying on the forecast. Kanban teams often check right-sizing against the SLE: if an item cannot plausibly finish within the SLE, split it.
- **Epic-count throughput** ("~5 epics per quarter") is misleading because epic sizes vary widely. Count stories across epics instead.
- **Monte Carlo assumes the future resembles the sampled past.** Name known disruptions (holidays, team changes, process switch, new dependencies). Encode holidays via `--holidays` in workday mode, or shorten the history window instead of silently ignoring the change.

## Going further

To set up continuous, automated forecasting, such as a scheduled job that posts P50/P85/P95 to each epic and flags aging items, see [`references/automation.md`](references/automation.md).
