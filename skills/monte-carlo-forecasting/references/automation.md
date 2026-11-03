# Continuous forecasting (automation)

A forecast decays the moment it is made. Its value comes from **re-forecasting on every new data point**, the way a navigation app updates arrival time. Automate it so nobody has to run the forecast by hand.

```text
tracker (finished items) → throughput history → mc_forecast.py --json → epic comment / dashboard / report
```

## Design choices

- **Trigger:**
  - Kanban: run daily on workdays, or when an item closes.
  - Scrum: run after each sprint ends. A daily run adds noise mid-sprint because of batched closing.
- **Cadence flags:**
  - Kanban: `--workdays-only --holidays <file>`
  - Scrum: `--period-days <sprint length> --period-label sprints --start-date <next sprint start>`
  - Mixed or transition: `--period-days 7`
- **Window:** keep it rolling, e.g. the last 60 workdays, 12 weeks, or 10 sprints, so the forecast tracks the current system. Pin the window in config so the number does not move without a reason. After a process switch, move the window start to the switch date once there is enough data.
- **Aging items (Kanban):** in the same job, run `cycle-time --started <date>` for every in-progress item. Flag items whose age exceeds the SLE. These items are the earliest signal that a forecast will slip.
- **Reproducibility:** pass `--seed` together with a date-derived value, such as `--seed $(date +%Y%m%d)`, so reruns on the same day match.
- **Output:** use `--json`, then render a short block per epic: progress, remaining scope, P50/P70/P85/P95 dates, target probability, and data warnings. Update one comment in place so the thread does not fill with new ones.
- **Trend:** store each run's P85 per epic as CSV or a JSON artifact. A P85 that drifts later week after week is the early warning that matters most.

## Example: GitHub Actions (adapt to the tracker/CI in use)

```yaml
name: forecast
on:
  schedule: [{ cron: "0 6 * * 1-5" }]
  workflow_dispatch:
jobs:
  forecast:
    runs-on: ubuntu-latest
    permissions: { issues: write }
    steps:
      - uses: actions/checkout@v4
      - env: { GH_TOKEN: "${{ github.token }}" }
        run: |
          gh issue list --state closed --limit 1000 --search "closed:>=$(date -d '-120 days' +%F) reason:completed" \
            --json closedAt --jq '.[].closedAt' > closed.csv
          for epic in $(gh issue list --label epic --state open --json number --jq '.[].number'); do
            remaining=$(gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){subIssues(first:100){nodes{state}}}}}' \
              -f o="${GITHUB_REPOSITORY%/*}" -f r="${GITHUB_REPOSITORY#*/}" -F n="$epic" \
              --jq '[.data.repository.issue.subIssues.nodes[]|select(.state=="OPEN")]|length')
            python3 tools/mc_forecast.py when --dates-file closed.csv --period-days 1 --workdays-only \
              --last 60 --remaining "$remaining" --start-date "$(date +%F)" --period-label days \
              --seed "$(date +%Y%m%d)" > "forecast-$epic.txt"
            gh issue comment "$epic" --edit-last --body-file "forecast-$epic.txt" \
              || gh issue comment "$epic" --body-file "forecast-$epic.txt"
          done
```

Copy `scripts/mc_forecast.py` into the target repo, for example to `tools/`, so the pipeline has no dependency on the skill directory.
