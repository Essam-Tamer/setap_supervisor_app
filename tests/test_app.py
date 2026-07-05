import sqlite3
import tempfile
import unittest
from pathlib import Path

import app


class SupervisorMatchTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "test.sqlite3"
        self.conn = app.get_connection(self.db_path)
        app.init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tempdir.cleanup()

    def test_seed_creates_staff_with_projects_and_areas(self):
        app.seed_db(self.conn)
        staff = app.list_staff(self.conn)

        self.assertGreaterEqual(len(staff), 3)
        self.assertTrue(any("Requirements Engineering" in row["areas"] for row in staff))
        self.assertTrue(any(row["project_count"] > 0 for row in staff))

    def test_search_matches_area_and_project_titles(self):
        app.seed_db(self.conn)

        ai_results = app.list_staff(self.conn, "responsible ai")
        project_results = app.list_staff(self.conn, "traceable requirements")

        self.assertEqual(len(ai_results), 1)
        self.assertEqual(ai_results[0]["name"], "Dr Aisha Rahman")
        self.assertEqual(len(project_results), 1)
        self.assertEqual(project_results[0]["name"], "Dr Claudia Iacob")

    def test_staff_validation_rejects_missing_and_bad_email(self):
        errors = app.validate_staff(
            {
                "name": "",
                "email": "bad-email",
                "title": "Lecturer",
                "department": "Computing",
                "bio": "Research profile",
                "office_hours": "Monday",
            }
        )

        self.assertIn("Name is required.", errors)
        self.assertIn("Email must be a valid address.", errors)

    def test_create_update_delete_staff_profile(self):
        data = {
            "name": "Dr Sam Reed",
            "email": "sam.reed@example.ac.uk",
            "title": "Lecturer",
            "department": "Data Science",
            "bio": "Supervises data visualisation projects.",
            "office_hours": "Mondays 10:00-11:00",
        }

        staff_id = app.create_staff(self.conn, data)
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(profile["staff"]["name"], "Dr Sam Reed")

        data["department"] = "Applied Data Science"
        app.update_staff(self.conn, staff_id, data)
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(profile["staff"]["department"], "Applied Data Science")

        app.delete_staff(self.conn, staff_id)
        self.assertIsNone(app.get_staff_profile(self.conn, staff_id))

    def test_project_crud_and_capacity_validation(self):
        staff_id = app.create_staff(
            self.conn,
            {
                "name": "Dr Priya Cole",
                "email": "priya.cole@example.ac.uk",
                "title": "Senior Lecturer",
                "department": "Software Engineering",
                "bio": "Supervises web app projects.",
                "office_hours": "Thursdays",
            },
        )
        invalid = app.validate_project(
            {
                "title": "Portal",
                "description": "Build a portal.",
                "level": "BSc",
                "capacity": "0",
                "status": "Open",
            }
        )
        self.assertIn("Capacity must be between 1 and 8.", invalid)

        invalid_high = {
            "title": "Portal",
            "description": "Build a portal.",
            "level": "BSc",
            "capacity": "9",
            "status": "Open",
        }
        self.assertIn(
            "Capacity must be between 1 and 8.",
            app.validate_project(invalid_high),
        )

        project = {
            "title": "Supervisor Portal",
            "description": "Build a profile browsing portal.",
            "level": "BSc",
            "capacity": "2",
            "status": "Open",
        }
        app.create_project(self.conn, staff_id, project)
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(len(profile["projects"]), 1)

        project_id = profile["projects"][0]["id"]
        project["status"] = "Limited"
        app.update_project(self.conn, project_id, project)
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(profile["projects"][0]["status"], "Limited")

        app.delete_project(self.conn, project_id)
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(len(profile["projects"]), 0)

    def test_area_create_and_delete(self):
        staff_id = app.create_staff(
            self.conn,
            {
                "name": "Dr Lee Chen",
                "email": "lee.chen@example.ac.uk",
                "title": "Lecturer",
                "department": "Computing",
                "bio": "Supervises accessible software projects.",
                "office_hours": "Wednesdays",
            },
        )

        app.create_area(self.conn, staff_id, "Accessibility")
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(profile["areas"][0]["name"], "Accessibility")

        app.delete_area(self.conn, profile["areas"][0]["id"])
        profile = app.get_staff_profile(self.conn, staff_id)
        self.assertEqual(profile["areas"], [])

    def test_data_persists_across_database_connections(self):
        app.create_staff(
            self.conn,
            {
                "name": "Dr Morgan Hale",
                "email": "morgan.hale@example.ac.uk",
                "title": "Reader",
                "department": "Computing",
                "bio": "Supervises dependable systems projects.",
                "office_hours": "Fridays",
            },
        )
        self.conn.close()

        self.conn = app.get_connection(self.db_path)
        staff = app.list_staff(self.conn)
        self.assertEqual(staff[0]["name"], "Dr Morgan Hale")

    def test_unique_email_constraint_supports_data_quality(self):
        data = {
            "name": "Dr One",
            "email": "unique@example.ac.uk",
            "title": "Lecturer",
            "department": "Computing",
            "bio": "Bio",
            "office_hours": "Monday",
        }
        app.create_staff(self.conn, data)

        with self.assertRaises(sqlite3.IntegrityError):
            app.create_staff(self.conn, data)

    def test_rendered_staff_data_is_html_escaped(self):
        app.create_staff(
            self.conn,
            {
                "name": "Dr <script>alert(1)</script>",
                "email": "escaped@example.ac.uk",
                "title": "Lecturer",
                "department": "Computing & Design",
                "bio": "Safe output",
                "office_hours": "Monday",
            },
        )

        rendered = app.staff_card(app.list_staff(self.conn)[0])
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("Computing &amp; Design", rendered)

    def test_layout_escapes_title_and_flash_message(self):
        rendered = app.layout("A & B", "<p>Content</p>", "Saved <success>").decode()

        self.assertIn("A &amp; B | Supervisor Match", rendered)
        self.assertIn("Saved &lt;success&gt;", rendered)
        self.assertIn("<p>Content</p>", rendered)

    def test_stylesheet_contains_responsive_breakpoint(self):
        stylesheet = (app.BASE_DIR / "static" / "style.css").read_text()

        self.assertIn("@media (max-width: 760px)", stylesheet)
        self.assertIn("grid-template-columns: 1fr", stylesheet)


if __name__ == "__main__":
    unittest.main()
