# V3工程变更与回退证据

真实商品质量主要优化轮次0/3：人工gold为0，不能声称完成Validation驱动质量训练。以下是工程修复，未冒充准确率提升。

|变更|失败证据|修复与回归|回退|
|---|---|---|---|
|五Skill V3初始实现|旧V2有第六Skill、无前审、新旧状态混用|旧成果保存在local/v2-*；新固定五Skill、Reviewer双模式、新统一契约；初始实现commit f692f71|保留旧本地快照；不得重新发布六Skill|
|Category知识版本一致性|独立专项首轮输出none-approved，与manifest/其他Skill不同|仅改Category入口，使用实际manifest版本+独立空知识状态；同输入追加回归6项通过，首轮输出与hash未覆盖|如需撤回用新revert提交；旧文件可从f692f71读取|
|保留引用结构契约明确|首轮集成Schema拒绝实际结构化source引用；第二次拒绝canonical_decision_id对象|契约明确字符串/原文对象/canonical指针三种引用；Schema和机械检查增加原文可定位及canonical存在约束；实际43决定、29账本通过，新增2个正/负控制，离线16项通过|旧Schema在da64299/f692f71；用新revert提交，不改旧评测|

Reviewer独立后审对原C候选未发现译文问题，但源冲突/截断仍REVIEW_REQUIRED；对主智能体刻意删事实的另一个合成候选发现P0×1/P1×3，原候选与扰动候选都保留。故障注入不是专业Skills真实商品发生了4个已确认错误，也不是人工gold。
