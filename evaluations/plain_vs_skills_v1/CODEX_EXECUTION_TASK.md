# Codex 执行指令：启动真正的普通 Codex vs 当前五 Skills 对照

你是独立基准评测执行者。已有用户的 `SpanishRetailTranslationSkills` 本地仓库及历史 Action/Amazon/IKEA 实际训练数据。目标：**分别在30个从未用于该项目训练/优化/审查的真实商品上执行普通 Codex（A）和当前五 Skills（B），独立核验并统计两臂结果**。本轮不是继续训练，也不是对比两个 Skills 版本。

先读取本目录 README.md / PROTOCOL.md、根 AGENTS.md、五个 SKILL.md、契约和 existing evaluation 报告，执行 git status。只从仓库与本机可读的真实数据得出结论。禁止修改正式 Skills、历史回归、approved 知识、任何采集程序/数据库。禁止把私有货盘或完整商品译文推到公开 GitHub。

1. **盘点历史曝光**：识别历史 local/ 中 Action/Amazon 的早期训练和回归、Amazon 200+200/100+1000、IKEA 两批1000、全部特例回归，建立 SKU/ASIN、父子/系列/同款关系和近重复标题黑名单。若不能证明足够排除覆盖，不要写“新 Holdout”，说明缺口。
2. **选样并冻结**：从真实 Action、Amazon.es、IKEA Spain 的只读西语源快照各选10，确认正文西语、身份准确、来源路径、原始 source hash。不能从已曝光组/变体/跨快照重复选。冻结 sample/排除台账 SHA256、当前五个技能文件及 refs、contracts、manifest 的 SHA256，生成只读的30件完整原文输入，所有源与中间文件放 Git 忽略 local/。
3. **建两个真正隔离的 Codex 工作区**：两者均放在原 repo 的祖先路径之外。A 工作区只接受完全相同的输入与中性共同翻译任务，绝不能读取原 AGENTS/Skills/术语库/旧翻译；B 工作区按准确冻结的 commit 提供当前五个 Skills 与专项参考、所需共享契约，不读旧评测报告或 A 输出。双方共同输出 JSON：item_id/platform/product_id/source_sha256、中文标题、规格、描述、平台原类目译名与中文研究类目、品牌/型号/兼容项、源定位、未知槽与来源冲突。允许 A 自行选普通翻译过程，但两臂输入字段/自检次数/输出 schema/模型/批次/沙箱一致。要核实 B 技能实际载入。
4. **实际运行 Codex，不以计划冒充执行**：先查 `codex exec --help`，选择两边确实可用的同一模型，建议 `codex exec --ephemeral --sandbox read-only --skip-git-repo-check -C <workspace> -m <same-model> --json -o <output> <task>`；不同 CLI 版本按实测参数调整。每批5件左右，A/B采用相同顺序。记录 CLI 版本、实际可观测模型、调用设置、运行日志、失败和最终原件；token/费用不可得则 null，不估算。不要启用高权限模式。
5. **独立 QA，先原文后候选**：新的审查上下文先独立完成30件原始西语事实台账并冻结，然后核查 A/B 全部真实翻译，对关键事实、数量/代际、配件、型号兼容全清单、材质、规格、遗漏、幻觉、术语逐个标注证据。区分 P0/P1/P2、真错误与待核、AI意见与人工确认，同根因多处只计一次。不能用结构验证代替语义验收。
6. **交付评测报告**：固定 Action10/Amazon10/IKEA10 与合计30分母；列 A/B 实际产出/完整独立审查覆盖、P0/P1 影响商品、源事实遗漏、术语差异、典型失败、实际 token/时长/费用（若可观测）。没有人工 gold 则用“AI工程性观察”，不可说“已验证准确率提升 X%”。给出下轮最应修的至多3类问题，且不自行修改 Skills。

始终交付**真实完成**与 **BLOCKED/NOT_RUN**。任务授权仅用于本次隔离评测：不合并 main、不自动 push 旧数据、不给 approved 晋级。