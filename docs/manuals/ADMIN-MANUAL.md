# Admin Dashboard Manual

## 1. Purpose
This manual is for `Admin` users.

Admins have the broadest access in the dashboard and are responsible for:
- user administration
- password resets
- role management
- manual Beacon sync
- CSV imports
- audit review
- full dashboard access across operational views

Admin views:
- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

## 2. Signing In
1. Open the dashboard.
2. Enter your email address and password.
3. If you are prompted to change password, complete that step.

If the dashboard reports `Admin client not available`, check the Supabase configuration.

## 3. View Mode
Use `View Mode` in the sidebar to change between dashboards.

As Admin, you can move between all main views without changing account.

## 4. Admin Dashboard Overview
Open `Admin Dashboard` when you need to manage users, data, or system operations.

Main areas include:
- Password Reset Requests
- Create New User
- Existing Users & Actions
- Sync Performance
- Beacon API Sync
- Beacon CSV Upload
- Dashboard data reset actions
- Audit log review

## 5. Password Reset Requests
Use this section when a user has clicked `Forgot password?`.

Workflow:
1. open `Password Reset Requests`
2. choose the pending email
3. enter a temporary password
4. click `Set Temporary Password`

What happens:
- the temporary password is set
- the user is marked to change password at next login
- the request is marked as completed

## 6. Create New User
Use `Create New User` to add staff or funder accounts.

Required fields:
- full name
- email
- password
- at least one role

Roles available:
- `RPL`
- `ML`
- `Manager`
- `Admin`
- `Funder`

If you assign `Funder`:
- choose an existing funder name, or
- enter a new funder name manually

## 7. Existing Users and Actions
This area allows three main actions.

### 7.1 Reset Password
1. select a user
2. enter a new password
3. click `Reset Password`

### 7.2 Update Role
1. select a user
2. choose the new role set
3. if `Funder` is included, choose or enter the funder name
4. enter a reason
5. confirm the change
6. click `Update Role`

### 7.3 Delete User
1. select a user
2. enter the reason
3. confirm deletion
4. click `Delete User`

Use deletion carefully. It removes the user from dashboard access.

## 8. Sync Performance
Use `Sync Performance` to inspect the Beacon import pipeline.

It shows:
- last total sync duration
- fetch duration
- transform duration
- upsert duration
- average total duration across recent successful syncs
- last successful sync time
- sync type, automatic or manual

Use this section when:
- the dashboard feels stale
- a sync appears slow
- you are checking whether overnight syncs are completing normally

## 9. Beacon API Sync
This is the main operational data refresh area.

### 9.1 Smoke Test
Use `Run Beacon API Smoke Test` to verify Beacon connectivity and shape without doing a full sync.

### 9.2 Manual Sync
Use `Sync Beacon API to Database` to run a manual sync.

While a sync is active you can:
- monitor progress
- stop the sync
- clear a stuck sync

The dashboard logs progress and status into the audit trail.

## 10. Beacon CSV Upload
Use this when importing Beacon exports manually.

Typical workflow:
1. click `Upload Beacon Exports`
2. add the relevant CSV files
3. click `Import`

Use this only when you intentionally want to import from export files rather than the Beacon API.

## 11. Refresh All Dashboard Data
This is an administrative reset action.

Use it carefully.

It is intended for situations where:
- dashboard data must be rebuilt
- import problems need a clean restart
- stale datasets must be cleared

Do not use it casually during active reporting.

## 12. Audit Logs
Admins can review audit history from the Admin Dashboard.

The audit trail includes:
- login-related admin activity
- role changes
- user deletion
- sync actions
- custom report save/share actions
- dashboard filter and UI interaction logs

Use it for:
- support investigations
- governance checks
- confirming who changed what

## 13. KPI Dashboard
Admins can use the KPI Dashboard in the same way as Managers, with one extra advantage:
- `Show KPI Debug` is available for deeper validation

Admins can also see participant names and IDs in KPI event drill-downs where source data supports it.

## 14. Custom Reports Dashboard
Admins have full access to all report types and exports.

Recommended uses:
- operational analysis
- data QA
- export packs
- funding checks
- distance analysis

Remember:
- click `Apply Report Filters`
- click `Apply Advanced Filters` when advanced settings change

## 15. ML Dashboard
Admins can use the ML Dashboard for event-by-event operational review.

This is especially useful when troubleshooting:
- missing attendee detail
- unexpected participant counts
- medical or emergency data field mapping

## 16. Funder Dashboard
Admins can use the Funder Dashboard with:
- region filter
- timeframe filter
- selectable funder

Use it for:
- preparing funder-facing summaries
- checking funding trends
- monitoring bids and grants by funder

## 17. Case Studies
Admins can:
- read case studies
- filter by date and region
- upload new case studies

## 18. Best Practice for Admins
- use Smoke Test before troubleshooting full sync failure
- use Manual Sync when urgent fresh data is required
- record meaningful reasons for role changes and deletions
- use audit logs before making assumptions about user behaviour
- prefer role updates over account recreation when possible

## 19. Troubleshooting
### Admin client not available
- check Supabase secrets
- confirm the service role configuration is present

### Sync appears stuck
- use `Stop Manual API Sync`
- if needed, use `Clear Stuck Sync`

### Users cannot log in
- check whether they have a pending password reset
- reset their password manually if needed
- confirm their role assignment exists

### Dashboard data looks outdated
- check `Last Data Refresh`
- check Sync Performance
- run a smoke test or manual sync if appropriate
