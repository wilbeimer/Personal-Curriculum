import json
import sys
import yaml
from pathlib import Path
import time

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.ai.client import client

AI_DIR = Path(__file__).parent
DEFAULT_SYSTEM_PROMPT = "You are an expert AI assistant. Return only valid JSON, no markdown, no explanation."


# --- Model ---

def call_model(prompt: str, system_prompt: str) -> str:
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("No response from AI")
    return content


def parse_json_response(content: str) -> dict:
    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()
    return json.loads(content, strict=False)


# --- Context loading ---

def load_pipeline_context(stages_dir: Path) -> tuple[str, str, str]:
    """Returns (identity_md, workspace_context, system_prompt)"""
    identity_md = (stages_dir.parent.parent / "IDENTITY.md").read_text()

    workspace_raw = (stages_dir.parent / "CONTEXT.md").read_text()
    _, workspace_frontmatter, workspace_context = workspace_raw.split("---", 2)
    workspace_meta = yaml.safe_load(workspace_frontmatter)
    system_prompt = workspace_meta.get("system_prompt", DEFAULT_SYSTEM_PROMPT)

    return identity_md, workspace_context, system_prompt


def load_stage_context(stage_path: Path) -> tuple[dict, str]:
    """Returns (meta, context)"""
    context_raw = (stage_path / "CONTEXT.md").read_text()
    _, frontmatter, context = context_raw.split("---", 2)
    meta = yaml.safe_load(frontmatter)
    return meta, context


def load_references(stage_path: Path) -> str:
    references = ""
    ref_path = stage_path / "references"
    if ref_path.exists():
        for f in ref_path.glob("*.md"):
            references += f"\n\n# {f.stem}\n{f.read_text()}"
    return references


def load_previous_outputs(stage_name: str, depends_on: list | None, stages_dir: Path) -> dict:
    previous_outputs = {}
    if depends_on is None:
        for prev_stage in sorted(stages_dir.iterdir()):
            if prev_stage.name >= stage_name:
                break
            prev_output = prev_stage / "output" / "result.json"
            if prev_output.exists():
                previous_outputs[prev_stage.name] = json.loads(prev_output.read_text())
    else:
        for dep in depends_on:
            prev_output = stages_dir / dep / "output" / "result.json"
            if prev_output.exists():
                previous_outputs[dep] = json.loads(prev_output.read_text())
    return previous_outputs


# --- Prompt building ---

def build_prompt(identity_md: str, workspace_context: str, context: str, references: str, previous_outputs: dict) -> str:
    return f"""
{identity_md}

---

{workspace_context}

---

## Stage Contract
{context}

---

## Reference Material
{references}

---

## Previous Stage Outputs
{json.dumps(previous_outputs, indent=2)}
"""


# --- Stage execution ---

def run_loop_stage(loop_over: str, full_prompt: str, previous_outputs: dict, merge_item: bool, system_prompt: str) -> dict:
    items = None
    for stage_output in previous_outputs.values():
        if loop_over in stage_output:
            items = stage_output[loop_over]
            break

    if items is None:
        raise ValueError(f"loop_over key '{loop_over}' not found in previous outputs")

    results = []
    for item in items:
        content = call_model(full_prompt + f"\n\n## Current Item\n{json.dumps(item, indent=2)}", system_prompt)
        result = parse_json_response(content)
        if merge_item:
            result = {**item, **result}
        results.append(result)
        time.sleep(2)

    return {loop_over: results}


def run_stage(stage_name: str, user_inputs: dict = {}, stages_dir: Path = AI_DIR / "curriculum" / "stages") -> dict:
    stage_path = stages_dir / stage_name
    output_path = stage_path / "output"
    output_path.mkdir(exist_ok=True)

    identity_md, workspace_context, system_prompt = load_pipeline_context(stages_dir)
    meta, context = load_stage_context(stage_path)
    references = load_references(stage_path)
    previous_outputs = load_previous_outputs(stage_name, meta.get("depends_on"), stages_dir)

    for key, value in user_inputs.items():
        context = context.replace(f"{{{key}}}", str(value))

    full_prompt = build_prompt(identity_md, workspace_context, context, references, previous_outputs)

    loop_over = meta.get("loop_over")
    if loop_over:
        result = run_loop_stage(loop_over, full_prompt, previous_outputs, meta.get("merge_item", False), system_prompt)
    else:
        content = call_model(full_prompt, system_prompt)
        result = parse_json_response(content)

    (output_path / "result.json").write_text(json.dumps(result, indent=2))
    return result
