from __future__ import annotations

import html
import os
import re
import sqlite3
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "supervisor_match.sqlite3"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))


def get_connection(db_path: Path | str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            department TEXT NOT NULL,
            bio TEXT NOT NULL,
            office_hours TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS areas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            level TEXT NOT NULL,
            capacity INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'Open',
            FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()


def seed_db(conn: sqlite3.Connection) -> None:
    existing = conn.execute("SELECT COUNT(*) FROM staff").fetchone()[0]
    if existing:
        return

    staff_rows = [
        (
            "Dr Claudia Iacob",
            "claudia.iacob@example.ac.uk",
            "Senior Lecturer",
            "Software Engineering",
            "Supervises projects around requirements engineering, human-centred design, software quality and prototyping.",
            "Tuesdays 10:00-12:00, Richmond Building",
            ["Requirements Engineering", "UX Evaluation", "Software Quality"],
            [
                (
                    "Traceable Requirements Assistant",
                    "Build a tool that helps students link interview evidence to user and system requirements.",
                    "BSc",
                    2,
                    "Open",
                ),
                (
                    "Usability Test Planner",
                    "Prototype a planner for building task-based usability studies and recording observations.",
                    "BSc/MSc",
                    1,
                    "Open",
                ),
            ],
        ),
        (
            "Dr Aisha Rahman",
            "aisha.rahman@example.ac.uk",
            "Lecturer",
            "Artificial Intelligence",
            "Interested in applied machine learning systems, responsible AI and practical model evaluation.",
            "Wednesdays 13:00-15:00, Lion Gate Building",
            ["Machine Learning", "Responsible AI", "Data Analysis"],
            [
                (
                    "Bias Dashboard for Student Data",
                    "Create a dashboard that highlights missing data, class imbalance and fairness risks before modelling.",
                    "MSc",
                    1,
                    "Open",
                )
            ],
        ),
        (
            "Prof Martin Evans",
            "martin.evans@example.ac.uk",
            "Professor",
            "Cyber Security",
            "Supervises security-focused projects involving web application hardening, authentication and threat modelling.",
            "Fridays 09:30-11:30, Buckingham Building",
            ["Web Security", "Authentication", "Threat Modelling"],
            [
                (
                    "Secure Supervisor Matching Portal",
                    "Design and test a small portal with access control, validation and audit-friendly security documentation.",
                    "BSc",
                    2,
                    "Open",
                )
            ],
        ),
    ]

    for name, email, title, department, bio, office_hours, areas, projects in staff_rows:
        cur = conn.execute(
            """
            INSERT INTO staff (name, email, title, department, bio, office_hours)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, email, title, department, bio, office_hours),
        )
        staff_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO areas (staff_id, name) VALUES (?, ?)",
            [(staff_id, area) for area in areas],
        )
        conn.executemany(
            """
            INSERT INTO projects (staff_id, title, description, level, capacity, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [(staff_id, *project) for project in projects],
        )
    conn.commit()


def ensure_database(db_path: Path | str = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        init_db(conn)
        seed_db(conn)


def clean_text(value: str, max_len: int = 500) -> str:
    return re.sub(r"\s+", " ", value.strip())[:max_len]


def validate_staff(data: dict[str, str]) -> list[str]:
    errors = []
    required = ["name", "email", "title", "department", "bio", "office_hours"]
    for field in required:
        if not clean_text(data.get(field, "")):
            errors.append(f"{field.replace('_', ' ').title()} is required.")
    email = clean_text(data.get("email", ""))
    if email and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("Email must be a valid address.")
    return errors


def validate_project(data: dict[str, str]) -> list[str]:
    errors = []
    if not clean_text(data.get("title", "")):
        errors.append("Project title is required.")
    if not clean_text(data.get("description", "")):
        errors.append("Project description is required.")
    try:
        capacity = int(data.get("capacity", "1"))
        if capacity < 1 or capacity > 8:
            errors.append("Capacity must be between 1 and 8.")
    except ValueError:
        errors.append("Capacity must be a number.")
    if data.get("status", "Open") not in {"Open", "Limited", "Closed"}:
        errors.append("Status must be Open, Limited or Closed.")
    return errors


def list_staff(conn: sqlite3.Connection, query: str = "") -> list[sqlite3.Row]:
    params: list[Any] = []
    where = ""
    if query:
        like = f"%{query.lower()}%"
        where = """
            WHERE lower(staff.name) LIKE ?
               OR lower(staff.department) LIKE ?
               OR lower(staff.bio) LIKE ?
               OR lower(COALESCE(area_names.names, '')) LIKE ?
               OR lower(COALESCE(project_titles.titles, '')) LIKE ?
        """
        params = [like, like, like, like, like]
    return conn.execute(
        f"""
        SELECT
            staff.*,
            COALESCE(area_names.names, '') AS areas,
            COALESCE(project_titles.titles, '') AS project_titles,
            COUNT(projects.id) AS project_count
        FROM staff
        LEFT JOIN (
            SELECT staff_id, GROUP_CONCAT(name, ', ') AS names
            FROM areas
            GROUP BY staff_id
        ) area_names ON area_names.staff_id = staff.id
        LEFT JOIN (
            SELECT staff_id, GROUP_CONCAT(title, ', ') AS titles
            FROM projects
            GROUP BY staff_id
        ) project_titles ON project_titles.staff_id = staff.id
        LEFT JOIN projects ON projects.staff_id = staff.id
        {where}
        GROUP BY staff.id
        ORDER BY staff.name
        """,
        params,
    ).fetchall()


def get_staff_profile(conn: sqlite3.Connection, staff_id: int) -> dict[str, Any] | None:
    staff = conn.execute("SELECT * FROM staff WHERE id = ?", (staff_id,)).fetchone()
    if not staff:
        return None
    areas = conn.execute(
        "SELECT * FROM areas WHERE staff_id = ? ORDER BY name", (staff_id,)
    ).fetchall()
    projects = conn.execute(
        "SELECT * FROM projects WHERE staff_id = ? ORDER BY status, title", (staff_id,)
    ).fetchall()
    return {"staff": staff, "areas": areas, "projects": projects}


def create_staff(conn: sqlite3.Connection, data: dict[str, str]) -> int:
    cur = conn.execute(
        """
        INSERT INTO staff (name, email, title, department, bio, office_hours)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            clean_text(data["name"], 120),
            clean_text(data["email"], 120).lower(),
            clean_text(data["title"], 120),
            clean_text(data["department"], 120),
            clean_text(data["bio"], 800),
            clean_text(data["office_hours"], 160),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)


def update_staff(conn: sqlite3.Connection, staff_id: int, data: dict[str, str]) -> None:
    conn.execute(
        """
        UPDATE staff
        SET name = ?, email = ?, title = ?, department = ?, bio = ?, office_hours = ?
        WHERE id = ?
        """,
        (
            clean_text(data["name"], 120),
            clean_text(data["email"], 120).lower(),
            clean_text(data["title"], 120),
            clean_text(data["department"], 120),
            clean_text(data["bio"], 800),
            clean_text(data["office_hours"], 160),
            staff_id,
        ),
    )
    conn.commit()


def delete_staff(conn: sqlite3.Connection, staff_id: int) -> None:
    conn.execute("DELETE FROM staff WHERE id = ?", (staff_id,))
    conn.commit()


def create_area(conn: sqlite3.Connection, staff_id: int, name: str) -> None:
    cleaned = clean_text(name, 80)
    if not cleaned:
        raise ValueError("Area name is required.")
    conn.execute("INSERT INTO areas (staff_id, name) VALUES (?, ?)", (staff_id, cleaned))
    conn.commit()


def delete_area(conn: sqlite3.Connection, area_id: int) -> None:
    conn.execute("DELETE FROM areas WHERE id = ?", (area_id,))
    conn.commit()


def create_project(conn: sqlite3.Connection, staff_id: int, data: dict[str, str]) -> None:
    conn.execute(
        """
        INSERT INTO projects (staff_id, title, description, level, capacity, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            staff_id,
            clean_text(data["title"], 160),
            clean_text(data["description"], 1000),
            clean_text(data.get("level", "BSc"), 40),
            int(data.get("capacity", "1")),
            data.get("status", "Open"),
        ),
    )
    conn.commit()


def update_project(conn: sqlite3.Connection, project_id: int, data: dict[str, str]) -> None:
    conn.execute(
        """
        UPDATE projects
        SET title = ?, description = ?, level = ?, capacity = ?, status = ?
        WHERE id = ?
        """,
        (
            clean_text(data["title"], 160),
            clean_text(data["description"], 1000),
            clean_text(data.get("level", "BSc"), 40),
            int(data.get("capacity", "1")),
            data.get("status", "Open"),
            project_id,
        ),
    )
    conn.commit()


def delete_project(conn: sqlite3.Connection, project_id: int) -> None:
    conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()


def project_owner(conn: sqlite3.Connection, project_id: int) -> int | None:
    row = conn.execute("SELECT staff_id FROM projects WHERE id = ?", (project_id,)).fetchone()
    return int(row["staff_id"]) if row else None


def area_owner(conn: sqlite3.Connection, area_id: int) -> int | None:
    row = conn.execute("SELECT staff_id FROM areas WHERE id = ?", (area_id,)).fetchone()
    return int(row["staff_id"]) if row else None


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def layout(title: str, body: str, flash: str = "") -> bytes:
    flash_html = f'<p class="flash">{esc(flash)}</p>' if flash else ""
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} | Supervisor Match</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/">Supervisor Match</a>
    <nav>
      <a href="/staff">Student browse</a>
      <a href="/admin">Staff workspace</a>
    </nav>
  </header>
  <main>
    {flash_html}
    {body}
  </main>
</body>
</html>"""
    return page.encode("utf-8")


def staff_card(row: sqlite3.Row) -> str:
    areas = row["areas"] or "No areas listed"
    return f"""
    <article class="card staff-card">
      <div>
        <p class="eyebrow">{esc(row["department"])}</p>
        <h2>{esc(row["name"])}</h2>
        <p class="muted">{esc(row["title"])}</p>
        <p>{esc(row["bio"])}</p>
        <p class="tags">{esc(areas)}</p>
      </div>
      <div class="card-actions">
        <span class="count">{row["project_count"]} project(s)</span>
        <a class="button" href="/staff/{row["id"]}">View profile</a>
      </div>
    </article>
    """


def staff_form(action: str, values: dict[str, Any] | sqlite3.Row | None = None) -> str:
    values = values or {}
    def val(name: str) -> str:
        return esc(values[name] if name in values.keys() else "")

    return f"""
    <form class="form" method="post" action="{esc(action)}">
      <label>Name <input name="name" value="{val("name")}" required></label>
      <label>Email <input type="email" name="email" value="{val("email")}" required></label>
      <label>Title <input name="title" value="{val("title")}" required></label>
      <label>Department <input name="department" value="{val("department")}" required></label>
      <label>Biography <textarea name="bio" required>{val("bio")}</textarea></label>
      <label>Office hours <input name="office_hours" value="{val("office_hours")}" required></label>
      <button class="button primary" type="submit">Save profile</button>
    </form>
    """


def project_form(action: str, values: dict[str, Any] | sqlite3.Row | None = None) -> str:
    values = values or {}
    def val(name: str, default: str = "") -> str:
        if hasattr(values, "keys") and name in values.keys():
            return esc(values[name])
        return esc(default)

    level = str(values["level"]) if hasattr(values, "keys") and "level" in values.keys() else "BSc"
    status = str(values["status"]) if hasattr(values, "keys") and "status" in values.keys() else "Open"
    level_options = "".join(
        f'<option value="{esc(item)}" {"selected" if item == level else ""}>{esc(item)}</option>'
        for item in ["BSc", "MSc", "BSc/MSc"]
    )
    status_options = "".join(
        f'<option value="{esc(item)}" {"selected" if item == status else ""}>{esc(item)}</option>'
        for item in ["Open", "Limited", "Closed"]
    )
    return f"""
    <form class="form" method="post" action="{esc(action)}">
      <label>Project title <input name="title" value="{val("title")}" required></label>
      <label>Description <textarea name="description" required>{val("description")}</textarea></label>
      <label>Level <select name="level">{level_options}</select></label>
      <label>Capacity <input type="number" name="capacity" min="1" max="8" value="{val("capacity", "1")}" required></label>
      <label>Status <select name="status">{status_options}</select></label>
      <button class="button primary" type="submit">Save project</button>
    </form>
    """


class SupervisorHandler(BaseHTTPRequestHandler):
    server_version = "SupervisorMatch/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        if os.environ.get("QUIET_LOGS") != "1":
            super().log_message(format, *args)

    def send_html(self, title: str, body: str, status: HTTPStatus = HTTPStatus.OK, flash: str = "") -> None:
        payload = layout(title, body, flash)
        self.send_response(status.value)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER.value)
        self.send_header("Location", location)
        self.end_headers()

    def read_form(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        return {key: values[0] for key, values in parse_qs(raw).items()}

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = parse_qs(parsed.query)

        if path == "/static/style.css":
            css = (BASE_DIR / "static" / "style.css").read_bytes()
            self.send_response(HTTPStatus.OK.value)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Content-Length", str(len(css)))
            self.end_headers()
            self.wfile.write(css)
            return

        with get_connection() as conn:
            if path == "/":
                body = """
                <section class="hero">
                  <p class="eyebrow">Final year project supervision</p>
                  <h1>Find staff expertise and project ideas in one place.</h1>
                  <p>Students can browse staff profiles by research area, while staff can maintain their areas of interest and proposed project ideas.</p>
                  <div class="hero-actions">
                    <a class="button primary" href="/staff">Browse as student</a>
                    <a class="button" href="/admin">Manage as staff</a>
                  </div>
                </section>
                <section class="grid two">
                  <article class="panel"><h2>For students</h2><p>Search by staff name, department, interest area or project topic before contacting a potential supervisor.</p></article>
                  <article class="panel"><h2>For staff</h2><p>Add, update and remove profile details, research areas and project ideas from a single workspace.</p></article>
                </section>
                """
                self.send_html("Home", body)
                return

            if path == "/staff":
                search = clean_text(query.get("q", [""])[0], 120)
                rows = list_staff(conn, search.lower())
                cards = "".join(staff_card(row) for row in rows)
                body = f"""
                <section class="page-head">
                  <p class="eyebrow">Student browse</p>
                  <h1>Staff profiles</h1>
                  <p>Use search to find a supervisor by expertise, department or project topic.</p>
                </section>
                <form class="search" method="get" action="/staff">
                  <input name="q" value="{esc(search)}" placeholder="Search AI, security, requirements, staff name...">
                  <button class="button primary" type="submit">Search</button>
                  <a class="button" href="/staff">Clear</a>
                </form>
                <section class="stack">{cards or '<p class="empty">No staff match that search.</p>'}</section>
                """
                self.send_html("Staff profiles", body)
                return

            staff_match = re.match(r"^/staff/(\d+)$", path)
            if staff_match:
                profile = get_staff_profile(conn, int(staff_match.group(1)))
                if not profile:
                    self.send_html("Not found", "<p class='empty'>Staff profile not found.</p>", HTTPStatus.NOT_FOUND)
                    return
                staff = profile["staff"]
                area_html = "".join(f"<li>{esc(area['name'])}</li>" for area in profile["areas"])
                project_html = "".join(
                    f"""
                    <article class="project">
                      <div>
                        <h3>{esc(project["title"])}</h3>
                        <p>{esc(project["description"])}</p>
                      </div>
                      <dl>
                        <dt>Level</dt><dd>{esc(project["level"])}</dd>
                        <dt>Capacity</dt><dd>{esc(project["capacity"])}</dd>
                        <dt>Status</dt><dd>{esc(project["status"])}</dd>
                      </dl>
                    </article>
                    """
                    for project in profile["projects"]
                )
                body = f"""
                <section class="page-head">
                  <p class="eyebrow">{esc(staff["department"])}</p>
                  <h1>{esc(staff["name"])}</h1>
                  <p>{esc(staff["title"])} · <a href="mailto:{esc(staff["email"])}">{esc(staff["email"])}</a></p>
                </section>
                <section class="grid two">
                  <article class="panel">
                    <h2>Profile</h2>
                    <p>{esc(staff["bio"])}</p>
                    <p><strong>Office hours:</strong> {esc(staff["office_hours"])}</p>
                  </article>
                  <article class="panel">
                    <h2>Areas of interest</h2>
                    <ul class="clean-list">{area_html or '<li>No areas listed.</li>'}</ul>
                  </article>
                </section>
                <section class="page-head slim"><h2>Project ideas</h2></section>
                <section class="stack">{project_html or '<p class="empty">No project ideas listed.</p>'}</section>
                """
                self.send_html(staff["name"], body)
                return

            if path == "/admin":
                rows = list_staff(conn)
                cards = "".join(
                    f"""
                    <article class="card staff-card">
                      <div>
                        <p class="eyebrow">{esc(row["department"])}</p>
                        <h2>{esc(row["name"])}</h2>
                        <p>{esc(row["areas"] or "No areas listed")}</p>
                      </div>
                      <div class="card-actions">
                        <a class="button" href="/admin/staff/{row["id"]}/edit">Edit</a>
                        <form method="post" action="/admin/staff/{row["id"]}/delete"><button class="button danger" type="submit">Delete</button></form>
                      </div>
                    </article>
                    """
                    for row in rows
                )
                body = f"""
                <section class="page-head">
                  <p class="eyebrow">Staff workspace</p>
                  <h1>Manage staff profiles</h1>
                  <p>This workspace demonstrates add, update and delete operations for staff profiles, areas of interest and project ideas.</p>
                  <a class="button primary" href="/admin/staff/new">Add staff profile</a>
                </section>
                <section class="stack">{cards}</section>
                """
                self.send_html("Staff workspace", body, flash=query.get("flash", [""])[0])
                return

            if path == "/admin/staff/new":
                body = f"<section class='page-head'><h1>Add staff profile</h1></section>{staff_form('/admin/staff/new')}"
                self.send_html("Add staff", body)
                return

            edit_match = re.match(r"^/admin/staff/(\d+)/edit$", path)
            if edit_match:
                staff_id = int(edit_match.group(1))
                profile = get_staff_profile(conn, staff_id)
                if not profile:
                    self.send_html("Not found", "<p class='empty'>Staff profile not found.</p>", HTTPStatus.NOT_FOUND)
                    return
                staff = profile["staff"]
                area_rows = "".join(
                    f"<li>{esc(area['name'])} <form method='post' action='/admin/areas/{area['id']}/delete'><button class='link danger' type='submit'>remove</button></form></li>"
                    for area in profile["areas"]
                )
                project_rows = "".join(
                    f"""
                    <article class="project compact">
                      <div><h3>{esc(project["title"])}</h3><p>{esc(project["status"])} · {esc(project["level"])} · capacity {esc(project["capacity"])}</p></div>
                      <div class="card-actions">
                        <a class="button" href="/admin/projects/{project["id"]}/edit">Edit</a>
                        <form method="post" action="/admin/projects/{project["id"]}/delete"><button class="button danger" type="submit">Delete</button></form>
                      </div>
                    </article>
                    """
                    for project in profile["projects"]
                )
                body = f"""
                <section class="page-head">
                  <p class="eyebrow">Staff workspace</p>
                  <h1>Edit {esc(staff["name"])}</h1>
                </section>
                {staff_form(f"/admin/staff/{staff_id}/edit", staff)}
                <section class="grid two">
                  <article class="panel">
                    <h2>Areas of interest</h2>
                    <ul class="editable-list">{area_rows or '<li>No areas listed.</li>'}</ul>
                    <form class="inline-form" method="post" action="/admin/staff/{staff_id}/areas/new">
                      <input name="name" placeholder="Add area of interest" required>
                      <button class="button" type="submit">Add area</button>
                    </form>
                  </article>
                  <article class="panel">
                    <h2>Project ideas</h2>
                    <a class="button" href="/admin/staff/{staff_id}/projects/new">Add project idea</a>
                  </article>
                </section>
                <section class="stack">{project_rows or '<p class="empty">No project ideas listed.</p>'}</section>
                """
                self.send_html("Edit staff", body, flash=query.get("flash", [""])[0])
                return

            new_project_match = re.match(r"^/admin/staff/(\d+)/projects/new$", path)
            if new_project_match:
                staff_id = int(new_project_match.group(1))
                body = f"<section class='page-head'><h1>Add project idea</h1></section>{project_form(f'/admin/staff/{staff_id}/projects/new')}"
                self.send_html("Add project", body)
                return

            edit_project_match = re.match(r"^/admin/projects/(\d+)/edit$", path)
            if edit_project_match:
                project_id = int(edit_project_match.group(1))
                project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
                if not project:
                    self.send_html("Not found", "<p class='empty'>Project not found.</p>", HTTPStatus.NOT_FOUND)
                    return
                body = f"<section class='page-head'><h1>Edit project idea</h1></section>{project_form(f'/admin/projects/{project_id}/edit', project)}"
                self.send_html("Edit project", body)
                return

        self.send_html("Not found", "<p class='empty'>Page not found.</p>", HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        form = self.read_form()

        with get_connection() as conn:
            if path == "/admin/staff/new":
                errors = validate_staff(form)
                if errors:
                    self.send_html("Add staff", staff_form(path, form), HTTPStatus.BAD_REQUEST, "; ".join(errors))
                    return
                try:
                    create_staff(conn, form)
                except sqlite3.IntegrityError:
                    self.send_html("Add staff", staff_form(path, form), HTTPStatus.BAD_REQUEST, "Email must be unique.")
                    return
                self.redirect("/admin?flash=" + urlencode({"": "Profile created."})[1:])
                return

            edit_match = re.match(r"^/admin/staff/(\d+)/edit$", path)
            if edit_match:
                staff_id = int(edit_match.group(1))
                errors = validate_staff(form)
                if errors:
                    self.send_html("Edit staff", staff_form(path, form), HTTPStatus.BAD_REQUEST, "; ".join(errors))
                    return
                try:
                    update_staff(conn, staff_id, form)
                except sqlite3.IntegrityError:
                    self.send_html("Edit staff", staff_form(path, form), HTTPStatus.BAD_REQUEST, "Email must be unique.")
                    return
                self.redirect(f"/admin/staff/{staff_id}/edit?flash=Profile updated.")
                return

            delete_staff_match = re.match(r"^/admin/staff/(\d+)/delete$", path)
            if delete_staff_match:
                delete_staff(conn, int(delete_staff_match.group(1)))
                self.redirect("/admin?flash=Profile deleted.")
                return

            new_area_match = re.match(r"^/admin/staff/(\d+)/areas/new$", path)
            if new_area_match:
                staff_id = int(new_area_match.group(1))
                try:
                    create_area(conn, staff_id, form.get("name", ""))
                    self.redirect(f"/admin/staff/{staff_id}/edit?flash=Area added.")
                except ValueError as exc:
                    self.redirect(f"/admin/staff/{staff_id}/edit?flash={urlencode({'': str(exc)})[1:]}")
                return

            delete_area_match = re.match(r"^/admin/areas/(\d+)/delete$", path)
            if delete_area_match:
                area_id = int(delete_area_match.group(1))
                staff_id = area_owner(conn, area_id) or 0
                delete_area(conn, area_id)
                self.redirect(f"/admin/staff/{staff_id}/edit?flash=Area removed.")
                return

            new_project_match = re.match(r"^/admin/staff/(\d+)/projects/new$", path)
            if new_project_match:
                staff_id = int(new_project_match.group(1))
                errors = validate_project(form)
                if errors:
                    self.send_html("Add project", project_form(path, form), HTTPStatus.BAD_REQUEST, "; ".join(errors))
                    return
                create_project(conn, staff_id, form)
                self.redirect(f"/admin/staff/{staff_id}/edit?flash=Project added.")
                return

            edit_project_match = re.match(r"^/admin/projects/(\d+)/edit$", path)
            if edit_project_match:
                project_id = int(edit_project_match.group(1))
                staff_id = project_owner(conn, project_id)
                errors = validate_project(form)
                if errors:
                    self.send_html("Edit project", project_form(path, form), HTTPStatus.BAD_REQUEST, "; ".join(errors))
                    return
                update_project(conn, project_id, form)
                self.redirect(f"/admin/staff/{staff_id}/edit?flash=Project updated.")
                return

            delete_project_match = re.match(r"^/admin/projects/(\d+)/delete$", path)
            if delete_project_match:
                project_id = int(delete_project_match.group(1))
                staff_id = project_owner(conn, project_id)
                delete_project(conn, project_id)
                self.redirect(f"/admin/staff/{staff_id}/edit?flash=Project deleted.")
                return

        self.send_html("Not found", "<p class='empty'>Action not found.</p>", HTTPStatus.NOT_FOUND)


def run(host: str = HOST, port: int = PORT) -> None:
    ensure_database()
    server = ThreadingHTTPServer((host, port), SupervisorHandler)
    print(f"Supervisor Match running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init-db":
        ensure_database()
        print(f"Database ready: {DB_PATH}")
    else:
        run()
