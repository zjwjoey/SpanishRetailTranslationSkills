# V1 数据就绪增量审计

2026-10-18执行补充：六条TRAIN开发源已完成四路线共24份生成与独立AI审读，下文“没有生成译文”是选样时状态。此前记录的排除清单hash/容量为当时版本；审计维护发生过覆盖及逻辑调整，不能视作最终固定版本。第二次试验已单独固定最终清单字节并通过hash复核，详见[开发报告](DEVELOPMENT_RESULTS_20261018.md)。

## AMAZON_ONLY_SCOPE（当前优先范围）

本轮范围已切换为仅使用 Amazon.es。下面的三平台审计是先前已完成的历史盘点，保留作证据，不参与当前 Amazon-only 样本配额。Amazon 目标池建议为 120 个 parent/近标题组：TRAIN 60、VALIDATION 36、FINAL 24；不公布或冻结最终 24 条身份。

Amazon 专项脚本 [`amazon_scope_audit.py`](../../../local/skill-competition/data-audit/amazon_scope_audit.py) 已应用恢复的保守 exposure 黑名单、父 ASIN 家族、预留候选、fresh reserve、精确标题和近标题规则。黑名单路径为 `local/skill-competition/exposure-recovery/blacklist.json`，SHA256 `58c8001d9b9a44812f94fe4ad68f2806231da3cd2b2250149d4e55283f59e086`；本次消费 `classification_policy.all_blacklist_tokens` 共 2,949 个 token。其分类包含历史输入、候选/来源池和保守关系闭包，不代表 2,949 个都已翻译或人工确认。按该集合排除后，来源表中 1,589 行 ASIN 或 Parent ASIN 命中；应用家族和标题合并后剩余 3,307 个候选组（普通 950、复杂 2,357，29 类目、26 类目至少 2 组）。这足以覆盖 120 的工程候选容量估算，但仍不能证明跨源同款关系已解决，也不冻结任何 split。

标题规则为 NFKD 去重音、转小写、仅保留 ASCII 字母数字；同 parent 家族归一组，同一规范化标题合并。近标题采用同一来源类目和首个非停用标题词分桶、标题长度差不超过 20%、`SequenceMatcher >= 0.90`。此规则可复现但不是完备的商品实体解析，因此仍需完整曝光关系表和人工抽查。变体始终按 parent 家族闭合；不得把同一 parent 下另一颜色/规格拆成新样本。

Amazon 当前探针文件 [`amazon-dev-probe.json`](../../../local/skill-competition/data-audit/amazon-dev-probe.json) 有 6 条 TRAIN 开发探针（普通 3、复杂 3），其中 2 条沿用此前 Amazon-only steering 前已公开的源探针；它们现在永久计为本轮 TRAIN 开发曝光，不能进入后续验证或 FINAL。新增的 4 条及沿用的 2 条均已按完整 2,949-token 黑名单检查 ASIN/Parent ASIN，并与命中黑名单的当前西语来源行执行精确/近标题比较：六条均为零命中。可复现逐条记录见 [`amazon-dev-probe-exposure-check.json`](../../../local/skill-competition/data-audit/amazon-dev-probe-exposure-check.json)。这只允许把六条作为 TRAIN 开发源冻结，不证明跨源同款新颖性；均标记 `NOVELTY_UNVERIFIED`，不能进入 VALIDATION 或 FINAL。所有 6 条都只有源先行记录，没有生成译文、配对输出或人工 gold。对应语义台账见 [`amazon-dev-source-facts.json`](../../../local/skill-competition/data-audit/amazon-dev-source-facts.json)。旧三平台探针及事实台账归档说明在 [`legacy-pre-user-source-steer.json`](../../../local/skill-competition/data-audit/legacy-pre-user-source-steer.json)。

Amazon-only 120 条后续方案暂定按 parent 家族先分组，再按复杂度配额和类目轮转：训练 60、验证 36、最终 24；将已公开的 6 条探针计入 TRAIN，其余训练位 54。当前可用候选容量计数为普通 950、复杂 2,357（总计 3,307），这里只报告数量和分配方案，不选择或输出任何 VALIDATION/FINAL 身份。此为配额方案，不是冻结样本清单；跨源同款关系仍为 `NOVELTY_UNVERIFIED`。

审计脚本：[`incremental_audit.py`](../../../local/skill-competition/data-audit/incremental_audit.py)；机器结果：[`audit-result.json`](../../../local/skill-competition/data-audit/audit-result.json)。脚本复用已保存的 inventory、exposure 与候选清单，只读三份源工作簿并定位来源行；没有读取任何翻译、生成日志、答案或裁定。开发探针与源事实记录分别见 [`dev-probe.json`](../../../local/skill-competition/data-audit/dev-probe.json) 和 [`dev-source-facts.json`](../../../local/skill-competition/data-audit/dev-source-facts.json)。

## 先前三平台盘点（历史记录）

本节留存用户切换到 Amazon-only 之前完成的三平台增量审计，供追溯历史曝光范围；当前样本池只按上面的 AMAZON_ONLY_SCOPE 处理。

### 可用分组数

以下为排除已记录的曝光、65 条库存候选、10 月 17 日运行计划中的 30 条商品，以及 Amazon fresh reserve 后，按平台本地关系组去重的源行候选数。数字说明工程容量，不构成所有跨平台同款都已查清的证明。

