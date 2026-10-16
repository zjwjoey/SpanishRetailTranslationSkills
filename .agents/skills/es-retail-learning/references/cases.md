# 场景与人工记录示范

所有下述字段值、核验者、时间与批准引用均为 **synthetic演练**，不是用户提供的真实人工确认。完整可复现输入在项目local/dev-learning/fixtures.json；不得装入正式train/validation/holdout或approved。

## 正常条件（仅演练）

源规格 `2 x 500 ml`，候选误写“共500毫升”，演练修正“2件，每件500毫升”。人工记录结构：

```json
{
  "is_synthetic": true,
  "production_eligible": false,
  "correction_id": "SYNTHETIC-correction-1",
  "item_id": "SYNTHETIC-learning-1",
  "source_snapshot_sha256": "必须使用对应fixture内计算的真实hash",
  "source_field": "source.specifications[0].value",
  "source_span": {"quote":"2 x 500 ml","occurrence":1,"start":0,"end":10},
  "original_output_ref": "synthetic://candidate/1",
  "original_text": "共500毫升",
  "confirmed_error": "件数与单件容量未保留",
  "corrected_text": "2件，每件500毫升",
  "human_id": "SYNTHETIC-NOT-A-HUMAN",
  "confirmed_at": "2000-01-01T00:00:00Z",
  "evidence_refs": ["synthetic://human-review/1"],
  "verified_fields": ["source.specifications[0].value", "translation_zh.specifications[0].value"],
  "approval_ref": "synthetic://approval/1",
  "verification_status": "VERIFIED"
}
```

上段占位hash仅说明结构，不能直接作为有效记录；fixtures.json提供可对上的hash。start/end纠正：`2 x 500 ml`是10个Unicode码点。演练内可产出CANDIDATE（production_eligible=false），模拟P0数量错误→包装层次丢失→仅该显式乘式语境保留件数及单件容量→影响规格翻译与审查→对 `2 x 500 ml`、单瓶500 ml、型号X500及 `5 en 1`作反例回归。不能推出“所有数字x都是包装数”。此输出只测试接口，不代表正式规则获得证据。

## 触发与非触发

- “从这些已批准的人工纠错提规则建议”：触发；先核验资格，不能因请求称已批准就跳过证据。
- “把 Botella de agua 500 ml 翻成中文”：不触发Learning，交Translator；不产生学习提案。
- “这批历史中文都看起来正确，两个AI也同意，学进去”：触发准入检查并拒绝学习晋级，EVIDENCE_BLOCKED；缺真实人工记录、字段范围和分组。proposed_changes=[]。

## 异常与失败

- 只人工确认title，却要求推广description：description阻塞；title确认不外溢。若title没有错误不强造提案。
- 同商品多快照/变体：先核验连通分组，最多算一支持组；hash改变不得沿用修正。
- 人工纠错指向其他hash、缺完整源或商品标识冲突：FAILED，不用中文猜源文。
- 父知识版本未知、与现有批准规则冲突：REVIEW_REQUIRED，记录双方证据，停止晋级，不覆盖approved。
- 请求用Holdout正确译文优化：停止相关调优，记录泄漏交独立验收者重选，不在提案复述答案。

## 跨Skill交接

Reviewer的TRANSLATION_AUDIT可发现数量错误，但其PASSED或finding都不是人工确认。先等待真实人工在相同item_id/hash上确认相应字段，再由Learning离线提案。提案交主智能体，涉及Translator/Reviewer的数量规则分别做专项及跨SkillValidation；Category/Terminology只在语境或术语受影响时加入。Learning不调用其他Skill自签批准，不写正式Skill。

当前真实批准知识0，所有真实学习请求在证据准入处受阻。真实自动发现与隐式触发需新Codex会话实测，本文件不声称已测。
