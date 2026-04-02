# Manager Dashboard Manual

## 1. Purpose
This manual is for `Manager` users.

Managers have broad operational access and can use:
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

Managers cannot use:
- `Admin Dashboard`

## 2. Signing In
1. Open the dashboard.
2. Enter your email address and password.
3. Change your password if prompted.

If access fails, contact an Admin.

## 3. Main Views
Use `View Mode` in the left sidebar.

Manager views:
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

## 4. Shared Filters
Across the dashboard you will commonly use:
- region filters
- timeframe filters

Timeframe options vary slightly by page, but generally include:
- `All Time`
- `Year`
- `Quarter`
- `Month`
- `Week`
- `Custom Range`

## 5. KPI Dashboard
The KPI Dashboard is the main operational summary page.

### 5.1 KPI sections
Choose a section from the sidebar:
- `Governance`
- `Partnerships`
- `Delivery`
- `Income` when region is `Global`
- `Comms` when region is `Global`
- `Case Studies`

### 5.2 Drill-down behaviour
Managers can open KPI popovers and inspect source rows.

For `Delivery > Total Participants`, Managers can view:
- attendee names when available
- attendee IDs when available
- placeholder entries when only counts exist

This is broader access than RPL users have.

### 5.3 KPI Debug
Managers can enable `Show KPI Debug` in the sidebar.

This shows internal count checks such as:
- people in region
- volunteers
- steering volunteers
- event counts
- participant counts
- grant counts

Use this when validating whether a KPI is being driven by the expected amount of source data.

## 6. Custom Reports Dashboard
Managers can use the full Custom Reports Dashboard.

### 6.1 Core workflow
1. choose datasets
2. choose an output type
3. select region and timeframe
4. click `Apply Report Filters`
5. optionally refine with `Advanced Report Controls`
6. click `Apply Advanced Filters`
7. export if needed

### 6.2 Recommended uses
Use Custom Reports for:
- monthly and quarterly reporting
- checking event activity by region
- funding and grant reviews
- exportable evidence packs

### 6.3 Distance Analysis
Managers can use Distance Analysis to review participant travel.

It includes:
- event rankings by travel distance
- an event drill-down selector
- participant-level journey details
- CSV export for all rows or a selected event

Because Managers have wider event access, this is often the best place to investigate reach and travel burden across delivery.

## 7. ML Dashboard
Managers can also open the ML Dashboard.

Use it when you need event-specific operational detail.

The workflow is:
1. set region and timeframe
2. choose an event
3. review event metadata
4. select an attendee
5. inspect participant details when available

Available information may include:
- event details
- participant names and IDs
- medical information fields
- emergency contact fields
- raw event payload

Use this carefully because it may expose operationally sensitive attendee data.

## 8. Funder Dashboard
Managers can open the Funder Dashboard and choose a funder.

This dashboard is aggregated and GDPR-safe.

Use it to:
- view bids submitted
- view total funds raised
- review partnership mix
- review delivery demographics
- view the income trend for a selected funder

Important note:
- the funder filter affects funding metrics and income trend
- non-funding operational metrics remain region/timeframe totals

## 9. Case Studies
Managers can:
- read case studies
- filter by region and date
- upload new case studies

Use this area to support reports with qualitative evidence.

## 10. Good Working Practice
- use KPI Dashboard for quick monitoring
- use KPI Debug when a headline number looks wrong
- use Custom Reports for exportable analysis
- use ML Dashboard for event-level operational checking
- use Funder Dashboard for sponsor conversations and updates

## 11. Troubleshooting
### The KPI number looks wrong
- switch on `Show KPI Debug`
- narrow the date range
- drill into the KPI card

### The report did not refresh
- click `Apply Report Filters`
- click `Apply Advanced Filters`

### No attendee detail is visible
- some events only contain counts
- attendee names depend on Beacon source data

### Funder Dashboard looks empty
- try `All Time`
- change the selected funder
- confirm the selected funder actually appears in payments or grants
