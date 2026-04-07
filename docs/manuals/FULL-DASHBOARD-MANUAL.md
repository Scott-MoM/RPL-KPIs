# Full Regional KPI Dashboard Manual

> Combined guide for `RPL`, `Manager`, `ML`, `Admin`, and `Funder` users

![Navigation and screen areas](images/dashboard-navigation.svg)

## 1. Introduction
This is the full handbook for the Regional KPI Dashboard.

It is intended for:

- new starters
- support staff
- managers helping other users
- anyone who wants one complete guide to the whole system

The dashboard combines several types of work in one place:

- headline KPI review
- structured reporting and exports
- event-level operational review
- funder-facing summary reporting
- qualitative case study capture
- administrative support and maintenance

Not every user sees every part of the dashboard. Access depends on role.

## 2. Core ideas shared across the dashboard
### 2.1 View Mode
Users move between screens using `View Mode` in the left sidebar.

Common screens include:

- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Data Request Form`
- `Funder Dashboard`
- `ML Dashboard`

### 2.2 Region and timeframe
Most views depend on:

- region filters
- timeframe filters

If expected data is missing, start broad and then narrow down.

### 2.3 Last Data Refresh
The sidebar shows when the dashboard last refreshed.

Always check this before using data in:

- meetings
- reports
- presentations
- support decisions

### 2.4 Drill-down
Many KPI cards can be opened to show the rows behind a total.

Drill-down helps users move from:

- summary

to:

- explanation

### 2.5 Role-based access
Different users see different views and different levels of detail. This is intentional. Missing screens or missing fields often reflect role design rather than a problem.

## 3. Role overview
| Role | Main views | Typical use | Main limits |
| --- | --- | --- | --- |
| `RPL` | KPI, Custom Reports, Case Studies | regional monitoring and reporting | no Admin, no ML, no personal data |
| `Manager` | KPI, Custom Reports, Case Studies, Funder, ML | operational management and validation | no Admin |
| `ML` | ML, Case Studies | event-by-event operational work | no KPI, reports, funder, or admin access |
| `Admin` | all views | user management, sync control, full reporting | highest responsibility |
| `Funder` | Funder only | safe high-level reporting | no operational drill-down or personal data |

## 4. Screen-by-screen guide
### 4.1 KPI Dashboard
![KPI dashboard annotated guide](images/kpi-dashboard-guide.svg)

Use `KPI Dashboard` for:

- headline KPI review
- checking delivery, governance, and partnerships
- opening drill-downs behind KPI cards

Typical workflow:

1. Choose a region.
2. Choose a timeframe.
3. Choose a KPI section.
4. Review the cards.
5. Open drill-downs where needed.

Use this screen first when you want the fastest answer.

### 4.2 Custom Reports Dashboard
![Custom reports annotated guide](images/custom-reports-guide.svg)

Use `Custom Reports Dashboard` for:

- row-level tables
- charts
- filtered analysis
- exports
- comparison work
- distance analysis

Typical workflow:

1. Choose one or more datasets.
2. Choose an output type.
3. Set region and timeframe.
4. Click `Apply Report Filters`.
5. Use advanced filters if needed.
6. Review or export the result.

This screen uses two levels of filtering:

- the main report filters control datasets, output type, region, and timeframe
- the advanced filters refine the rows after the main report has loaded

Available datasets can include:

- `People` where the role allows it
- `Organisations`
- `Events`
- `Payments`
- `Grants`

Available output types include:

- `Tabular`
- `Bar`
- `Line`
- `Pie`
- `UK Map`
- `Comparison Analysis`
- `Distance Analysis`

Use `Tabular` for row checking and exports, `Line` for time trends, `Comparison Analysis` for direct group-versus-group comparison, and `Distance Analysis` for participant travel summaries.

### 4.3 ML Dashboard
![ML dashboard annotated guide](images/ml-dashboard-guide.svg)

Use `ML Dashboard` for:

- reviewing one event at a time
- checking event details
- reviewing participant information where the role allows it
- reviewing medical and emergency information where available

Typical workflow:

1. Set region and timeframe.
2. Choose the event.
3. Review `Event Details`.
4. Review participant or additional event information.

### 4.4 Funder Dashboard
![Funder dashboard annotated guide](images/funder-dashboard-guide.svg)

Use `Funder Dashboard` for:

- safe external-style reporting
- bids submitted
- funds raised
- funding trends over time

Typical workflow:

1. Set the timeframe.
2. Review the headline cards.
3. Review the trend.
4. Check `Last Data Refresh`.

### 4.5 Admin Dashboard
![Admin dashboard annotated guide](images/admin-dashboard-guide.svg)

Use `Admin Dashboard` for:

- creating and updating users
- resetting passwords
- checking sync health
- running manual sync actions
- reviewing audit history

Admin work should be deliberate and reasoned because many actions affect other users.

### 4.6 Case Studies
Use `Case Studies` for:

- reading stories and testimonials
- adding narrative evidence to reporting
- uploading new qualitative evidence

Typical workflow:

1. Filter first to avoid duplicates.
2. Review existing entries.
3. Add a clear title, date, region, and story text when uploading.

### 4.7 Data Request Form
Use `Data Request Form` for formal data access requests.

All fields are required:

- `Name`
- `Email`
- `Date`
- `Time`
- `Reason for data request`

When a request is submitted, `Admin` and `Manager` users are notified in the dashboard.

Admins can also use the same page to grant temporary access permissions to a single user with an expiry date and time.

## 5. Role-by-role guide
### 5.1 RPL
RPL users mainly work with:

- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Data Request Form`

