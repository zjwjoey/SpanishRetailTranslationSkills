# 第一阶段实际验收：Foundation Candidate

2026-10-16；任务版本V3。工作目录F:/ai文件/SpanishRetailTranslationSkills，分支feature/foundation-v1，origin=https://github.com/zjwjoey/SpanishRetailTranslationSkills.git。基础工程与手工载入演练已执行；V1正式训练/质量/发现Gate尚未通过，不能宣布生产可用或完成5500SKU。

## 已交付

恰好五个原生Skill入口及专项references；Reviewer双模式；五份统一契约及3份JSON Schema；人工批准知识空清单、数据协议、独立上游报告、只读数据审计、可复跑工程检查、真实合成运行记录及独立后审。旧V2成果含第六Skill已移存Git忽略的local，不在正式五入口中；根AGENTS承担协调。README仅更新实际状态提示，AGENTS和V3保留用户原文。

|Skill|实际开发及调用证据|未通过项|
|---|---|---|
|es-retail-category|来源路径/研究分类分离、结构语境交接；独立显式手工载入和版本修复回归|客户端自动发现、人工分类gold|
|es-retail-terminology|语境消歧、品牌/系列/型号/编码保护；未知词实际保持待核|客户端自动发现、批准专业词库|
|es-retail-reviewer|SOURCE_AUDIT与TRANSLATION_AUDIT均实际执行；完整源/动作/中文独立核对|客户端自动发现、真实商品人工验收|
|es-retail-translator|普通短字段和OneBlade长字段实际候选，局部冲突隔离且不自批|客户端自动发现、真实商品质量|
|es-retail-learning|无人工证据实际拒绝学习晋级、proposed_changes为空|真实人工纠错训练/Validation/Holdout|

## 实际测试及边界

|测试层|结果|证据|
|---|---|---|
|官方Skill静态校验|5/5通过|evaluations/results/official-skill-validation.json|
|离线工程正/负控制|16/16通过，0失败|python -X utf8 evaluations/check_foundation.py；results/foundation-tests.txt|
|独立显式手工载入|五Skill各1次，另Category同输入回归1次；共5个合成商品、6输出|results/specialist-runs.json及reports/evaluations/INDEPENDENT_SPECIALIST_TESTS.md|
|description路由演练|10请求实际选择：5选择、5排除；非客户端触发准确率|同上，保存请求和实际选择|
|独立记录机械核对|25一致性、19源span、43入口链接、8源定位及6项修复回归检查无失败|同上，不能相加当商品数|
|OneBlade四阶段|1手工合成商品；43源动作、29非TRANSLATE均有账本、11保护位置；输入源与身份未变|results/oneblade-*.json；oneblade-mechanical-checks.json|
|独立后审|2份同商品候选各19原子；原C无本次译文发现但源冲突/截断仍待核；刻意缺事实候选检出P0×1/P1×3|reports/evaluations/INDEPENDENT_POST_AUDIT.md；不是2个独立商品或真实错误率|
|产物/数据Schema|3份生成/后审输出Schema通过；72私有候选输入Schema通过且72有两侧来源|results/integration-validation.json；Schema通过不等于事实正确|
|CLI真实探测|失败，自动发现/显式/自然触发NOT_VERIFIED|CLI0.137.0-alpha.4；本轮ignore-user-config探测exit1，默认gpt-5.5返回400不支持；前轮配置默认gpt-6.1-sol亦不支持；用户全局配置未改|

CLI只使用合成/无商品探测；本轮具体提示是17+25且要求不用Skill。失败在模型启动阶段，不是五Skill误触发，不能把它计作五项Skill失败或排除测试通过。完整日志留local，公开只保留脱敏错误摘要。

## 来源、训练与对照

三个实时上游HEAD已核对，35文件哈希一致；Claude/game有MIT，Codex新增部分许可未明，独立创作不复制。game核心未实现，Claude运行机制不原样兼容，B=NOT_COMPARABLE。详见research/四报告。
96原始文件本轮再算hash，96未变；Action32、Amazon40候选，人工确认0；正式train/validation/holdout为0/0/0。数据可读，受阻的是人工gold与真实权限隔离，不是数据访问。完整审计口径见SOURCE_DATA_STATUS.md。
A与C已对同一synthetic在不同上下文实际执行，B未执行；模型标识unknown、token/费用不可得，计时窗口不同，不能比较成本或声称质量优于普通/上游。BASELINE_COMPARISON.md保存条件与限制。

## 修复、风险和停止门槛

真实工程问题Category版本歧义已单文件修复并追加独立回归；Schema两次拒绝合法引用形式后明确接口且扩展负控制，实际产物通过，旧证据未覆盖。详见SKILL_CHANGELOG.md。主要真实质量优化轮次0/3。
尚无人工标准答案和独立Holdout权限；同模型不同上下文不是多模型复核。源包装数冲突和兼容句截断不能猜测解决。合成产物嵌套较大，未测真实批量吞吐；不扩大到5500SKU。

## Git与恢复

已实际提交阶段：d652c6d（V3基础契约）、da64299（研究/Schema/数据门槛）、f692f71（五Skill）、b161375（接口修复）。后续评测/交接提交以git log为准；没有重写历史、合并main或创建正式Release。Git作者仅本仓库设置为已登录GitHub账号zjwjoey的noreply身份，未修改全局Git身份。
V3明确授权该origin的非强制开发分支推送；仅推feature/foundation-v1，实际远端提交以最终交接和git ls-remote核对，不由报告预言。完整原始货盘、私有候选、人工队列、第三方clone和原始CLI服务日志均不提交。
下一步和实际检查命令见NEXT_PHASE_HANDOFF.md。正式V1仍BLOCKED；本轮交付Foundation Candidate，不发布正式Release。
