---
name: game-c-protection
description: Check literal protected tokens explicitly listed for a source and candidate translation; use only for token preservation, not translation or overall quality review.
---

# Game C protection challenge

Use this candidate only to check preservation of tokens that the caller explicitly declares, such as a model code or placeholder. It does not translate text, discover every brand or model, or establish translation quality.

Require a JSON manifest with `source_file`, `candidate_file`, and a non-empty `protected_tokens` array. Paths are relative to the manifest. If the manifest or token list is missing, say the check is `NOT_RUN` and request the explicit list. Never infer a complete token list from patterns or claim that a regular expression recognizes all protected names.

Run `scripts/check_protected_tokens.py --manifest <path>`. It compares each listed token as a case-sensitive literal string. Each token must occur in the source and the candidate must contain exactly the same number of occurrences. A missing source token or any candidate count change is `FAILED`; all checks passing is `PASS`. The checker reports counts and never edits either text.

Use `PASS`, `FAILED`, or `NOT_RUN` only for this narrow check. A `PASS` says nothing about translation meaning, completeness, or fluency. Do not present this candidate as a complete translation workflow or include it in a comprehensive translation ranking.