Best for:

- summary monitoring
- regional reporting
- structured exports
- narrative evidence

Important limit:

- RPL users should not see personal data

### 5.2 Manager
Managers mainly work with:

- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Data Request Form`
- `ML Dashboard`
- `Funder Dashboard`

Best for:

- KPI validation
- operational review
- event-level checking
- leadership reporting
- sponsor-facing quality assurance

### 5.3 ML
ML users mainly work with:

- `ML Dashboard`
- `Case Studies`
- `Data Request Form`

Best for:

- checking one event at a time
- confirming operational details
- reviewing participant information where available

### 5.4 Admin
Admins can use every view and are responsible for:

- user management
- password resets
- sync review
- manual refresh actions
- audit and support work
- temporary access review and granting

### 5.5 Funder
Funder users mainly work with:

- `Funder Dashboard`
- `Data Request Form`

Best for:

- high-level funding review
- restricted summary reporting

## 6. Common tasks
### 6.1 Check a KPI
1. Open `KPI Dashboard`.
2. Set region and timeframe.
3. Choose the KPI section.
4. Review the headline card.
5. Open the drill-down if needed.

### 6.2 Build a report
1. Open `Custom Reports Dashboard`.
2. Choose the datasets.
3. Choose an output type.
4. Apply the main filters.
5. Apply advanced filters if required.
6. Review the result.
7. Export CSV if needed.

### 6.3 Review participant travel
1. Open `Custom Reports Dashboard`.
2. Choose `Distance Analysis`.
3. Apply the main filters.
4. Review the summary metrics.
5. Drill into a single event if needed.
6. Export the results if needed.

### 6.4 Review a single event
1. Open `ML Dashboard`.
2. Set region and timeframe.
3. Choose the event.
4. Review event details.
5. Review participant or operational information as needed.

### 6.5 Handle a password reset
1. Open `Admin Dashboard`.
2. Open `Password Reset Requests`.
3. Set a temporary password.
4. Ask the user to change it after sign-in.

### 6.6 Submit or review a data request
1. Open `Data Request Form`.
2. Complete the required fields.
3. Submit the request.
4. If you are an `Admin` or `Manager`, review the submitted request list and update its status.
5. If you are an `Admin`, grant temporary access only where justified and with an expiry time.

## 7. How to read the main outputs
### 7.1 Headline cards
Best for:

- quick checks
- status updates
- meeting preparation

### 7.2 Drill-downs
Best for:

- understanding what sits behind a number
- checking whether records look reasonable
- validating unusual totals

### 7.3 Reports
Best for:

- structured analysis
- exports
- comparison across regions, dates, statuses, or categories

### 7.4 Case studies
Best for:

- adding context to a number
- giving a real-life example
- supporting reports with narrative evidence

## 8. Good working practice
- check `Last Data Refresh` before using figures
- widen filters first if something appears to be missing
- use the correct screen for the task
- validate unusual numbers before circulating them
- handle personal data carefully and only where the role allows it

## 9. Troubleshooting
### No data is showing
1. Widen the timeframe.
2. Try `All Regions` where available.
3. Confirm that you are in the correct screen.

### A report is not updating
1. Click `Apply Report Filters`.
2. Click `Apply Advanced Filters` if you changed advanced options.

### Participant names are missing
- not all source records include names
- some roles are not permitted to see personal data

### The dashboard looks out of date
1. Check `Last Data Refresh`.
2. Ask an `Admin` to review sync health if needed.

### A user cannot do something they expect to do
1. Check the user's role first.
2. Confirm whether the task belongs in another view.
3. Ask an `Admin` if access may need to change.
