# V2：简单业务要求 vs 专业提示词 vs 原生按需 Skills

日期：2026-10-17。状态：**PROTOCOL_READY / REAL_RUN_NOT_STARTED**。

## 为什么重做
V1 30 SKU / 60 候选由 AI 全部审读，未确认双方有 P0/P1；但普通组接受了很强的专家约束，而 Skills 组采用了 123,603 字节规则全文注入，既不是朴素普通翻译也不是原生按需加载。V1 的输入 token 为 108,194 vs 478,454（约 4.42 倍），其成本结论不可直接外推。另有 AI 审查误报及未决问题。不能宣称 Skills 优于专业提示词，也不能替它开脱。

本轮不扩大训练，也不更改五个 Skills。重新预登记三组：
- **A / Simple**：真正简短业务要求 + 对所有组相同的结构化交付格式；没有专家检查清单、没有 Skills。
- **B / Expert Prompt**：A 同样的业务要求与格式 + 固定的专业检查清单；没有 Skills。
- **C / Native Skills**：与 A 一字不差的业务要求和格式，仅在隔离工作区中启用冻结的五个专业 Skills，让 Codex 原生按需发现和阅读；**不得用规则全文注入代替原生调用**。

先执行**24 个全新真实西语 SKU 的小规模诊断**：Action、Amazon.es、IKEA Spain 各 8 个，每平台按预登记源文复杂度选择 4 普通、4 复杂。同一批 24 个 SKU 同时交给 A/B/C，共计划 72 份原始译文。先前 30 SKU 全部视为已曝光，仅可用于流程冒烟测试，不作为此次未知数据成果。新样本与全部旧批次/变体/系列/近重复组做交叉排除，不能核实则 NOVELTY_UNVERIFIED，不冒称正式 Holdout。

## 开始前的双门禁
1. 先在隔离外部工作区用手工 synthetic 文本进行 Codex **native discovery + on-demand SKILL.md / reference 读取**验证，留下真实宿主事件。光有目录或模型口头说“调用了 Skill”不算；不通过则本轮 C=NOT_RUN，不得退回全文注入凑数据。
2. 再核查 A/B 工作区无法看到项目五 Skills、根 AGENTS 的专门规则、之前的输出和全局同类技能。若不能证明隔离，整个 A/B/C 标记 NOT_COMPARABLE，不冒称三组对照。

执行任务见 [CODEX_EXECUTION_TASK.md](CODEX_EXECUTION_TASK.md)，详细预登记见 [PROTOCOL.md](PROTOCOL.md)，两份提示文本和 C 原生约束见 [PROMPTS.md](PROMPTS.md)，报告字段见 [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)。

## 质量证据与结论
独立 QA 先对源文作事实清单，再审查盲化的 A/B/C 输出；审查意见可以撤回，不能直接当错误。真实**人工返工秒数、实际修订字段、确认问题**必须有人工作业记录，没有人工记录则报告 N/A，不能以 AI 估算代替。复杂和普通商品分别统计，平台分别展示。

旧仓库的 local/ 数据、原始商品、完整译文、CLI 原始日志应继续保持 Git 忽略及只读。此分支仅新增评测说明和将来的匿名汇总，不改主程序、批准词库、既有 Skills 或历史测试。用户未授权合并，禁止自动合并、发布或自行改 Skill。
