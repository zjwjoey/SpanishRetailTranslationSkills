# 独立专项测试与description路由演练

日期：2026-10-16。执行者为未参与五Skill开发的独立子智能体；同模型不同上下文不等于多模型复核。实际模型标识不可得，记unknown。

## 范围与方法

只读README、AGENTS、contracts、approved及五Skill与必要接口引用（Learning必需DATASET_PROTOCOL）。未读其他评测产物、预期标签、开发者自查、references/cases.md或Holdout。完整逐文件hash及本次输入、输出、请求见 `evaluations/results/specialist-runs.json`。本报告与该JSON是仅有写入。

这是手工载入SKILL.md后实际生成输出，以及根据五description进行的手工路由选择。五入口在同一上下文中载入，不是客户端自动发现/触发实验；不声明原生发现Gate通过。读取的translator/output-example仅用于输出形状；本次商品Tijeras不同于该示例。本次没有收费服务、外部上传或知识升级。

## 五次显式运行的实际结果

|Skill|新造合成输入|实际产物及判断|状态|
|---|---|---|---|
|Category|Espátula de cocina；Hogar→Cocina|平台家居→厨房单列；研究厨房工具/锅铲另列；无材质扩写|PASSED，仅语境交接|
|Terminology|仅标题Gato|zh_candidate=null，保留猫/千斤顶备选，要求类目/用途|REVIEW_REQUIRED|
|Reviewer|Jabón, 2 x 500 ml；Para manos.重复；Ver más；评分|6条动作，第二次出现去重至d2；4条非TRANSLATE账本；评分实际值保留；网页提示与缺后文待核并记|REVIEW_REQUIRED|
|Translator|Tijeras, 21 cm|实际中文“剪刀，21厘米”；2个事实引用；短字段跳过前审有原因，独立后审待执行|TRANSLATION_CANDIDATE / REVIEW_REQUIRED|
|Learning|Taza, 300 ml；AI建议将错误300升改300毫升，无人工确认|eligible_fields=[]、proposed_changes=[]；明确人工证据缺口，production_eligible=false|EVIDENCE_BLOCKED / REVIEW_REQUIRED|

全部产品为is_synthetic=true及显式非生产sentinel；每个源hash由序列化source的UTF-8规范JSON实际SHA256计算。captured_at=null，无伪造采集日期。输入含原文及synthetic定位；5个输出均保留身份、完整source及source_snapshot。Reviewer依赖使用另行手工构造且绑定该商品hash的类目/术语候选，不复用其他专项商品结果，不冒称生产批准知识。

首轮专项运行共5次：普通2、异常3；收到主智能体版本修复后追加Category同输入回归1次，合计实际输出6条，独立合成商品仍为5。Reviewer本轮仅实际执行SOURCE_AUDIT，TRANSLATION_AUDIT为静态读取，未另造后审通过记录。

## 十条路由选择

完整原请求与实际选择保存于JSON的description_routing.requests。以下为本执行者按description的选择，非有独立标签的准确率。

|自然请求要点|实际选择|
|---|---|
|Action西语原平台分类及另列研究类目|Category|
|Amazon清洁用途cepillo消歧并保护型号|Terminology|
|Amazon西语长文重复标题/评分逐段去向，不初译|Reviewer|
|Action西班牙语名称/规格译简体中文|Translator|
|人工确认纠错归因并提出规则/回归|Learning；仍须核实证据|
|中文商品标题译西班牙语|不选五Skill，反向语言|
|纯中文商品文案润色|不选五Skill|
|德语新闻译中文|不选五Skill|
|中文摄影展开幕致辞|不选五Skill|
|西班牙语旅游日记译英文|不选五Skill|

实际10条，选择5、拒绝5。没有将“只有中文的润色请求”误充西中审查；自然请求可以用中文表述，是否触发由任务方向而非请求文字语言决定。

## 静态契约与依赖审查

五Skill的运行状态/核验状态区分一致；Translator不自行PASSED；SOURCE_AUDIT不能初译，TRANSLATION_AUDIT需完整源与账本；Learning无人工证据不可提规则；分类/术语同源依赖、旧hash失效、局部冲突隔离均与contracts一致。批准知识为空，未有事实依据支持学习或生产级质量。

发现一处接口歧义：Category入口要求无批准知识时knowledge_version=none-approved，而Terminology输出接口要求使用实际manifest版本，Translator亦取实际manifest；当前为1.0.0-foundation。跨Skill日志因此可对同一个知识快照使用不同version字符串。已通知主智能体，由主智能体修改Category单一入口：knowledge_version始终取manifest版本，空知识另以knowledge_status=EVIDENCE_BLOCKED表达。本执行者重读更新后的入口，对原Espátula输入实际追加1次针对性交接回归：版本与manifest/Terminology相同、空知识状态独立、身份/源/类别判断不变共6项检查为真，失败0。初次none-approved输出及before/after入口hash仍保留在JSON；没有用新结果覆盖旧证据。此修复只解决静态交接一致性，不证明翻译质量提升。未由本执行者修改Skill/合同。

曾初步误报../../../contracts链接不存在；主智能体要求后，本执行者实际以SKILL.md所在目录解析，目标根contracts存在，撤回原判断。全部入口相对链接实际核对43个，缺失0个；没有按错误初判降级执行。

## 实际检查计数与可评判范围

- 五条身份/原文/hash/不标VERIFIED/输入hash检查共25个布尔为真，失败0个；只证明记录一致性。
- synthetic源定位实际解析8处，失败0；Reviewer去重canonical实际对应decisions[1].decision_id=d2。
- 源span精确子串及occurrence实际核对19次，失败0次。重复记录的span属于不同输出证据位置，不当独立商品计数。
- 首轮每Skill输入/输出各1条，另Category针对性回归输出1条；总合成商品5，Action4、Amazon1；无真实货盘、无真实人工确认、无Holdout。
- 人工gold=0：语义准确率、P0/P1真实错误率、人工自然度/修改率、真实成本比较均N/A，不能报告零错误或提升。token/耗时/费用不可取得为null。
- 普通/上游基线本子任务未运行，比较NOT_COMPARABLE；客户端发现/自动触发NOT_TESTED；本报告不签发质量通过或发布通过。

## 交接

实际只写入 `evaluations/results/specialist-runs.json` 和 `reports/evaluations/INDEPENDENT_SPECIALIST_TESTS.md`。未修改Skills、合同、approved、生产源或其他评测结果。后续需真实客户端发现证据与人工gold质量评测；它们不由本手工演练替代。
