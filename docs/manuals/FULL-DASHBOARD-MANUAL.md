# Full Regional KPI Dashboard Manual

> Combined guide for `RPL`, `Manager`, `ML`, `Admin`, and `Funder` users

![Navigation and screen areas](images/dashboard-navigation.svg)

## 1. About this guide
This is the all-in-one handbook for the Regional KPI Dashboard.

Use it when:

- onboarding new users
- checking which role can do what
- supporting people across different teams
- you want one guide instead of several separate manuals

## 2. Main dashboard areas
The dashboard is split into these views:

- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

Most users move between screens using `View Mode` in the left sidebar.

## 3. Shared ideas across the dashboard
### Region and timeframe
Most screens use filters for:

- region
- timeframe

If you are not sure where data sits, start with a wide range first and then narrow down.

### Drill-down
Many KPI cards open a popup that shows the records behind the number.

### Last Data Refresh
The sidebar shows when the dashboard was last refreshed. Check this before using figures in meetings or reports.

### Audit logging
Important changes and actions are recorded to support governance and support work.

## 4. Role summary
| Role | Main views | Main purpose | Main limits |
| --- | --- | --- | --- |
| `RPL` | KPI, Custom Reports, Case Studies | regional monitoring and reporting | no Admin, no ML, no personal data on the dashboard |
| `Manager` | KPI, Custom Reports, Case Studies, Funder, ML | operational management and validation | no Admin |
| `ML` | ML, Case Studies | event-by-event operational review | no KPI, reports, funder, or admin access |
| `Admin` | all views | user management, sync control, full reporting | highest responsibility |
| `Funder` | Funder only | safe summary reporting | no operational drill-down or personal data |

## 5. Screen guide
### KPI Dashboard
![KPI dashboard annotated guide](images/kpi-dashboard-guide.svg)

Best for:

- headline KPI review
- checking delivery, governance, and partnerships
- opening drill-downs behind KPI cards

### Custom Reports Dashboard
![Custom reports annotated guide](images/custom-reports-guide.svg)

Best for:

- tables and charts
- filtering large datasets
- CSV exports
- comparison work
- distance analysis

### ML Dashboard
![ML dashboard annotated guide](images/ml-dashboard-guide.svg)

Best for:

- one event at a time
- reviewing event details
- checking participant, medical, and emergency information where the role allows it

### Funder Dashboard
![Funder dashboard annotated guide](images/funder-dashboard-guide.svg)

Best for:

- safe funder-facing reporting
- bids submitted
- funds raised
- funding trends over time

### Admin Dashboard
![Admin dashboard annotated guide](images/admin-dashboard-guide.svg)

Best for:

- creating and updating users
- password resets
- sync monitoring and manual refresh work
- audit review

## 6. Role-by-role summary
### RPL
Use RPL access for:

- KPI monitoring
- custom reporting
- CSV export
- case study uploads

RPL users can view summary figures but should not expect personal data anywhere in the dashboard.

### Manager
Use Manager access for:

- operational analysis
- KPI validation
- event review
- funder conversations
- cross-checking delivery detail

### ML
Use ML access for:

- reviewing one event at a time
- checking operational details before or after delivery
- reading and uploading case studies

### Admin
Use Admin access for:

- managing users
- resetting passwords
- monitoring sync health
- running manual sync actions
- reviewing audit history

### Funder
Use Funder access for:

- sponsor reporting
- high-level funding review
- safe aggregated summaries

## 7. Common tasks
### Check a KPI
1. Open `KPI Dashboard`.
2. Set region and timeframe.
3. Choose the KPI section you need.
4. Click the KPI card to see the supporting records.

### Run a report
1. Open `Custom Reports Dashboard`.
2. Choose the dataset or datasets you need.
3. Choose the output type.
4. Set region and timeframe.
5. Click `Apply Report Filters`.
6. Use advanced filters if needed.
7. Export the result if required.

### Review participant travel
1. Open `Custom Reports Dashboard`.
2. Set `Output Type` to `Distance Analysis`.
3. Apply your filters.
4. Review the summary figures.
5. Drill into a single event if needed.
6. Export the result if needed.

### Review a specific event
1. Open `ML Dashboard`.
2. Set region and timeframe.
3. Select the event.
4. Review the event details and any participant information available to your role.

### Handle a password reset
1. Open `Admin Dashboard`.
2. Open `Password Reset Requests`.
3. Set a temporary password.
4. Tell the user to change it after signing in.

## 8. Troubleshooting
### No data is showing
- widen the timeframe
- try `All Regions` where available
- check that you are in the right screen

### A report is not updating
- click `Apply Report Filters`
- click `Apply Advanced Filters` if you changed advanced controls

### Participant names are missing
- not all events include names in the source data
- some roles do not have permission to view personal data

### The dashboard looks out of date
- check `Last Data Refresh`
- ask an Admin to review sync status if needed

### Funder figures look empty
- widen the timeframe
- confirm the correct funder is selected or assigned
