# Admin Dashboard Manual

> Audience: `Admin` users  
> Scope: user management, data refresh operations, audit review, and full reporting access

![Admin dashboard annotated guide](images/admin-dashboard-guide.svg)

## 1. What this manual covers
Admins have the broadest access in the Regional KPI Dashboard. This role is responsible for:

- maintaining user access
- handling password reset requests
- assigning and updating roles
- monitoring Beacon sync health
- triggering manual sync or CSV import when needed
- reviewing audit activity
- supporting Managers, RPLs, MLs, and Funders

Available views:

- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Funder Dashboard`
- `ML Dashboard`

## 2. Before you start
Use this checklist before making any administrative change:

1. Confirm you are signed in with your own Admin account.
2. Check the `Last Data Refresh` card in the sidebar.
3. Record a clear business reason before changing roles, deleting users, or resetting data.
4. Prefer the smallest action that solves the problem.

![Navigation and screen areas](images/dashboard-navigation.svg)

## 3. Signing in and moving around
1. Open the dashboard URL.
2. Enter your email address and password.
3. If prompted, change your password before continuing.
4. Use `View Mode` in the left sidebar to move between dashboards.

If the application reports `Admin client not available`, the admin Supabase configuration is likely incomplete and should be checked before you continue.

## 4. Admin Dashboard screen tour
The `Admin Dashboard` is the operational control panel for the application.

Main areas:

- `Password Reset Requests`: pending self-service reset requests
- `Create New User`: create staff, admin, ML, RPL, manager, or funder users
- `Existing Users & Actions`: reset passwords, update roles, delete users
- `Sync Performance`: timing and status for recent sync activity
- `Beacon API Sync`: smoke test, manual sync, stop, and stuck-sync controls
- `Beacon CSV Upload`: manual import from exported CSV files
- data reset actions: controlled rebuild or refresh operations
- `Audit Logs`: review of administrative and user activity

## 5. User management workflows
### 5.1 Handle a password reset request
Use this when a user has selected `Forgot password?` and needs access restored.

1. Open `Password Reset Requests`.
2. Select the pending email address.
3. Enter a temporary password.
4. Click `Set Temporary Password`.
5. Tell the user to sign in and change the password immediately.

Expected result:

- the request is marked as completed
- the user is forced to change password on next login
- the action is recorded in the audit trail

### 5.2 Create a new user
1. Open `Create New User`.
2. Enter full name, email, and a starting password.
3. Select one or more roles.
4. If `Funder` is included, choose the funder name or enter a new one.
5. Submit the form.

Good practice:

- use named organisational email addresses where possible
- avoid shared accounts
- confirm the least-privilege role before saving

### 5.3 Reset an existing user's password
1. Find the user in `Existing Users & Actions`.
2. Choose `Reset Password`.
3. Enter the new temporary password.
4. Confirm the reset.

Use this when the self-service route is unavailable or urgent support is required.

### 5.4 Update roles
1. Select the user.
2. Choose the revised role set.
3. If `Funder` is included, verify the mapped funder.
4. Enter a reason that explains the change.
5. Confirm and apply the update.

Prefer updating the role over deleting and recreating an account. It preserves continuity and makes the audit history easier to follow.

### 5.5 Delete a user
1. Select the user record.
2. Enter the deletion reason.
3. Confirm the action carefully.
4. Click `Delete User`.

Use deletion only when the account should no longer have dashboard access. If the person still works with the system, a role change is usually safer.

## 6. Sync and data operations
### 6.1 Read the Sync Performance panel
Use `Sync Performance` to understand whether the data pipeline is healthy.

Key indicators:

- last total sync duration
- fetch, transform, and upsert timings
- average duration across recent successful syncs
- last successful sync time
- whether the latest run was `automatic` or `manual`

Use this section when:

- the dashboard looks stale
- overnight syncs may have failed
- a manual sync seems slower than expected

### 6.2 Run a Beacon smoke test
Use `Run Beacon API Smoke Test` first when diagnosing a sync issue.

This is the lowest-risk check because it validates connectivity and response shape without running a full import.

### 6.3 Run a manual sync
1. Open `Beacon API Sync`.
2. Start with a smoke test if you are troubleshooting.
3. Click `Sync Beacon API to Database`.
4. Monitor progress messages.
5. Use `Stop Manual API Sync` only if the run is genuinely stuck or was started by mistake.
6. Use `Clear Stuck Sync` only after confirming no live sync is still running.

### 6.4 Upload Beacon CSV exports
Use this route only when you intentionally want to import exported files instead of using the API.

1. Open `Beacon CSV Upload`.
2. Select the required CSV files.
3. Start the import.
4. Review the outcome before moving on to reporting.

### 6.5 Refresh or rebuild data
Administrative reset actions should be treated as controlled maintenance tasks.

Use them only when:

- a failed import needs a clean restart
- the working dataset must be rebuilt
- support or data QA has agreed a reset is necessary

Do not use them casually during active reporting periods.

## 7. Audit logs
Audit review is the first place to look before assuming a user error or data issue.

The log can help confirm:

- who changed a role
- who reset a password
- who started a sync
- who deleted a user
- who saved or shared reports
- which major dashboard interactions took place

Use the audit trail for support tickets, governance checks, and internal accountability.

## 8. Using the other dashboards as Admin
Admins can use every operational and reporting view.

### KPI Dashboard
- full regional KPI access
- drill-down into supporting rows
- `Show KPI Debug` for validation checks
- attendee names and IDs visible where source data supports them

### Custom Reports Dashboard
- all datasets and report outputs
- CSV export
- advanced filter controls
- distance analysis for participant travel review

### ML Dashboard
- event-by-event operational review
- participant, medical, and emergency fields where available
- raw event payload for support investigation

### Funder Dashboard
- funder summary view with selectable funder
- useful for preparing sponsor updates or QA of funder-facing figures

### Case Studies
- read, filter, and upload qualitative evidence

## 9. Recommended admin operating pattern
1. Check `Last Data Refresh`.
2. Review `Sync Performance` if the data looks old.
3. Run a smoke test before a manual sync.
4. Make user-access changes with a clear reason recorded.
5. Validate suspicious numbers in KPI or Custom Reports before responding to stakeholders.
6. Review audit logs if the history of an issue is unclear.

## 10. Troubleshooting
### `Admin client not available`
- check the admin Supabase secrets and service-role configuration
- confirm the application has the required admin credentials loaded

### Sync appears stuck
- review the sync status first
- use `Stop Manual API Sync` if a manual run is genuinely hung
- use `Clear Stuck Sync` only after confirming the process is not still active

### Users cannot sign in
- check whether there is a pending reset request
- reset the password manually if needed
- confirm the account still has a valid role assignment

### Dashboard data looks out of date
- check `Last Data Refresh`
- review `Sync Performance`
- run a smoke test, then a manual sync if needed

### A user asks for more access
- review whether a role change is sufficient
- apply least privilege
- record the reason in the audit trail