| 平台 | 可用商品组 | 普通 | 复杂 | 类目数 | 至少有 2 组的类目数 | 40 组目标 |
|---|---:|---:|---:|---:|---:|---|
| Action | 4,764 | 1,860 | 2,904 | 15 | 15 | 容量满足 |
| Amazon.es | 3,386 | 974 | 2,412 | 29 | 27 | 暂定满足，见关系证据缺口 |
| IKEA | 1,136 | 312 | 824 | 125 | 104 | 容量满足 |

复杂度规则是源级工程分层，不是质量标签。Action 按字段长度、数字和字段数；IKEA 同样按源字段；Amazon 核心标题/变体/规格、数字密度和卖点长度单独判定，避免平台重复属性与抓取元数据把所有商品误标成复杂。Amazon 的 974/2,412 分层因此不同于先前将全字段拼接后得到的“全部复杂”结果。

源快照与清单哈希已写入 `audit-result.json`。本轮复用的源快照为 Action 2026-10-12、Amazon 2026-10-05、IKEA 2026-10-16；工作簿路径和文件 SHA256 记录在机器结果中。

## 曝光排除和关系边界

- **Action：**采用 `exposures-v2.jsonl` 的 80 个曝光 ID（旧清单为 79）；另排除 20 条库存候选。10 月 17 日的 10 条 Action 商品均可映射到候选清单，和这 20 条候选重叠。按规范化标题关系组排除近似标题组。该清单有 79 个关系组，跨平台同款仍为 `NOVELTY_UNVERIFIED`。
- **IKEA：**复用结构化清单的 2,020 个曝光货号、1,331 个系列组，另排除 30 条候选。10 月 17 日的 10 条 IKEA 商品都能映射到候选清单。对已曝光或已预留的系列整组排除；不会把系列内另一货号自动视作新商品。
- **Amazon：**复用 1,564 行 exposure ledger，按父 ASIN 家族排除；另排除 15 条候选、已解析的 10 条 10 月 17 日商品及 Amazon 的 source-only fresh reserve。fresh reserve 两份 20 条清单和第二轮 12 条 Amazon 记录合计 52 条记录、35 个不同 ASIN，脚本排除这些 ASIN 及其父家族。不得把被拒绝的 root fresh selection 当作有效盲测样本。

Amazon inventory 另记有 2,899 个历史 ASIN、2,905 个关系 ASIN 和 69,122 个证据文件，但该 inventory 只保存汇总数字与来源路径，没有提供完整、可逐项应用的关系黑名单；exposure ledger 中也只有 1,564 行。因此 3,386 是现存 ledger 与父子闭包后的**可复现候选上界**，不是已经证明全新且无历史同款关系的下界。后续要冻结 Amazon 分组，必须由独立核查补齐该历史关系黑名单或以其它可核实依据覆盖这项缺口。此限制不影响 6 条开发探针已逐行避开可见曝光和 reserve 清单，但跨平台/未落入 ledger 的历史关系仍标记 `NOVELTY_UNVERIFIED`。

候选资格、平台类目和西语确认均来自结构化源与本地来源记录；没有人工逐条确认商品同款或翻译，所有候选仍是 `CANDIDATE`，没有任何项目被标为 `VERIFIED` 或人工 gold。对于已人工确认依据，当前可报告数量为 0。

### 先前三平台 120 组方案（历史记录）

容量上可先按每平台 40 组设计：每个平台普通 20、复杂 20；训练 20（普通/复杂各 10）、验证 12（各 6）、最终测试 8（各 4）。每个平台两条开发探针计入训练组，剩余训练名额为 18。先按平台关系组抽取，再按普通/复杂分层，并在各分层内轮转类目、尽量使三集类目分布均匀；同一 Action 标题组、Amazon Parent/Child 家族、IKEA 系列不得跨集。跨平台同款只有在得到可核实关系证据后才可合并为一个分组并固定在同一数据集。当前不输出任何最终测试商品 ID、源文或分组清单，也不冻结 120 条划分；Amazon 关系黑名单与跨平台同款状态未充分证明，不能据此启动正式最终集实验。

### 三平台历史开发探针与门禁记录

已生成 6 条真实西语源探针：每平台普通、复杂各 1 条，均来自可用源池，列入未来 TRAIN 开发样本。`dev-probe.json` 保留每条源字段全文、商品 ID、工作簿/工作表/行号、源字段 SHA256 和源快照 SHA256。Amazon 探针筛选增加了西语词汇检查，避免把英语属性模板误标成西语样本。`dev-source-facts.json` 是仅基于这些西语原文的源事实表，逐项保留西语精确引文；它不是译文、人工标准答案或金标准。

主智能体已另行确认 Codex 原生只读门禁通过。本次数据审计没有生成候选答案，也没有启动最终集实验；6 条探针可用于 TRAIN 开发。最终集仍须等候选冻结、商品关系分组和人工标准答案证据齐备后再定。

## 复现

在仓库根目录运行：

```powershell
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' local/skill-competition/data-audit/incremental_audit.py
```

三平台旧脚本最近一次运行输出候选组数 `action=4764`、`amazon=3386`、`ikea=1136`，并生成旧版 6 条探针。当前 Amazon-only 脚本独立输出 3,317 个可见 ledger 下的近标题组和 6 条 TRAIN 源候选；这组数量仍等待完整曝光关系恢复复核。源工作簿以只读模式打开；所有写入仅落在 `local/skill-competition/data-audit/` 和本报告。
