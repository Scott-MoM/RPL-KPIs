# Full Regional KPI Dashboard Manual

> Combined handbook for `RPL`, `Manager`, `ML`, `Admin`, and `Funder` users

![Navigation and screen areas](images/dashboard-navigation.svg)

## 1. Purpose
This document is the master guide for the Regional KPI Dashboard. Use it when:

- onboarding multiple user types
- supporting staff across roles
- checking which role should perform a task
- needing one handbook instead of several short manuals

## 2. Dashboard areas
The application is organised into these views:

- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

Most users move between views using `View Mode` in the left sidebar.

## 3. Shared concepts
### Region and timeframe
Most operational screens use:

- region selection
- timeframe selection

When investigating missing data, start broad, then narrow.

### Drill-down
KPI cards can open a detailed popup showing the source rows behind a number.

### Last Data Refresh
The sidebar includes a refresh status card showing how current the dashboard data is.

### Audit logging
Major changes and important interactions are recorded for governance and support.

## 4. Role comparison
| Role | Main views | Typical purpose | Key restrictions |
| --- | --- | --- | --- |
| `RPL` | KPI, Custom Reports, Case Studies | regional monitoring and self-service reporting | no Admin, no ML, no named attendee detail in KPI participant drill-down |
| `Manager` | KPI, Custom Reports, Case Studies, Funder, ML | operational management and validation | no Admin |
| `ML` | ML, Case Studies | event-by-event operational review | no KPI, reports, funder, or admin views |
| `Admin` | all views | access management, data operations, full reporting | highest responsibility, use admin actions carefully |
| `Funder` | Funder only | aggregated funding summary | no operational drill-down or personal data |

## 5. Screen guide
### KPI Dashboard
![KPI dashboard annotated guide](images/kpi-dashboard-guide.svg)

Best for:

- headline KPIs
- governance and delivery review
- validating figures with drill-down

### Custom Reports Dashboard
![Custom reports annotated guide](images/custom-reports-guide.svg)

Best for:

- tables and charts
- advanced filtering
- CSV export
- distance analysis

### ML Dashboard
![ML dashboard annotated guide](images/ml-dashboard-guide.svg)

Best for:

- selecting one event
- reviewing attendees
- checking medical and emergency information where available

### Funder Dashboard
![Funder dashboard annotated guide](images/funder-dashboard-guide.svg)

Best for:

- GDPR-safe sponsor reporting
- bids submitted
- funds raised
- income trend

### Admin Dashboard
![Admin dashboard annotated guide](images/admin-dashboard-guide.svg)

Best for:

- user administration
- password reset handling
- sync monitoring and control
- audit review

## 6. Role-by-role operating guide
### RPL
Use RPL access for:

- KPI monitoring
- self-service reports
- CSV export
- case study uploads

RPL users should move from KPI to Custom Reports when they need more than a headline number.

### Manager
Use Manager access for:

- KPI validation
- event and participant investigation
- sponsor-facing review
- broader operational analysis

Managers can see attendee names and IDs in KPI delivery drill-downs where the data exists.

### ML
Use ML access for:

- reviewing one event at a time
- checking participant information before delivery
- reading or adding case studies

### Admin
Use Admin access for:

- creating and updating users
- resetting passwords
- running sync checks and manual refresh activity
- reviewing audit logs

### Funder
Use Funder access for:

- summary-level funding oversight
- time-based review of bids and funds raised
- checking refresh recency

## 7. Common workflows
### Check a KPI
1. Open `KPI Dashboard`.
2. Set region and timeframe.
3. Choose the correct KPI section.
4. Click the KPI card to inspect supporting rows.

### Run a report
1. Open `Custom Reports Dashboard`.
2. Choose datasets and output type.
3. Set region and timeframe.
4. Click `Apply Report Filters`.
5. Optionally use `Advanced Report Controls`.
6. Click `Apply Advanced Filters`.
7. Export CSV if required.

### Investigate participant travel
1. Open `Custom Reports Dashboard`.
2. Set `Output Type` to `Distance Analysis`.
3. Keep `Events` selected.
4. Apply filters.
5. Drill down into a selected event.
6. Review or export the participant journey rows.

### Review a live or recent event
1. Open `ML Dashboard`.
2. Set region and timeframe.
3. Choose the event.
4. Review event details and participant information.

### Handle a password reset
1. Open `Admin Dashboard`.
2. Open `Password Reset Requests`.
3. Set a temporary password.
4. Tell the user to change it on next login.

## 8. Troubleshooting
### No data appears
- widen the timeframe
- try `All Regions` where available
- confirm you are in the correct dashboard view

### Reports do not refresh
- click `Apply Report Filters`
- click `Apply Advanced Filters`

### Participant names are missing
- not every event provides names in Beacon
- RPL users do not get named attendee detail in KPI participant drill-down

### Dashboard looks stale
- check `Last Data Refresh`
- ask an Admin to review sync status if needed

### Funder data looks empty
- widen the timeframe
- confirm the selected or assigned funder has matching records

## 9. File guide
Role manuals:

- `docs/manuals/RPL-MANUAL.md`
- `docs/manuals/MANAGER-MANUAL.md`
- `docs/manuals/ML-MANUAL.md`
- `docs/manuals/ADMIN-MANUAL.md`
- `docs/manuals/FUNDER-MANUAL.md`

Shared visuals:

- `docs/manuals/images/dashboard-navigation.svg`
- `docs/manuals/images/kpi-dashboard-guide.svg`
- `docs/manuals/images/custom-reports-guide.svg`
- `docs/manuals/images/ml-dashboard-guide.svg`
- `docs/manuals/images/funder-dashboard-guide.svg`
- `docs/manuals/images/admin-dashboard-guide.svg`
