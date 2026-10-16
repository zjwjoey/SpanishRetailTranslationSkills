# 真实货盘状态（V3）

2026-10-16。数据可访问，状态DATA_AVAILABLE，不能写DATA_BLOCKED。原始目录F:/按日期整理，Action88文件（86xlsx+2既有ndjson）、Amazon8xlsx。本轮再算96文件SHA256，96/96与前轮一致，0变化；只读，没有重写原工作簿。证据local/data-v3/integrity.json及summary.json，不提交完整商品数据。

前轮同一会话真实审计成果保留，V3复核文件未变化，未重复夸大审计量：

|平台|结构/连接审计|有限AI语义审读|V3候选|人工确认|
|---|---|---|---:|---:|
|Action|18日期；40主表220650行；93325日期/数字SKU组；跨日期9946数字SKU|32描述+9规格，目的性诊断抽样|32|0|
|Amazon|2快照；同快照唯一ASIN配对5000+5300；跨快照7835 ASIN|40名称/核心规格配对，非随机总体样本|40|0|

不能把Action121332多版本配对比较次数当独立商品；四月5993合成ID身份未证实，多版本5511日期/SKU需保留源hash。七月西语原版有大量中文字段污染。Amazon两快照共有2465ASIN，Parent变化440，规格/详情变化不可直接复用旧中文。目录日期与文件标签日期差异保留，未认证真实采集时间。

完整历史取证报告：[Action](ACTION_SOURCE_AUDIT.md)、[Amazon](AMAZON_SOURCE_AUDIT.md)。这些报告描述已真实执行的诊断审计，非完整人工语义核验。
本轮规范化local/data-v3/candidates-v3.jsonl共72条，旧UNCERTAIN状态映射REVIEW_REQUIRED；全部group_id=null、dataset_split=unassigned。人工确认0，正式train/validation/holdout=0/0/0，HUMAN_VERIFICATION_BLOCKED。
人工可读清单：local/data-v3/HUMAN_REVIEW_QUEUE.md，含原文、历史中文、候选风险、两侧出处和人工确认字段。建议中文未获得可信生成/确认时如实留待补，不以历史译文填成正确答案。

未完成：图片语义检查、官网采集真实性核验、全字段语义遍历、跨平台与近重复关系分组、人工gold、真正Holdout访问隔离、正式质量/成本试运行。共享目录和worktree不是答案隔离。
