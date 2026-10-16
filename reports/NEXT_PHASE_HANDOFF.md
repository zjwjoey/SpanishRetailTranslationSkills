# 下一阶段交接

从本仓库根目录和feature/foundation-v1继续；先读README、AGENTS、CODEX_DEVELOPMENT_PROMPT_V3、FOUNDATION_ACCEPTANCE。

2026-10-16最新：第二轮已实际运行32件新商品及内部修复/回归，但新P1使两次候选均未通过，当前Reviewer恢复1.0.1。先读[第二轮结果与回退](ROUND2_TUNING_REPORT.md)；knowledge/proposals/ROUND2_REVIEWER_CANDIDATE.patch禁止自动应用。原始失败证据及排除问题后的候选字段在local/tuning-round-02，不能当人工gold。下一轮先修Translator目标事实覆盖、字段角色和引用闭合，再冻结新版本/新商品验证。

2026-10-16更新：第一轮工程候选调优及24件新商品配对验证已执行，先读[本轮真实结果与证据](ROUND1_TUNING_REPORT.md)。Reviewer为1.0.1-candidate-r1；正式人工知识和Train/Validation/Holdout准入仍0。local/tuning-round-01/post-review/attempt2/results.json为后审候选，不能替代原A/B统计或人工gold。下列人工核验、隔离、自然发现和完整三方评测任务仍未完成。

1. 人工核验local/data-v3/HUMAN_REVIEW_QUEUE.md。72候选可按风险和类目先取少量，逐字段填写human_id/confirmed_at/evidence_refs/verified_fields及正确中文；勿直接全批批准历史中文。优先核对Action四月合成身份/七月污染、Amazon版本漂移/配置归属/截断。此目录未上传，需原开发机或重新授权读取原货盘。
2. 先确认稳定源，再按同款/父子/近重复/跨快照/跨平台关系分组；人工确认不足就小样本。按组建立train/validation；真正Holdout交独立权限保管，共享目录不算隔离。本轮所有候选已暴露，正式盲测要新样本。
3. 修复本机Codex CLI与账户支持模型的兼容性后，重新从根目录测试五Skill显式/自然发现、排除请求；本轮默认和忽略配置的真实探测均报unsupported，未改用户全局配置或换模型伪造通过。
4. 先重跑工程检查，再用人工核验集建立A/B/C；上游B若做MIT Claude适配，先写明差异及实际模型条件，无法比较继续NOT_COMPARABLE。
5. 单Skill/规则定向变化，专项与跨Skill回归、独立后审，最多3轮主要质量优化。先减少嵌套证据输出体积，测量完整端到端时长/Token再做真实小样本批次；未通过不得放大5500SKU。

已实际运行的本地检查命令（仅评测，不是正式Skill依赖）：

```powershell
git status --short --branch
python -X utf8 evaluations/check_foundation.py
python -X utf8 C:/Users/Administrator/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/es-retail-reviewer
```

离线评测器需要系统Python的PyYAML和jsonschema；本机已存在，没有安装依赖。其他四Skill可同样运行官方校验。正式Skills本身不依赖这些Python包。原始只读审计工具和完整商品仅在local（Git忽略），无需把它们变成产品程序。
