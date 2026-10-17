# Game C protection adapter

This isolated Codex candidate implements only a deterministic check for literal protected tokens explicitly supplied by a caller. The upstream C project is [`game-localization-skill`](https://github.com/tokyboop/game-localization-skill), pinned for this comparison at `bccaac8abde17bcd9e507a9c729e259ae1750251` (MIT). Its `scripts/translate.py` contains TODO translation and QA steps and reaches exit 0 without writing the promised output files for a valid CSV.

The candidate does not execute or copy C's translation script. It adds a Codex Skill entrypoint and a standard-library Python manifest checker for the narrow placeholder/model-token preservation challenge. There is no translation model call, automatic token discovery, spreadsheet support, semantic QA, or complete translation workflow. Source and candidate text must be provided by the caller, and the protected-token list must be explicit.
