# 候选输出参考

按TRANSLATION_OUTPUT_CONTRACT输出，不把此例当商品知识。最小正常例的`source.title`为`Botella, 500 ml`，source_locations.title为synthetic定位。source_snapshot.sha256应实际计算，不填写虚构hash。

字段采用以下关系（非完整JSON模板）：

- `stage: TRANSLATION_CANDIDATE`、`status: REVIEW_REQUIRED`；身份、快照与完整source不变。
- `translation_zh.title: 水瓶，500毫升`；其他未提供字段null，有序规格/详情保持数组语义。
- `field_alignment`: source_field=`source.title`，source_span=`{quote: "Botella, 500 ml", occurrence: 1, start: 0, end: 14}`，target_field=`translation_zh.title`，translated_text=`水瓶，500毫升`，fact_ids引用主体/容量，source_audit_decision_ids=[]。
- `retained_facts`: 主体与容量各含fact_id、source位置、target路径/值、限定词及冲突状态；容量值为500ml，不能改写成包装总量。
- `identifiers`、`research_metadata`无内容时为空对象；protected_identifiers、preservation_ledger、conflicts为空数组。category_context不凭空发明源类目。
- `uncertainties`注明`awaiting_post_audit`；若确有其他问题另列，不能将正常待审写成源错误。
- `source_audit: null`、`skip_reason: short_clear_fields`。
- `review`: mode=`TRANSLATION_AUDIT`，independence_method=null，checked_fields=[]，unreviewed_fields=[`translation_zh.title`]，candidate_findings=[]，结论=`awaiting_post_audit`。
- `run_metadata`: 契约/Skill版本=`1.0.0-foundation`，知识版本来自实际manifest；模型不知为unknown，时间、token等未知为null；只列实际读取的Skills和真实输入hash。

有SOURCE_AUDIT时，field_alignment引用相关decision_id；每个非TRANSLATE决策都保留账本和实际去向。完整动作记录与不可变source引用必须可供后审读取，不只保存精简描述。
