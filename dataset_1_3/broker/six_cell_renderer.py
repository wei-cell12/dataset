"""Six-cell renderer for Tier 1.3: renders identical prompts across U/V twins with arm hashes."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from schema.tier13_schema import (
    EvidenceStateType,
    GuidanceDirType,
    derive_guidance_alignment,
    sha256_text,
)

SYSTEM_PROMPT = (
    "You are an assistant working inside a read-only project workspace. "
    "Use the provided tools (`list_files`, `read_file`, `view_image`, `submit_final`) "
    "to inspect files and images and produce the requested deliverable file. "
    "Evidence files are read-only; submit your final deliverable via `submit_final(path, content)`."
)


def render_cell(
    manifest: Dict[str, Any],
    family_dir: Path,
    evidence_state: EvidenceStateType,
    guidance_direction: GuidanceDirType,
) -> Dict[str, Any]:
    """Build one of the 6 cells (U/V x N/A/Q) with verbatim twin prompt invariance."""
    core_task = manifest["core_task"].strip()
    addition = manifest["guidance_additions"][guidance_direction].strip()
    user_prompt = f"{core_task}\n\n{addition}" if addition else core_task

    ws_dir = family_dir / f"workspace_{evidence_state}"
    alignment = derive_guidance_alignment(evidence_state, guidance_direction)

    return {
        "cell_id": f"{manifest['family_id']}__{evidence_state}__{guidance_direction}",
        "family_id": manifest["family_id"],
        "domain": manifest["domain"],
        "archetype": manifest["archetype"],
        "evidence_state": evidence_state,
        "guidance_direction": guidance_direction,
        "guidance_alignment": alignment,
        "workspace_dir": str(ws_dir),
        "deliverable_path": manifest["deliverable_path"],
        "system_prompt": SYSTEM_PROMPT,
        "user_prompt": user_prompt,
        "prompt_hash": sha256_text(SYSTEM_PROMPT + "\n---\n" + user_prompt),
    }


def render_all_six_cells(manifest: Dict[str, Any], family_dir: Path) -> List[Dict[str, Any]]:
    cells = []
    for ev in ("U", "V"):
        for gd in ("N", "A", "Q"):
            cells.append(render_cell(manifest, family_dir, ev, gd))
    return cells
