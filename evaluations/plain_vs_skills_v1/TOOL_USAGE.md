# 本地评测工具与证据边界

本轮实际检查的 ZIP 仅含三份 Markdown 文档，没有 bench.py / test_bench.py。这里的脚本为本地补充实现，测试结果只能代表记账工具，不能代表译文质量。

`python -m unittest discover -s evaluations/plain_vs_skills_v1 -p test_bench.py -v`

`python evaluations/plain_vs_skills_v1/bench.py prepare --pool <private-pool.jsonl> --exposures <private-exposures.json> --out <new-private-freeze-directory>`

默认必须有 complete=true 的历史证据及实际文件哈希；不完整记录不能假装通过。协议允许探索性实验时，可显式追加 `--allow-novelty-unverified`。这会永久记录 NOVELTY_UNVERIFIED 和 exposure_coverage_complete=false，不改变真实曝光台账，不构成正式 Holdout。两种模式均排除已知产品、家族和近重复标题；脚本不识别所有隐含同款关系，人工/AI源文核查仍必需。

冻结目录包含 selected.jsonl、freeze.json。真实执行后放入 plain.jsonl / skills.jsonl、独立 reviews.jsonl 与 findings.jsonl，再执行：

`python evaluations/plain_vs_skills_v1/bench.py score --dir <private-freeze-directory>`

缺失输出/审查只能是 NOT_RUN 或 PARTIAL_NOT_COMPARABLE。即使全部完成，结论仍是 AI 工程性审查，accuracy_improvement=null。源码事实台账先于译文核查的证据、原始执行日志、源哈希与人工确认状态必须另外保留，不能只写几个布尔字段。

## 运行条件

本次两臂均为外部独立目录、新 CLI 上下文、相同 gpt-5.6-luna / medium、同源同序同批次同schema、一轮最终自查、read-only 沙箱、关闭网页搜索和浏览器。普通臂显式禁用已安装的全局 Skills；Skills 臂仅加载冻结的五个项目 Skills 及必需资源。正式 Skills、历史样本和 approved 文件不改动。

技能禁用配置应指向实际 SKILL.md 文件，而非只写目录；实际效果须检查当前 CLI 的 prompt-input 和运行日志。[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills) 说明配置形式。工作区分离和路径隐藏不等于已证明操作系统级完全不可访问；本次不宣称权限隔离的正式 Holdout。

所有货盘、完整商品原文/译文、曝光明细、原始日志与盲审映射都仅保存在 Git 忽略的 local/ 目录。公开提交仅含脚本、合成测试、方法和匿名汇总。

## 本机实际降级与首次失败保留

首个文件读取试跑中，两臂的只读命令均被宿主策略拒绝，未取得有效输出；没有改用高权限。后续以 stdin 直接提供完整源文，两臂共同任务/结构相同，B 附上与冻结文件哈希一致的全部规则文本。原生目录仍分别展示零/五个项目 Skills，但本次不宣称成功测试了模型自行读取文件的原生按需加载。Learning 无已确认纠错，记为不适用；不强迫为翻译商品伪造学习调用。

直接文本模式的首次四件批次，B 仅回一件，原件保留；因此对两臂都增加完全相同的批次数量约束，并从首批重新执行 v3。最终汇总必须将探索性 v3 的结果与前两次运行故障分开，不能挑选几轮中的最佳译文。哈希抄写错误保留 model_reported_source_sha256；宿主关联原输入哈希只作运输记账，不修改译文，另记 MODEL_HASH_MISMATCH。

全量规则注入会放大 token 开销；本次成本仅适用于该降级条件，不代表正式原生按需读取的成本。没有人工 gold，独立 AI 源事实和其中文解释也可能有错；审查须回到完整西语源文，保留台账纠正意见。
