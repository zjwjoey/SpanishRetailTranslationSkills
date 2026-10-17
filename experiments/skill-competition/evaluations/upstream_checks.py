#!/usr/bin/env python3
"""Read-only audit helpers for the V1 upstream repositories.

The script inventories the already cloned repositories, verifies remote HEAD and
tree hashes, and runs small synthetic controls. It never copies upstream text
into the report and writes only under local/skill-competition/upstream-audit.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "local" / "skill-competition" / "upstream-audit"
REPOS = {
    "translation-quality-codex": "https://github.com/WenhaoLiu0218/translation-quality-codex",
    "claude-translation-skill": "https://github.com/senshinji/claude-translation-skill",
    "game-localization-skill": "https://github.com/tokyboop/game-localization-skill",
}


def run(cmd: list[str], cwd: Path | None = None) -> dict:
    # Upstream shell checks can emit UTF-8 while this Windows host defaults to
    # GBK. Decode diagnostically and preserve output instead of losing the run.
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    p = subprocess.run(cmd, cwd=cwd, env=env, text=True, encoding="utf-8", errors="replace", capture_output=True)
    return {"command": cmd, "cwd": str(cwd) if cwd else None, "exit_code": p.returncode,
            "stdout": (p.stdout or "")[-12000:], "stderr": (p.stderr or "")[-12000:]}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(repo: Path) -> list[dict]:
    out = []
    for path in sorted(p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts):
        rel = path.relative_to(repo).as_posix()
        data = path.read_bytes()
        # Reading every file here is deliberate; only metadata is emitted.
        _ = data.decode("utf-8", errors="replace")
        out.append({"path": rel, "bytes": len(data), "sha256": sha256(path)})
    return out


def main() -> int:
    AUDIT.mkdir(parents=True, exist_ok=True)
    result = {"checked_at": datetime.now(timezone.utc).isoformat(), "repos": [], "controls": []}
    for name, url in REPOS.items():
        repo = AUDIT / name
        if not (repo / ".git").exists():
            result["repos"].append({"name": name, "url": url, "status": "MISSING_CLONE"})
            continue
        rev = run(["git", "rev-parse", "HEAD"], repo)
        remote = run(["git", "ls-remote", "origin", "HEAD"], repo)
        status = run(["git", "status", "--porcelain"], repo)
        tree = run(["git", "rev-parse", "HEAD^{tree}"], repo)
        result["repos"].append({"name": name, "url": url,
            "commit": rev["stdout"].strip(), "remote_head": remote["stdout"].split()[0] if remote["stdout"].split() else None,
            "tree": tree["stdout"].strip(), "clean": not bool(status["stdout"].strip()),
            "files": inventory(repo), "read_all_files": True})

    a = AUDIT / "translation-quality-codex"
    if a.exists():
        probe = AUDIT / "probe-a"
        probe.mkdir(exist_ok=True)
        source = probe / "source.md"
        source.write_text("# Synthetic\n\nA model QP2734/30 has 2 units and 5 cm.\n", encoding="utf-8")
        job = probe / "job"
        result["controls"].append({"name": "A_prepare", **run([sys.executable, "skills/translation-quality-codex/scripts/prepare_translation_job.py", str(source), "--out-dir", str(job)], a)})
        result["controls"].append({"name": "A_validate_pending", **run([sys.executable, "skills/translation-quality-codex/scripts/validate_translation_job.py", str(job)], a)})
        aligned = job / "translation_aligned.md"
        if aligned.exists():
            aligned.write_text(aligned.read_text(encoding="utf-8").replace("<translation pending>", "unrelated English"), encoding="utf-8")
        result["controls"].append({"name": "A_build_unrelated", **run([sys.executable, "skills/translation-quality-codex/scripts/build_readable_output.py", "--job-dir", str(job)], a)})
        result["controls"].append({"name": "A_validate_unrelated", **run([sys.executable, "skills/translation-quality-codex/scripts/validate_translation_job.py", str(job)], a)})
        result["controls"][-1]["unrelated_translation_used"] = bool(aligned.exists() and "unrelated English" in aligned.read_text(encoding="utf-8"))

    c = AUDIT / "game-localization-skill"
    if c.exists():
        probe = AUDIT / "probe-c"
        probe.mkdir(exist_ok=True)
        csv = probe / "input.csv"
        csv.write_text("id,text\n1,QP2734/30 {0} 2 unidades\n", encoding="utf-8")
        result["controls"].append({"name": "C_translate_csv", **run([sys.executable, "scripts/translate.py", str(csv), "--target", "zh-CN", "--output", str(probe / "out.csv")], c),
            "expected_output": str(probe / "out.csv"), "output_exists": (probe / "out.csv").exists(),
            "qa_report_exists": (probe / "out_qa_report.json").exists()})
        result["controls"].append({"name": "C_translate_missing", **run([sys.executable, "scripts/translate.py", str(probe / "missing.csv"), "--target", "zh-CN"], c)})

    b = AUDIT / "claude-translation-skill"
    if b.exists():
        bash = Path(r"C:\Program Files\Git\bin\bash.exe")
        if bash.exists():
            result["controls"].append({"name": "B_test-skill-integrity", **run([str(bash), "references/test-skill-integrity.sh"], b)})
            probe = AUDIT / "probe-b"
            probe.mkdir(exist_ok=True)
            source = probe / "source.html"
            translation = probe / "translation.md"
            source.write_text("<table><tr><td>Model</td><td>Units</td></tr><tr><td>QP2734/30</td><td>2</td></tr></table>\n", encoding="utf-8")
            translation.write_text("| Modelo | Unidades |\n|---|---|\n| QP2734/30 | 2 |\n", encoding="utf-8")
            result["controls"].append({"name": "B_test-translation-structure", **run([str(bash), "references/test-translation-structure.sh", str(source), str(translation)], b)})
        else:
            for name in ("B_test-skill-integrity", "B_test-translation-structure"):
                result["controls"].append({"name": name, "command": ["bash"], "cwd": str(b), "exit_code": None, "stdout": "", "stderr": "bash unavailable; NOT_RUN"})

    (AUDIT / "UPSTREAM_CHECKS.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"repos": len(result["repos"]), "controls": len(result["controls"]),
                      "output": str(AUDIT / "UPSTREAM_CHECKS.json")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
