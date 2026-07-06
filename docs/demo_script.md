# Demo Video Script

Target length: 3 to 5 minutes. Record the final build in one clear pass where
possible. Do not show passwords, personal files or unrelated browser tabs.

## 0:00-0:25 Introduction

State your name, module/coursework title and the problem solved:

"Supervisor Match allows staff to maintain research interests and project ideas,
and allows students to browse and search staff profiles when choosing a final year
project supervisor."

## 0:25-1:10 Student Browse And Search

1. Open `/staff`.
2. Briefly identify the profile summaries, interests and project counts.
3. Search for `responsible AI` or `traceable requirements`.
4. Explain that search covers staff, department, research area and project title.

## 1:10-1:45 Public Profile

1. Open a matching staff profile.
2. Show biography, office hours and areas of interest.
3. Show project title, description, level, capacity and status.
4. Link these fields to the student requirements found in interviews.

## 1:45-3:20 Staff Workspace

1. Open `/admin`.
2. Create or edit a demonstration staff profile.
3. Add and remove an area of interest.
4. Add a project idea.
5. Edit its status or capacity.
6. Delete the demonstration project or profile.
7. Briefly show one validation error, such as capacity `0` or an invalid email.

## 3:20-4:10 Testing And Quality

1. Show the terminal command `python3 -m unittest discover -s tests -v`.
2. Show that all 11 tests pass.
3. Mention the 21-case requirement-linked test plan.
4. State that SQLite preserves data between sessions and input is HTML-escaped.

## 4:10-4:40 Closing

Summarise what is implemented and state one honest limitation:

"The prototype implements the required staff and student workflows. A current
limitation is that authentication and authorisation are outside this prototype, so
the staff workspace would need secured accounts before production deployment."

## Recording Checklist

- Keep the video between 3 and 5 minutes.
- Use the final repository version and final dataset.
- Make text readable and keep the cursor movement deliberate.
- Show successful behaviour as well as one validation case.
- Confirm the uploaded video link is viewable by the marker.
- Do not claim manual tests passed unless they were actually performed.
