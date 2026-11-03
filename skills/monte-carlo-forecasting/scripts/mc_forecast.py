#!/usr/bin/env python3
"""Monte Carlo delivery forecasting from historical flow data (stdlib only).

Works for Scrum (sprint periods) and Kanban (continuous flow: workday/week periods).

Modes
  when        fixed scope  -> how many periods / which date (P50..P95)
  how-many    fixed time   -> how many items at least (P50..P95)
  roadmap     ordered epics sharing one throughput stream (sequential or --parallel K)
  cycle-time  single items -> cycle-time percentiles, SLE, forecast for an in-progress item

Throughput input (when / how-many / roadmap, pick one)
  --throughput "7,5,8,4"          items finished per period, oldest first
  --throughput-file f.csv         one count per row (last integer cell is used)
  --dates-file f.csv              one completion date per row -> bucketed into periods

Run `mc_forecast.py <mode> -h` for all options.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
import random
import statistics
import sys
from collections import Counter

DEFAULT_PERCENTILES = "50,70,85,95"
MAX_PERIODS = 2000
ONE_DAY = dt.timedelta(days=1)
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ---------------------------------------------------------------- dates & calendar


def parse_date(text: str) -> dt.date:
    return dt.date.fromisoformat(text.strip()[:10])


def try_date(text: str) -> dt.date | None:
    try:
        return parse_date(text)
    except ValueError:
        return None


def daterange(start: dt.date, end: dt.date):
    for i in range((end - start).days + 1):
        yield start + dt.timedelta(days=i)


def parse_holidays(spec: str | None) -> set[dt.date]:
    if not spec:
        return set()
    if os.path.exists(spec):
        with open(spec, encoding="utf-8-sig") as fh:
            cells = [c for row in csv.reader(fh) for c in row]
    else:
        cells = spec.split(",")
    return {d for c in cells if (d := try_date(c))}


class Calendar:
    """Period arithmetic. Workday mode = 1 period per working day (skips weekends + holidays)."""

    def __init__(self, period_days: int | None, workdays_only: bool, holidays: set[dt.date]):
        if workdays_only and period_days not in (None, 1):
            sys.exit("error: --workdays-only means daily periods; use --period-days 1 or omit it")
        if holidays and not workdays_only:
            sys.exit("error: --holidays needs --workdays-only")
        self.period_days = 1 if workdays_only else period_days
        self.workdays_only = workdays_only
        self.holidays = holidays

    def is_workday(self, d: dt.date) -> bool:
        return d.weekday() < 5 and d not in self.holidays

    def period_end(self, start: dt.date, n: int) -> dt.date:
        """Last calendar day of the n-th period (n >= 1); start is day 1 of period 1."""
        if n <= 0:
            return start - ONE_DAY
        if not self.workdays_only:
            return start + dt.timedelta(days=n * (self.period_days or 1) - 1)
        day, counted = start, 0
        while True:
            if self.is_workday(day):
                counted += 1
                if counted == n:
                    return day
            day += ONE_DAY

    def periods_until(self, start: dt.date, until: dt.date) -> int:
        """Complete periods from start through until (inclusive)."""
        if until < start:
            return 0
        if self.workdays_only:
            return sum(1 for d in daterange(start, until) if self.is_workday(d))
        return ((until - start).days + 1) // (self.period_days or 1)

    def span_days(self, start: dt.date, end: dt.date) -> int:
        """Cycle time in days, start and end inclusive (same-day item = 1)."""
        if self.workdays_only:
            return max(1, sum(1 for d in daterange(start, end) if self.is_workday(d)))
        return (end - start).days + 1

    def day_end(self, start: dt.date, days: int) -> dt.date:
        """Date on which a span of `days` (inclusive, see span_days) that began on start ends."""
        if not self.workdays_only:
            return start + dt.timedelta(days=days - 1)
        day, counted = start, 0
        while True:
            if self.is_workday(day):
                counted += 1
                if counted == days:
                    return day
            day += ONE_DAY

    def default_label(self) -> str:
        if self.workdays_only:
            return "workdays"
        return {1: "days", 7: "weeks"}.get(self.period_days or 0, "periods")


# ---------------------------------------------------------------- input


def read_counts(path: str) -> list[int]:
    counts: list[int] = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.reader(fh):
            ints = [c.strip() for c in row if c.strip().lstrip("-").isdigit()]
            if ints:
                counts.append(int(ints[-1]))
    return counts


def read_dates(path: str, column: str | None) -> list[dt.date]:
    dates: list[dt.date] = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        if column:
            for row in csv.DictReader(fh):
                if (value := (row.get(column) or "").strip()) and (d := try_date(value)):
                    dates.append(d)
        else:
            for row in csv.reader(fh):
                for cell in row:
                    if d := try_date(cell):
                        dates.append(d)
                        break
    return dates


def bucket_dates(dates, cal: Calendar, start, end) -> tuple[list[int], list[str]]:
    """Count completions per period, oldest first. Empty periods count as 0."""
    if not dates:
        sys.exit("error: no parseable dates in --dates-file")
    start = start or min(dates)
    end = end or max(dates)
    window = [d for d in dates if start <= d <= end]
    warns = batch_warnings(window, cal)
    if cal.workdays_only:
        days = [d for d in daterange(start, end) if cal.is_workday(d)]
        counts = dict.fromkeys(days, 0)
        for d in window:
            while not cal.is_workday(d) and d > start:  # weekend/holiday -> previous workday
                d -= ONE_DAY
            if d in counts:
                counts[d] += 1
        return [counts[d] for d in days], warns
    n_buckets = ((end - start).days + 1) // cal.period_days
    if n_buckets < 1:
        sys.exit("error: history window is shorter than one period")
    counts = [0] * n_buckets
    first = end - dt.timedelta(days=n_buckets * cal.period_days - 1)  # drop partial oldest bucket
    for d in window:
        if d >= first:
            counts[(d - first).days // cal.period_days] += 1
    return counts, warns


def batch_warnings(dates: list[dt.date], cal: Calendar) -> list[str]:
    """Detect sprint-end / batch closing, which breaks daily sampling."""
    warns = []
    if cal.period_days == 1 and not cal.workdays_only:
        warns.append("calendar-day periods include weekends as zero days - use --workdays-only for daily sampling")
    if cal.period_days == 1 and len(dates) >= 30:
        day, count = Counter(d.weekday() for d in dates).most_common(1)[0]
        share = count / len(dates)
        if share > 0.4:
            warns.append(
                f"{share:.0%} of completions fall on a {WEEKDAYS[day]} - looks like sprint-end/batch closing; "
                "daily sampling overstates variance, use --period-days 7 (or the sprint length) instead"
            )
    return warns


def load_samples(args, cal: Calendar) -> tuple[list[int], list[str]]:
    extra: list[str] = []
    if args.throughput:
        raw = args.throughput.replace(";", ",").replace(" ", ",")
        samples = [int(x) for x in raw.split(",") if x]
    elif args.throughput_file:
        samples = read_counts(args.throughput_file)
    elif args.dates_file:
        if not cal.period_days:
            sys.exit("error: --dates-file needs a period: --workdays-only (Kanban), --period-days 7, or the sprint length")
        samples, extra = bucket_dates(
            read_dates(args.dates_file, args.date_column),
            cal,
            parse_date(args.history_from) if args.history_from else None,
            parse_date(args.history_to) if args.history_to else None,
        )
    else:
        sys.exit("error: provide --throughput, --throughput-file or --dates-file")
    if args.last:
        samples = samples[-args.last :]
    if not samples:
        sys.exit("error: no throughput samples")
    if any(s < 0 for s in samples):
        sys.exit("error: throughput samples must be >= 0")
    if sum(samples) == 0:
        sys.exit("error: all throughput samples are 0 - nothing to forecast from")
    return samples, extra


# ---------------------------------------------------------------- statistics


def when_percentile(sorted_vals: list[int], p: float) -> int:
    """Smallest value v with P(X <= v) >= p  (duration: lower is better)."""
    idx = max(0, math.ceil(p / 100 * len(sorted_vals)) - 1)
    return sorted_vals[idx]


def howmany_percentile(sorted_vals: list[int], p: float) -> int:
    """Largest value v with P(X >= v) >= p  (output: higher is better)."""
    idx = min(len(sorted_vals) - 1, int(math.floor((1 - p / 100) * len(sorted_vals))))
    return sorted_vals[idx]


def data_warnings(samples: list[int], cal: Calendar) -> list[str]:
    warns = []
    n = len(samples)
    mean = statistics.mean(samples)
    daily = cal.period_days == 1
    if n < 6:
        warns.append(f"only {n} samples - forecast is fragile; aim for 8-20 sprints/weeks or 40-90 workdays")
    if n > (130 if daily else 30):
        warns.append(f"{n} samples - old history may no longer represent the current system; consider --last")
    zeros = samples.count(0) / n
    if zeros > (0.6 if daily else 0.3):
        warns.append(f"{zeros:.0%} of periods have 0 items - items too big, batched closing, or period too short")
    if n >= 2 and mean > 0 and not daily:
        cv = statistics.pstdev(samples) / mean
        if cv > 0.75:
            warns.append(f"high variability (CV {cv:.2f}) - check item sizing and status hygiene (bulk closing)")
    if n >= 8:
        half = n // 2
        old, new = statistics.mean(samples[:half]), statistics.mean(samples[half:])
        if old > 0 and abs(new - old) / old > 0.3:
            direction = "up" if new > old else "down"
            warns.append(
                f"throughput trends {direction} (first half avg {old:.1f}, second half {new:.1f}) "
                "- system may have changed (e.g. Scrum→Kanban switch); consider a shorter recent window"
            )
    return warns


# ---------------------------------------------------------------- simulations


def scoped(rng: random.Random, remaining: int, split) -> int:
    return math.ceil(remaining * rng.uniform(*split)) if split else remaining


def sim_when(samples, remaining, trials, rng, split):
    out = []
    for _ in range(trials):
        need, done, n = scoped(rng, remaining, split), 0, 0
        while done < need and n < MAX_PERIODS:
            done += rng.choice(samples)
            n += 1
        out.append(n)
    return out


def sim_howmany(samples, periods, trials, rng):
    return [sum(rng.choice(samples) for _ in range(periods)) for _ in range(trials)]


def sim_roadmap(samples, epics, trials, rng, split, parallel):
    """Epics in priority order share one throughput stream.

    Up to `parallel` epics are active at once; finished items are dealt round-robin to the
    active epics. parallel=1 is strictly sequential.
    """
    per_epic = [[] for _ in epics]
    for _ in range(trials):
        need = [scoped(rng, rem, split) for _, rem in epics]
        done = [0] * len(epics)
        finished = [False] * len(epics)
        for i, n_i in enumerate(need):
            if n_i <= 0:
                finished[i] = True
                per_epic[i].append(0)
        n, rr = 0, 0
        while not all(finished) and n < MAX_PERIODS:
            n += 1
            for _ in range(rng.choice(samples)):
                active = [i for i in range(len(epics)) if not finished[i]][:parallel]
                if not active:
                    break
                i = active[rr % len(active)]
                rr += 1
                done[i] += 1
                if done[i] >= need[i]:
                    finished[i] = True
                    per_epic[i].append(n)
        for i in range(len(epics)):
            if not finished[i]:
                per_epic[i].append(MAX_PERIODS)
    return per_epic


# ---------------------------------------------------------------- output


def bar(fraction: float, width: int = 20) -> str:
    filled = round(fraction * width)
    return "█" * filled + "░" * (width - filled)


def histogram(results: list[int], label: str, cumulative_le: bool) -> list[str]:
    counts = Counter(results)
    total = len(results)
    keys = sorted(counts)
    peak = max(counts.values())
    rows, running = [], 0
    for k in keys if cumulative_le else reversed(keys):
        running += counts[k]
        rows.append((k, counts[k], running / total))
    if not cumulative_le:
        rows.reverse()
    rows = [r for r in rows if r[1] / total >= 0.002] or rows  # trim negligible tails
    if len(rows) > 40:  # bucket very wide distributions for readability
        rows = rows[:: math.ceil(len(rows) / 40)]
    sym = "≤" if cumulative_le else "≥"
    return [f"  {k:>5} {label:<8} {'▇' * max(1, round(c / peak * 30)):<30} {sym}{k}: {cum:6.1%}" for k, c, cum in rows]


def date_of(n: int, args) -> str | None:
    if args.start_date and n < MAX_PERIODS and args.cal.period_days:
        return args.cal.period_end(args.start_date, n).isoformat()
    return None


def fmt_period(n: int, args) -> str:
    if n >= MAX_PERIODS:
        return "not finished"
    d = date_of(n, args)
    return f"{n} {args.period_label}" + (f" ({d})" if d else "")


def common_header(samples, args) -> list[str]:
    shown = str(samples) if len(samples) <= 26 else f"[… {', '.join(map(str, samples[-25:]))}]"
    cal = args.cal
    cadence = "workdays (weekends" + (" + holidays" if cal.holidays else "") + " skipped)" if cal.workdays_only else args.period_label
    return [
        f"History: {len(samples)} {cadence}, oldest→newest {shown}",
        f"         mean {statistics.mean(samples):.2f}, median {statistics.median(samples)}, min {min(samples)}, max {max(samples)}",
        f"Trials:  {args.trials}" + (f", seed {args.seed}" if args.seed is not None else ""),
    ]


def target_to_periods(target: str, args) -> int:
    if target.isdigit():
        return int(target)
    if not (args.start_date and args.cal.period_days):
        sys.exit("error: date targets need --start-date and a period (--period-days or --workdays-only)")
    return args.cal.periods_until(args.start_date, parse_date(target))


def run_when(args, samples, rng, pcts):
    split = tuple(args.split_factor) if args.split_factor else None
    res = sim_when(samples, args.remaining, args.trials, rng, split)
    s = sorted(res)
    table = {p: when_percentile(s, p) for p in pcts}
    unfinished = sum(1 for r in res if r >= MAX_PERIODS) / len(res)
    target_periods = args.target_periods
    if args.target_date:
        target_periods = target_to_periods(args.target_date, args)
    p_target = sum(1 for r in res if r <= target_periods) / len(res) if target_periods is not None else None
    naive = args.remaining / statistics.mean(samples)
    out = {
        "mode": "when",
        "samples": samples,
        "remaining": args.remaining,
        "split_factor": split,
        "percentiles": {f"P{p:g}": {"periods": v, "date": date_of(v, args)} for p, v in table.items()},
        "naive_average_periods": round(naive, 2),
        "target_periods": target_periods,
        "probability_target": p_target,
        "unfinished_share": unfinished,
    }
    lines = common_header(samples, args)
    lines.append(f"Scope:   {args.remaining} remaining items" + (f", split factor {split[0]}–{split[1]}" if split else ""))
    lines += ["", "Confidence   Done within"]
    lines += [f"  P{p:<9g} {fmt_period(v, args)}" for p, v in table.items()]
    lines.append(f"\nNaive average (for contrast): {naive:.1f} {args.period_label} – hides the spread")
    if p_target is not None:
        by = f" (by {args.target_date})" if args.target_date else ""
        lines.append(f"Probability to finish within {target_periods} {args.period_label}{by}: {bar(p_target)} {p_target:.0%}")
    if unfinished:
        lines.append(f"! {unfinished:.1%} of trials did not finish within {MAX_PERIODS} periods")
    lines += ["", "Distribution (cumulative = probability of being done by then):"]
    lines += histogram(res, args.period_label, cumulative_le=True)
    return out, lines


def run_howmany(args, samples, rng, pcts):
    periods = args.periods
    if args.until:
        periods = target_to_periods(args.until, args)
    if not periods:
        sys.exit("error: provide --periods N or --until DATE (>= 1 period)")
    res = sim_howmany(samples, periods, args.trials, rng)
    s = sorted(res)
    table = {p: howmany_percentile(s, p) for p in pcts}
    p_target = sum(1 for r in res if r >= args.target_items) / len(res) if args.target_items is not None else None
    naive = statistics.mean(samples) * periods
    out = {
        "mode": "how-many",
        "samples": samples,
        "periods": periods,
        "horizon_end": date_of(periods, args),
        "percentiles": {f"P{p:g}": v for p, v in table.items()},
        "naive_average_items": round(naive, 1),
        "target_items": args.target_items,
        "probability_target": p_target,
    }
    lines = common_header(samples, args)
    horizon = f"{periods} {args.period_label}"
    if args.start_date and args.cal.period_days:
        horizon += f" ({args.start_date} → {date_of(periods, args)})"
    lines.append(f"Horizon: {horizon}")
    lines += ["", "Confidence   At least"]
    lines += [f"  P{p:<9g} {v} items" for p, v in table.items()]
    lines.append(f"\nNaive average (for contrast): {naive:.1f} items")
    if p_target is not None:
        lines.append(f"Probability to finish ≥ {args.target_items} items: {bar(p_target)} {p_target:.0%}")
    lines += ["", "Distribution (cumulative = probability of at least that many):"]
    lines += histogram(res, "items", cumulative_le=False)
    return out, lines


def parse_epic(spec: str) -> tuple[str, int, str | None]:
    """NAME=REMAINING[@TARGET]  e.g. 'Checkout=12@2025-11-14' or 'B=8@6' (6 periods)."""
    if "=" not in spec:
        sys.exit(f"error: bad --epic '{spec}', expected NAME=REMAINING[@TARGET]")
    name, rest = spec.rsplit("=", 1)
    target = None
    if "@" in rest:
        rest, target = rest.split("@", 1)
    return name.strip(), int(rest), target


def run_roadmap(args, samples, rng, pcts):
    specs = [parse_epic(e) for e in args.epic]
    split = tuple(args.split_factor) if args.split_factor else None
    per_epic = sim_roadmap(samples, [(n, r) for n, r, _ in specs], args.trials, rng, split, args.parallel)
    epics_out = []
    for (name, rem, target), res in zip(specs, per_epic):
        s = sorted(res)
        tp = target_to_periods(target, args) if target else None
        epics_out.append(
            {
                "name": name,
                "remaining": rem,
                "percentiles": {f"P{p:g}": {"periods": when_percentile(s, p), "date": date_of(when_percentile(s, p), args)} for p in pcts},
                "target": target,
                "target_periods": tp,
                "probability_target": (sum(1 for r in res if r <= tp) / len(res)) if tp is not None else None,
            }
        )
    out = {"mode": "roadmap", "samples": samples, "split_factor": split, "parallel": args.parallel, "epics": epics_out}
    lines = common_header(samples, args)
    order = "sequential" if args.parallel == 1 else f"up to {args.parallel} epics in parallel (epic WIP limit), items dealt round-robin"
    lines.append(f"Order:   {order}; priority as given; one shared throughput stream")
    if split:
        lines.append(f"Split:   factor {split[0]}–{split[1]} per epic")
    lines.append("")
    lines.append(f"  {'Epic':<24}{'Rem':>5}  " + "  ".join(f"{'P%g' % p:<24}" for p in pcts))
    for e in epics_out:
        cells = "  ".join(f"{fmt_period(v['periods'], args):<24}" for v in e["percentiles"].values())
        lines.append(f"  {e['name'][:23]:<24}{e['remaining']:>5}  {cells}")
    for e in epics_out:
        if e["probability_target"] is not None:
            lines.append(f"  {e['name']}: P(done by {e['target']}) {bar(e['probability_target'])} {e['probability_target']:.0%}")
    return out, lines


# ---------------------------------------------------------------- cycle time (Kanban SLE)


def load_cycle_times(args, cal: Calendar) -> list[int]:
    if args.cycle_times:
        cts = [int(x) for x in args.cycle_times.replace(";", ",").replace(" ", ",").split(",") if x]
    elif args.items_file:
        if not (args.start_column and args.end_column):
            sys.exit("error: --items-file needs --start-column and --end-column")
        lo = parse_date(args.history_from) if args.history_from else None
        hi = parse_date(args.history_to) if args.history_to else None
        rows = []
        with open(args.items_file, newline="", encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                s, e = try_date(row.get(args.start_column) or ""), try_date(row.get(args.end_column) or "")
                if s and e and e >= s and (not lo or e >= lo) and (not hi or e <= hi):
                    rows.append((e, cal.span_days(s, e)))
        cts = [ct for _, ct in sorted(rows)]
    else:
        sys.exit("error: provide --cycle-times or --items-file")
    if args.last:
        cts = cts[-args.last :]
    if not cts or any(c < 1 for c in cts):
        sys.exit("error: need cycle times >= 1 day")
    return cts


def run_cycle_time(args, pcts):
    cal = args.cal
    unit = "workdays" if cal.workdays_only else "days"
    cts = load_cycle_times(args, cal)
    s = sorted(cts)
    table = {p: when_percentile(s, p) for p in pcts}
    sle = when_percentile(s, args.sle_percentile)
    warns = []
    if len(cts) < 20:
        warns.append(f"only {len(cts)} finished items - percentiles are rough; aim for 30+")
    if s[-1] > 4 * table.get(50.0, s[len(s) // 2]):
        warns.append(f"long tail (max {s[-1]} vs. median {s[len(s) // 2]} {unit}) - check for oversized or blocked items")

    age = args.age
    if args.started:
        age = cal.span_days(parse_date(args.started), args.today)
    item = None
    if age is not None:
        survivors = sorted(c for c in cts if c >= age)
        if survivors:
            cond = {p: when_percentile(survivors, p) for p in pcts}
            item = {
                "age": age,
                "comparable_items": len(survivors),
                "percentiles": {
                    f"P{p:g}": {
                        "total_cycle_time": v,
                        "remaining": v - age,
                        "date": cal.day_end(parse_date(args.started), v).isoformat() if args.started else None,
                    }
                    for p, v in cond.items()
                },
                "beyond_sle": age > sle,
            }
        else:
            item = {"age": age, "comparable_items": 0, "beyond_history": True}

    out = {"mode": "cycle-time", "unit": unit, "items": len(cts), "percentiles": {f"P{p:g}": v for p, v in table.items()},
           "sle": {"percentile": args.sle_percentile, "days": sle}, "in_progress_item": item, "warnings": warns}
    lines = [
        f"History: {len(cts)} finished items, cycle time in {unit} (start and end day inclusive)",
        f"         median {statistics.median(cts)}, mean {statistics.mean(cts):.1f}, min {s[0]}, max {s[-1]}",
        "",
        "Confidence   Single item finishes within",
    ]
    lines += [f"  P{p:<9g} {v} {unit}" for p, v in table.items()]
    lines.append(f"\nSLE proposal: {args.sle_percentile:g}% of items finish within {sle} {unit}")
    if item:
        lines.append("")
        if item.get("beyond_history"):
            lines.append(f"In-progress item, age {age} {unit}: older than every finished item in history - act now (swarm, split, unblock)")
        else:
            lines.append(f"In-progress item, age {age} {unit} (conditional on {item['comparable_items']} items that reached this age):")
            for k, v in item["percentiles"].items():
                when = f" → {v['date']}" if v["date"] else ""
                lines.append(f"  {k:<10} total {v['total_cycle_time']} {unit}, {v['remaining']} more{when}")
            if item["comparable_items"] < 10:
                lines.append(f"  ! only {item['comparable_items']} historical items ever got this old - treat as rough signal")
            if item["beyond_sle"]:
                lines.append(f"  ! already beyond the SLE of {sle} {unit} - aging item, act now")
    lines += ["", "Distribution (cumulative = share of items done within):"]
    lines += histogram(cts, unit, cumulative_le=True)
    return out, lines, warns


# ---------------------------------------------------------------- cli


def calendar_parent() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(add_help=False)
    c = p.add_argument_group("calendar / cadence")
    c.add_argument("--period-days", type=int, help="calendar days per period: sprint length (Scrum) or 7 (weekly)")
    c.add_argument("--workdays-only", action="store_true", help="Kanban daily flow: 1 period = 1 working day (skips Sat/Sun)")
    c.add_argument("--holidays", help="non-working dates (comma list or CSV file); needs --workdays-only")
    c.add_argument("--start-date", type=parse_date, help="first day of the first forecast period (enables dates)")
    c.add_argument("--period-label", help='display name, e.g. "sprints" (default derived from cadence)')
    o = p.add_argument_group("output")
    o.add_argument("--percentiles", default=DEFAULT_PERCENTILES)
    o.add_argument("--json", action="store_true", help="machine-readable output")
    return p


def build_parser() -> argparse.ArgumentParser:
    cal = calendar_parent()
    flow = argparse.ArgumentParser(add_help=False)
    g = flow.add_argument_group("throughput history")
    g.add_argument("--throughput", help='items per period, oldest first, e.g. "7,5,8,4"')
    g.add_argument("--throughput-file", help="CSV/text, one period per row; last integer cell is the count")
    g.add_argument("--dates-file", help="CSV/text with one completion date (ISO) per row")
    g.add_argument("--date-column", help="header name of the date column in --dates-file")
    g.add_argument("--history-from", help="first day of history window (dates-file)")
    g.add_argument("--history-to", help="last day of history window (dates-file); default: latest date")
    g.add_argument("--last", type=int, help="use only the most recent N samples")
    s = flow.add_argument_group("simulation")
    s.add_argument("--trials", type=int, default=10000)
    s.add_argument("--seed", type=int, help="fix RNG for reproducible output")

    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="mode", required=True)

    w = sub.add_parser("when", parents=[flow, cal], help="fixed scope -> completion period/date")
    w.add_argument("--remaining", type=int, required=True, help="remaining items")
    w.add_argument("--split-factor", type=float, nargs=2, metavar=("LOW", "HIGH"), help="scope growth multiplier range, e.g. 1.0 1.3")
    w.add_argument("--target-periods", type=int, help="probability of finishing within N periods")
    w.add_argument("--target-date", help="probability of finishing by DATE (needs --start-date)")

    h = sub.add_parser("how-many", parents=[flow, cal], help="fixed time -> items done")
    h.add_argument("--periods", type=int, help="forecast horizon in periods")
    h.add_argument("--until", help="horizon end date (needs --start-date)")
    h.add_argument("--target-items", type=int, help="probability of finishing at least N items")

    r = sub.add_parser("roadmap", parents=[flow, cal], help="ordered epics -> completion per epic")
    r.add_argument("--epic", action="append", required=True, help="NAME=REMAINING[@TARGET_DATE|@TARGET_PERIODS], repeat in priority order")
    r.add_argument("--split-factor", type=float, nargs=2, metavar=("LOW", "HIGH"))
    r.add_argument("--parallel", type=int, default=1, help="max epics in progress at once (epic WIP limit); 1 = sequential")

    c = sub.add_parser("cycle-time", parents=[cal], help="single-item cycle-time percentiles, SLE, in-progress item forecast")
    c.add_argument("--cycle-times", help='cycle times in days, e.g. "1,3,2,8"')
    c.add_argument("--items-file", help="CSV with a start and an end date column per finished item")
    c.add_argument("--start-column", help="header of the start (e.g. first 'In Progress') date column")
    c.add_argument("--end-column", help="header of the done date column")
    c.add_argument("--history-from", help="only items finished on/after this date")
    c.add_argument("--history-to", help="only items finished on/before this date")
    c.add_argument("--last", type=int, help="only the N most recently finished items")
    c.add_argument("--sle-percentile", type=float, default=85.0)
    c.add_argument("--age", type=int, help="age of an in-progress item in days (same unit as cycle time)")
    c.add_argument("--started", help="start date of an in-progress item (alternative to --age; enables dates)")
    c.add_argument("--today", type=parse_date, default=dt.date.today(), help="reference date for --started (default: today)")
    return p


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    args.cal = Calendar(args.period_days, args.workdays_only, parse_holidays(args.holidays))
    args.period_label = args.period_label or args.cal.default_label()
    pcts = [float(x) for x in args.percentiles.split(",")]

    if args.mode == "cycle-time":
        out, lines, warns = run_cycle_time(args, pcts)
    else:
        if args.trials < 100:
            sys.exit("error: use at least 100 trials (10000 recommended)")
        if getattr(args, "split_factor", None) and not (0 < args.split_factor[0] <= args.split_factor[1]):
            sys.exit("error: --split-factor LOW HIGH needs 0 < LOW <= HIGH")
        if getattr(args, "parallel", 1) < 1:
            sys.exit("error: --parallel must be >= 1")
        samples, extra = load_samples(args, args.cal)
        runner = {"when": run_when, "how-many": run_howmany, "roadmap": run_roadmap}[args.mode]
        out, lines = runner(args, samples, random.Random(args.seed), pcts)
        warns = extra + data_warnings(samples, args.cal)
        out["warnings"] = warns

    if args.json:
        print(json.dumps(out, indent=2, default=str))
        return
    print("\n".join(lines))
    if warns:
        print("\nData warnings:")
        print("\n".join(f"  ! {w}" for w in warns))


if __name__ == "__main__":
    main()
