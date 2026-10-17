# Claude B → Codex adapter

This adapter maps the fixed upstream Claude Code workflow to the capabilities available to a Codex candidate runtime. It is an execution wrapper, not an additional translation knowledge source.

| Upstream concept | Codex candidate mapping | Boundary |
| --- | --- | --- |
| Team lead | Current Codex lead session | Owns manifest, sequencing, contracts, and final evidence |
| `TeamCreate` | Codex task delegation when available; otherwise logical roles run sequentially | No claim of parallel execution without runtime evidence |
| `SendMessage` | Declared files plus the runtime's task handoff/message mechanism | No hidden cross-role state |
| Translator / researcher / reviewer | Codex roles using the configured model | Sonnet and Opus labels are removed; roles do not imply model changes |
| `/tmp/translation-workspace` | Current workspace or explicit temporary task directory | No macOS-only paths or utilities are assumed |
| Claude settings / Agent Teams flag | Codex skill discovery and available task runtime | No Claude configuration is read or changed |
| `.docx`/`.pdf` typesetting phase | Omitted from this minimal retail candidate | Formatting is outside the candidate unless the caller separately requests it |
| General translation workflow | `candidates/claude-b/SKILL.md` | Spanish retail facts remain source-bound; no project Five Skills are injected |

The adapter preserves the upstream role separation and anti-fabrication intent. It does not copy product terminology, historical answers, or repository-specific rules into the public candidate. The caller must provide the source, target, output contract, and any approved evidence separately.

## Candidate invocation

Invoke `experiments/skill-competition/candidates/claude-b/SKILL.md` as a standalone candidate. Load the linked references only when the corresponding workflow phase needs them. Keep each role's artifacts in the caller-provided workspace and record role status as `PLANNED`, `RUNNING`, `TESTED`, `BLOCKED`, `FAILED`, or `NOT_RUN`.

