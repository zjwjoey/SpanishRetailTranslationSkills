"""Exercise actual read-only CLI reads; never inject Skill bodies or source answers."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import time
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def probe(config, arm, output):
    env = load(config)
    flags = env["flags"]
    assert flags[flags.index("--sandbox") + 1] == "read-only"
    assert not any("dangerously" in flag for flag in flags)
    workspace = Path(env["workspaces"][arm]).resolve()
    source = workspace / "probe-input.json"
    source_data = load(source)
    destination = Path(output) / arm
    destination.mkdir(parents=True, exist_ok=False)
    prompt = (
        "Synthetic runtime test only, not real product quality. Use a local read tool "
        "with login=false and an explicit workdir equal to " + str(workspace) + ". "
        "Read the actual file at " + str(source) + ". Use absolute paths, because shell "
        "startup can change the working directory. Read no other workspace or old answers. "
        "No network, no agents, no writes. Translate BOTH source_es strings into zh-CN. "
        "Return a single final JSON object with canary (exact value read from file), "
        "items [{id,title_zh}], skills_used, and observed_read_paths. Do not guess the "
        "canary or source. If any required read fails, return READ_BLOCKED."
    )
    if arm == "current-skills":
        prompt += (
            " Use $es-retail-translator and relevant other available retail Skills natively. "
            "Actually read the selected SKILL.md and its necessary references using their "
            "absolute paths in this workspace. Do not load every reference indiscriminately. "
            "The small probe JSON is an output adapter; no Skill text is supplied inline."
        )
    elif arm == "claude-b":
        prompt += (
            " Use $claude-b-translation-quality natively. Read its actual SKILL.md and "
            "necessary references in this workspace. No Skill body is supplied inline. "
            "For this read-only readiness probe, roles run sequentially in this context; "
            "do not claim independent review or parallel handoffs."
        )
    (destination / "prompt.txt").write_text(prompt, encoding="utf-8")
    command = [env["cli"], "exec", *flags, "-C", str(workspace), "--json",
               "-o", str((destination / "last.txt").resolve()), "-"]
    started = time.monotonic()
    with (destination / "events.jsonl").open("wb") as stdout, (destination / "stderr.txt").open("wb") as stderr:
        result = subprocess.run(command, input=prompt.encode(), stdout=stdout,
                                stderr=stderr, timeout=240, cwd=workspace)
    elapsed = time.monotonic() - started
    raw = (destination / "last.txt").read_text(encoding="utf-8-sig") if (destination / "last.txt").exists() else ""
    parsed = None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        pass
    events = [json.loads(line) for line in (destination / "events.jsonl").read_text(encoding="utf-8").splitlines() if line]
    reads = [event["item"] for event in events if event.get("type") == "item.completed"
             and event.get("item", {}).get("type") == "command_execution"]
    canary_ok = bool(parsed and parsed.get("canary") == source_data["canary"])
    ids_ok = bool(parsed and [item.get("id") for item in parsed.get("items", [])]
                  == [item["id"] for item in source_data["items"]])
    skill_read_commands = [item for item in reads if "SKILL.md" in item.get("command", "") and item.get("exit_code") == 0]
    evidence = {"arm": arm, "exit_code": result.returncode, "elapsed_seconds": round(elapsed, 3),
                "model_requested": env["model_requested"], "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "canary_matches": canary_ok, "item_ids_match": ids_ok,
                "successful_commands": sum(item.get("exit_code") == 0 for item in reads),
                "successful_skill_read_commands": len(skill_read_commands),
                "native_read_probe_passed": canary_ok and ids_ok and bool(reads)
                    and (arm in ("plain", "professional") or bool(skill_read_commands)),
                "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "usage": [event.get("usage") for event in events if event.get("type") == "turn.completed"],
                "quality_acceptance": "NOT_RUN"}
    (destination / "result.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False), flush=True)
    return evidence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--arms", nargs="+", default=["plain", "current-skills"])
    args = parser.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda arm: probe(args.config, arm, args.out), args.arms))
    raise SystemExit(0 if all(result["native_read_probe_passed"] for result in results) else 1)
