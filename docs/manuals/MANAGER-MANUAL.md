# Manager Dashboard Manual

> Audience: `Manager` users  
> Scope: operational reporting, KPI validation, event review, funder conversations, and case study evidence

![KPI dashboard annotated guide](images/kpi-dashboard-guide.svg)

## 1. Role overview
Managers have broad operational access across the reporting and delivery views.

Available views:

- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

Managers cannot access:

- `Admin Dashboard`

## 2. Quick start
1. Sign in and change your password if prompted.
2. Use `View Mode` in the sidebar to switch between screens.
3. Check `Last Data Refresh` before relying on figures for external reporting.
4. Start with KPI for summary, then move to reports or ML view when you need detail.

![Navigation and screen areas](images/dashboard-navigation.svg)

## 3. Shared filters and navigation
Across most manager workflows you will use:

- `View Mode`
- region filters
- timeframe filters

Typical timeframes:

- `All Time`
- `Year`
- `Quarter`
- `Month`
- `Week`
- `Custom Range`

Use a wide range first when investigating missing data, then narrow once you know the records are present.

## 4. KPI Dashboard
The KPI screen is the main operational summary view for managers.

### 4.1 KPI sections
Use the section selector to move between:

- `Governance`
- `Partnerships`
- `Delivery`
- `Income` when region is `Global`
- `Comms` when region is `Global`
- `Case Studies`

### 4.2 Drill-down behaviour
Managers can click KPI cards and inspect supporting rows in detail.

In `Delivery > Total Participants`, managers can see:

- attendee names where available
- attendee IDs where available
- placeholder entries when only participant counts exist

This makes the manager role suitable for reconciling participant totals or validating delivery evidence.

### 4.3 KPI Debug
Managers can turn on `Show KPI Debug` from the sidebar.

Debug mode exposes validation counters such as:

- people in region
- volunteers
- steering volunteers
- events in region
- walk events
- participants
- grants in region
- bids submitted

Use it when a headline figure looks wrong and you want to confirm whether the underlying dataset is the issue or the KPI logic is the issue.

## 5. Custom Reports Dashboard
The report builder is the best place for structured analysis and export.

![Custom reports annotated guide](images/custom-reports-guide.svg)

### 5.1 Standard workflow
1. Choose the relevant datasets.
2. Select the output type.
3. Set region and timeframe.
4. Click `Apply Report Filters`.
5. Refine with `Advanced Report Controls` if needed.
6. Click `Apply Advanced Filters`.
7. Export the resulting CSV if required.

### 5.2 Strong use cases for managers
- monthly and quarterly reporting packs
- regional comparisons
- grant and payment reviews
- delivery trend reviews
- evidence packs for leadership or trustees

### 5.3 Distance Analysis
Distance Analysis is especially useful for managers because it reveals reach and travel burden across delivery.

Use it to:

- rank events by average participant travel
- inspect the participant-level journey rows for one event
- export a selected event or the full dataset

If the output is empty, review postcode quality and whether resolved distance filtering is excluding rows.

## 6. ML Dashboard
Managers can use the ML screen for event-level operational detail without needing Admin permissions.

![ML dashboard annotated guide](images/ml-dashboard-guide.svg)

Recommended workflow:

1. Set the region and timeframe.
2. Choose the relevant event.
3. Review the event details panel.
4. Select a participant if attendee data exists.
5. Review personal, medical, and emergency fields carefully.
6. Use the raw event payload only when deeper investigation is needed.

Use this screen when:

- an event record needs checking
- attendee detail needs validating
- support staff ask for confirmation of what Beacon supplied

## 7. Funder Dashboard
Managers can open the `Funder Dashboard` and choose a funder from the selector.

![Funder dashboard annotated guide](images/funder-dashboard-guide.svg)

Use it for:

- sponsor update meetings
- checking funding trends
- reviewing bid totals and funds raised
- quality-assuring what a funder-facing user will see

Important interpretation note:

- funder-related financial measures follow the selected funder
- wider operational figures remain region and timeframe based

## 8. Case Studies
Managers can read, filter, and upload case studies.

This is useful when you need a narrative example to sit alongside KPI or report data.

Suggested use:

- add case studies after notable delivery
- tag the right region and date
- keep titles descriptive so other staff can find them later

## 9. Recommended operating pattern
1. Start in KPI for the headline view.
2. Use `Show KPI Debug` if a number needs validating.
3. Move to Custom Reports for structured analysis or export.
4. Move to ML Dashboard when the question is event-specific.
5. Use Funder Dashboard for sponsor-facing summaries.

## 10. Troubleshooting
### A KPI number looks wrong
- switch on `Show KPI Debug`
- narrow the timeframe
- drill into the KPI card to inspect the source rows

### The report did not refresh
- click `Apply Report Filters`
- click `Apply Advanced Filters` if advanced controls changed

### No attendee detail is visible
- some events only contain counts or partial attendee detail
- names and IDs depend on the source Beacon payload

### The Funder Dashboard looks empty
- try `All Time`
- change the selected funder
- confirm the selected funder appears in grants or payments
