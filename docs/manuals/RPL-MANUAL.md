# RPL Dashboard Manual

## 1. Purpose
This manual is for Regional Programme Leads (`RPL`) using the Regional KPI Dashboard.

As an RPL, you can:
- view KPI summaries for your region or all regions
- run custom reports
- read and upload case studies
- drill into KPI source rows

As an RPL, you cannot:
- open the Admin Dashboard
- use the ML Dashboard
- see named attendee details in KPI event drill-downs

## 2. Signing In
1. Open the dashboard.
2. Enter your email address and password.
3. If the system asks you to change your password, complete that step before continuing.

If you cannot log in, use `Forgot password?` or contact an Admin.

## 3. Main Navigation
Use `View Mode` in the left sidebar.

Available views for RPL:
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`

## 4. Global Filters
Most RPL pages use the left sidebar for filters.

Main filters:
- `All Regions` or a specific region
- `Timeframe`

Timeframe options:
- `All Time`
- `Year`
- `Quarter`
- `Month`
- `Week`
- `Custom Range`

Best practice:
- start broad with `All Time`
- confirm the data exists
- then narrow to the region and period you need

## 5. KPI Dashboard
The KPI Dashboard gives headline operational figures.

### 5.1 KPI Section selector
Use `KPI Section` in the sidebar to switch between:
- `Governance`
- `Partnerships`
- `Delivery`
- `Income` when region is `Global`
- `Comms` when region is `Global`
- `Case Studies`

### 5.2 Governance
This section shows:
- steering group active status
- active volunteers
- new volunteers

Click a metric card to open its drill-down popup.

Inside the popup you can:
- review the related rows
- select a row for more detail
- open `Technical View (JSON)` if needed

### 5.3 Partnerships
This section shows:
- active organisations in the selected region
- network memberships placeholder metric

Use the organisation drill-down to inspect supporting rows.

### 5.4 Delivery
This section shows:
- events delivered
- total participants
- bursary participants placeholder metric
- average wellbeing change placeholder metric
- aggregated demographics

Important RPL limitation:
- RPL users can see attendee totals
- RPL users cannot see named attendee lists or IDs in the KPI event drill-down

### 5.5 Income and Comms
These are shown only when the region filter is `Global`.

Income includes:
- total funds raised
- bids submitted
- corporate partners
- in-kind value placeholder metric

Comms currently contains placeholder metrics.

### 5.6 KPI Drill-Down
When you click a KPI card:
1. a popup opens
2. a list of source rows appears
3. you select a row
4. the dashboard shows a readable record

Use this when:
- a number looks unusually high or low
- you need to validate which records are included
- you need source evidence behind a KPI

## 6. Custom Reports Dashboard
This is the main self-service analysis area for RPL users.

### 6.1 What you can do
You can:
- choose one or more datasets
- choose an output type
- filter by region and time
- apply advanced report filters
- export the results to CSV

### 6.2 Datasets
Available datasets:
- `People`
- `Organisations`
- `Events`
- `Payments`
- `Grants`

### 6.3 Output Types
Available report outputs:
- `Tabular`
- `Bar`
- `Line`
- `Pie`
- `UK Map`
- `Comparison Analysis`
- `Distance Analysis`

### 6.4 Apply filters
The report page now uses explicit apply buttons.

Use them in this order:
1. choose your report filters
2. click `Apply Report Filters`
3. if needed, open `Advanced Report Controls`
4. change advanced filters
5. click `Apply Advanced Filters`

If you change a filter and nothing updates yet, that is expected until you apply it.

### 6.5 Distance Analysis
Distance Analysis estimates participant travel to events.

What it shows:
- journey count
- average, median, and maximum distance
- distance bands
- event ranking by average travel distance
- event drill-down
- participant-level journey detail

How to use it:
1. choose `Output Type = Distance Analysis`
2. keep `Events` selected in datasets
3. click `Apply Report Filters`
4. choose event types if needed
5. use `Drill down into event` to inspect one event

Important notes:
- the report prefers road distance when routing is configured
- it falls back to straight-line distance when routing is unavailable
- missing participant or event postcode data will reduce results

## 7. Case Studies
The Case Studies area lets you read and add qualitative stories.

You can:
- filter case studies by region and date
- upload a new case study

To add one:
1. open `Upload New Case Study`
2. enter a title
3. enter the story or testimonial
4. choose the case study date
5. choose the region
6. submit

## 8. Exports
CSV export is available in Custom Reports and Distance Analysis.

Use exports when:
- you need offline analysis
- you want to circulate a report
- you want to check rows in Excel

## 9. Troubleshooting
### I see no KPI data
- check region and timeframe
- try `All Regions` and `All Time`
- confirm you are in the right KPI section

### The report looks unchanged
- click `Apply Report Filters`
- click `Apply Advanced Filters` if you changed advanced controls

### Distance Analysis shows nothing
- confirm the dataset includes `Events`
- confirm your date range contains events
- try turning off `Only include rows with resolved distance`

### I cannot see participant names
- that is expected for the RPL role in KPI event drill-downs

## 10. Good Working Practice
- use KPI sections for quick headline checks
- use Custom Reports for analysis and exports
- use Case Studies when you need qualitative examples alongside metrics
- validate unusual numbers using KPI drill-down before sharing them
