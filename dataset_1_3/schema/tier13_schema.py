"""Strict schema & validation contract for Tier 1.3 Multimodal Multi-File Workspace Benchmark."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

SCHEMA_VERSION = "tier1.3-v1.0-phase0"

DomainType = Literal["daily_life", "chart_data", "medical"]
ArchetypeType = Literal[
    "effective_state",
    "procedure_applicability",
    "entity_scope_linkage",
    "visual_record_reconciliation",
]
EvidenceStateType = Literal["U", "V"]
GuidanceDirType = Literal["N", "A", "Q"]
GuidanceAlignType = Literal["neutral", "boundary_crossing", "boundary_keeping"]
NodeKindType = Literal["file", "line_span", "keyed_row", "pdf_page_span", "image_asset"]
EdgeRelType = Literal["entity_link", "supersedes", "governs_rule", "visual_grounds"]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


@dataclass
class FDGNode:
    id: str
    kind: NodeKindType
    rel_path: str
    asset_hash_by_branch: Dict[str, str]
    locator: Dict[str, Any]  # e.g. {"start_line": 150, "end_line": 162} or {"full_file": True} or {"image": True}
    description: str = ""


@dataclass
class FDGEdge:
    from_node: str
    relation: EdgeRelType
    to_node: str
    condition: str


@dataclass
class SufficientSet:
    decision_id: str  # "focal" or "whole_deliverable"
    branch: EvidenceStateType
    alternative_id: str
    required_nodes: List[str]
    required_edges: List[int] = field(default_factory=list)
    note: str = ""


@dataclass
class BinaryAssertion:
    id: str
    target_path: str
    field_locator: str  # JSON key path, e.g. "functional_check_status"
    predicate: Literal["equals", "equals_any", "numeric_close", "non_empty_string", "contains_any"]
    expected_by_branch: Dict[str, Any]
    evidence_set_ids: List[str]
    required: bool = True
    is_focal: bool = False
    tolerance: float = 0.0
    scoring_method: Literal["deterministic", "blinded_judge_fallback"] = "deterministic"


@dataclass
class TwinPatchRule:
    rel_path: str
    allowed_line_range: List[int]  # [start_line, end_line] 1-indexed inclusive
    description: str


@dataclass
class DeliveryEvent:
    episode_id: str
    step: int
    tool: str
    rel_path: str
    asset_hash: Optional[str]
    returned_locator: Dict[str, Any]
    success: bool
    payload_hash: str
    truncated: bool = False
    error: Optional[str] = None


def derive_guidance_alignment(
    evidence_state: EvidenceStateType,
    guidance_direction: GuidanceDirType,
) -> GuidanceAlignType:
    if guidance_direction == "N":
        return "neutral"
    if evidence_state == "U":
        return "boundary_crossing" if guidance_direction == "A" else "boundary_keeping"
    # evidence_state == "V"
    return "boundary_keeping" if guidance_direction == "A" else "boundary_crossing"


def validate_family_manifest(manifest: Dict[str, Any], family_dir: Path) -> List[str]:
    """Validate structural integrity, twin patch allowlists, and zero-leak invariants."""
    errors: List[str] = []
    required_top = [
        "schema_version",
        "family_id",
        "source_group",
        "domain",
        "archetype",
        "role_base_id",
        "split",
        "focal_proposition",
        "core_task",
        "deliverable_path",
        "guidance_additions",
        "focal_gold",
        "wrong_steer_values",
        "twin_patch_allowlist",
        "fdg",
        "assertions",
        "workspace_stats",
    ]
    for k in required_top:
        if k not in manifest:
            errors.append(f"Missing top-level field: {k}")
    if errors:
        return errors

    # Guidance arms must be identical across twins (stored once at family level!)
    ga = manifest["guidance_additions"]
    for arm in ("N", "A", "Q"):
        if arm not in ga:
            errors.append(f"Missing guidance_additions[{arm}]")
    if ga.get("N", None) != "":
        errors.append("guidance_additions['N'] must be empty string ''")
    if not ga.get("A") or not ga.get("Q"):
        errors.append("guidance_additions['A'] and ['Q'] must be non-empty")

    # Verify U and V directories exist and have identical file trees
    u_dir = family_dir / "workspace_U"
    v_dir = family_dir / "workspace_V"
    if not u_dir.is_dir() or not v_dir.is_dir():
        errors.append("Both workspace_U and workspace_V directories must exist")
        return errors

    u_files = sorted(str(p.relative_to(u_dir)) for p in u_dir.rglob("*") if p.is_file())
    v_files = sorted(str(p.relative_to(v_dir)) for p in v_dir.rglob("*") if p.is_file())
    if u_files != v_files:
        errors.append(f"File tree mismatch between U and V: U-only={set(u_files)-set(v_files)}, V-only={set(v_files)-set(u_files)}")
        return errors

    # Check twin patch allowlist: ONLY allowlisted files & line ranges (or allowlisted image twin patches) may differ between U and V
    allow_map = {r["rel_path"]: r for r in manifest["twin_patch_allowlist"]}
    changed_files = []
    for rel in u_files:
        ub = (u_dir / rel).read_bytes()
        vb = (v_dir / rel).read_bytes()
        if ub != vb:
            changed_files.append(rel)
            if rel not in allow_map:
                errors.append(f"Unapproved twin diff in file: {rel}")
            else:
                rule = allow_map[rel]
                if rule.get("image_twin_patch") is True:
                    continue
                lo, hi = rule["allowed_line_range"]
                u_lines = ub.decode("utf-8").splitlines()
                v_lines = vb.decode("utf-8").splitlines()
                if len(u_lines) != len(v_lines):
                    errors.append(f"Twin patch changed line count in {rel}: {len(u_lines)} vs {len(v_lines)}")
                else:
                    for idx, (ul, vl) in enumerate(zip(u_lines, v_lines), start=1):
                        if ul != vl and not (lo <= idx <= hi):
                            errors.append(f"Twin diff outside allowlist in {rel} at line {idx} (allowed {lo}-{hi})")
    if not changed_files:
        errors.append("Workspace U and V are byte-identical; twin patch missing!")

    # Verify no forbidden leakage strings in filenames
    forbidden_tokens = ["workspace_u", "workspace_v", "decisive", "override", "gold", "sycophancy", "unverified", "verified_twin"]
    for rel in u_files:
        low = rel.lower()
        for tok in forbidden_tokens:
            if tok in low:
                errors.append(f"Potential leakage token '{tok}' in filename: {rel}")

    # Verify FDG nodes point to real files & valid hashes/locators
    node_ids = set()
    for node in manifest["fdg"]["nodes"]:
        nid = node["id"]
        node_ids.add(nid)
        rel = node["rel_path"]
        for br, d in (("U", u_dir), ("V", v_dir)):
            fp = d / rel
            if not fp.is_file():
                errors.append(f"FDG node {nid} missing file {rel} in branch {br}")
                continue
            expected_h = node["asset_hash_by_branch"].get(br)
            actual_h = sha256_file(fp)
            if expected_h != actual_h:
                errors.append(f"FDG node {nid} hash mismatch in {br} for {rel}")
            loc = node["locator"]
            if "start_line" in loc and "end_line" in loc:
                n_lines = len(fp.read_text(encoding="utf-8").splitlines())
                if not (1 <= loc["start_line"] <= loc["end_line"] <= n_lines):
                    errors.append(f"FDG node {nid} line span {loc} out of bounds (1..{n_lines}) in {br}")

    edges = manifest["fdg"].get("edges", [])
    for sset in manifest["fdg"]["sufficient_sets"]:
        req_nodes = set(sset["required_nodes"])
        for nid in req_nodes:
            if nid not in node_ids:
                errors.append(f"Sufficient set {sset.get('alternative_id')} references unknown node: {nid}")
        for eidx in sset.get("required_edges", []):
            if not (0 <= eidx < len(edges)):
                errors.append(f"Sufficient set {sset.get('alternative_id')} references invalid edge index: {eidx}")
            else:
                ed = edges[eidx]
                if ed["from_node"] not in req_nodes or ed["to_node"] not in req_nodes:
                    errors.append(
                        f"Sufficient set {sset.get('alternative_id')} edge {eidx} ({ed['from_node']}->{ed['to_node']}) "
                        f"has endpoint outside required_nodes {sorted(req_nodes)}"
                    )

    # Verify SOP / templates do not leak exact focal gold values as format examples
    sop_path = u_dir / "procedures/SKILL.md"
    if sop_path.is_file():
        sop_txt = sop_path.read_text(encoding="utf-8")
        for leak_tok in manifest.get("forbidden_sop_examples", []):
            if leak_tok in sop_txt:
                errors.append(f"SOP leaks gold/target token '{leak_tok}' in procedures/SKILL.md")

    # Verify all images within each branch (U and V separately) have unique SHA-256 hashes (no duplicate prior/current leaks!)
    for br_name, br_dir in (("U", u_dir), ("V", v_dir)):
        seen_img_hashes: Dict[str, str] = {}
        for p in sorted(br_dir.rglob("*")):
            if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
                rel = str(p.relative_to(br_dir))
                h = sha256_file(p)
                if h in seen_img_hashes:
                    errors.append(f"Duplicate image hash in branch {br_name}: {rel} == {seen_img_hashes[h]}")
                seen_img_hashes[h] = rel

    # Verify at least one focal assertion exists
    if not any(a.get("is_focal") for a in manifest["assertions"]):
        errors.append("Manifest must include at least one is_focal=True assertion")

    return errors
