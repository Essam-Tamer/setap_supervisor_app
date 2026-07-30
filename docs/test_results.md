# Test Results

## Automated Run

- Date: 30 July 2026
- Command: `python3 -m unittest discover -s tests -v`
- Result: 11 tests run, 11 passed, 0 failed, 0 skipped.
- Duration: 0.029 seconds on the development machine.

Covered behaviours:

- database seeding
- topic and project-title search
- staff validation and CRUD
- project CRUD and capacity boundaries
- area create/delete
- duplicate-email integrity
- persistence across database connections
- HTML escaping of stored and flash-message content
- presence of the responsive CSS breakpoint

## Test Plan Status

`docs/test_plan.csv` contains 21 cases mapped to FR1-FR4 and NFR1-NFR6. The
workbook version is `docs/SETAP_Test_Plan.xlsx` and follows the previous test
plan format with method, signature, partition, inputs, expected output,
description and valid or invalid columns. The automated cases are implemented in
`tests/test_app.py`. Manual browser cases must be executed on the final
submission build and supported with the screenshots or recording named in the
evidence column.

Do not mark a manual case as passed until it has actually been performed. Record
the observed result, date, browser and evidence filename in the final report.

## Remaining Manual Evidence

- Desktop and mobile-width layout screenshots.
- Safari and Chrome compatibility checks.
- A timed browse-page load using the final dataset.
- Screenshots of profile, interest and project create/edit/delete workflows.
- The 3-5 minute demonstration recording.
