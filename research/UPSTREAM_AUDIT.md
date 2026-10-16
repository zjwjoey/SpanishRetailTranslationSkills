# 三个上游翻译 Skills 实证审查（V3）

审查日期：2026-10-16（Asia/Shanghai）。本轮 task_id=R1。范围仅上游研究；写入 research/ 与 local/research-v3/。此报告取代旧 V2 六技能设计结论，当前正式目标固定为五个 Skills，由根 AGENTS.md 协调。

## 本轮研究结论

P1_RESEARCH_GATE=PASSED_FOR_INDEPENDENT_AUTHORING：三个远端 HEAD 均已实时核对，与先前实际克隆、逐文件阅读、运行检查的固定提交完全相同；本轮重新核对源码关键位置、许可清单和运行边界。可以在明确许可边界内独立创作五 Skills；本结论不等于 Skills 可调用、可信知识训练、对比质量、批量性能或生产发布通过。

| 来源 | 本轮实时 HEAD / 固定 Commit | 已核对文件数 | 与之前实际审查内容 |
|---|---|---:|---|
| [translation-quality-codex](https://github.com/WenhaoLiu0218/translation-quality-codex) | fb3be31df931a0e71fe8955e25a12245dbf29453 | 14 | 14/14 文件 SHA256 一致 |
| [claude-translation-skill](https://github.com/senshinji/claude-translation-skill) | 42d6c8a2a07b77f085d6cafe6d4102d36aeafd02 | 12 | 12/12 一致 |
| [game-localization-skill](https://github.com/tokyboop/game-localization-skill) | bccaac8abde17bcd9e507a9c729e259ae1750251 | 9 | 9/9 一致 |

本轮实时核验时间和全部文件哈希见 [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json)，命令及 stdout/stderr 在 `local/research-v3/LIVE_REPOSITORY_CHECK.json`。使用 git ls-remote 对比 HEAD，再 git rev-parse HEAD / ls-tree / status；三个本地上游工作树均无变更。既有 checkout 为浅克隆，不代表已研究完整历史。原始第三方正文仍留被忽略的 upstream/checkouts/，未复制到 research/。

## 1. translation-quality-codex

[固定提交](https://github.com/WenhaoLiu0218/translation-quality-codex/tree/fb3be31df931a0e71fe8955e25a12245dbf29453)。已读 README、SKILL、agents/openai.yaml、全部 7 references 和 3 Python 实现；本轮文件内容与旧审查一致。

**已有能力**：原生 Codex 入口和元数据；先抽取/源块对齐，再术语、翻译、独立 reviewer、lead 修订；未知内容保留疑点；逐段双向核查遗漏与虚构。术语 schema 有上下文、confidence、来源链接，提取与验证由智能体执行。prepare_translation_job.py 确有文本/Markdown 分块建包，build_readable_output.py 确有阅读版 Markdown 与可选 reportlab PDF，validate_translation_job.py 确有文件/JSON/块 ID/占位符校验。

**不能算实现或质量保障**：没有内置翻译模型调用或独立事实判定器；PDF/DOCX/XLSX 的处理是写 extraction_required 返回 2，实际提取需别的工具。VALID 不检查每块事实语义、数字单位等价、术语适用、独立角色真实执行或审核者资格。用无关英文替换全部译文仍能通过，已在本轮复现。词库为空、review 仍写未执行也不妨碍结构通过。

**缺陷与兼容边界**：SKILL 30–31 行要求 translation_aligned.md 保留 ID、translation.md 清洁版，但 118–120 行推荐角色提示仍用 translation.md 保存 ID，契约不一致。五份 Markdown references 与 MIT Claude 同名文件哈希完全相同；scaling 等含 Claude 模型和 /tmp 遗留，integrity 脚本仍查 Phase/Sonnet 文本，不能验证改写后的 Codex 入口。原生 Codex 格式存在，不等于本轮已验证自动发现和触发。

**许可**：固定提交无 LICENSE/COPYING/NOTICE，README 没有明确授予新增文本/脚本的许可。新增 SKILL/实现不复制，通用方法仅独立表述。论文/PDF 交付、固定四角色逐任务和文档块结构不直接迁入商品批量流程。

## 2. claude-translation-skill

[固定提交](https://github.com/senshinji/claude-translation-skill/tree/42d6c8a2a07b77f085d6cafe6d4102d36aeafd02)。已读 README、SKILL、7 references、CI 与 MIT LICENSE。

**已有能力**：具体多角色提示词、文件所有权、任务依赖、术语合并和翻译修订流程。正向从译文回查源防虚构，反向从源查译文防遗漏；结构 manifest 与 reviewer 对照表有明确要求。术语记录原词/类别/context/译法/confidence/sources/notes，来源不通时保留低置信度，不阻塞全部工作。

**实现形态**：核心是智能体工作指令，非自主翻译程序。Bash 校验脚本真实存在，CI 只跑文本完整性，不提供真实商品语义质量实验。排版给规范/示例，并没有完整独立生成成品脚本。术语“高置信”依据来源数量不能自动变成人工 VERIFIED；按 original 去重对零售多义词不适用。

**平台依赖与缺陷**：TeamCreate/SendMessage、CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS、Sonnet/Opus 和 macOS textutil 路由不原样适用当前 Codex/Windows。结构脚本 set -e 下第一次 ((PASS++)) 会因初值 0 返回非零而早退，两个上游副本均实际复现。integrity 在本机 31 passed / 1 failed，JSON 子进程错误被上游脚本隐藏；先前加 Python3 兼容 shim 仍未解决，但直接 Python 解析两段 glossary JSON 有效，不把失败强归因于无效 JSON 或模型质量。

**许可与基线**：根 LICENSE 是 MIT（senshinji, 2026）。可在遵守通知条件下复用，当前采用独立实现通用工作流。若未来运行 Codex 适配 B，应准确命名并列出角色/路径/模型适配，不能称“原始 Claude 自动流程未改动运行”。

## 3. game-localization-skill

[固定提交](https://github.com/tokyboop/game-localization-skill/tree/bccaac8abde17bcd9e507a9c729e259ae1750251)。已读 README、SKILL、translate.py、placeholder_patterns、TEST_GUIDE、2 docs 和 MIT LICENSE。

**已实现**：命令行参数、输入路径存在检查、扩展名 CSV/XLS/XLSX 分支与明确退出。占位符参考是模式说明，单次执行为指令设计。

**未实现**：translate.py 58 行 TODO；load_glossary、extract_glossary、load_csv/load_xlsx、translate_with_llm、run_qa_checks、save_file、save_qa_report 都是注释。119 行直接 exit 0。README 明示 WIP，但 SKILL/指南表述像完整功能。运行模板显示完成，实际不生成译文与 QA 文件，本轮再次复现。

**缺失文件**：SKILL 引用的 glossary_extraction.md、qa_rules.md、advanced_usage.md、troubleshooting.md，extract_glossary.py、config.py、batch_translate.py、config.yaml 均不在树中。TEST_GUIDE/会话总结声称的两个 20 行 CSV 也不在该版本，指南样例计数不是已运行结果。

**适用边界**：品牌/型号/技术代码保护可借鉴占位符不随意改写的通用思想；不套用游戏词表、Unity 富文本场景或西中长度比 50%-150%。历史译文提词不能跳过可信核验。MIT 不会让未实现脚本自动成为可运行基线。

## 4. 本轮真实控制实验

运行：`python local/research-v3/recheck.py`，仅上游审查用临时命令，非正式 Skills 依赖。3 个实时远端核验，35 个内容文件哈希重核；9 个工程控制命令均有真实 stdout/stderr，见 `local/research-v3/CONTROL_RESULTS.json`。输入是新造合成字符串，不是用户历史商品、训练样本或标准答案。

| 控制序号 | 操作 | 实际结果 | 判定范围 |
|---:|---|---|---|
| 1 | Codex prepare，2 块 | exit 0，建包 | 工程建包实现 |
| 2 | 未翻译模板 validate | exit 1，指出 pending 和未生成阅读版 | 预期拒绝有效 |
| 3 | 全部填无关英文后 build | exit 0，Markdown存在 | 交付构建实现 |
| 4 | 无关英文 validate | exit 0，VALID 2 blocks | 语义缺陷复现；不能当质量通过 |
| 5 | game 存在的合成 CSV | exit 0；译文存在=false，QA存在=false | 假成功缺陷复现 |
| 6 | Claude integrity | exit 1，31 pass / 1 fail | 未通过兼容检查 |
| 7 | Claude structure，同行列表 | exit 1，首项 PASS 后提前停止 | 早退缺陷复现 |
| 8 | Codex integrity | exit 1，缺 Claude 阶段和模型文本，提前结束 | 未适配 Codex 内容 |
| 9 | Codex structure，同行列表 | exit 1，同样首项后停止 | 同源脚本缺陷复现 |

这不是“4 成功/5 失败”的统一质量测量：其中有预期拒绝和缺陷探针，必须分别解释。真实商品翻译质量、术语准确率、A/B/C 同条件比较、Token/耗时与批量吞吐量均 NOT_RUN，分母为 0 时记 N/A。

## 5. 进入五 Skills 开发的边界

- 五个专业入口为 category、terminology、reviewer、translator、learning；协调在 AGENTS.md，不新增正式协调 Skill。
- Reviewer 的 SOURCE_AUDIT 与 TRANSLATION_AUDIT 是本项目按 V3 独立设计；不能声称上游已实现完整商品噪声筛选/事实保留证明。
- 保护源、已批准术语优先于去重，完整源与审查日志必须保留；批次按风险加载能力，避免每 SKU 固定多角色。
- 当前可合法同条件原样运行的上游 B 未得到证实，状态 NOT_COMPARABLE；未来 MIT 适配需单独运行验证。上游研究通过不解除真实样本、人工确认、自动调用与隔离门槛。
