# SOURCE_AUDIT 契约 1.0.0-foundation

输入：完整ITEM_INPUT_CONTRACT记录 + category_context + terminology_decisions/protected_identifiers。类别与术语可并行初判；歧义解决后才能给确定筛选结论。缺少必要上下文时列出缺口，不自行假定。

输出：item_id、product_id、source_snapshot、mode=SOURCE_AUDIT、contract_version、knowledge_version、decisions[]、preservation_ledger[]、conflicts[]、truncations[]、status。决策只决定内容去向，不生成最终中文译文。

每个decision字段：`decision_id/item_id/source_field/source_span/action/reason/target_field/review_status`。source_span为`{quote,occurrence,start,end}`；quote必须是原文精确子串，occurrence从1起。偏移可null（以Unicode码点、半开区间为准）；重复同句必须指明出现次数或唯一定位。review_status=PROPOSED/REVIEW_REQUIRED；本次AI决策不等于人工批准。

动作严格六种：

|action|约束|
|---|---|
|TRANSLATE|明确商品事实，进入对应中文字段；不能混入推断|
|PRESERVE|品牌、系列、型号、ASIN/GTIN/零件号/技术代码原样保存，记录目标路径|
|METADATA|评分/排名/发布日期/评论等转至research_metadata或identifiers，不删除来源|
|DEDUPLICATE|仅当重复片段无独有事实，记录canonical_decision_id及事实等价理由；不同部件、不同字段数量不因文字相近去重|
|EXCLUDE_FROM_DESCRIPTION|网页噪声等不进中文描述；target_field=source_archive，完整源仍在输入中|
|REVIEW_REQUIRED|冲突、截断、信息归属或删除价值不明；不输出确定替代值|

任何非TRANSLATE动作都必须在preservation_ledger中有decision_id/source_field/source_span/disposition/target_field/retained_fact_refs，覆盖所有转出/去重/保留片段。去重指回保留的canonical位置，不能仅写“重复”。元数据与保护词的实际值应出现在对应目标，不能只有抽象动作。
retained_fact_refs每项可以是可解析目标路径/事实ID字符串、结构化原文引用`{source_field,source_span,value}`，或去重保留指针`{canonical_decision_id}`。原文引用用于归档或冲突槽证据，必须能在不可变输入回查；去重指针必须指向存在且实际保留事实的decision。两者不能替代品牌/元数据要求的实际目标值。不得用空数组敷衍应保存的事实。

配置冲突按同一语义槽比较：如两处明确的包装刀片数量2与1。`5 en 1`不是5件，`60 minutos`不是包装数，型号中的30不是件数；“含两刀片”和“机身已装一片”可能兼容，未证实包装归属时待审，不强判冲突。
`Ver más/查看更多/…`要同时判断网页残留与是否缺后文。不能仅剔除提示就声称正文完整。部分无歧义事实可以保留，但整件有未决冲突/截断则status=REVIEW_REQUIRED。

status=PASSED/REVIEW_REQUIRED/FAILED。PASSED只说明本次源筛选检查无未决问题，不批准译文或样本VERIFIED。缺完整源或身份无法确定为FAILED。不得覆盖原始源。
