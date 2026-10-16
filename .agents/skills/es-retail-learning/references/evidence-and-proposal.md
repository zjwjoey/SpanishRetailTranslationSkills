# 证据与提案接口

## 人工记录

输入ITEM记录之外，接收 `correction_records[]`。每条保留：

- `correction_id/item_id/source_snapshot_sha256/source_field/source_span`：源片段精确quote、occurrence（从1开始），可用Unicode码点半开start/end；定位须与完整源一致。
- `original_output_ref/original_text/confirmed_error/corrected_text`：原输出不可变引用和原值；无获批替代值时corrected_text=null。
- `human_id/confirmed_at/evidence_refs/verified_fields/approval_ref`：真实人工身份、确认时间、可访问依据、精确字段路径、人工批准记录；说明确认了错误、修正还是两者。
- `verification_status`：沿用RAW/CANDIDATE/VERIFIED/REJECTED/SOURCE_ISSUE/ALIGNMENT_UNCERTAIN/REVIEW_REQUIRED；状态标签本身不能替代证据。REJECTED不意味着修订已VERIFIED。

核验字段需覆盖源事实路径和目标修正路径，例如 `source.specifications[0].value` 与 `translation_zh.specifications[0].value`。确认title不能支持description。人工记录和源版本不一致、证据引用不可取回、确认文本不含所需字段均列出缺口。synthetic记录即使形式完整也不能作为真实人类确认。

## 学习输出

公共信封保留 `item_id/platform/product_id/source_snapshot/source_ref/contract_version/knowledge_version`。`status`只有REVIEW_REQUIRED/FAILED；`learning_status`为CANDIDATE或EVIDENCE_BLOCKED。两者与输入verification_status分开，Learning不更改样本状态。

输出 `eligibility`（eligible_fields、blocked_fields、missing_evidence、is_synthetic）、`proposed_changes[]`、`conflicts[]`、`unresolved_questions[]` 与运行元数据。运行元数据含实际模型/未知unknown、实际读取Skill、输入hash、调用方式、时间和可得token（不可得null）。synthetic演练的eligible_fields仅指演练内条件成立，production_eligible=false。

每项拟改包含：

- `change_id/rule_id/parent_commit/parent_knowledge_version/intended_path`，落点knowledge/proposals；parent未知则缺证，不写READY或批准结论。
- `error_type/severity/cause/cause_evidence`，区分已证实原因与假设。
- `before_rule/proposed_rule/affected_skill`，没有原规则则before_rule=null。
- `platform/category_context/applicable_context/excluded_context/impact/risks`。
- `evidence_refs/correction_ids/verified_fields/item_ids/source_hashes/group_ids/supporting_group_count`，不把快照/变体复制数算独立商品证据。
- `regression_plan`：train来源、validation版本及权限依据，正常/反例/边界、预期不变量、专项和跨Skill路径、比较父版本、判失败及回退条件、实际结果或NOT_RUN。Holdout仅独立冻结后验收，不附答案。
- `conflicts/rollback`：冲突规则及双方定位；回退目标与新revert提交方案；`approval=null`，主智能体和独立审查待办。

没有准入证据时输出缺证清单和proposed_changes=[]，不能用“候选”二字绕过学习准入。真有人类确认但尚未完成分组/分集时可以整理已确认错误，不进行train规则提炼，并列出分组阻塞。
