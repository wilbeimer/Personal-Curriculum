---
name: score
version: 0.1
---

## Inputs
- assignment_title = {assignment_title}
- requirements = {requirements}

## Process
Using the requirement analysis from the previous stage, assign a numerical grade out of 100.
Weight each requirement equally unless the number of requirements suggests otherwise.
Justify the score by referencing specific findings from the analysis.

## Output
Return as JSON:
{
    "grade": 82,
    "justification": "...",
    "requirement_scores": [
        {
            "requirement": "...",
            "score": 18,
            "max_score": 20,
            "reason": "..."
        }
    ]
}
