---
name: assignment_resources
version: 0.1
model: groq/compound-beta-mini
loop_over: assignments
merge_item: true
depends_on:
  - 05_assignment_description
---

## Inputs
- course: {course_name}

## Process
Search the web for 2-3 high quality learning resources for this specific assignment. Look for articles, research papers, or documentation that would help a student complete this assignment. Return only real URLs that you have verified exist.

## Output
Return as JSON:
{
    "resources": [
        {
            "title": "...",
            "url": "...",
            "type": "article | paper | documentation",
            "description": "..."
        }
    ]
}
