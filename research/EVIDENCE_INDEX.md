# R1 证据清单与复现

日期 2026-10-16。正式研究输出为 UPSTREAM_AUDIT.md、REUSE_MATRIX.md、LICENSE_REVIEW.md、DESIGN_DECISIONS.md；本清单与 SOURCE_MANIFEST.json 提供追溯。

| 证据 | 位置 | 支持范围 |
|---|---|---|
| 实时git ls-remote、固定HEAD、文件树、上游干净状态 | local/research-v3/LIVE_REPOSITORY_CHECK.json | 三远端当前提交与克隆一致，命令实跑 |
| 上游35文件路径/大小/哈希、核验时间 | research/SOURCE_MANIFEST.json | 固定源码内容和许可文件可追溯 |
| 本轮独立控制探针代码 | local/research-v3/recheck.py | 仅上游审查，不作为正式Skills运行依赖 |
| 9项控制命令/退出码/输出 | local/research-v3/CONTROL_RESULTS.json | 建包、结构校验、假成功、Bash兼容等边界 |
| 合成输入与建包/输出产物 | local/research-v3/control-run/ | 自造工程控制输入，非商品样本或正确答案 |
| 完整第三方原文 | upstream/checkouts/ | 原有浅克隆，被Git忽略，不重新分发 |
| 上轮内容哈希清单 | upstream/SOURCE_MANIFEST.json | 本轮比较35/35文件一致，复用先前逐文件阅读证据 |
| 上轮实际逐文件研究与控制实验 | reports/UPSTREAM_AUDIT.md；upstream/checkouts/audit-run/ | 只复用固定提交技术事实，六技能旧范围已由V3取代 |

复跑方式（仓库根，PowerShell）：

```powershell
python local/research-v3/recheck.py
```

此命令会查询远端及重建本地合成工程控制产物，正常情况下打印 repo_count=3、remote_matches=3、control_commands=9；不以该数值本身代替人工审读日志。它不会安装上游Skill、调用翻译API、生成真实商品翻译或评判质量。

研究范围实数：3/3仓库实时HEAD已核对，35/35文件哈希与旧审查一致，2/3有明确MIT许可，1/3许可未确认；运行9个工程控制命令。可信商品质量样本=0，A/B/C语义比较运行=0，真实SKU批量试运行=0；这些项目的质量分母为0，指标N/A。没有读取Holdout答案。

未解决事项：Codex新增部分许可未确认；Claude原始运行机制不能原样用于本环境；game翻译逻辑未实现；部分上游测试脚本兼容/早退问题已复现，未修改上游。本轮可合法同条件运行上游B尚未证实，记NOT_COMPARABLE。

复跑健壮性说明：脚本现以实际旧 Commit/文件哈希比较，任一远端失败或变更即停止复用。一次复跑 Codex 远端发生 schannel TLS握手失败，已原样保留 `local/research-v3/LIVE_REPOSITORY_RETRY_FAILURE.json` 与 `SOURCE_MANIFEST_RETRY_FAILURE.json`；随后重试三个远端均成功且SHA未变，再完成9项控制命令。网络失败未改写为成功，也未忽略失败继续使用空HEAD。
