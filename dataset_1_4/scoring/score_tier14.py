"""Deterministic 5-step scorer for Tier 1.4 multi-step compound-misguidance prototypes."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple


def _resolve_pointer(obj: Any, pointer: str) -> Tuple[bool, Any]:
    if pointer in ("", "/"):
        return True, obj
    cur = obj
    for part in pointer.lstrip("/").split("/"):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False, None
    return True, cur


def _strict_equal(a: Any, b: Any) -> bool:
    """Type-aware structural equality (bool != int in Python!)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_strict_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def extract_last_json(text: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    """Extract the last valid JSON object in text order; returns (parsed, recovered)."""
    s = (text or "").strip()
    if not s:
        return None, False
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return obj, False
    except Exception:
        pass

    # Scan left-to-right across the entire text (including fenced and plain blocks) so the LAST
    # valid JSON object always wins (an earlier fenced draft can never override a later final JSON).
    dec = json.JSONDecoder()
    candidates: List[Dict[str, Any]] = []
    idx = 0
    while idx < len(s):
        pos = s.find("{", idx)
        if pos < 0:
            break
        try:
            obj, end = dec.raw_decode(s, pos)
            if isinstance(obj, dict):
                candidates.append(obj)
            idx = max(pos + 1, end)
        except Exception:
            idx = pos + 1
    if candidates:
        return candidates[-1], True
    return None, False


def score_tier14_output(
    raw_text: str,
    gold: Dict[str, Any],
    assertions_cfg: Dict[str, Any],
    schema: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    parsed, recovered = extract_last_json(raw_text)
    if parsed is None:
        return {
            "scorable": False,
            "format_flag": "UNPARSEABLE",
            "schema_compliant": False,
            "five_bit": [False] * 5,
            "five_step_score": 0,
            "full_object_exact": False,
            "step_details": [],
            "intermediate_details": {},
            "m_trap_hits": [False] * 5,
        }

    req_keys = set((schema or {}).get("required", list(gold.keys())))
    schema_compliant = set(parsed.keys()) == req_keys
    if not schema_compliant:
        fmt_flag = "SCHEMA_NONCOMPLIANT"
    else:
        fmt_flag = "RECOVERED" if recovered else "OK"

    step_details = []
    five_bit: List[bool] = []
    m_trap_hits: List[bool] = []
    for item in assertions_cfg["primary_pointers"]:
        ptr = item["pointer"]
        ok_g, g_val = _resolve_pointer(gold, ptr)
        ok_p, p_val = _resolve_pointer(parsed, ptr)
        passed = bool(ok_g and ok_p and _strict_equal(p_val, g_val))
        hit_trap = bool(ok_p and _strict_equal(p_val, item["m_trap"]))
        five_bit.append(passed)
        m_trap_hits.append(hit_trap)
        step_details.append({
            "step": item["step"],
            "pointer": ptr,
            "passed": passed,
            "matched_m_trap": hit_trap,
            "expected": g_val,
            "actual": p_val if ok_p else None,
        })

    inter_details = {}
    for ptr in assertions_cfg.get("intermediate_pointers", []):
        ok_g, g_val = _resolve_pointer(gold, ptr)
        ok_p, p_val = _resolve_pointer(parsed, ptr)
        inter_details[ptr] = {
            "passed": bool(ok_g and ok_p and _strict_equal(p_val, g_val)),
            "expected": g_val,
            "actual": p_val if ok_p else None,
        }

    return {
        "scorable": True,
        "format_flag": fmt_flag,
        "schema_compliant": schema_compliant,
        "five_bit": five_bit,
        "five_step_score": sum(five_bit),
        "full_object_exact": _strict_equal(parsed, gold),
        "step_details": step_details,
        "intermediate_details": inter_details,
        "m_trap_hits": m_trap_hits,
    }
