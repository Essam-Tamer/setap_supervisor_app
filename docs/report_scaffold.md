# SETAP Referral/Deferral Report Scaffold

This scaffold is designed around the uploaded mark scheme. Replace all bracketed
notes with your own evidence, screenshots and wording before submission.

## Chapter 1: Problem Specification

### 1.1 Problem Context

[Explain the final year project supervision problem: staff have research interests
and project ideas; students need a way to browse staff profiles before choosing a
supervisor.]

### 1.2 Requirements Elicitation Process

Recommended honest approach:

- Participants: 4-6 final year or second year students, plus 1-2 staff/tutor perspectives if possible.
- Method: short semi-structured interviews or questionnaire.
- Rationale: students are the primary browsing users; staff are profile-maintenance users.
- Data collected: anonymised notes, answers, and any recurring concerns.
- Analysis method: thematic analysis, grouping answers into themes such as discoverability,
  staff expertise clarity, project availability, and contact confidence.

Include:

- who you asked
- why they were relevant
- what questions you used
- how you analysed the answers
- what patterns appeared

### 1.3 Key Findings

Use a table like this:

| Finding | Evidence Source | Design Impact |
| --- | --- | --- |
| Students need to search by topic, not only staff name. | [Participant evidence] | Add search over areas and project titles. |
| Students need project availability/status. | [Participant evidence] | Add project status field. |
| Staff need quick profile maintenance. | [Participant evidence] | Add staff workspace with CRUD forms. |

### 1.4 User Requirements

| ID | User Requirement | Source |
| --- | --- | --- |
| UR1 | Staff should be able to create and maintain their profile. | [Interview/brief] |
| UR2 | Staff should be able to add, update and delete areas of interest. | [Brief/staff evidence] |
| UR3 | Staff should be able to add, update and delete project ideas. | [Brief/staff evidence] |
| UR4 | Students should be able to browse staff profiles. | [Brief/student evidence] |
| UR5 | Students should be able to search by topic, department or project idea. | [Student evidence] |

### 1.5 System Requirements

| ID | Type | Linked UR | System Requirement | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR1 | Functional | UR1 | The system shall allow staff profiles to be created, updated and deleted. | Valid profile details can be saved, edited and removed. |
| FR2 | Functional | UR2 | The system shall allow areas of interest to be added and removed from staff profiles. | Areas appear on the public staff profile and can be removed. |
| FR3 | Functional | UR3 | The system shall allow staff project ideas to be created, edited and deleted. | Project title, description, level, capacity and status are stored and displayed. |
| FR4 | Functional | UR4/UR5 | The system shall allow students to browse and search staff profiles. | Search returns matching staff by name, department, area or project title. |
| NFR1 | Non-functional | UR4 | The interface should be usable on desktop and mobile-width screens. | Layout remains readable at narrow viewport widths. |
| NFR2 | Non-functional | UR1 | The system should preserve data between sessions. | SQLite stores staff, areas and projects after restart. |
| NFR3 | Non-functional | UR1 | The system should validate profile and project data. | Empty required fields, invalid email and invalid capacity are rejected. |
| NFR4 | Non-functional | UR4 | The browse page should respond within two seconds for the prototype dataset. | Manual local timing remains below two seconds. |
| NFR5 | Non-functional | UR1-UR5 | The implementation should be maintainable and traceable. | Data, validation, routing and tests are separated and requirement IDs appear in the test plan. |
| NFR6 | Non-functional | UR4 | Core pages should work in current Safari and Chrome versions. | Browse, profile and workspace pages render without broken layouts. |

## Chapter 2: Design

### 2.1 Architecture

Use this explanation:

The prototype follows a layered web architecture. The browser sends HTTP requests
to a Python server. Route handlers process student browse and staff workspace
actions. Data access functions validate and store profile, area and project records
in SQLite. This pattern was chosen because the coursework needs a small web
prototype with persistent CRUD operations and clear traceability between
requirements, routes, data functions and tests.

Suggested architecture diagram content:

- Browser/UI layer
- HTTP route/controller layer
- Validation/application logic
- SQLite persistence layer
- Entities: Staff, AreaOfInterest, ProjectIdea

### 2.2 Use Case Diagram

Actors:

- Student
- Staff member

Use cases:

- Browse staff profiles
- Search staff/project ideas
- View staff profile
- Manage staff profile
- Manage areas of interest
- Manage project ideas

### 2.3 Detailed Use Case Specifications

Include 5 detailed specs:

1. Browse staff profiles
2. Search staff/project ideas
3. View staff profile
4. Manage areas of interest
5. Manage project ideas

For each:

- Primary actor
- Preconditions
- Main success scenario
- Alternative/error flows
- Postconditions
- Linked requirements

Use `docs/design.md` for the prepared architecture, data model and five detailed
specifications. Redraw or export the diagrams for the final report and explain them
in your own words.

## Chapter 3: Implementation

### 3.1 Repository Link

[Add GitHub repository link after you create/push the repo.]

### 3.2 Demo Link

[Add 3-5 minute demo link.]

### 3.3 Technology Stack

- Python standard library HTTP server
- SQLite database
- HTML/CSS templates generated server-side
- `unittest` automated tests

### 3.4 Implemented Features

Map features to requirements:

| Requirement | Implementation Evidence |
| --- | --- |
| FR1 | Staff workspace profile create/edit/delete forms. |
| FR2 | Area add/remove controls on staff edit page. |
| FR3 | Project idea create/edit/delete forms. |
| FR4 | Student browse/search pages. |
| NFR2 | SQLite persistence. |
| NFR3 | Validation functions and automated tests. |

### 3.5 Code Quality

Mention:

- data access functions separated from request handlers
- validation functions tested independently
- Git commits show incremental development
- test files included in repository

## Chapter 4: Testing

### 4.1 Testing Strategy

Explain that testing combines:

- automated unit tests for validation and data operations
- manual system tests for browser workflows
- partition testing for valid, invalid and boundary inputs

### 4.2 Requirement-To-Test Matrix

Use `docs/test_plan.csv` as the base.

### 4.3 Automated Test Evidence

Run:

```bash
python3 -m unittest discover -s tests
```

Paste or screenshot the output.

### 4.4 Evaluation

Discuss:

- what passed
- what defects were found
- what you fixed
- limitations, such as no real authentication in the prototype

## Final Checklist Against The Mark Scheme

- [ ] Requirements gathering process includes design, motivation, data and analysis.
- [ ] User requirements are clear statements with sources.
- [ ] System requirements clearly translate user requirements into functional and non-functional requirements.
- [ ] Architecture pattern is named and justified.
- [ ] Architecture components are explained and linked to requirements.
- [ ] At least 5 representative use cases are specified.
- [ ] Demo link is included.
- [ ] Repository link is included.
- [ ] Test plan covers every requirement.
- [ ] Automated test evidence or complete manual test evidence is included.
