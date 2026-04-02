# Full Regional KPI Dashboard Manual

## 1. Introduction
This document combines the role-based manuals for the Regional KPI Dashboard into one reference.

Included manuals:
- RPL Manual
- Manager Manual
- Mountain Leader Manual
- Admin Manual
- Funder Manual

Use this document when:
- you need one complete handbook
- you support multiple user types
- you are onboarding new users across several roles

## 2. Roles Covered
The dashboard supports these roles:
- `RPL`
- `Manager`
- `ML`
- `Admin`
- `Funder`

## 3. Shared Concepts
### 3.1 View Mode
Most users switch between dashboard areas using `View Mode` in the sidebar.

### 3.2 Region and timeframe filters
Most operational pages allow:
- region selection
- timeframe selection

### 3.3 Drill-down
Several KPI cards open a popup with supporting rows and readable record detail.

### 3.4 Data refresh
The sidebar shows the last dashboard data refresh time.

### 3.5 Audit logging
The dashboard records user interactions and major administrative actions into the audit trail.

## 4. RPL Manual

### 4.1 Access
RPL users can access:
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`

RPL users cannot access:
- `Admin Dashboard`
- `ML Dashboard`
- participant names or IDs in KPI event drill-downs

### 4.2 KPI Dashboard
RPL users can:
- switch KPI sections
- review governance, partnerships, and delivery metrics
- use `Income` and `Comms` when region is `Global`
- drill into KPI source rows

RPL users can see participant totals, but not named attendee detail in KPI drill-downs.

### 4.3 Custom Reports
RPL users can:
- run reports on People, Organisations, Events, Payments, and Grants
- use Tabular, Bar, Line, Pie, UK Map, Comparison, and Distance Analysis outputs
- export CSV files

Distance Analysis supports:
- event ranking
- selected event drill-down
- participant-level travel rows
- selected-event CSV export

### 4.4 Case Studies
RPL users can read and upload case studies.

## 5. Manager Manual

### 5.1 Access
Manager users can access:
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

Managers cannot access:
- `Admin Dashboard`

### 5.2 KPI Dashboard
Managers can:
- use KPI drill-down
- see attendee names and IDs in Delivery drill-downs where available
- use `Show KPI Debug`

### 5.3 Custom Reports
Managers can run and export all report types, including Distance Analysis.

### 5.4 ML Dashboard
Managers can inspect event-level operational detail and attendee information.

### 5.5 Funder Dashboard
Managers can use aggregated funder views and choose the funder from a selector.

## 6. Mountain Leader Manual

### 6.1 Access
ML users can access:
- `ML Dashboard`
- `Case Studies`

### 6.2 ML Dashboard purpose
The ML Dashboard is event-focused.

ML users can:
- filter by region and timeframe
- choose an event
- review event details
- select a participant
- inspect personal, medical, and emergency contact information where available
- inspect the raw event payload

### 6.3 Case Studies
ML users can also read and upload case studies.

## 7. Admin Manual

### 7.1 Access
Admins can access every dashboard area:
- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

### 7.2 Admin Dashboard
The Admin Dashboard includes:
- password reset request handling
- user creation
- user role updates
- user deletion
- sync performance review
- Beacon API smoke testing
- manual Beacon sync
- CSV import
- audit log review

### 7.3 User management
Admins can:
- create users
- assign one or more roles
- assign funder-specific users
- reset passwords
- update roles with audit reason and confirmation
- delete users with audit reason and confirmation

### 7.4 Sync operations
Admins can:
- run Beacon smoke tests
- start manual API sync
- stop or clear stuck sync jobs
- review sync timings

### 7.5 Reporting access
Admins can use all KPI, report, ML, and funder views.

## 8. Funder Manual

### 8.1 Access
Funder users can access:
- `Funder Dashboard`

### 8.2 Privacy model
The Funder Dashboard is GDPR-safe and aggregated only.

It does not show:
- personal data
- attendee detail
- operational row-level drill-down

### 8.3 What funders can see
Funders can see:
- bids submitted
- total funds raised
- income trend
- last data refresh time

Their assigned funder is applied automatically.

## 9. Common Workflows

### 9.1 Check a KPI
1. open the relevant dashboard
2. choose the right region and timeframe
3. switch to the correct section
4. click a KPI card to inspect its source rows

### 9.2 Run a report
1. open `Custom Reports Dashboard`
2. choose datasets
3. choose output type
4. set region and time
5. click `Apply Report Filters`
6. refine advanced controls if needed
7. click `Apply Advanced Filters`
8. export CSV if needed

### 9.3 Investigate participant travel
1. open `Custom Reports Dashboard`
2. choose `Distance Analysis`
3. keep `Events` selected
4. apply report filters
5. select an event in the event drill-down
6. review the participant-level distance rows

### 9.4 Handle a password reset
1. open `Admin Dashboard`
2. open `Password Reset Requests`
3. choose the pending user
4. set a temporary password

### 9.5 Review a live event
1. open `ML Dashboard`
2. set region and timeframe
3. choose the event
4. review event details
5. select a participant
6. inspect medical or emergency fields if present

## 10. Troubleshooting

### 10.1 No data appears
- widen timeframe
- use `All Regions` where available
- confirm the user is in the correct dashboard view

### 10.2 Reports do not refresh
- click `Apply Report Filters`
- click `Apply Advanced Filters`

### 10.3 Participant names are missing
- some source rows only contain counts or IDs
- RPL users do not get named attendee detail in KPI drill-downs

### 10.4 Funder data is empty
- widen timeframe
- confirm there are grants or payments for that funder

### 10.5 Dashboard looks stale
- check `Last Data Refresh`
- ask an Admin to review sync status if needed

## 11. File Guide
The individual manuals are stored here:
- `docs/manuals/RPL-MANUAL.md`
- `docs/manuals/MANAGER-MANUAL.md`
- `docs/manuals/ML-MANUAL.md`
- `docs/manuals/ADMIN-MANUAL.md`
- `docs/manuals/FUNDER-MANUAL.md`

This combined manual is:
- `docs/manuals/FULL-DASHBOARD-MANUAL.md`
