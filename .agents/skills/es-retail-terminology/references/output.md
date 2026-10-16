# 术语输出及交接

沿用contracts的`1.0.0-foundation`；这里定义术语专项附加字段，不覆盖共享契约。每个商品独立输出：

- `item_id/platform/product_id/source_snapshot`：与输入一致；`source`原样保留或给可访问的不可变`source_ref`。缺必需信息失败时保留已收到部分，不伪造值。
- `contract_version/knowledge_version/skill_version`：实际读取版本。知识manifest无术语时使用其版本，不能用Skill版本冒充知识版本。
- `terminology_decisions[]`：`decision_id/es_term/source_field/source_span/context/zh_candidate/alternatives/decision_status/knowledge_entry_id/evidence_refs/reason/excluded_interpretations`。
- `protected_identifiers[]`：至少`value/type/source_field/source_span/target_field`，可附`role`区分本商品与兼容对象；重复出现分别定位。type为brand/series/model/asin/gtin/part_number/technical_code等，未知类型可写unknown并复核。target_field指向下游`identifiers`实际保存路径，不只说“应保留”。
- `uncertainties[]/conflicts[]/input_gaps[]`：问题、涉及decision_id及原文位置、需要的最小证据。完整源不改写。
- `checked_fields/unreviewed_fields/status/status_reason`：精确说明覆盖范围及未决风险；`run_metadata`记录实际模型（未知unknown）、调用方式、输入hash、实际读取Skills、耗时/token（不可得null）。

`source_field`指向source内确切字段/数组序号，例如`source.specifications[1].value`；`source_span={quote,occurrence,start,end}`，quote是原串精确子串，occurrence从1计数，偏移未知为null，有值时按Unicode码点半开区间。重复属性不折叠；跨字段证据分别定位。

另含 `semantic_slots[]`（可空）：有数量、尺寸、组合或时长时，按 `kind/value/unit/qualifier/source_field/source_span` 分离事实槽，避免保护数字却误解语义。该数组是候选术语依据，不代替翻译保留事实账本。

decision_status为`CANDIDATE/APPROVED/UNCERTAIN`。APPROVED只表示实际存在的人工批准知识条目适用，不批准新商品，也不修改verification_status；无适用条目填knowledge_entry_id=null，evidence_refs列原文位置，不制造批准号。UNCERTAIN的zh_candidate可为null并保留alternatives。

context记录来源类目、原文用途、采用的类别候选及适用/排除条件。原文用途优先；category_context仅推断时明确标记候选，不能转换为商品事实。相同source_snapshot的Category输出可合并，无需互调。下游应能从这些位置重新检查，不能只接收一张脱离语境的中西词表。

PASSED不意味着翻译已通过后审；Reviewer仍需完整源与其独立筛选账本。术语Skill不产生`DEDUPLICATE`等片段去向决策，不填最终`translation_zh`以替代Translator，不修改knowledge/approved。
