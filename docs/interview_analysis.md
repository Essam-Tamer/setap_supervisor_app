# Interview Analysis For Chapter 1

This file converts the anonymised interview responses into coursework evidence.
Use it to write the requirements process, findings, requirement traceability and
reflection sections. Do not include participant names or identifying details.

## Data Set

<table>
<tr><th>Code</th><th>Role</th><th>Date recorded</th><th>Consent</th><th>Notes</th></tr>
<tr><td>S1</td><td>Student</td><td>10 July 2026</td><td>Yes</td><td>Strong focus on interests, availability, search, favourites and mobile use.</td></tr>
<tr><td>S2</td><td>Student</td><td>12 July 2026</td><td>Yes</td><td>Strong focus on topic search, project skills, difficulty and updated data.</td></tr>
<tr><td>S3</td><td>Student</td><td>15 July 2026</td><td>Yes</td><td>Strong focus on comparison, capacity, simple navigation and last updated dates.</td></tr>
<tr><td>T1</td><td>Tutor</td><td>17 July 2026</td><td>Yes</td><td>Strong focus on consistent profile formats, staff updates, capacity and enquiry handling.</td></tr>
</table>

Date check: T1 is recorded as 17 July 2026. If the final report is completed
before that date, correct the date or confirm that it is the intended interview
date before submission.

## Method Summary

The requirements evidence was collected using short semi structured interviews
with three student participants and one tutor participant. Students were selected
because they represent the main browsing users of the system. The tutor view was
included to represent staff maintenance needs and to test whether the student
requirements were realistic from an academic staff perspective.

The questions covered supervisor selection, current difficulties, topic based
searching, staff profile content, usability, staff editing needs and additional
features. The answers were analysed using a simple thematic coding approach.
Repeated points were grouped into themes, then those themes were translated into
user requirements and system requirements.

## Thematic Coding

<table>
<tr><th>Theme</th><th>Supporting evidence</th><th>Design impact</th></tr>
<tr><td>Centralised supervisor information</td><td>S1, S2, S3 and T1 all said current information is spread across staff pages, emails, module documents or informal communication.</td><td>The prototype provides a single staff browsing area and a public profile page for each staff member.</td></tr>
<tr><td>Topic based discovery</td><td>All participants supported searching by topic or area of interest. Examples included AI, data science, web development, cybersecurity, mobile applications and machine learning.</td><td>The browse page includes keyword search across staff names, departments, biographies, areas of interest and project titles.</td></tr>
<tr><td>Consistent profile content</td><td>S1 and T1 noted inconsistent profile information. S2 and S3 wanted clearer information on expertise, qualifications, experience and project expectations.</td><td>Profiles use a consistent format with name, title, department, email, biography, office hours, interests and project ideas.</td></tr>
<tr><td>Project availability and capacity</td><td>S1, S2, S3 and T1 all referred to availability, capacity, remaining spaces or project status.</td><td>Project records include capacity and status fields so students can see whether a project is open, limited or closed.</td></tr>
<tr><td>Staff self maintenance</td><td>All participants said staff should be able to update profile details, interests and project ideas. T1 specifically noted that staff should not need technical support.</td><td>The staff workspace supports create, update and delete actions for profiles, areas of interest and project ideas.</td></tr>
<tr><td>Usability and mobile access</td><td>S1 mentioned phone use. S2 mentioned clear results and avoiding long paragraphs. S3 wanted visible filters and few steps. T1 wanted clear navigation.</td><td>The interface uses simple pages, visible search, short profile cards and responsive CSS for narrower screens.</td></tr>
<tr><td>Data currency and reliability</td><td>S2 warned that outdated information would reduce usefulness. S3 wanted last updated dates. T1 suggested reminders for staff to review profiles.</td><td>The implemented prototype supports staff updates. Last updated dates and reminders are recorded as future improvements.</td></tr>
</table>

## Requirements Derived From Interviews

