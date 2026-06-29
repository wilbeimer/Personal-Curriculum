---
name: analyze
version: 0.1
---

## Inputs
- assignment_title = {assignment_title}
- assignment_description = {assignment_description}
- requirements = {requirements}
- submission_content = {submission_content}

## Process
Analyze the student's submission against the assignment description and requirements.
For each requirement, assess whether the student addressed it, how thoroughly, and what is missing or weak.
Do not score yet — focus only on analysis and evidence from the submission.

## Output
Return as JSON:
{
    "summary": "Brief overall summary of the submission quality",
    "requirement_analysis": [
        {
            "requirement": "...",
            "addressed": true,
            "thoroughness": "fully | partially | minimally | not addressed",
            "notes": "Specific observations about how the student addressed or missed this requirement"
        }
    ],
    "strengths": ["..."],
    "weaknesses": ["..."]
}
