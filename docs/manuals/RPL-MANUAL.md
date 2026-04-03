# RPL Dashboard Manual

> Audience: Regional Programme Leads (`RPL`)  
> Scope: KPI monitoring, self-service reporting, exports, and case study management

![KPI dashboard annotated guide](images/kpi-dashboard-guide.svg)

## 1. What this manual covers
RPL users use the dashboard to monitor delivery, review trends, validate headline numbers, and prepare evidence for internal reporting.

RPL access includes:

- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`

RPL users cannot access:

- `Admin Dashboard`
- `ML Dashboard`
- named attendee details inside KPI event drill-downs

## 2. Quick start
1. Sign in with your email address and password.
2. Use `View Mode` in the left sidebar to choose the screen you need.
3. Start with `All Regions` and a broad timeframe if you are not sure where data sits.
4. Narrow the filters once you confirm the records are present.

![Navigation and screen areas](images/dashboard-navigation.svg)

## 3. Shared filters and navigation
Most RPL tasks begin in the left sidebar.

Main controls:

- `View Mode`
- `All Regions` or a specific region
- `Timeframe`
- `KPI Section` on the KPI screen

Typical timeframe options:

- `All Time`
- `Year`
- `Quarter`
- `Month`
- `Week`
- `Custom Range`

Best practice:

- start broad
- confirm the data is present
- then narrow to the reporting period you need

## 4. KPI Dashboard
The KPI Dashboard is the fastest way to review headline figures.

### 4.1 Screen tour
Use `KPI Section` to move between:

- `Governance`
- `Partnerships`
- `Delivery`
- `Income` when region is `Global`
- `Comms` when region is `Global`
- `Case Studies`

The page title shows the active region. KPI cards update from the chosen filters.

### 4.2 What each section is for
`Governance`

- steering group and volunteer-related metrics
- useful for oversight and governance reporting

`Partnerships`

- active organisations and partnership-related counts
- useful for regional relationship tracking

`Delivery`

- events delivered
- total participants
- aggregated demographics and other delivery measures

`Income`

- available only when the region is `Global`
- funding totals, bids submitted, partner-related measures

`Comms`

- available only when the region is `Global`
- communications-related summary measures

`Case Studies`

- qualitative evidence alongside KPI reporting

### 4.3 Drill-down and validation
Click any KPI card to inspect the source records behind the number.

Typical flow:

1. Click the KPI card.
2. Review the list of supporting rows.
3. Select a row to inspect it in readable detail.
4. Open `Technical View (JSON)` only if you need the raw structure.

Use drill-down when:

- a KPI looks unexpectedly high or low
- you need confidence before sharing a figure
- a stakeholder asks which records are included

### 4.4 Important RPL privacy limit
In `Delivery > Total Participants`, RPL users can review totals but not named attendee details or IDs.

This is intentional. If participant-level operational detail is required, ask a Manager or Admin to review it in the appropriate view.

## 5. Custom Reports Dashboard
The Custom Reports screen is the main self-service analysis workspace for RPL users.

![Custom reports annotated guide](images/custom-reports-guide.svg)

### 5.1 What you can do
- combine datasets
- build tables and charts
- narrow by date and region
- apply advanced filters
- download CSV files for offline analysis

### 5.2 Datasets
Available datasets:

- `People`
- `Organisations`
- `Events`
- `Payments`
- `Grants`

### 5.3 Output types
Available outputs:

- `Tabular`
- `Bar`
- `Line`
- `Pie`
- `UK Map`
- `Comparison Analysis`
- `Distance Analysis`

### 5.4 Standard report workflow
1. Choose one or more datasets.
2. Select an output type.
3. Set region and timeframe.
4. Click `Apply Report Filters`.
5. Open `Advanced Report Controls` if you need extra filtering.
6. Click `Apply Advanced Filters`.
7. Review the results and export if needed.

If you change a filter and the report does not move immediately, that is expected until the relevant `Apply` button is clicked.

### 5.5 Advanced filtering
Advanced controls can be used to limit the result set by:

- dataset
- category
- status
- metric value range
- rows with valid dates only

This is useful for tidying large mixed reports before export.

### 5.6 Distance Analysis
Distance Analysis estimates participant travel from home postcode to the event location.

It can show:

- participant journey count
- average, median, and maximum distance
- distance bands
- events ranked by average travel distance
- participant-level journey rows

Recommended workflow:

1. Set `Output Type` to `Distance Analysis`.
2. Keep `Events` selected in the dataset filter.
3. Click `Apply Report Filters`.
4. Limit to event types if needed.
5. Decide whether to keep `Only include rows with resolved distance` turned on.
6. Use `Drill down into event` to inspect one event in detail.
7. Download the selected-event or full CSV when needed.

Important notes:

- road distance is used when routing is configured
- otherwise the report falls back to straight-line miles
- missing participant or event postcode data will reduce the available rows

## 6. Case Studies
Case Studies adds qualitative evidence to the numbers.

Use it to:

- read regional stories and testimonials
- filter by date and region
- upload a new case study for future reporting

Suggested workflow for uploads:

1. Open `Case Studies`.
2. Choose `Upload New Case Study`.
3. Add a clear title.
4. Paste the story or testimonial.
5. Enter the correct date.
6. Assign the correct region.
7. Submit and review the saved result.

## 7. Typical RPL tasks
### Check a KPI before a meeting
1. Open `KPI Dashboard`.
2. Choose the right section.
3. Set the region and timeframe.
4. Click the KPI card to validate the supporting rows.

### Prepare a CSV for offline analysis
1. Open `Custom Reports Dashboard`.
2. Choose the relevant dataset and output type.
3. Apply filters.
4. Refine with advanced controls if required.
5. Click `Download Report CSV`.

### Add a case study to support a monthly update
1. Open `Case Studies`.
2. Filter first to avoid duplicating an existing story.
3. Upload the new case study with a clear title and date.

## 8. Troubleshooting
### I see no KPI data
- check region and timeframe first
- try `All Regions` and `All Time`
- confirm you are on the correct KPI section

### The report looks unchanged
- click `Apply Report Filters`
- click `Apply Advanced Filters` if you changed advanced controls

### Distance Analysis shows no rows
- confirm `Events` is included as a dataset
- widen the date range
- try clearing `Only include rows with resolved distance`

### I cannot see participant names
- that is expected for the RPL role in KPI drill-downs

## 9. Good working practice
- use KPI cards for fast monitoring
- use Custom Reports when you need evidence, export, or charting
- validate unusual numbers with drill-down before circulating them
- pair a quantitative report with a case study where possible
