# Supervisor Match

Supervisor Match is a small web prototype for the SETAP referral/deferral brief.
It lets staff maintain profiles, areas of interest and project ideas, while students
can browse and search staff profiles before choosing a final year project supervisor.

## Features

- Student-facing staff browse page with search by name, department, interests and project titles.
- Staff workspace for adding, updating and deleting staff profiles.
- CRUD support for staff areas of interest.
- CRUD support for staff project ideas.
- SQLite persistence with seeded demo data.
- Input validation for required fields, email format, unique emails and project capacity.
- Automated tests using Python's built-in `unittest`.

## Run The Prototype

```bash
python3 app.py
```

Then open:

```text
http://127.0.0.1:8000
```

To use a different port:

```bash
PORT=5001 python3 app.py
```

The server is local-only by default. For a container-based preview, explicitly bind
to all interfaces:

```bash
HOST=0.0.0.0 python3 app.py
```

## Run Tests

```bash
python3 -m unittest discover -s tests
```

## Documentation

- `docs/design.md`: architecture, data model, five detailed use cases and route map.
- `docs/2555176 CW.docx`: polished final coursework report.
- `docs/test_plan.csv`: 21 requirement-linked automated and manual test cases.
- `docs/SETAP_Test_Plan.xlsx`: workbook version matching the previous test plan format.
- `docs/test_results.md`: latest verified automated result and remaining manual evidence.
- `docs/report_scaffold.md`: four-chapter structure mapped to the uploaded rubric.
- `docs/interview_pack.md`: ethical, anonymised requirements-gathering template.
- `docs/interview_response_template.md`: duplicate and complete once per participant.
- `docs/demo_script.md`: timed 3-5 minute recording script and checklist.
- `recordings/SETAP_Supervisor_Match_Demo.mp4`: checked demo recording.

## Coursework Mapping

- Staff add/update/delete areas of interest: implemented in the staff workspace.
- Staff add/update/delete project ideas: implemented in the staff workspace.
- Students browse staff profiles: implemented in the student browse page and profile pages.
- Search/filter support: implemented through the `/staff?q=...` search route.
- Persistence: SQLite database created on first run.
- Testing evidence: see the tests folder and generated test output when run locally.

## Demo Script

For a 3-5 minute demo, show:

1. Home page and purpose of the app.
2. Student browse page.
3. Search for a topic such as `security`, `requirements` or `AI`.
4. Open a staff profile and show areas/project ideas.
5. Open staff workspace.
6. Add a new staff profile.
7. Add an area of interest.
8. Add a project idea.
9. Edit the project status/capacity.
10. Delete the test project or test profile.

## Notes For Submission

Replace the sample staff/project data with your own demonstration data before recording.
Do not submit the report without adding your own requirements evidence and screenshots.
