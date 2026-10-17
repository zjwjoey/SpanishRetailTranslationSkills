# 预登记：新商品同条件对照协议

## 样本
从三个平台当前真实西语货盘中固定各10个**未曝光的新 SKU**。必须先合并全量本机历史 exposure ledger：Action/Amazon 早期审查、Amazon 200 / 回归200+100 / 第三轮1000、IKEA 两批各1000、已知回归失败以及所有局部验证。排除相同商品 ID、Parent/child、变体/系列、跨快照与跨平台近重复组。证据不全只能标 NOVELTY_UNVERIFIED，不可声称新样本 Holdout。选样前确认重要内容确属 es-ES，不凭文件名或西语短标题推断。

每条保留 item_id、platform、product_id、group_id、source_snapshot.sha256、原完整 source、source_locations；以源文件和曝光 ledger 的 SHA256 冻结。A/B 不接收历史中文、旧纠错、QA 答案。见到译文后不得更换题目。

## 隔离
两个全新 Codex 上下文、**两个都在本仓库祖先目录之外的临时工作区**。A 不能读仓库 AGENTS 或 skills；B 只读冻结的五个 SKILL.md、refs、必需 contracts 与 approved manifest，不能读历史评测报告、A 输出。双方完全相同模型选择、任务、输出字段、商品顺序、批次、自查次数、沙箱及联网条件；仅 B 额外可加载当前 Skills。保存实际命令、模型/CLI版本、可观测配置、技能载入证据。无法确认同等模型或环境记 NOT_COMPARABLE。

尝试 Codex 前先执行本机 codex exec --help。使用 --ephemeral --sandbox read-only --skip-git-repo-check 以及外部 workspace -C，按本机支持情况选择共同模型。每批约5商品；两边相同。全部首次输出与返工原件另存，不择优重算。

## 共同输出与独立审查
统一 JSONL：身份与 source_sha256、中文标题、规格、描述、平台类目对应中文/建议研究类目分别记录、品牌/型号/兼容对象、待核槽以及未译/排除理由。不得用模版前缀 + 原西语回显假装中文译文。未知值局部保留 null，不抹去邻近确定事实。

独立 QA 先看完整原文，冻结事实清单，再读双臂候选，按同一事实原子核查主体/规格/单位/数量角色/兼容全清单/材质部件/否定和限制条件、术语、遗漏和凭空添加。评级：P0 身份/关键事实错误或重大幻觉；P1 重要遗漏/错译/术语错误；P2 展示与流程问题。同根因在多字段只计一次最高级。AI 意见、源异常、人工确认分开，P0/P1 影响商品数的分母固定 10/10/10，漏审不能算通过。

成本：只比较实际有日志的 token/时间/费用，不能用文本字符数当 token。任何未经核验的 AI 审查不能当正式人工 gold 或生产准确率。已知 P0 和关键 P1 就阻止扩大规模、记录失败和建议，不在本轮现场修改五个 Skills、采集器、数据库或 approved 知识。

## 实际交付
Git 忽略的 local/ 中保留：exposures、frozen inputs/hash/规则快照、A/B 原始输出和 JSONL、CLI usage/log、独立源事实台账、审查疑点与撤回记录、逐平台/总体汇总。提交到本分支的仅是无敏感数据的协议、脚本、合成测试和匿名化总结。