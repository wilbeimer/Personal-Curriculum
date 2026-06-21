---
name: assignments
version: 0.1
loop_over: weekly_goals
---

## Inputs
- 01_course_description (description, domain, subdomains, prerequisites)
- 02_course_length (weeks, hours per week, reasoning)
- 03_weekly_goals (week, goal, topics)

## Process
Using this week's goal and topics, create a set of assignments that 
progress the student toward the weekly goal.
Make sure the total time to complete all assignments fits within the hours per week constraint.
Each assignment should have a title and type.

## Output
Return as JSON:
{
    "week": 1,
    "assignments": [
        {
            "title": "...",
            "type": "quiz | written | checklist"
        }
    ]
}
