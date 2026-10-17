---
name: claude-b-translation-quality
description: "Candidate translation workflow adapted from claude-translation-skill for Codex. Use for professional Spanish-to-Chinese document or product-field translation when terminology, omission, fabrication, and structure checks are required."
metadata:
  short-description: "Codex-adapted terminology, translation, review, and revision workflow"
---

# Translation Quality — Codex Candidate B

This is a V1 competition candidate adapted from `senshinji/claude-translation-skill` at the fixed commit recorded in the adaptation report. It keeps the source workflow's separation of terminology research, translation, review, and revision while using Codex-compatible execution. It is a candidate only; it does not modify or invoke the repository's five formal retail Skills.

## Execution contract

The lead session owns orchestration and the final output. Treat translator, terminology researcher, reviewer, and reviser as logical roles. If Codex delegation is available, each role may run in an isolated task with explicit file ownership; otherwise execute the roles sequentially in the same session. Do not claim parallelism, model specialization, or a completed handoff unless the runtime provides evidence.

Use the configured Codex model for every role. The role names describe responsibilities, not model tiers. Use the current workspace or a task-specific temporary workspace; never assume `/tmp`, macOS utilities, or a Claude settings file. Pass role results through declared files and structured messages available in the current Codex runtime.

Before translating, read the whole source and define source language, target language, document/field boundaries, structure, and uncertainty. Preserve source facts and mark uncertainty for review rather than guessing. Do not turn a candidate observation into an approved rule.

## Workflow

1. Lead creates a manifest describing source fields/sections, tables or lists when present, and output paths. For long material, use the chunking guidance in [references/scaling-guidelines.md](references/scaling-guidelines.md), never splitting a table or field.
2. Terminology role extracts terms and records translation, confidence, context, and evidence in a glossary following [references/glossary-schema.md](references/glossary-schema.md). Web evidence is optional and must be recorded when used. For product fields, protect brands, model strings, technical codes, measurements, and quantities even when no external source is available.
3. Translator role produces a first pass with source-to-target correspondence and structure preservation. Unclear source facts remain marked for review; they are not guessed. A structure report is required when the source contains tables or lists.
4. Reviewer role checks the complete source against the first pass in both directions. Prioritize fabrication, omission, numbers, identity, specifications, compatibility, terminology, and structure. Write feedback using [references/review-feedback-schema.md](references/review-feedback-schema.md), including the structure comparison table.
5. Reviser role applies critical and major corrections by text-level edits while preserving source structure. The lead then performs a bounded spot check and records unresolved issues as candidate evidence.

## Output boundary

Return only the output fields and metadata requested by the caller. Keep source facts traceable by field or paragraph. Do not declare translation quality, human accuracy, or production readiness from this workflow alone.

## Anti-fabrication and failure handling

Read [references/anti-fabrication-checklist.md](references/anti-fabrication-checklist.md) when translating or reviewing. If a required role, file, source segment, or runtime capability is unavailable, record `BLOCKED` or `NOT_RUN` and continue only with unaffected checks. A quick structural check is engineering evidence, not a product-quality pass.
