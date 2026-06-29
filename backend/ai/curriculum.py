import json
import sqlite3
import uuid
from backend.ai.runner import run_stage
from backend.models import CourseCreate


def generate_curriculum(course_id: str, course: CourseCreate):
    conn = sqlite3.connect("curriculum.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    try:
        # Run pipeline, save to db
        result_01 = run_stage("01_course_description", {"course_name": course.name, "course_description": course.description})
        result_02 = run_stage("02_course_length")
        result_03 = run_stage("03_weekly_goal")
        _ = run_stage("04_assignments")
        result_05 = run_stage("05_assignment_description")

        # Insert course
        cur.execute("""
            UPDATE courses SET
                description = ?,
                domain = ?,
                subdomains = ?,
                prerequisites = ?,
                weeks = ?,
                hours_per_week = ?,
                status = 'completed'
            WHERE id = ?
        """, (
            result_01["description"],
            result_01["domain"],
            json.dumps(result_01["subdomains"]),
            json.dumps(result_01["prerequisites"]),
            result_02["weeks"],
            result_02["hours_per_week"],
            course_id,
        ))

        # Insert weeks
        week_id_map = {}
        for week in result_03["weekly_goals"]:
            week_id = str(uuid.uuid4())
            week_id_map[week["week"]] = week_id
            cur.execute("""
                INSERT INTO course_weeks (id, courseId, week, goal, topics)
                VALUES (?, ?, ?, ?, ?)
            """, (week_id, course_id, week["week"], week["goal"], json.dumps(week["topics"])))

        # Insert assignments
        for assignment in result_05["assignments"]:
            cur.execute("""
                INSERT INTO assignments (id, courseId, weekId, week, title, type, description, requirements)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()), course_id,
                week_id_map.get(assignment["week"], ""),
                assignment["week"],
                assignment["title"],
                assignment["type"],
                assignment["description"],
                json.dumps(assignment["requirements"]),
            ))
        # Update course status to complete

        conn.commit()

    except Exception as e:
        # Update course status to failed with error message
        conn.rollback()
        cur.execute("UPDATE course SET status = 'failed' WHERE id = ?", (course_id,))
        conn.commit()
        print(f"Pipeline failed for course {course_id}: {e}")

    finally:
        conn.close()
