---
name: course_resources
version: 0.1
model: groq/compound-beta-mini
depends_on:
  - 01_course_description
---

## Inputs
- course: {course_name}

## Process
Search the web for the best textbook for this course. Look for widely used, highly regarded academic textbooks that cover the course material comprehensively. Prefer textbooks that are commonly used in university courses.

## Output
Return as JSON:
{
    "textbook": {
        "title": "...",
        "author": "...",
        "url": "...",
        "description": "..."
    }
}
