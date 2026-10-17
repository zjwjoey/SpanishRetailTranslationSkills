# Upstream-to-Codex adaptation diff

Source: `senshinji/claude-translation-skill` at `42d6c8a2a07b77f085d6cafe6d4102d36aeafd02`.
Adapted entrypoint: `experiments/skill-competition/candidates/claude-b/SKILL.md`.

The candidate keeps the upstream translation stages and linked schemas/checklist. Its entrypoint changes are limited to the execution environment and this candidate's declared scope:

| Upstream instruction | Candidate form | Reason |
| --- | --- | --- |
| Claude Agent Teams, `TeamCreate`, and `SendMessage` | Lead session owns orchestration; roles run sequentially or use available Codex delegation; artifacts pass through declared files and supported handoff | Codex runtime compatibility; no assumed Claude API |
| Sonnet/Opus-specific role assignments | Use the configured Codex model for all roles | Preserve responsibilities without implying unavailable model selection |
| `/tmp/translation-workspace` and macOS `textutil` paths/tools | Use the caller-provided workspace or task temporary directory | Remove platform-specific execution assumptions |
| Mandatory Word/PDF typesetting phase | Omitted from this retail translation candidate | Typesetting is outside this candidate's declared scope |
| Claude skill installation/settings instructions | Omitted | Not applicable to Codex |

The four linked references are byte-for-byte copies of the fixed upstream files; the MIT license notice is retained. The final candidate entrypoint adds no product glossary, project-specific translation rules, or sample answers. Earlier draft wording that listed retail-specific attributes was removed before this adaptation was frozen.

For a line-level unified diff of the entrypoints, compare the upstream clone's `SKILL.md` with `../../candidates/claude-b/SKILL.md`; the table above records the intentional transformations and the full unmodified source remains in the ignored local clone.
