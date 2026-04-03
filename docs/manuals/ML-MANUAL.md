# Mountain Leader Dashboard Manual

> Audience: `ML` users  
> Scope: event-by-event review, participant detail checks, and case study capture

![ML dashboard annotated guide](images/ml-dashboard-guide.svg)

## 1. Role overview
Mountain Leaders mainly use the dashboard for delivery support rather than broad management reporting.

Available views:

- `ML Dashboard`
- `Case Studies`

ML users cannot access:

- `Admin Dashboard`
- `KPI Dashboard`
- `Custom Reports Dashboard`
- `Funder Dashboard`

## 2. Quick start
1. Sign in with your dashboard account.
2. Use `View Mode` to switch between `ML Dashboard` and `Case Studies`.
3. Choose the correct region and timeframe before selecting an event.
4. Review the event panel first, then the participant details.

![Navigation and screen areas](images/dashboard-navigation.svg)

## 3. ML Dashboard purpose
The ML Dashboard is designed to help you work on one event at a time.

It supports:

- confirming you are looking at the correct event
- checking event information before delivery
- reviewing participant details where available
- surfacing medical and emergency fields when Beacon supplies them
- checking the raw source payload during troubleshooting

## 4. Filters and event selection
Use the sidebar to set:

- `All Regions` or a specific region
- timeframe

Then use the `Event` selector on the page to choose the event you need.

If the event list is empty:

- widen the timeframe
- switch to `All Regions`
- confirm the event has synced from Beacon

## 5. Event Details panel
Once an event is selected, the dashboard shows an `Event Details` area.

Typical fields include:

- event ID
- event name
- date
- region
- event type
- participant count
- location
- status
- description

Always check this panel first to confirm you are working in the right record.

## 6. Participant selection and detail
If attendee detail is available, the dashboard provides a participant chooser.

Typical workflow:

1. Select the event.
2. Open the participant selector.
3. Choose one participant at a time.
4. Review the available fields carefully.

Possible detail sections:

- `Personal Information`
- `Medical Information`
- `Emergency Contact Details`
- `Participant Record`

Not every attendee will have every field. Blank or missing sections usually mean Beacon did not provide that value.

## 7. Event-level medical and emergency information
Below the participant-level sections, the dashboard may also surface event-level medical or emergency fields extracted from the event payload.

Use these as an operational prompt, not as a substitute for normal safety procedures.

## 8. Raw Event Payload
The `Raw Event Payload` expander is for deeper checking.

Use it when:

- a value appears to be missing from the formatted sections
- support staff ask how Beacon stored a field
- you need to confirm exactly what synced into the app

Only use this section when needed. The formatted view is easier to read for day-to-day work.

## 9. Case Studies
ML users can also read and upload case studies.

This is useful after delivery when you want to capture:

- participant feedback
- outcome stories
- short event reflections

Suggested upload steps:

1. Open `Case Studies`.
2. Check whether the story already exists.
3. Add a descriptive title.
4. Paste the story text.
5. Choose the correct date and region.
6. Submit.

## 10. Good working practice
- set the correct date range before selecting an event
- confirm the event details panel before reviewing participants
- treat medical and emergency information carefully and only for operational need
- report missing attendee data to Managers or Admins when the source record should contain it

## 11. Troubleshooting
### No events are showing
- widen the timeframe
- choose `All Regions`
- confirm the event exists in Beacon and has synced

### No participant names are shown
- some events only sync counts or limited attendee data
- this depends on the Beacon source structure

### Medical or emergency sections are blank
- the source record may not contain those fields
- not all events or attendees include those values in Beacon

### The selected event looks wrong
- check the event date in the selector
- adjust the region and timeframe filters
- reselect the event after changing filters
