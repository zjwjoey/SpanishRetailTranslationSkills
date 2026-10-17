# Codex 执行单：V2 原生 Skills 三臂真实对照

任务前提：用户已要求停止单纯扩大翻译训练，纠正前次对照的专业提示词混入及 Skills 全文注入偏差。先读本目录 README.md、PROTOCOL.md、PROMPTS.md。先 git status、检查当前分支及旧数据，不覆盖用户未提交变更；若当前分支不是 eval/three-arm-native-v2-20261017，优先用独立 worktree。

**仅此评测任务**：不改正式五 Skills、其 refs/共享契约、approved、Action/Amazon/IKEA 采集器与数据库。完整原文、译文、日志放 Git ignored local/three-arm-native-v2/；不 push 私有数据、不合并、不自行发布。

步骤：
1. 审计本机安装的 Codex CLI / model / sandbox 与技能发现机制。先用 synthetic 测 C 组 **原生发现并实际读取** SKILL.md/相关 reference；保留命令与宿主日志。若 native read 不可证，则 C=NOT_RUN，立即停止三臂比较，不用全文注入应付。
2. 证实 A/B 两个外部工作区（不位于原仓库及祖先目录）没有可见专业 Skills 或根 AGENTS 专家指令；配置相同的隔离与模型。若无法保证，报告 NOT_COMPARABLE。
3. 盘点此前已曝光案例（包括前次30 SKU、Action/Amazon/IKEA 所有训练测试及失败样本/近重复组）；使用只读商品货盘挑选新 24 SKU（每平台8，普通4复杂4），按实际源文难度分层。冻结源 hash、SKU/Parent/系列/exposure hash、同一 OUTPUT_SCHEMA、prompt/skill/rules hash；禁止事后换样。
4. 运行 A/B/C，三组 COMMON_TASK 相同。仅 B 附加 EXPERT_APPENDIX；仅 C 启用原生发现并按需读取冻结五 Skills。每个 SKU 在各组均同一次首次生成与相同一次自查机会；保留失败、重试和未成功输出，按平台/难度配对。绝不将完整 Skills 内容粘贴进用户提示词。
5. 全新独立 QA 先完整读24个商品原文并冻结具体事实清单，再阅读随机盲化的三组原始译文。逐项核查原文证据、完整兼容/数量/部件/材料/型号/限制、真正遗漏与虚构；审查误报和撤回保留。人工返工时间 **只能记录真人实际审校计时**；未实际人工验证则 N/A。
6. 输出汇总：三组各 24 计划与有效结果、Action/Amazon/IKEA 各8、普通/复杂各12；语义 P0/P1/P2 影响商品、可核事实保留、审查分歧、首次成功率、native 文件读取证据、真实 input/cached/output tokens、墙钟耗时、真实费用（否则N/A）。单列 A→B、B→C，勿将 AI 一致称准确率。不足证据则明确 BLOCKED/NOT_RUN，不能臆造。
7. 仅把匿名汇总、方法与可以共享的工程脚本提交评测分支；真实样本仍在 ignored local/。不改五 Skills、不升 approved、不合并 main、不推送，除非用户另外明确要求。

重要：本执行单建立之后的真实执行仍须 Codex 真正运行，评测协议文件本身不代表已运行。