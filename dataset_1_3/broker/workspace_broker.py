"""Unified read-only 4-tool Workspace Broker for Tier 1.3.

Enforces:
- Zero-leak opaque sandbox isolation
- Exact line-span & pixel-delivery logging (DeliveryEvent)
- Read-only evidence files; atomic deliverable write via submit_final(path, content)
- Strict tool-call budget tracking & clean termination reasons
"""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from schema.tier13_schema import DeliveryEvent, sha256_bytes, sha256_file, sha256_text

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def _get_image_dimensions(path: Path) -> Tuple[Optional[int], Optional[int]]:
    """Read PNG or JPEG dimensions natively without external dependencies."""
    import struct

    data = path.read_bytes()
    # PNG
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return int(w), int(h)
    # JPEG
    if len(data) >= 4 and data[:2] == b"\xff\xd8":
        idx = 2
        while idx + 9 < len(data):
            if data[idx] != 0xFF:
                break
            marker = data[idx + 1]
            idx += 2
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[idx + 3 : idx + 7])
                return int(w), int(h)
            if idx + 2 > len(data):
                break
            seg_len = struct.unpack(">H", data[idx : idx + 2])[0]
            if seg_len < 2:
                break
            idx += seg_len
    return None, None


class WorkspaceBroker:
    def __init__(
        self,
        source_workspace_dir: Path,
        episode_id: str,
        deliverable_path: str,
        max_tool_calls: int = 24,
        default_max_lines: int = 120,
        simulate_image_failure: bool = False,
    ) -> None:
        self.source_workspace_dir = Path(source_workspace_dir)
        self.episode_id = episode_id
        self.deliverable_path = deliverable_path
        self.max_tool_calls = max_tool_calls
        self.default_max_lines = default_max_lines
        self.simulate_image_failure = simulate_image_failure

        # Opaque temporary directory — ZERO case ID, branch, or arm leakage!
        self._tmpdir = tempfile.TemporaryDirectory(prefix="ws_sb_")
        self.root = (Path(self._tmpdir.name) / "workspace").resolve()
        shutil.copytree(self.source_workspace_dir, self.root)
        (self.root / "deliverables").mkdir(parents=True, exist_ok=True)

        self.step_count: int = 0
        self.events: List[DeliveryEvent] = []
        self.terminated: bool = False
        self.termination_reason: str = "in_progress"
        self.submitted_path: Optional[str] = None
        self.submitted_content: Optional[str] = None
        self.submitted_hash: Optional[str] = None

    def close(self) -> None:
        self._tmpdir.cleanup()

    def __enter__(self) -> "WorkspaceBroker":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _resolve_safe(self, rel_path: str) -> Optional[Path]:
        clean = rel_path.strip().lstrip("/")
        if clean in ("", "."):
            return self.root
        candidate = (self.root / clean).resolve()
        root_resolved = self.root.resolve()
        if root_resolved == candidate or root_resolved in candidate.parents:
            return candidate
        return None

    def _check_budget(self, tool: str, rel_path: str) -> Optional[Dict[str, Any]]:
        if self.terminated:
            return {"ok": False, "error": f"Episode already terminated ({self.termination_reason})."}
        if self.step_count >= self.max_tool_calls:
            self.terminated = True
            self.termination_reason = "budget_exhausted"
            return {"ok": False, "error": f"Tool call budget exhausted ({self.max_tool_calls})."}
        self.step_count += 1
        return None

    def list_files(self, path: str = ".") -> Dict[str, Any]:
        err = self._check_budget("list_files", path)
        if err:
            return err
        target = self._resolve_safe(path)
        if target is None or not target.exists() or not target.is_dir():
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="list_files",
                rel_path=path,
                asset_hash=None,
                returned_locator={},
                success=False,
                payload_hash=sha256_text("NOT_FOUND"),
                error="Directory not found or outside workspace",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        entries = []
        for child in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name)):
            rel = str(child.relative_to(self.root))
            entries.append({"path": rel, "type": "dir" if child.is_dir() else "file"})
        payload_str = json.dumps(entries, ensure_ascii=False)
        ev = DeliveryEvent(
            episode_id=self.episode_id,
            step=self.step_count,
            tool="list_files",
            rel_path=str(target.relative_to(self.root)) if target != self.root else ".",
            asset_hash=None,
            returned_locator={"listed_count": len(entries)},
            success=True,
            payload_hash=sha256_text(payload_str),
        )
        self.events.append(ev)
        return {"ok": True, "entries": entries}

    def read_file(self, path: str, start_line: int = 1, max_lines: Optional[int] = None) -> Dict[str, Any]:
        err = self._check_budget("read_file", path)
        if err:
            return err
        raw_limit = self.default_max_lines if max_lines is None else int(max_lines)
        if raw_limit < 1:
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="read_file",
                rel_path=path,
                asset_hash=None,
                returned_locator={},
                success=False,
                payload_hash=sha256_text("INVALID_MAX_LINES"),
                error="max_lines must be a positive integer (>= 1).",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}
        limit = min(raw_limit, self.default_max_lines)
        start = max(1, int(start_line))
        target = self._resolve_safe(path)
        if target is None or not target.is_file():
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="read_file",
                rel_path=path,
                asset_hash=None,
                returned_locator={},
                success=False,
                payload_hash=sha256_text("NOT_FOUND"),
                error="File not found or outside workspace",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        if target.suffix.lower() in IMAGE_EXTS:
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="read_file",
                rel_path=str(target.relative_to(self.root)),
                asset_hash=sha256_file(target),
                returned_locator={},
                success=False,
                payload_hash=sha256_text("BINARY_IMAGE"),
                error="Image file cannot be read as text; use view_image(path).",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        raw_bytes = target.read_bytes()
        asset_h = sha256_bytes(raw_bytes)
        lines = raw_bytes.decode("utf-8", errors="replace").splitlines()
        total_lines = len(lines)
        end = min(total_lines, start + limit - 1)
        sliced = lines[start - 1 : end] if start <= total_lines else []
        eof_reached = end >= total_lines
        numbered = "\n".join(f"{i}: {ln}" for i, ln in enumerate(sliced, start=start))
        footer = "[EOF]" if eof_reached else f"[TRUNCATED: showing lines {start}-{end} of {total_lines}]"
        text_payload = f"{numbered}\n{footer}" if numbered else footer

        rel = str(target.relative_to(self.root))
        ev = DeliveryEvent(
            episode_id=self.episode_id,
            step=self.step_count,
            tool="read_file",
            rel_path=rel,
            asset_hash=asset_h,
            returned_locator={
                "start_line": start if sliced else 0,
                "end_line": end if sliced else 0,
                "total_lines": total_lines,
                "eof_reached": eof_reached,
            },
            success=True,
            payload_hash=sha256_text(text_payload),
            truncated=not eof_reached,
        )
        self.events.append(ev)
        return {
            "ok": True,
            "path": rel,
            "start_line": start,
            "end_line": end,
            "total_lines": total_lines,
            "eof_reached": eof_reached,
            "content": text_payload,
        }

    def view_image(self, path: str) -> Dict[str, Any]:
        err = self._check_budget("view_image", path)
        if err:
            return err
        target = self._resolve_safe(path)
        if target is None or not target.is_file() or target.suffix.lower() not in IMAGE_EXTS:
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="view_image",
                rel_path=path,
                asset_hash=None,
                returned_locator={},
                success=False,
                payload_hash=sha256_text("IMAGE_NOT_FOUND"),
                error="Image not found or unsupported format",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        rel = str(target.relative_to(self.root))
        raw_bytes = target.read_bytes()
        asset_h = sha256_bytes(raw_bytes)

        if self.simulate_image_failure:
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="view_image",
                rel_path=rel,
                asset_hash=asset_h,
                returned_locator={"image": False},
                success=False,
                payload_hash=sha256_text("SIMULATED_IMAGE_DELIVERY_FAILURE"),
                error="Simulated image delivery failure",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        w, h = _get_image_dimensions(target)
        if not w or not h or w <= 0 or h <= 0:
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="view_image",
                rel_path=rel,
                asset_hash=asset_h,
                returned_locator={"image": False},
                success=False,
                payload_hash=sha256_text("UNREADABLE_IMAGE_HEADER"),
                error="Image header unreadable or zero dimensions",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        ev = DeliveryEvent(
            episode_id=self.episode_id,
            step=self.step_count,
            tool="view_image",
            rel_path=rel,
            asset_hash=asset_h,
            returned_locator={"image": True, "width": w, "height": h},
            success=True,
            payload_hash=asset_h,
        )
        self.events.append(ev)
        # Note: host sandbox path AND asset_hash are kept in internal DeliveryEvent trace only,
        # NOT returned in model-visible response (prevents exact hash-matching shortcuts!).
        return {
            "ok": True,
            "path": rel,
            "width": w,
            "height": h,
        }

    def get_internal_image_path(self, rel_path: str) -> Optional[Path]:
        """Adapter-only helper to fetch local image bytes for multimodal API attachment."""
        target = self._resolve_safe(rel_path)
        if target is not None and target.is_file() and target.suffix.lower() in IMAGE_EXTS:
            return target
        return None

    def submit_final(self, path: str, content: str) -> Dict[str, Any]:
        import os

        err = self._check_budget("submit_final", path)
        if err:
            return err
        target = self._resolve_safe(path)
        canonical = (self.root / self.deliverable_path).resolve()
        deliverables_root = (self.root / "deliverables").resolve()
        if (
            target is None
            or deliverables_root not in target.parents
            or target != canonical
        ):
            ev = DeliveryEvent(
                episode_id=self.episode_id,
                step=self.step_count,
                tool="submit_final",
                rel_path=path,
                asset_hash=None,
                returned_locator={},
                success=False,
                payload_hash=sha256_text("INVALID_DELIVERABLE_PATH"),
                error=f"Deliverable must target the exact canonical path `{self.deliverable_path}`; evidence files are read-only.",
            )
            self.events.append(ev)
            return {"ok": False, "error": ev.error}

        target.parent.mkdir(parents=True, exist_ok=True)
        # Atomic write via temp file + os.replace
        tmp_path = target.with_suffix(target.suffix + ".tmp")
        tmp_path.write_text(content, encoding="utf-8")
        os.replace(tmp_path, target)

        rel_clean = str(target.relative_to(self.root))
        content_h = sha256_text(content)
        self.submitted_path = rel_clean
        self.submitted_content = content
        self.submitted_hash = content_h
        self.terminated = True
        self.termination_reason = "submitted"

        ev = DeliveryEvent(
            episode_id=self.episode_id,
            step=self.step_count,
            tool="submit_final",
            rel_path=rel_clean,
            asset_hash=content_h,
            returned_locator={"bytes": len(content.encode("utf-8"))},
            success=True,
            payload_hash=content_h,
        )
        self.events.append(ev)
        return {
            "ok": True,
            "submitted_path": rel_clean,
            "content_hash": content_h,
            "terminated": True,
        }

    def export_trace(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "steps_used": self.step_count,
            "max_tool_calls": self.max_tool_calls,
            "termination_reason": self.termination_reason,
            "submitted_path": self.submitted_path,
            "submitted_hash": self.submitted_hash,
            "submitted_content": self.submitted_content,
            "events": [asdict(e) for e in self.events],
        }
