#!/usr/bin/env python3
"""Dry-run renderer validation across all 1,040 primary v2.1 prompts + 48 companion accurate-draft prompts."""

import json
import pathlib

D12 = pathlib.Path("/Users/zzh/Documents/Codex/2026-10-09/proofwriter50-users-zzh-documents-codex-2026/dataset_1_2")


def render_skill_catalog(case: dict, cat_by_pool: dict) -> str:
    entries = cat_by_pool[case["skill_pool"]]
    order = case["catalog_order"]
    by_name = {e["name"]: e for e in entries}
    lines = ["Available Skills (select exactly one skill name, or NONE if no listed skill directly supports the requested artifact from the attached image):"]
    for i, name in enumerate(order, 1):
        e = by_name[name]
        lines.append(f"{i}. `{e['name']}`: {e['description']}")
    return "\n".join(lines)


def render_memory_block(case: dict) -> str:
    m_lines = ["[Retrieved User Memory]"]
    for m in case["retrieved_memory"]:
        m_lines.append(f"- ({m['date']} | {m['category']}) {m['content']}")
    m_lines.append("\n[Past Dialogue History]")
    for d in case["past_dialogue"]:
        m_lines.append(f"[{d['session']}] {d['role'].upper()}: {d['content']}")
    return "\n".join(m_lines)


def main():
    d = json.loads((D12 / "benchmark_1_2_240.json").read_text())
    comp = json.loads((D12 / "pure_80/accurate_draft_companion_16.json").read_text())

    cat_by_pool = {}
    for e in d["skill_discovery_catalog"]:
        cat_by_pool.setdefault(e["pool"], []).append(e)

    rendered = 0
    for c in d["cases"]:
        img = D12 / c["source"]["image"]
        assert img.exists() and img.stat().st_size > 0, c["id"]
        if c["regime"] == "skill":
            if c["interaction_protocol"] == "two_step_catalog":
                cat_txt = render_skill_catalog(c, cat_by_pool)
                assert len(cat_txt) > 100
                # Also verify stage-2 SKILL.md loads cleanly for every skill in the pool
                for e in cat_by_pool[c["skill_pool"]]:
                    md = (D12 / e["path"]).read_text()
                    assert md.startswith("---\nname:"), e["path"]
            else:
                e = cat_by_pool[c["skill_pool"]][0]
                md = (D12 / e["path"]).read_text()
                assert md.startswith("---\nname:"), e["path"]
            for ck, cv in c["conditions"].items():
                assert isinstance(cv["user_prompt"], str) and len(cv["user_prompt"]) > 20
                rendered += 1
        elif c["regime"] == "memory":
            mem_txt = render_memory_block(c)
            assert len(mem_txt) > 100
            for ck, cv in c["conditions"].items():
                full = (mem_txt + "\n\n" + cv["user_prompt"]) if cv["include_memory"] else cv["user_prompt"]
                assert len(full) > 20
                rendered += 1
        elif c["regime"] == "pure":
            for ck, ptxt in c["conditions"].items():
                assert isinstance(ptxt, str) and len(ptxt) > 20
                rendered += 1

    comp_rendered = 0
    for c in comp["cases"]:
        img = D12 / "pure_80" / c["source"]["image"]
        assert img.exists() and img.stat().st_size > 0, c["id"]
        for ck, ptxt in c["conditions"].items():
            assert isinstance(ptxt, str) and len(ptxt) > 20
            comp_rendered += 1

    print(f"DRY-RUN RENDER PASSED 100%: {rendered} primary prompts + {comp_rendered} companion prompts = {rendered + comp_rendered} total inputs validated with 0 errors!")


if __name__ == "__main__":
    main()
