# 翻译输出契约 1.0.0-foundation

输出必须保留item_id/platform/product_id/source_snapshot，以及原始source或不可变引用。`stage`为TRANSLATION_CANDIDATE/TRANSLATION_AUDIT；`status`为PASSED/REVIEW_REQUIRED/FAILED。

`translation_zh`分title、categories（只译来源平台类目）、specifications（有序key/value）、bullets、description、details、brand。未提供/冲突影响的目标字段null，不能用null抹去未受影响的事实。`identifiers`保存品牌/系列/型号/条码/ASIN等保护原串；`research_metadata`保存转出的排名/评分等；`category_context.proposed_research_categories`单列研究建议，不能冒充平台分类。

每个字段`field_alignment[]`含source_field、source_span、target_field、translated_text、fact_ids、source_audit_decision_ids。`protected_identifiers[]`含value/type/source_field/source_span/target_field；`retained_facts[]`含fact_id、source位置、target路径/值、限定词及冲突状态。去重/迁移/排除继续沿用SOURCE_AUDIT账本，不以最终短描述替代证明。

`uncertainties[]`和`conflicts[]`保留问题及原文证据；`review`含mode、independence_method、checked_fields、unreviewed_fields、candidate_findings（severity/field/source_span/target_span/reason）、结论。`run_metadata`含实际模型（未知写unknown）、契约/Skills/知识版本、实际读取的Skills、输入hash、调用方式、起止时间/耗时与token（不可得null）。不得编造调用、成本、人工核验。

Translator永远stage=TRANSLATION_CANDIDATE，不可status=PASSED；无明显问题的草稿也用REVIEW_REQUIRED并注明awaiting_post_audit，不表示源有错误。Reviewer.TRANSLATION_AUDIT在独立重读完整源、源动作账本和中文后才能就实际检查范围判PASSED。未独立审查、只查部分却要求整商品通过、存在未决P0/P1/源问题都保持REVIEW_REQUIRED。身份/关键原文无法获得为FAILED。
PASSED不意味着人工确认或VERIFIED，AI审查无法替代后续训练准入。

不同字段的事实迁移必须可追溯；源“2 x 500 ml”保留件数与单件容量；1,5与1.5可等价；品牌或型号不能因为不译就丢失。矛盾值按局部事实槽隔离，不擅自挑选一个。数据状态与运行状态分开。
