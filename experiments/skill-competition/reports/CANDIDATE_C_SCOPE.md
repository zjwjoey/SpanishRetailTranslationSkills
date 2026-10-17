# C 标识保护专项挑战者

状态：`CANDIDATE`（工程专项挑战者）；真实 SKU 质量与完整翻译能力：`NOT_RUN`。该候选只检查调用者明确列出的 literal protected tokens 是否在候选文本中按原样、按出现次数保留。它不翻译、不发现全部品牌或型号，也不参与完整翻译方案综合排名。

## 上游依据与许可

来源 C：[`game-localization-skill`](https://github.com/tokyboop/game-localization-skill)，固定 commit `bccaac8abde17bcd9e507a9c729e259ae1750251`。该 commit 的 `LICENSE` 是 MIT，版权主体 tokyboop，2026；10/18 上游快照记录的 SHA256 为 `d7bd356d42ac640a25e2421c53babf0a64c86d88d0421281e14e6004c790ae59`。其 `scripts/translate.py` SHA256 为 `5ed662d13396d9f02d76b3982c74054f6d772e9f29590296ebfaadec57b0e133`。完整原始哈希清单在 `local/skill-competition/upstream-audit/UPSTREAM_CHECKS.json`。

上游 C 的翻译、载入、QA、保存步骤仍为 TODO；对有效合成 CSV 实测 exit 0，但译文与 QA 输出文件均不存在。本专项因此把 C 划为可运行的 token 保护挑战者，不包装成翻译器。

本候选未复制上游代码、文档或样例文件，因此无需在候选中附带 MIT 文本；复制文件 SHA256：无。新写的 `SKILL.md`、Python 检查器、Codex adapter 说明和合成控制均为本项目独立新增。适配范围限于 token 保存这一项工程性质的核验。

## 行为契约

输入 JSON manifest 需要提供相对 manifest 的 `source_file`、`candidate_file` 和非空 `protected_tokens` 字符串数组。检查按大小写敏感的字符串原样匹配：每个声明 token 必须在源文出现，且候选文中的出现次数须与源文相同。缺 manifest 或缺少显式 token 清单时返回 `NOT_RUN` 并说明需要清单；源文没有声明 token，或候选修改/漏掉/改变 token 数量时返回 `FAILED`。检查器不改写文本，输出 token 级计数。

命令：

```powershell
python scripts/check_protected_tokens.py --manifest <manifest.json>
```

退出码：`0=PASS`、`1=FAILED`、`2=NOT_RUN`。`PASS` 只覆盖 manifest 里的 token 保存，不代表意思准确、内容完整或中文自然。

## 合成控制结果

测试输入只在 `local/skill-competition/upstream-audit/c-protection/`，未读取或使用真实 SKU。Python 使用工作区自带 runtime 执行。

| 控制 | 输出状态 | 退出码 | 观察 |
|---|---|---:|---|
| token 原样保留（`QP2734/30`、`{0}`） | `PASS` | 0 | 两个 token 源/候选计数均为 1 |
| 候选把型号改为 `QP2734-30`、占位符改为 `(0)` | `FAILED` | 1 | 两 token 候选计数均为 0 |
| manifest 声明源文中不存在的型号 | `FAILED` | 1 | `TOKEN_ABSENT_FROM_SOURCE`，不把它报作通过 |
| manifest 文件不存在 | `NOT_RUN` | 2 | `PROTECTION_MANIFEST_MISSING` |

这些合成结果证明程序按契约响应，不构成真实商品翻译质量或 token 自动识别覆盖率证据。由于没有真实 SKU 与人工确认的候选译文，真实商品质量为 `NOT_RUN`；未做语言质量打分、完整流水线评测或综合排名。

## 交付与结构验证

- `experiments/skill-competition/candidates/game-c-protection/SKILL.md`：Skill Creator 格式入口，明确触发范围与能力边界。
- `experiments/skill-competition/candidates/game-c-protection/agents/openai.yaml`：候选界面的名称与调用提示。
- `experiments/skill-competition/candidates/game-c-protection/scripts/check_protected_tokens.py`：Python 标准库检查器。
- `experiments/skill-competition/adapters/game-c/README.md`：上游固定版本、适配边界和未实现状态。
- `local/skill-competition/upstream-audit/c-protection/`：合成 source、candidate 和 manifest 控制输入。

尝试运行 Skill Creator `quick_validate.py`，但当前工作区 Python 没有 PyYAML，工具在验证 frontmatter 前以 `ModuleNotFoundError: No module named 'yaml'` 退出；所以该项标记为 `NOT_RUN`。四个 CLI 行为控制已真实执行并通过预期结果核验；命令、原始 JSON 标准输出和退出码保存在 `local/skill-competition/upstream-audit/c-protection/control_results.json`。没有运行额外 CI，也没有改动其他 Skills、共享协议或正式内容。

