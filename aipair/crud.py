"""CRUD operations for Courses table in SQLite database `college.db`.

Provides: create_course, get_course, update_course, delete_course, list_courses,
and ensure_db to create the table if missing.

All functions raise exceptions on invalid input or on errors.
"""
from typing import Dict, List, Optional
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "college.db")


def _get_conn(path: str = DB_PATH) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"Unable to connect to database: {e}") from e


def ensure_db(path: str = DB_PATH) -> None:
    """Create Courses table if it does not exist.

    Table schema: Courses(cid INTEGER PRIMARY KEY, name TEXT NOT NULL,
    fee REAL NOT NULL, duration INTEGER NOT NULL)
    """
    try:
        conn = _get_conn(path)
        with conn:
            conn.execute(
                """
				CREATE TABLE IF NOT EXISTS Courses (
					cid INTEGER PRIMARY KEY,
					name TEXT NOT NULL,
					fee REAL NOT NULL,
					duration INTEGER NOT NULL
				)
				"""
            )
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to ensure Courses table: {e}") from e


def _validate_cid(cid: int) -> None:
    if not isinstance(cid, int):
        raise TypeError("cid must be an integer")
    if cid <= 0:
        raise ValueError("cid must be a positive integer")


def _validate_name(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    name = name.strip()
    if not name:
        raise ValueError("name must be a non-empty string")


def _validate_fee(fee) -> None:
    try:
        f = float(fee)
    except (TypeError, ValueError):
        raise TypeError("fee must be a number")
    if f < 0:
        raise ValueError("fee must be non-negative")


def _validate_duration(duration) -> None:
    if not (isinstance(duration, int) or (isinstance(duration, float) and duration.is_integer())):
        raise TypeError("duration must be an integer number of units")
    d = int(duration)
    if d <= 0:
        raise ValueError("duration must be a positive integer")


def create_course(cid: int, name: str, fee, duration, path: str = DB_PATH) -> None:
    """Insert a new course into the Courses table.

    Raises: TypeError, ValueError for invalid input; RuntimeError for DB errors.
    If a course with the same `cid` already exists, raises ValueError.
    """
    _validate_cid(cid)
    _validate_name(name)
    _validate_fee(fee)
    _validate_duration(duration)

    try:
        conn = _get_conn(path)
        with conn:
            cur = conn.execute(
                "INSERT INTO Courses (cid, name, fee, duration) VALUES (?, ?, ?, ?)",
                (cid, name.strip(), float(fee), int(duration)),
            )
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Course with cid {cid} already exists") from e
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to create course: {e}") from e


def get_course(cid: int, path: str = DB_PATH) -> Dict:
    """Return course as a dict for given cid. Raises LookupError if missing."""
    _validate_cid(cid)
    try:
        conn = _get_conn(path)
        cur = conn.execute(
            "SELECT cid, name, fee, duration FROM Courses WHERE cid = ?", (cid,))
        row = cur.fetchone()
        if row is None:
            raise LookupError(f"Course with cid {cid} not found")
        return {"cid": row["cid"], "name": row["name"], "fee": row["fee"], "duration": row["duration"]}
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch course: {e}") from e


def update_course(cid: int, name: Optional[str] = None, fee=None, duration=None, path: str = DB_PATH) -> None:
    """Update fields for a course. At least one of `name`, `fee`, or `duration` must be provided.

    Raises TypeError/ValueError for invalid input, LookupError if course missing.
    """
    _validate_cid(cid)
    updates = {}
    if name is not None:
        _validate_name(name)
        updates['name'] = name.strip()
    if fee is not None:
        _validate_fee(fee)
        updates['fee'] = float(fee)
    if duration is not None:
        _validate_duration(duration)
        updates['duration'] = int(duration)

    if not updates:
        raise ValueError(
            "At least one field (name, fee, duration) must be provided for update")

    set_clause = ', '.join(f"{k} = :{k}" for k in updates.keys())
    params = updates.copy()
    params['cid'] = cid

    try:
        conn = _get_conn(path)
        with conn:
            cur = conn.execute(
                f"UPDATE Courses SET {set_clause} WHERE cid = :cid", params)
            if cur.rowcount == 0:
                raise LookupError(f"Course with cid {cid} not found")
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to update course: {e}") from e


def delete_course(cid: int, path: str = DB_PATH) -> None:
    """Delete course by cid. Raises LookupError if not found."""
    _validate_cid(cid)
    try:
        conn = _get_conn(path)
        with conn:
            cur = conn.execute("DELETE FROM Courses WHERE cid = ?", (cid,))
            if cur.rowcount == 0:
                raise LookupError(f"Course with cid {cid} not found")
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to delete course: {e}") from e


def list_courses(path: str = DB_PATH) -> List[Dict]:
    """Return list of all courses as dicts."""
    try:
        conn = _get_conn(path)
        cur = conn.execute(
            "SELECT cid, name, fee, duration FROM Courses ORDER BY cid")
        rows = cur.fetchall()
        return [{"cid": r["cid"], "name": r["name"], "fee": r["fee"], "duration": r["duration"]} for r in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to list courses: {e}") from e


__all__ = [
    "ensure_db",
    "create_course",
    "get_course",
    "update_course",
    "delete_course",
    "list_courses",
]
