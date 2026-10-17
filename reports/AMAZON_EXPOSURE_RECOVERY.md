# Amazon 历史曝光集合恢复

状态：`CANDIDATE_BLACKLIST`，`complete=false`。本轮恢复了旧构建器的固定历史 ASIN token 集合，并将 10/17 已保存的 Amazon 候选、选择、生成和 QA 标识纳入过滤。名单供新样本排除使用；它不表示名单中每个 ASIN 都已翻译。

## 重建结果

旧构建器 [`build_inventory.py`](../local/plain-vs-skills-v1/amazon-inventory/build_inventory.py) 的 `hist` 只由其中列出的 16 个固定路径正则提取，未由 69,122 个文件的遍历生成。已对这 16 个路径逐一重新读取并保存哈希，恢复出 **2,899 个不同 ASIN 形 token**，与当时 `inventory.json` 的 `historical_asin_count=2899` 完全相符。

重读源盘 5,000 行工作簿后，其中 **1,564 个 token** 命中工作簿 ASIN 列，**1,335 个不在该 ASIN 列**。原 `exposures.jsonl` 写入时对 `a not in source_rows` 执行 `continue`，因此只写出能匹配源表行的 1,564 条记录；缺失 1,335 个是导出范围差异，不能据此断言它们全部是已翻译商品或全部是遗漏翻译。原脚本仅为命中的行增加父 ASIN，重建后的旧单向关系并集为 **2,905**，也与原 `relation_asin_count=2905` 相符。

额外纳入 10/17 的历史材料：65 条候选池中 15 条 Amazon 商品记录（池内共 27 个 ASIN token，含父组标识）、Amazon selection/source-only 与 QA 记录（10 个商品记录，结构化字段含 18 个 ASIN 标识）、23 个 `fresh20_excluded_ids` 备选/排除标识，以及既有 10/17 Amazon exposures/QA 文件的 token 引用。当前 `plain-vs-skills-v1/runs` 只存在 Action 的运行目录，没有 Amazon 生成运行目录；QA 和 frozen source 标识作为已保存输入/审查证据记录，不推断额外模型生成。

在 5,000 行源表的 `ASIN` / `Parent ASIN` 两列上，对历史 token 和 10/17 选中、候选、备选标识展开商品家族闭包。最终 `blacklist.json` 有 **2,949 个去重 token**，其中 17 个是此次父子家族闭包新增项。旧 2,905 单向并集和完整闭包分别保留，便于复核。

## 分类与限制

逐项清单分开保留 `historical_selected_or_input_asins`、`historical_generation_record_asins`、`legacy_fixed_path_tokens`、`10_17_candidate_pool_asins`、`10_17_fresh_backup_or_excluded_asins`、`conservative_related_asins` 和 `parent_child_closure_asins`。每个 `records` 项含来源路径、来源文件 SHA256、匹配方式、源表匹配情况、行号及父 ASIN（若能关联）。文本中仅被 ASIN 正则命中的内容单独作为保守相关 token；这可能是描述里提到的其他型号，不能标成该商品的真实 selected ASIN。

所有输出显式保留 `complete=false`。已恢复的是旧构建器明列的 16 个文件和本次列明的 10/17 文件；没有证明历史文件集合穷尽全库。没有重复扫描旧构建器提到的 69,122 个本地文件，没有扫描当前 `local/skill-competition/` 开发数据，也没有读取未来 holdout。

## 来源哈希

源盘 5,000 行文件：`F:\按日期整理\亚马逊表格\20261005\AmazonES_5000SKU_西语不带图_20261005.xlsx`，SHA256 `a30cab8888a63822bc44853189d44f9fc878b4c422aa3a86e76bb0fb663237ef`。与旧 `inventory.json` 的 source hash claim 完全一致。

旧方法文件 `build_inventory.py` SHA256 为 `15b5ef713def0f2e3512010f934dfb1df76cdf1da2a0405d18d79ed6d3fea066`；旧 `inventory.json` SHA256 为 `7bb60f0519b9fcd3327b715163d47ea0e4978ec89787f03c682bc51b13d18e29`。固定 16 个旧证据文件与 21 个 10/17 证据文件均有实际 SHA256，清单见 [`evidence_manifest.json`](../local/skill-competition/exposure-recovery/evidence_manifest.json)；未发现缺失来源文件。

## 交付与过滤接口

- [`blacklist.json`](../local/skill-competition/exposure-recovery/blacklist.json)：逐项 ASIN token、分类、证据路径与父子闭包；数据任务应将 `classification_policy.all_blacklist_tokens` 用作过滤集合。
- [`recover_blacklist.py`](../local/skill-competition/exposure-recovery/recover_blacklist.py)：只读取固定 16 条旧路径、显式列出的 10/17 文件，以及源盘工作簿 ASIN/Parent ASIN 两列；可复现重建。
- [`evidence_manifest.json`](../local/skill-competition/exposure-recovery/evidence_manifest.json)：输入、方法与 manifest 的实际文件哈希。

根调度与数据 agent 已收到 blacklist 文件路径、去重计数和字段含义，用于过滤 Amazon 新 6 及 120 候选容量。该列表是当前已恢复证据的保守门禁，不构成 `complete=true` 或历史翻译计数。
