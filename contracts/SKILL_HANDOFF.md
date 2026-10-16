# 五技能交接与批次协调 1.0.0-foundation

主智能体读AGENTS调度；不存在第六个Skill。所有交接带item_id/source_snapshot/contract_version/knowledge_version，收到不同源hash不得套用旧结论。

Category输出category_context（source_categories、translated_source_categories、proposed_research_categories、evidence、status）；保留原层级。Terminology输出terminology_decisions及protected_identifiers；不决定整段去留。二者可并行初判，歧义最终由类目与原文合并解决，不能循环互调。
必要时Reviewer.SOURCE_AUDIT接收完整源、两者结论，按独立契约筛选。普通短字段可省复杂筛选，须记source_audit=null及skip_reason=short_clear_fields，不等于做过源审。
Translator读取完整源+适用知识+可选source_audit，按输出契约生成候选。后审Reviewer需完整源+源动作+实际中文；不能只看精简文本或译者解释。
Learning只读取已人工确认纠错，写knowledge/proposals候选，不覆写knowledge/approved。无确认则EVIDENCE_BLOCKED；正式规则合并由主智能体审核，Validation和独立复审后进行。

批量：先按平台、商品关系组、类目和复杂度分批。当前环境4个并发名额含主智能体，独立QA时可采用2个工作Agent+1 QA；不能误称3工作+QA同时运行。普通40–60/批、长字段5–15/批及首轮100–200SKU仅实验假设。无可信小样本时先做更小工程演练，不放大5500。
所有记录基础核查身份、完整性、数字单位/包装层次、状态；高风险全部独立深审，低风险按事先记录种子和规则抽检。被抽检不等于全部深审。保护词原串一致不能代替单位语义核查。
已人工核验旧译只在完整源hash、选中变体、相关规则/术语版本均未变时复用；记录命中依据，源改变则失效。禁止把历史RAW缓存当已批准缓存。

每批batch_id、input_item_ids、输入/知识/Skills版本、输入数/返回数/唯一身份数、各状态明细、审查覆盖、耗时/token（未知null）、恢复位置、重跑决策。缺失/重复返回阻止该批通过。分批结果只附加新尝试，不覆盖人工确认结果。
