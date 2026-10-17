# Candidate B adaptation record

2026-10-18运行补充：B已在同条件gpt-6-luna原生读取探针及六Amazon开发商品执行中通过入口证据门禁；独立AI核对已完成。下文早期NOT_RUN保留为适配完成时状态，不代表当前未执行。见[开发报告](DEVELOPMENT_RESULTS_20261018.md)，无质量胜出或人工金标结论。

状态：`CANDIDATE` / `TESTED`（来源、适配结构与 quick_validate）；真实商品翻译：`NOT_RUN`。

本次续作与最终入口审校/验证模型：`gpt-6-luna`（2026-10-18）。此前由其他模型形成的证据保持原记录和独立归属，不合并改写为本模型执行结果。

## 来源与许可证

- 上游：<https://github.com/senshinji/claude-translation-skill.git>
- 实际 `git ls-remote` HEAD/main：`42d6c8a2a07b77f085d6cafe6d4102d36aeafd02`
- 独立私有克隆：`local/skill-competition/candidate-b/upstream-clone-20261018/`
- `LICENSE` 已读取，明确为 MIT License，版权声明为 `Copyright (c) 2026 senshinji`。
- 上游 clone 未被候选适配改写；公共候选保留原 MIT `LICENSE` 文件。
- 未读取或复制其他候选答案、真实训练/验证/holdout 数据、现有五 Skills 规则或私有货盘。

上游文件 SHA256（固定 commit）：

| 文件 | SHA256 |
| --- | --- |
| `SKILL.md` | `4D01DE1756AE1526C0FCE31B800D3CDE6B42B6B596D4F4842008AEA2834A1610` |
| `references/glossary-schema.md` | `40C9C0ADEBEE73B92BBD6C5792C1430B7B0D718F21AB21B64BCCFC1A8ED77E83` |
| `references/review-feedback-schema.md` | `5CB82A0377243948B109D2C455D57EFE71C91E22D7D0F5C0F2D724E0C70EA23F` |
| `references/anti-fabrication-checklist.md` | `77439CA314C1FF09A13D4EDCDFBAD1F6DAF42F3B096AD5AE6225D806B5CD1CF4` |
| `references/scaling-guidelines.md` | `CBCD8B5163069AFE3C7C4AA989787D3F9C83FE1230F770990B70A480A7CC7B69` |

## 适配内容

公共候选入口为 [`candidates/claude-b/SKILL.md`](../candidates/claude-b/SKILL.md)，适配说明为 [`adapters/claude-b/README.md`](../adapters/claude-b/README.md)。实际保留的上游参考只有术语契约、审查契约、反虚构清单和长文分块指南；它们不含本项目商品答案。

| 原始能力/约束 | Codex 适配 | 适配边界 |
| --- | --- | --- |
| Team lead + Agent Teams | 当前 Codex lead session；有可用运行时时才委派任务 | 无运行时证据不声称并行 |
| `TeamCreate` / `SendMessage` | 角色任务、声明文件和 Codex 可用交接机制 | 不依赖 Claude API 或隐藏共享状态 |
| Sonnet / Opus | 同一配置模型下的逻辑角色 | 不引入模型等级或额外算力优势 |
| `/tmp/translation-workspace`、macOS `textutil` | 调用方工作区/临时目录 | 不假设 macOS 路径或工具 |
| 文档排版 `.docx`/`.pdf` | 从最小零售候选中移除 | 不是本候选的质量能力 |
| 通用翻译流程 | 保留术语→翻译→审查→修订闭环 | 不自动混入五个正式 Skills、商品术语或历史答案 |

可调用清单位于 [`adapters/claude-b/manifest.json`](../adapters/claude-b/manifest.json)，适配差异说明与逐行入口 diff 位于 [`adapters/claude-b/ADAPTATION_DIFF.md`](../adapters/claude-b/ADAPTATION_DIFF.md) 和 [`adapters/claude-b/entrypoint.diff`](../adapters/claude-b/entrypoint.diff)。最终入口已移除草稿中额外列出的零售属性清单，保持本候选只做运行时映射，没有新增商品知识、项目专属规则或真样本答案。

适配只改变执行接口、路径和角色表达，未针对本轮商品或数据加入新的翻译规则。公共候选没有上游完整 `SKILL.md` 的 Claude 专属安装/配置指令；私有原版仍在 local 克隆中作为适配前证据。

## 候选文件与哈希

| 文件 | SHA256 |
| --- | --- |
| `candidates/claude-b/SKILL.md` | `4AD33BB85C297A902BAFED1469218309975DF858F9D5A71B408037C467C0977B` |
| `candidates/claude-b/LICENSE` | `7C1CFD96F852BF4C228B7BAE61878D3B7401535405DAF15D81D3F21C26AFC8BE` |
| `candidates/claude-b/references/glossary-schema.md` | `40C9C0ADEBEE73B92BBD6C5792C1430B7B0D718F21AB21B64BCCFC1A8ED77E83` |
| `candidates/claude-b/references/review-feedback-schema.md` | `5CB82A0377243948B109D2C455D57EFE71C91E22D7D0F5C0F2D724E0C70EA23F` |
| `candidates/claude-b/references/anti-fabrication-checklist.md` | `77439CA314C1FF09A13D4EDCDFBAD1F6DAF42F3B096AD5AE6225D806B5CD1CF4` |
| `candidates/claude-b/references/scaling-guidelines.md` | `CBCD8B5163069AFE3C7C4AA989787D3F9C83FE1230F770990B70A480A7CC7B69` |
| `adapters/claude-b/README.md` | `51001D83888559DB55006D8B0DF0F5714E01E4662A167D9B1FC21D42CACD8A32` |

## 验证与边界

- `git ls-remote`、独立 clone、固定 commit checkout、MIT `LICENSE` 读取：`TESTED`。
- `git diff --no-index --check`（固定上游入口对适配入口）：`TESTED`，发现并清除入口末尾多余空行后无 whitespace error。
- 候选目录包含可调用 `SKILL.md`、MIT 通知和实际被入口链接的必要 references：`TESTED`（静态检查）。
- `skill-creator/scripts/quick_validate.py`：`TESTED`，官方验证器输出 `Skill is valid!`。通过临时安装到系统临时目录的 PyYAML 依赖运行，未写入全局 Skill 或修改 Codex 配置。
- 上游 shell integrity/structure tests：`NOT_RUN`，本候选不包含商品样例，也没有 macOS shell 运行前提。
- 真实商品翻译、批量运行、Codex 原生读取、质量评分：`NOT_RUN`，由 root 负责运行时读取和后续统一实验。
- 本候选没有新增商品内容；任何小合成控制只能证明接口/流程，不代表商品质量通过。

后续运行状态见 RUNTIME_20261018.md；入口差异另保存为零上下文unified diff，内容差异不变，原有带上下文版本保留在私有candidate-b证据目录。
