# RPL Dashboard Manual

> Audience: `RPL` users  
> Scope: KPI monitoring, reporting, exports, and case study management

![KPI dashboard annotated guide](images/kpi-dashboard-guide.svg)

## 1. Introduction
This manual explains how Regional Programme Leads use the dashboard in day-to-day reporting work.

The RPL role is designed for people who need to:

- monitor regional performance
- review headline delivery, partnership, and governance figures
- prepare internal updates and regional reports
- export structured data for offline use
- add qualitative evidence through case studies

RPL users can open:

- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Data Request Form`

RPL users cannot open:

- `Admin Dashboard`
- `ML Dashboard`
- `Funder Dashboard`

RPL users also have an important privacy limit. This role is intended for summary reporting rather than operational personal-detail review. You should not expect to see participant names, participant identifiers, postcodes, medical notes, or emergency contact details anywhere in the dashboard.

## 2. What the RPL role is for
The RPL role is best used when the question is:

- how is my region performing
- what has changed over time
- which areas need follow-up
- what evidence can I export for a report or discussion
- what case study can I use alongside the numbers

The RPL role is not intended for:

- checking one attendee in detail
- reviewing medical or emergency information
- creating or managing user accounts
- running sync or maintenance actions

If you need personal or event-level operational detail, escalate the question to a `Manager` or `Admin` user.

## 3. Signing in and first checks
When you open the dashboard:

1. Enter your email address and password.
2. If the system asks you to change your password, complete that step before continuing.
3. Look at the left sidebar.
4. Confirm the `View Mode` you need.
5. Check `Last Data Refresh` before relying on any figure.

If you are using the dashboard for a meeting, report, or update, make checking the refresh time a habit. A figure may be correct for the last completed refresh but still be too old for the purpose you have in mind.

![Navigation and screen areas](images/dashboard-navigation.svg)

## 4. Understanding the layout
Most RPL work begins in the left sidebar.

The sidebar normally contains:

- `View Mode`
- region controls
- timeframe controls
- screen-specific controls such as `KPI Section`

The main page changes depending on the screen you choose in `View Mode`.

Use the screens like this:

- `KPI Dashboard` for the quickest headline view
- `Custom Reports Dashboard` for structured analysis, charts, and exports
- `Case Studies` for qualitative stories and supporting evidence
- `Data Request Form` for formal requests for data access

If you are not sure where to start, begin in `KPI Dashboard`, confirm the headline, then move into `Custom Reports Dashboard` if you need more structure or exportable detail.

## 5. Filters and navigation
Most reporting tasks depend on choosing the right region and timeframe first.

### 5.1 Region controls
Use `All Regions` when you want an overall picture or when you are not sure where the records will appear.

Choose a single region when you need:

- a regional update
- a regional export
- a more focused chart
- a cleaner result set

If you expect data and cannot see it, widen to `All Regions` first. Once you confirm the data exists, narrow again.

### 5.2 Timeframe controls
Typical timeframe options include:

- `All Time`
- `Year`
- `Quarter`
- `Month`
- `Week`
- `Custom Range`

Use them like this:

- start with `All Time` if you are unsure whether the records exist
- use `Year`, `Quarter`, `Month`, or `Week` for routine reporting periods
- use `Custom Range` when the exact reporting window matters

### 5.3 Recommended navigation pattern
For most questions, this is the safest approach:

1. Start broad.
2. Confirm the data exists.
3. Narrow the region.
4. Narrow the timeframe.
5. Move into drill-down or reports only after the headline view makes sense.

This reduces the risk of concluding that data is missing when the filters are simply too narrow.

## 6. KPI Dashboard
The `KPI Dashboard` is the quickest place to review headline performance.

### 6.1 When to use KPI Dashboard
Use this screen when you want to:

- get a fast summary of the current picture
- review headline performance before a meeting
- sense-check whether a figure looks reasonable
- understand which KPI area needs further investigation
- open the records behind a card

This screen is best for monitoring and quick review. It is not the best screen for detailed export work.

### 6.2 KPI sections
Use `KPI Section` to move between the dashboard areas. Depending on the selected region, the available sections can include:

- `Governance`
- `Partnerships`
- `Delivery`
- `Income`
- `Comms`
- `Case Studies`

`Income` and `Comms` are shown only when the region context supports them, for example `Global`.

### 6.3 Step-by-step KPI workflow
When checking a KPI:

1. Open `KPI Dashboard`.
2. Set the correct region.
3. Set the correct timeframe.
4. Choose the correct `KPI Section`.
5. Review the headline cards on the page.
6. If a card looks unusual, click it.
7. Review the supporting rows shown in the drill-down.
8. Decide whether the KPI is correct, unclear, or needs further follow-up in Custom Reports.

### 6.4 Using drill-down properly
Drill-down helps you move from a summary number to the rows behind it.

Use it when:

- a total looks too high or too low
- you want to understand what is included in a KPI
- you need confidence before quoting a figure
- you want to identify which records are driving a change

When a drill-down opens:

1. Read the title so you know what metric you opened.
2. Review the returned list.
3. Look for obvious issues such as duplicates, missing categories, or surprising dates.
4. If the answer still is not clear, move to `Custom Reports Dashboard` and rebuild the question in a more structured way.

### 6.5 Demographics on KPI Dashboard
The `Delivery` section shows demographics in two separate cards:

- `Gender`
- `Age`

The `Gender` card can include `Men`, `Women`, `Trans / Non-binary / Gender diverse`, `Prefer not to say`, and `Unknown / Not provided`.

The `Age` card can include:

- `18-30`
- `30-40`
- `40-45`
- `45-65`
- `65-75`
- `75+`
- `Unknown Age`

If `Unknown Age` appears, attendee rows exist but usable age values are missing for some or all records in the filtered selection.

### 6.6 Privacy limits for RPL users
RPL users should not see personal data.

That means you should not expect to see:

- participant names
- participant IDs
- participant postcodes
- contact details
- medical information
- emergency contact information

You may still see summary-level counts and reporting totals. This is intentional. It allows regional monitoring while protecting privacy.

### 6.7 Good KPI habits
Use these habits consistently:

- check the region before discussing a number
- check the timeframe before discussing a trend
- open the drill-down before escalating a suspected issue
- compare a narrow period against a wider one if a number looks unusual
- use case studies to support narrative, not to replace factual checking

## 7. Custom Reports Dashboard
Use `Custom Reports Dashboard` when the KPI cards are not detailed enough.

![Custom reports annotated guide](images/custom-reports-guide.svg)

This is the main screen for structured reporting work. Use it when you need tables, charts, exports, comparison work, or summary-level travel analysis.

### 7.1 What this screen is for
Use `Custom Reports Dashboard` when you need to:

- produce a table instead of a single KPI figure
- export data as CSV
- compare categories, statuses, or time periods
- build a chart for a meeting or report
- narrow data more precisely than the KPI screen allows
- review summary-level distance analysis for events

### 7.2 Datasets available to RPL users
RPL users can work with these datasets:

- `Organisations`
- `Events`
- `Payments`
- `Grants`

Each dataset is useful for different questions:

- `Organisations`: partnership activity, organisation status, referral sources, and organisation-related counts
- `Events`: delivery activity, event types, event dates, event status, and region-based delivery questions
- `Payments`: income records and payment timing
- `Grants`: grant pipeline, grant outcomes, and close-date reporting

If a question spans more than one reporting area, select more than one dataset.

### 7.3 The main report workflow
Use this workflow every time:

1. Open `Custom Reports Dashboard`.
2. In the sidebar, choose one or more datasets.
3. Choose an `Output Type`.
4. Set `All Regions` or a specific region.
5. Set the timeframe.
6. Click `Apply Report Filters`.
7. Review the first result.
8. If it is too broad, open `Advanced Report Controls`.
9. Apply advanced filters.
10. Review the output again.
11. Export the CSV if needed.

This screen works in two stages:

- `Apply Report Filters` updates the main report selection, region, timeframe, and output type
- `Apply Advanced Filters` refines the rows already returned

If you change something and nothing happens yet, you probably still need to click the matching `Apply` button.

### 7.4 Output types explained
The available output types are:

- `Tabular`
- `Bar`
- `Line`
- `Pie`
- `UK Map`
- `Comparison Analysis`
- `Distance Analysis`

Use them as follows:

- `Tabular`: best for checking rows, sorting, and exporting
- `Bar`: best for comparing groups side by side
- `Line`: best for trend analysis over time
- `Pie`: best for simple share-of-total views
- `UK Map`: best for showing regional spread
- `Comparison Analysis`: best for direct group-versus-group comparison
- `Distance Analysis`: best for summary travel analysis

### 7.5 Grouping, metrics, and aggregation
Most chart-style outputs ask you to choose:

- `Group By`
- `Metric`
- `Aggregation`

These controls define what the chart means:

- `Group By` decides what the report is split by, such as region, category, status, month, or label
- `Metric` decides which numeric field is being measured
- `Aggregation` decides whether the values are summed, counted, or averaged

For example:

- a `Bar` chart grouped by `status` with `count` tells you how many rows fall into each status
- a `Line` chart grouped over time with `sum` can show total value across periods
- a `Pie` chart grouped by `category` can show how the total splits across categories

### 7.6 How to choose the right output
Use `Tabular` when:

- you want to inspect the actual rows
- you need to export data
- you are checking whether the data looks correct before charting it

Use `Bar` when:

- you want a simple visual comparison
- the categories are limited and readable

Use `Line` when:

- the question is about change over time
- the records contain valid dates

Use `Pie` when:

- you have a small number of categories
- the question is about share rather than trend

Use `UK Map` when:

- region is the main story
- you want to communicate spread rather than exact row detail

Use `Comparison Analysis` when:

- you want to compare one group against another directly
- you need the difference between two groups

Use `Distance Analysis` when:

- you want to understand travel patterns
- you want to discuss reach and travel burden at summary level

### 7.7 Advanced Report Controls
Use `Advanced Report Controls` when the first result is too broad.

Available advanced controls include:

- `Limit to datasets`
- `Category filter`
- `Status filter`
- `Metric value range`
- `Only include rows with valid date`

Use them like this:

- `Limit to datasets` when you started with more than one dataset but want to narrow within the returned report
- `Category filter` when you want only one strand, theme, or category
- `Status filter` when you want only completed, active, approved, or similar records
- `Metric value range` when you want to remove very small or very large values
- `Only include rows with valid date` when you are preparing for a date-based chart such as `Line`

If advanced filters remove everything:

1. Remove the most restrictive filter first.
2. Reapply.
3. Add filters back one by one.

This helps you identify which setting removed the expected rows.

### 7.8 Comparison Analysis
`Comparison Analysis` compares one selected group against another.

This is useful for questions such as:

- how one region compares with another
- whether one category is larger than another
- whether one status is changing more than another

A typical workflow is:

1. Choose the relevant dataset.
2. Choose `Comparison Analysis`.
3. Apply the main report filters.
4. Choose the comparison dimension.
5. Choose the baseline value.
6. Choose the comparison value.
7. Review the totals and the difference shown on screen.

### 7.9 Distance Analysis
`Distance Analysis` is different from the standard table and chart outputs. It focuses on participant travel to events.

It can show:

- number of journeys
- average distance
- median distance
- maximum distance
- distance bands
- events ranked by average travel distance

You can also:

- filter to relevant event types
- keep only rows with resolved distance
- drill into a selected event
- download a CSV

For RPL users, this analysis remains summary-level. Do not expect participant-level personal detail.

If the distance output looks sparse, the usual causes are:

- the timeframe is too narrow
- the event type filter is too restrictive
- participant or event postcode data is missing
- unresolved rows are excluded

### 7.10 Example reporting workflows
Use `Events` plus `Tabular` when you need a clean event list for a reporting period.

Use `Payments` plus `Line` when you want to show how income changes over time.

Use `Grants` plus `Bar` when you want to compare outcomes or statuses.

Use `Organisations` plus `Comparison Analysis` when you want to compare regions, categories, or statuses directly.

Use `Distance Analysis` when you need a high-level view of how far participants are travelling.

## 8. Case Studies
`Case Studies` gives you qualitative evidence to sit alongside the numbers.

Use it when you need:

- a story to support a report
- narrative context for a KPI trend
- an example to bring a presentation to life
- a place to upload a new regional story

### 8.1 Reading case studies
To review existing case studies:

1. Open `Case Studies`.
2. Set the relevant region if available.
3. Set the relevant timeframe.
4. Review the returned stories.
5. Check titles and dates carefully so that you use the right story for the right reporting period.

### 8.2 Uploading a case study
Suggested workflow:

1. Open `Case Studies`.
2. Filter first to avoid duplicates.
3. Add a clear title.
4. Add the story text.
5. Enter the correct date.
6. Choose the correct region.
7. Submit the form.

### 8.3 Good case study practice
When creating a case study:

- use a clear, descriptive title
- check the date carefully
- choose the correct region
- keep the content factual and readable
- avoid including sensitive personal details that should not be widely shared

## 9. Data Request Form
Use `Data Request Form` when you need to make a formal request for access to data.

This page is useful when:

- your current role does not allow the detail you need
- you need a time-specific data extract or permission review
- you want a clear recorded request rather than an informal message

### 9.1 What you must complete
All fields are required:

- `Name`
- `Email`
- `Date`
- `Time`
- `Reason for data request`

The `Name` and `Email` fields are dropdowns. Choose the matching values for the same user.

### 9.2 Step-by-step workflow
1. Open `Data Request Form`.
2. Choose your name from the dropdown.
3. Choose your email from the dropdown.
4. Select the date you need the request to be considered against.
5. Select the time.
6. Enter a clear reason in the text area.
7. Submit the form.

### 9.3 What happens after submission
When you submit the form:

- the request is saved
- `Admin` and `Manager` users are notified in the dashboard
- your recent requests remain visible on the page for reference

Be specific in the reason field. A clear reason makes it easier for the reviewing team to decide what access or data response is appropriate.

## 10. Common RPL tasks
### 9.1 Check a KPI before a meeting
1. Open `KPI Dashboard`.
2. Set the correct region.
3. Set the correct timeframe.
4. Choose the relevant KPI section.
5. Review the headline card.
6. Open the drill-down if anything looks unusual.
7. If needed, move into `Custom Reports Dashboard` for a more structured check.

### 9.2 Export data for offline analysis
1. Open `Custom Reports Dashboard`.
2. Choose the relevant dataset.
3. Choose `Tabular`.
4. Set the region and timeframe.
5. Click `Apply Report Filters`.
6. Narrow with advanced controls if needed.
7. Review the rows.
8. Click the CSV download button.

### 9.3 Check a regional trend
1. Open `Custom Reports Dashboard`.
2. Choose the relevant dataset.
3. Choose `Line`.
4. Set the correct region and timeframe.
5. Click `Apply Report Filters`.
6. If needed, use `Only include rows with valid date`.
7. Review the trend.
8. Compare with a wider period if the result seems surprising.

### 9.4 Add a case study to support a report
1. Open `Case Studies`.
2. Search or filter to confirm the story is not already there.
3. Add the new case study.
4. Check title, date, and region carefully.
5. Submit and review the saved result.

### 9.5 Submit a data request
1. Open `Data Request Form`.
2. Choose your name and email.
3. Set the date and time.
4. Explain the request clearly.
5. Submit and wait for Admin or Manager review.

## 11. Good working practice
Use these habits consistently:

- use KPI for quick checks
- use Custom Reports for deeper analysis
- check `Last Data Refresh` before using figures externally
- widen filters first if expected data is missing
- validate unusual totals before sharing them
- pair quantitative outputs with case studies where useful
- respect the privacy limits of the RPL role
- use the Data Request Form instead of asking informally when access needs to be reviewed

## 12. Troubleshooting
### No KPI data is showing
Check these in order:

1. Confirm the selected region.
2. Confirm the selected timeframe.
3. Try `All Regions`.
4. Try `All Time`.
5. Confirm that you are in the correct `KPI Section`.

### The report looks unchanged
This usually means the new settings have not been applied yet.

1. Click `Apply Report Filters` if you changed dataset, region, timeframe, or output type.
2. Click `Apply Advanced Filters` if you changed advanced controls.

### Distance Analysis shows no rows
Check:

- the date range
- the event types selected
- whether postcode data may be missing
- whether unresolved rows are being excluded

### I cannot see participant names
That is expected for the `RPL` role.

### A number still looks wrong
Use this process:

1. Widen the timeframe.
2. Open the supporting drill-down.
3. Rebuild the question in `Custom Reports Dashboard`.
4. Compare with another section or chart type.
5. Ask a `Manager` or `Admin` to investigate further if the issue needs deeper operational review.
