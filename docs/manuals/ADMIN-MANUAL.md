# Admin Dashboard Manual

> Audience: `Admin` users  
> Scope: user accounts, password resets, data refresh, audit review, and full reporting access

![Admin dashboard annotated guide](images/admin-dashboard-guide.svg)

## 1. Introduction
This manual explains how to use the dashboard as an `Admin`.

Admins are responsible for keeping the system working safely and making sure the right people have the right access.

Admin users can open:

- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Case Studies`
- `Data Request Form`
- `Funder Dashboard`
- `ML Dashboard`

Admin access should be used carefully. Many actions affect other users. Some actions affect the whole dataset or the overall health of the dashboard.

## 2. What the Admin role is for
The `Admin` role is designed for:

- user account management
- role assignment
- password support
- sync monitoring
- manual sync actions
- controlled data maintenance
- audit review
- support investigations

The Admin role is not simply a stronger reporting role. It is an operational support role with governance responsibility.

## 3. Before you make changes
Before making any important change:

1. Confirm that you are signed in with your own named Admin account.
2. Check `Last Data Refresh`.
3. Be clear about what problem you are solving.
4. Use the smallest action that solves it.
5. Record a clear reason for any significant access change or destructive action.

Good Admin habits:

- avoid shared accounts
- avoid deleting users unless removal is genuinely required
- prefer updating an existing user rather than recreating them
- check the audit log if you are not sure what already happened

![Navigation and screen areas](images/dashboard-navigation.svg)

## 4. Signing in and moving around
1. Open the dashboard link.
2. Enter your email address and password.
3. Change your password if prompted.
4. Use `View Mode` in the left sidebar to move between screens.

If you see a message such as `Admin client not available`, some Admin configuration is missing. In that situation, user-management functions may not work correctly and should be checked before you continue.

## 5. Main areas of the Admin Dashboard
The `Admin Dashboard` is the control centre for administration and support.

Main sections usually include:

- `Password Reset Requests`
- `Create New User`
- `Existing Users & Actions`
- `Sync Performance`
- `Beacon API Sync`
- `Beacon CSV Upload`
- reset or rebuild actions
- `Audit Logs`

Think of the page in three broad areas:

1. user access and security
2. sync and data operations
3. audit and investigation

## 6. Password reset requests
### 6.1 When to use this section
Use `Password Reset Requests` when a user has triggered `Forgot password?` and cannot complete sign-in.

### 6.2 Step-by-step reset workflow
1. Open `Password Reset Requests`.
2. Select the user's email address from the pending list.
3. Enter a temporary password.
4. Click `Set Temporary Password`.
5. Tell the user to sign in and change the password immediately.

### 6.3 What should happen next
After a successful reset:

- the reset request should be marked as completed
- the user should be prompted to change password at next sign-in
- the action should be recorded in the audit log

### 6.4 Good practice
- use a temporary password that is strong but can still be communicated safely
- avoid sending repeated resets unless necessary
- if the same user needs multiple resets, investigate whether there is a wider login problem

## 7. Creating a new user
### 7.1 When to create a new account
Create a new account when:

- a new staff member needs access
- an existing person needs a separate account
- a new funder contact needs a restricted reporting account

### 7.2 Step-by-step workflow
1. Open `Create New User`.
2. Enter the person's full name.
3. Enter their email address.
4. Enter a starting password.
5. Choose the role or roles.
6. If the user is not a funder, choose the correct region.
7. If the user is a funder, choose or enter the correct funder name.
8. Click `Create User`.
9. Confirm the creation result.

### 7.3 Choosing the correct role
Use least privilege.

Typical role choices:

- `RPL` for summary reporting and regional monitoring
- `Manager` for operational review across multiple views
- `ML` for event-by-event delivery work
- `Funder` for restricted summary access
- `Admin` only for people who genuinely need administrative control

### 7.4 Good practice
- use a named work email where possible
- avoid shared accounts
- check the region carefully
- check funder mapping carefully for funder users
- review the saved record after creation

## 8. Updating an existing user
The `Existing Users & Actions` area lets you manage current users without deleting and recreating them.

You can usually:

- reset a password
- update roles
- update user details
- delete a user

### 8.1 Reset Password
Use this when the user needs immediate access help and the self-service route is not enough.

Steps:

1. Open `Reset Password`.
2. Select the user.
3. Enter the temporary password.
4. Apply the change.
5. Tell the user to change the password after sign-in.

### 8.2 Update Role
Use this when a user's job changes or they need different access.

Steps:

1. Open `Update Role`.
2. Select the user.
3. Choose the correct role or roles.
4. If `Funder` is included, confirm the funder name carefully.
5. Enter the reason for the change.
6. Confirm the action.
7. Click `Update Role`.

Checks to make:

- does the user still need their previous role
- is the requested access broader than necessary
- is the reason clear enough for later audit review

### 8.3 Update User Details
Use this when a name, email address, or region needs correction.

Steps:

1. Open `Update User Details`.
2. Select the user.
3. Edit the full name if needed.
4. Edit the email address if needed.
5. Choose the correct region, or confirm the funder mapping for funder users.
6. Enter the reason for the update.
7. Confirm the action.
8. Click `Update User Details`.

### 8.4 Delete User
Delete a user only when the person should no longer retain access at all.

Steps:

1. Open `Delete User`.
2. Select the user.
3. Enter the reason for deletion.
4. Confirm the action.
5. Click `Delete User`.

Before deleting, ask:

- should the account be updated rather than deleted
- should the role simply be reduced
- is the reason clear enough for audit review

## 9. Sync Performance
### 9.1 What this section is for
`Sync Performance` helps you understand whether the data pipeline is healthy.

Use it when:

- the dashboard looks stale
- data appears to be missing
- a manual sync seems slow
- you need to know whether the latest refresh completed normally

### 9.2 What to review
Typical indicators may include:

- last total sync duration
- fetch time
- transform time
- upsert time
- average recent duration
- whether the latest run was automatic or manual

### 9.3 How to interpret it
Use this section to answer questions such as:

- did a sync actually complete
- was it unusually slow
- did the issue begin after a particular run

If the figures look normal but the data still looks wrong, the issue may be with source data rather than sync speed.

## 10. Beacon API Sync
### 10.1 Smoke test
Use `Run Beacon API Smoke Test` as the first low-risk check when troubleshooting connectivity or refresh issues.

It helps confirm:

- the Beacon connection is reachable
- the response shape is valid
- the dashboard can talk to the source

### 10.2 Manual sync
Use a manual sync when:

- the data is out of date
- you need the latest records immediately
- you are checking a support issue and need a fresh import

Step-by-step:

1. Open `Beacon API Sync`.
2. If you are troubleshooting, run a smoke test first.
3. Click `Sync Beacon API to Database`.
4. Watch the progress messages.
5. Wait for the success or error result.
6. Recheck the relevant dashboard view.

### 10.3 Stop or clear a stuck sync
Use `Stop Manual API Sync` only when a sync is genuinely stuck or was started in error.

Use `Clear Stuck Sync` only after checking that no live sync still is running.

These are intervention actions, not routine buttons.

## 11. Beacon CSV Upload
Use this when you are intentionally importing exported CSV files instead of relying on the API.

Typical reasons:

- API access is unavailable
- you have been asked to use a controlled export file set
- you are supporting a recovery or special maintenance task

Before using CSV upload:

1. Confirm why CSV upload is needed.
2. Confirm the files are the correct files.
3. Confirm the scope of what will be affected.

## 12. Data reset and rebuild actions
Reset or rebuild actions should be treated as controlled maintenance work.

Use them only when:

- a bad import needs to be cleared
- support work has agreed that a rebuild is required
- the dataset is clearly in a broken state

Before using a reset action:

1. Confirm the reason.
2. Confirm the target scope.
3. Check whether a smaller corrective action would solve the issue.
4. Record the reason clearly.

## 13. Audit Logs
The audit log is the main place to check what happened in the system.

Use it to answer questions such as:

- who changed a role
- who changed a profile
- who reset a password
- who started a sync
- who deleted a user

Use the audit log whenever the history of an issue is unclear.

## 14. Data Request Form and Temporary Access
Admins can use `Data Request Form` to both review requests and manage temporary access.

### 14.1 Reviewing requests
When a request is submitted:

- it is saved in the system
- `Admin` and `Manager` users are notified in the dashboard
- the request appears in the review section of `Data Request Form`

Admins can review the request list and change the request status to:

- `Pending`
- `In Review`
- `Completed`

### 14.2 Granting temporary access
Admins can also grant temporary access permissions to a single user from the same page.

This feature is designed for time-limited access only.

Required inputs include:

- the target user
- one or more temporary roles
- an expiry date and time
- the reason for the temporary access

Good practice:

- grant the smallest access needed
- set the shortest realistic expiry
- write a clear reason
- revoke access early if it is no longer needed

### 14.3 How temporary access behaves
Temporary access is additive. It adds temporary role access on top of the user's normal role until the expiry time or until it is revoked.

Use it when:

- a single user needs short-term access for a defined task
- permanent role change would be too broad
- a request has been reviewed and approved for limited-duration access

## 15. Using the other dashboards as an Admin
### 14.1 KPI Dashboard
Use this for:

- headline KPI review
- checking what operational users see
- opening drill-downs
- validating figures with `Show KPI Debug`

### 14.2 Custom Reports Dashboard
Use this for:

- detailed analysis
- exports
- charts
- advanced filtering
- comparison work
- distance analysis

Admins can also use it to:

- combine multiple datasets in one report
- validate whether row-level data supports a KPI
- compare groups directly with `Comparison Analysis`
- inspect travel patterns with `Distance Analysis`
- confirm what other roles will or will not see

### 14.3 ML Dashboard
Use this for:

- one-event-at-a-time checking
- operational detail review
- participant, medical, and emergency review where supported by source data

### 14.4 Funder Dashboard
Use this to check:

- what funder-facing users see
- whether sponsor-facing figures make sense
- whether the restricted presentation is appropriate

### 14.5 Case Studies
Use this for:

- reading supporting stories
- checking date and region tagging
- uploading new qualitative evidence

## 16. Recommended Admin working pattern
For most support issues:

1. Check `Last Data Refresh`.
2. Review `Sync Performance` if the data looks old or unusual.
3. Run a smoke test before a manual sync if troubleshooting.
4. Make access changes carefully and always record a clear reason.
5. Check `Audit Logs` if the history is unclear.
6. Verify the result in the relevant dashboard view after making a change.

## 17. Troubleshooting
### `Admin client not available`
Check the Admin-side configuration and confirm the required credentials are loaded correctly.

### A user cannot sign in
1. Check whether they requested a password reset.
2. Reset the password manually if needed.
3. Confirm the account still has a valid role.
4. Confirm the email address is correct.

### The dashboard looks out of date
1. Check `Last Data Refresh`.
2. Review `Sync Performance`.
3. Run a smoke test.
4. Run a manual sync if appropriate.

### A sync looks stuck
1. Review the current sync status.
2. Use `Stop Manual API Sync` only if needed.
3. Use `Clear Stuck Sync` only after confirming nothing active is still running.

### A user has the wrong access
1. Review the user's current role.
2. Confirm what access they actually need.
3. Update the role with a clear reason.
4. Ask the user to sign out and back in if needed.
