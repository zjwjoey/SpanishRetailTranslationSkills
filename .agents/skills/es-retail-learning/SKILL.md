---
name: es-retail-learning
description: 从已批准的西班牙语零售商品人工纠错记录归因，提出规则变更、影响分析和回归计划。用于明确的学习或规则调优请求；普通翻译、未核验历史中文或AI建议不能作为学习准入依据。
---

# 人工纠错驱动的学习提案

版本：1.0.0-foundation，Foundation Candidate；不是模型微调。当前真实人工批准商品知识为0，不能声称已完成训练。

## 接口与准入

遵循仓库[输入](../../../contracts/ITEM_INPUT_CONTRACT.md)、[交接](../../../contracts/SKILL_HANDOFF.md)、[质量](../../../contracts/QUALITY_AND_SEVERITY.md)、[批准知识政策](../../../knowledge/approved/KNOWLEDGE_POLICY.md)和[数据协议](../../../datasets/DATASET_PROTOCOL.md)。分析来源筛选错误时再读[SOURCE_AUDIT](../../../contracts/SOURCE_AUDIT_CONTRACT.md)；分析译文错误时再读[翻译输出](../../../contracts/TRANSLATION_OUTPUT_CONTRACT.md)。

接收完整源记录与错误输出、已批准人工修正/确定错误记录、父版本和允许访问的数据范围。每次交接保留 `item_id/product_id/platform/source_snapshot/source`（或不可变引用）、`contract_version/knowledge_version`。源和快照不得改写。具体记录和提案字段见[证据与提案接口](references/evidence-and-proposal.md)。

仅对具有真实 `human_id/confirmed_at/evidence_refs/verified_fields`、审批依据且能绑定相同商品/变体/源hash的字段开展学习。`REJECTED`错误记录也须有人类确认的具体错误字段和事实依据；确定错误但没有获批替代译法时，只能提议防错约束，不能编造标准译法。部分字段确认不得扩展至整件商品。AI审查PASSED、多个AI一致、AI读权威资料、历史中文都不能产生人工批准。

## 执行与交接

1. 检查JSON重复key、唯一身份、完整源、两侧快照及人工证据范围。重复属性保留有序key/value数组。身份/hash不能确定则 `status=FAILED`，不跨快照套用修正；证据不足则 `status=REVIEW_REQUIRED, learning_status=EVIDENCE_BLOCKED`，只列缺证和待核验问题，`proposed_changes=[]`，不提炼似是而非的规则。
2. 只读取已准入范围。按错误原子区分源问题、身份对齐、类目、术语、筛选、翻译、表达；源污染不能靠改中文掩盖。记录“错误类型→可证原因/尚不确定原因→拟改规则→影响→回归”。不要把猜测根因写成事实。
3. 核对 `knowledge/approved` 与父commit/规则版本。明确适用平台、类目、语境和排除条件；一个商品组只计一组支持，单例只支持窄范围。与批准规则或人工记录冲突时保留双方证据，标 `REVIEW_REQUIRED`，停止该条晋级。不存在父规则时写新增候选及实际父知识版本，不能虚构版本。
4. 按DATASET协议先核验关系分组，再决定用途。未知组 `group_id=null, dataset_split=unassigned`。规则提炼只接收相应字段已人工确认的train；validation反馈用于定向调优，不冒充新增train证据。不读Holdout答案；收到暴露内容即停止相关调优，记录泄漏并交独立验收者换样，目录/worktree不是保密隔离。
5. 生成窄范围可复核提案：`status=REVIEW_REQUIRED, learning_status=CANDIDATE`；不自签PASSED。唯一知识提案落点为 `knowledge/proposals/`。若当前写权限不包括该目录，在回复或授权临时目录准备交接稿并标明 `intended_path`，由主智能体落盘，不能绕过write_scope。绝不修改approved、正式Skill或发布版本。
6. 交主智能体审查，安排单一变更的专项与跨SkillValidation、独立复审。最多三轮主要优化，保留每轮输入/输出/差异，未跑为NOT_RUN；实际通过才记录检查范围。无人工gold不能计算正式准确率。列出父commit、回退目标及未来以新revert提交回退的方法，本Skill不执行提交或回退。

触发、异常和跨Skill演练见[案例](references/cases.md)。案例是手工载入演练，不等于自动发现、真实人工核验或独立盲测。
