#!/usr/bin/env python3
"""Check literal preservation of caller-declared tokens; this does not translate."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PASS = 0
FAILED = 1
NOT_RUN = 2


def result(status: str, reason: str, checks: list[dict[str, Any]] | None = None) -> int:
    print(json.dumps({"status": status, "reason": reason, "checks": checks or []}, ensure_ascii=False))
    return {"PASS": PASS, "FAILED": FAILED, "NOT_RUN": NOT_RUN}[status]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("protection_manifest.json"))
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    if not manifest_path.is_file():
        return result("NOT_RUN", "PROTECTION_MANIFEST_MISSING")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return result("NOT_RUN", f"PROTECTION_MANIFEST_UNREADABLE: {type(exc).__name__}")
    if not isinstance(manifest, dict):
        return result("NOT_RUN", "PROTECTION_MANIFEST_MUST_BE_OBJECT")

    tokens = manifest.get("protected_tokens")
    if not isinstance(tokens, list) or not tokens:
        return result("NOT_RUN", "EXPLICIT_PROTECTED_TOKEN_LIST_REQUIRED")
    if any(not isinstance(token, str) or not token for token in tokens):
        return result("NOT_RUN", "PROTECTED_TOKENS_MUST_BE_NONEMPTY_STRINGS")
    if len(tokens) != len(set(tokens)):
        return result("FAILED", "DUPLICATE_PROTECTED_TOKEN_IN_MANIFEST")

    source_name = manifest.get("source_file")
    candidate_name = manifest.get("candidate_file")
    if not isinstance(source_name, str) or not source_name or not isinstance(candidate_name, str) or not candidate_name:
        return result("NOT_RUN", "SOURCE_AND_CANDIDATE_FILES_REQUIRED")
    source_path = (manifest_path.parent / source_name).resolve()
    candidate_path = (manifest_path.parent / candidate_name).resolve()
    if not source_path.is_file() or not candidate_path.is_file():
        return result("NOT_RUN", "SOURCE_OR_CANDIDATE_FILE_MISSING")
    try:
        source = source_path.read_text(encoding="utf-8-sig")
        candidate = candidate_path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return result("NOT_RUN", f"SOURCE_OR_CANDIDATE_UNREADABLE: {type(exc).__name__}")

    checks = []
    for token in tokens:
        source_count = source.count(token)
        candidate_count = candidate.count(token)
        if source_count == 0:
            status = "FAILED"
            reason = "TOKEN_ABSENT_FROM_SOURCE"
        elif candidate_count != source_count:
            status = "FAILED"
            reason = "CANDIDATE_OCCURRENCE_COUNT_CHANGED"
        else:
            status = "PASS"
            reason = "EXACT_LITERAL_OCCURRENCE_COUNT_PRESERVED"
        checks.append({"token": token, "source_count": source_count,
                       "candidate_count": candidate_count, "status": status,
                       "reason": reason})
    overall = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAILED"
    return result(overall, "ALL_DECLARED_TOKENS_PRESERVED" if overall == "PASS" else "DECLARED_TOKEN_CHECK_FAILED", checks)


if __name__ == "__main__":
    raise SystemExit(main())
