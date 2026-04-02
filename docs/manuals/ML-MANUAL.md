# Mountain Leader Dashboard Manual

## 1. Purpose
This manual is for `ML` users.

Mountain Leaders mainly use the dashboard for event-level operational support rather than broad management reporting.

ML users can access:
- `ML Dashboard`
- `Case Studies`

ML users cannot access:
- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Funder Dashboard`

## 2. Signing In
1. Open the dashboard.
2. Enter your email address and password.
3. Change your password if prompted.

If you cannot log in, contact an Admin.

## 3. Main Navigation
Use `View Mode` in the left sidebar.

Available ML views:
- `ML Dashboard`
- `Case Studies`

## 4. ML Dashboard Overview
The ML Dashboard is focused on one event at a time.

It is designed to help you:
- select an event
- review event details
- review participant information
- inspect medical and emergency contact fields where available

## 5. ML Dashboard Filters
In the sidebar:
1. choose `All Regions` or a specific region
2. choose a timeframe

The event list updates based on these filters.

## 6. Choosing an Event
Use the `Event` selector to choose the event you want.

The label normally includes:
- event name
- event date

If no events appear:
- widen the date range
- switch to `All Regions`
- confirm the event exists in Beacon

## 7. Event Details
After selecting an event, the dashboard shows an `Event Details` section.

Typical fields may include:
- event ID
- event name
- date
- region
- event type
- participant counts
- location
- status
- description

Use this section as your first operational check before reviewing attendees.

## 8. Participant Selection
If attendee data is available, the dashboard shows a participant chooser.

You can:
1. select a participant
2. review the selected attendee details

Depending on the source data, the dashboard may show:
- names
- IDs
- linked participant records

If attendee data is missing, the dashboard will tell you that names or IDs are not yet available.

## 9. Participant Detail Sections
For a selected participant, the dashboard may show:
- `Personal Information`
- `Medical Information`
- `Emergency Contact Details`
- `Participant Record`

These sections depend on what exists in the Beacon source data.

Important:
- not every attendee will have every field
- blank sections usually mean the source record does not contain those values

## 10. Event-Level Medical and Emergency Fields
Below participant details, the dashboard may also show event-level:
- `Medical Information`
- `Emergency Contact Details`

These are extracted from the event payload itself when present.

## 11. Raw Event Payload
Use the `Raw Event Payload` expander only when needed.

This is useful when:
- you need to confirm how a field is stored
- you are troubleshooting missing values
- support staff ask for exact source details

## 12. Case Studies
ML users can also open `Case Studies`.

You can:
- read existing case studies
- filter them by date and region
- upload new case studies

This is useful if you want to add qualitative feedback after delivery.

## 13. Best Practice for ML Users
- filter to the right date range before selecting an event
- check `Event Details` first
- then review named participants one by one
- use medical and emergency sections as a prompt to verify relevant details before delivery activity
- report missing or incomplete attendee fields to Admins if they should exist

## 14. Troubleshooting
### No events are showing
- widen the timeframe
- choose `All Regions`
- confirm the event has synced from Beacon

### No participant names are shown
- some events only sync counts or limited attendee detail
- this depends on Beacon source structure

### Medical or emergency sections are blank
- the source record may not contain those fields
- not all attendees or events hold those details in Beacon

### The selected event looks wrong
- check the event date in the selector
- switch region/timeframe filters and reselect
