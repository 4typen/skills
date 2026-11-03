# Data sources for throughput, cycle time, and remaining scope

Goal: one CSV row per finished item, with a **done date** and, for Kanban cycle time, a **start date**. That one file feeds every mode:

- `--dates-file F --date-column Done` for throughput (`when`, `how-many`, `roadmap`)
- `--items-file F --start-column Started --end-column Done` for `cycle-time`

For remaining scope, you need **one count of open items** per epic. Use whatever access the session has: CLI, MCP server, REST API, or a user export. The snippets below are starting points. Check field names against the actual instance.

Universal rules:

- Done date = when the item reached the team's *Done* state, such as resolved, closed as completed, or merged to main. Exclude won't-fix, duplicate, and invalid items.
- Start date = first transition into an *in-progress* state (commitment point), not the creation date. Backlog wait time is not cycle time.
- Apply the same type filter to history and remaining scope.
- Pull 1.5× the intended window so `--history-from` can cut cleanly. For a Scrum→Kanban switch, note the switch date.

Start-date sources per tracker:

| Tracker | Start date |
|---|---|
| Jira | changelog: first `status` change into the *In Progress* category (`expand=changelog`) |
| Azure DevOps | `Microsoft.VSTS.Common.ActivatedDate` |
| Linear | `startedAt` |
| GitHub | no native field: use the first linked PR's `createdAt` or the first `assigned` timeline event as a proxy (Projects status history is not reliably exposed via API) |
| GitLab | first linked MR's `created_at`, or the `workflow::in progress` label event (`resource_label_events`) |

## GitHub Issues

```bash
# history: completed issues since a date (issue types: add `type:Story` if the org uses them)
gh issue list --repo OWNER/REPO --state closed --limit 1000 \
  --search "closed:>=2025-06-01 reason:completed -label:duplicate" \
  --json number,closedAt --jq '.[] | [.number, .closedAt] | @csv' > closed.csv
# → mc_forecast.py ... --dates-file closed.csv   (date is the 2nd cell; auto-detected)

# remaining: open sub-issues of an epic issue
gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){
  subIssues(first:100){nodes{number state}}}}}' -f o=OWNER -f r=REPO -F n=EPIC_NUMBER \
  --jq '[.data.repository.issue.subIssues.nodes[] | select(.state=="OPEN")] | length'
```

If epics are modeled as labels or milestones instead, use `gh issue list --state open --label epic:X --json number --jq length`.
For PR-based flow, use `gh pr list --state merged --search "merged:>=DATE" --json mergedAt`.

## Jira

```text
History JQL:   project = ABC AND issuetype in (Story, Bug) AND statusCategory = Done
               AND resolution not in (Duplicate, "Won't Do") AND resolutiondate >= -180d
Remaining JQL: parent = ABC-123 AND statusCategory != Done
               (older company-managed setups: "Epic Link" = ABC-123)
```

REST (Cloud): `GET /rest/api/3/search/jql?jql=<urlencoded>&fields=resolutiondate&maxResults=100`. Page with `nextPageToken`. Write `key,resolutiondate` to CSV. If the instance has no resolution field set, use the status-change date to Done from the changelog.

## Azure DevOps

```bash
az boards query --wiql "SELECT [System.Id],[Microsoft.VSTS.Common.ClosedDate] FROM WorkItems \
  WHERE [System.TeamProject]=@project AND [System.WorkItemType] IN ('User Story','Bug') \
  AND [System.State] IN ('Closed','Done') AND [Microsoft.VSTS.Common.ClosedDate] >= @Today-180" -o json \
  | jq -r '.[] | [.id, .fields["Microsoft.VSTS.Common.ClosedDate"]] | @csv' > closed.csv
```

For remaining scope, query child links of the epic/feature with state not in Closed/Done/Removed.

## GitLab

```bash
glab issue list --closed --per-page 100 -O json | jq -r '.[] | [.iid, .closed_at] | @csv' > closed.csv
```

Epics (Premium): `glab api groups/GROUP/epics/EPIC_IID/issues` → count `state=="opened"`.

## Linear

GraphQL: `issues(filter:{completedAt:{gte:"2025-06-01"}, team:{key:{eq:"ABC"}}}) { nodes { identifier completedAt } }`.
For remaining scope, query issues of a project with `state.type` not `completed`/`canceled`.

## Spreadsheet or manual data

- Per-period counts (e.g. sprint history): CSV with one row per sprint/week, count in the last column → `--throughput-file`.
- Completion dates: any CSV with an ISO date column → `--dates-file --date-column <name>`.
- Start/done pairs → `--items-file --start-column <a> --end-column <b>`, or plain cycle times via `--cycle-times "3,5,2"`.
- Inline: `--throughput "7,5,8,0,6"` (oldest first, zeros included).