<table>
<tr><th>ID</th><th>User requirement</th><th>Evidence source</th><th>Implemented</th></tr>
<tr><td>UR1</td><td>Staff should be able to create and maintain their own profile details.</td><td>S1, S2, S3, T1</td><td>Yes</td></tr>
<tr><td>UR2</td><td>Staff should be able to add, update and remove areas of interest.</td><td>S1, S2, S3, T1</td><td>Yes</td></tr>
<tr><td>UR3</td><td>Staff should be able to add, update and remove proposed project ideas.</td><td>S1, S2, S3, T1</td><td>Yes</td></tr>
<tr><td>UR4</td><td>Students should be able to browse staff profiles in a consistent format.</td><td>S1, S2, S3, T1</td><td>Yes</td></tr>
<tr><td>UR5</td><td>Students should be able to search by topic, area, staff details or project idea.</td><td>S1, S2, S3, T1</td><td>Yes</td></tr>
<tr><td>UR6</td><td>Students should be able to see project status, capacity and suitability information before contacting staff.</td><td>S1, S2, S3, T1</td><td>Partly. Status, level and capacity are implemented. Detailed prerequisites are a future improvement.</td></tr>
<tr><td>UR7</td><td>The system should be quick, simple and readable on mobile width screens.</td><td>S1, S2, S3, T1</td><td>Yes</td></tr>
</table>

## Requirement To Feature Traceability

<table>
<tr><th>Interview finding</th><th>User requirement</th><th>System requirement</th><th>Prototype evidence</th></tr>
<tr><td>Students find it difficult to compare information spread across emails, staff webpages and module documents.</td><td>UR4</td><td>FR4: allow students to browse staff profiles.</td><td>The staff browse page and staff profile page.</td></tr>
<tr><td>Students want to search by topics such as AI, cybersecurity, mobile applications or machine learning.</td><td>UR5</td><td>FR4: keyword search across staff and project information.</td><td>The staff listing search checks staff name, department, biography, areas and project titles.</td></tr>
<tr><td>Participants want to know whether a project or supervisor is still available.</td><td>UR6</td><td>FR3: store project title, description, level, capacity and status.</td><td>Project profile display includes level, capacity and status.</td></tr>
<tr><td>Staff should be able to update information without technical support.</td><td>UR1, UR2, UR3</td><td>FR1, FR2, FR3: create, read, update and delete operations for profiles, areas and projects.</td><td>Staff workspace routes in the prototype.</td></tr>
<tr><td>Users want a simple interface with clear navigation and mobile support.</td><td>UR7</td><td>NFR1, NFR4, NFR6.</td><td>Responsive CSS and manual or automated test plan coverage.</td></tr>
<tr><td>Outdated information would make the system less useful.</td><td>UR1, UR6</td><td>NFR2: data persists. NFR3: validation protects data quality.</td><td>SQLite persistence, validation and automated tests.</td></tr>
</table>

## Prioritisation

The first release prioritised the features most strongly supported by both the
coursework brief and the interviews: staff profile management, areas of interest,
project idea management, student browsing, search and project availability. These
features directly support the main supervision matching workflow.

Several interview suggestions were not implemented because they extend beyond the
core prototype scope.

<table>
<tr><th>Suggested feature</th><th>Source</th><th>Reason not included in this prototype</th></tr>
<tr><td>Save favourites</td><td>S1</td><td>Useful student convenience feature, but not required by the brief and would need user accounts.</td></tr>
<tr><td>Filter available projects only</td><td>S1</td><td>Feasible future improvement. Current profiles already display project status.</td></tr>
<tr><td>Project difficulty and recommended skills</td><td>S2, T1</td><td>Partly represented by project level. Detailed skill tagging would need extra data design.</td></tr>
<tr><td>Compare supervisors side by side</td><td>S3</td><td>Useful but secondary to the core browse, search and profile workflow.</td></tr>
<tr><td>Last updated dates and staff reminders</td><td>S3, T1</td><td>Important for production reliability, but not essential to demonstrate the coursework prototype.</td></tr>
<tr><td>Expression of interest or enquiry function</td><td>T1</td><td>Useful workflow extension, but it raises process and expectation issues because enquiries do not guarantee acceptance.</td></tr>
</table>

## Limitations To Mention

1. The sample is small and based on convenience participants, so the findings
support a prototype rather than a full institutional deployment.

2. Three student views and one tutor view were included. Further staff interviews
would strengthen the staff workflow evidence.

3. The interviews produced several useful future features that were not all
implemented, showing that the prototype is a first iteration.

4. The prototype does not include authentication, reminders, favourites or formal
application handling. These should be discussed as future work.

## Short Report Paragraph

The interview findings showed a consistent problem: students need a central place
to discover staff interests and proposed projects because current information is
spread across emails, staff webpages, module documents and informal communication.
All participants supported topic based searching, and all referred to the need for
clear project availability or capacity information. The tutor response also
confirmed that staff should be able to maintain profile and project information
without technical support. These findings directly informed the core requirements:
student browsing, topic search, consistent staff profiles, project status and
capacity fields, plus a staff workspace for maintaining profiles, interests and
project ideas.
