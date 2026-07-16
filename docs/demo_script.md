# Demo Video Script

Target length: 3 to 5 minutes. Record the final build in one clear pass where
possible. Do not show passwords, personal files or unrelated browser tabs.

## Opening

Time: 0:00 to 0:25

Say:

This is my SETAP supervisor matching prototype. The purpose of the system is to
help students find suitable project supervisors by browsing staff profiles, areas
of interest and project ideas. It also gives staff a simple workspace where they
can maintain their profile, interests and proposed projects.

Show:

1. The home page.
2. The two main entry points, Student browse and Staff workspace.

## Student Browse And Search

Time: 0:25 to 1:10

Say:

I will start with the student side. Students can browse staff profiles in one
place instead of checking separate emails, staff pages or module documents. This
responds to the interview evidence where students said supervisor information is
often spread across different places.

Show:

1. Open the staff browse page.
2. Point out staff names, departments, interests and project counts.
3. Search for responsible AI.
4. Search for traceable requirements.

Say:

The search checks staff information, departments, biographies, areas of interest
and project titles. This supports the requirement that students should be able to
search by topic or project idea.

## Public Staff Profile

Time: 1:10 to 1:50

Say:

Now I will open a staff profile. The profile uses a consistent format so students
can compare supervisors more easily.

Show:

1. Open one staff profile from the search results.
2. Show the biography.
3. Show office hours.
4. Show areas of interest.
5. Show project title, description, level, capacity and status.

Say:

Capacity and status were included because interview participants wanted to know
whether a project or supervisor was still available before contacting staff.

## Staff Workspace

Time: 1:50 to 3:20

Say:

I will now show the staff workspace. This side supports staff maintenance of
profiles, interests and project ideas.

Show:

1. Open the staff workspace.
2. Create a demonstration staff profile or edit an existing demonstration profile.
3. Add an area of interest.
4. Remove an area of interest.
5. Add a project idea.
6. Edit the project status or capacity.
7. Show one validation error, for example an invalid email address or capacity set to zero.

Say:

The validation is included to improve data quality. Staff can update information
without technical support, which was also raised in the interview evidence.

## Testing And Quality

Time: 3:20 to 4:15

Say:

The project includes automated tests and a manual test plan. The automated tests
cover database seeding, search, staff profile actions, project actions,
validation, persistence, duplicate email protection, output escaping and
responsive styling.

Show:

1. Open the terminal.
2. Run the unittest command from the README file.
3. Show that all 11 tests pass.
4. Open the test plan file.
5. Mention that the test plan maps test cases to the functional and non functional requirements.

Say:

The test plan covers the main requirements and the automated result shows that
the implemented behaviours pass in the current version.

## Closing

Time: 4:15 to 4:45

Say:

In summary, the prototype implements the required staff and student workflows:
staff profile management, interest management, project idea management, student
browsing and topic search. The main limitation is that authentication is outside
this prototype, so a production version would need secure staff accounts before
deployment.

## Recording Checklist

1. Keep the video between 3 and 5 minutes.
2. Use the final repository version and final dataset.
3. Make text readable.
4. Keep cursor movement deliberate.
5. Show successful behaviour.
6. Show one validation case.
7. Confirm the uploaded video link is viewable by the marker.
8. Do not claim manual tests passed unless they were actually performed.
