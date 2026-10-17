# 普通 Codex vs 五个西语零售 Skills：30 SKU 对照 V1

创建日期：2026-10-17。状态：**PREPARED，真实 Codex A/B 尚未运行，不能报告提升率。**

## 目标
使用新鲜且无历史暴露的真实 SKU（Action / Amazon.es / IKEA Spain 各10条），比较：
- A：普通 Codex，不读本仓库的 AGENTS、五个 Skills 和历史答卷；
- B：同一模型与相同任务条件下的 Codex，仅增加冻结的现有五个 Skills、其参考文件和必要契约；
- C：未参与翻译的独立 QA 先完整阅读原始西语事实、再核查 A/B。

审查主体、用途、品牌型号、包装数量、规格/材质/部件、兼容清单、关键条件、事实遗漏、虚构、术语和分类。固定分母 Action=10、Amazon=10、IKEA=10。实际 token/耗时/费用仅有可信日志时记录，不作猜测。无人工 gold 时不得输出正式翻译准确率。

## 执行入口
直接将本目录的 [CODEX_EXECUTION_TASK.md](CODEX_EXECUTION_TASK.md) 交给本机 Codex 执行。严格遵守 [PROTOCOL.md](PROTOCOL.md)；其职责是实际运行并给出证据，不是编写建议后宣布任务完成。

## 当前状态
- [x] 选定三平台各10条的首轮方案
- [x] 独立评测分支和禁止修改正式 Skills 的边界
- [x] 公平性/数据泄漏/质量核查协议
- [ ] 盘点本机全部既往曝光 SKU、ASIN 父子/系列/近重复组
- [ ] 从真实只读源中冻结30个全新西语 SKU
- [ ] 普通 Codex 和五 Skills 分别真实生成30条
- [ ] 独立 source-first QA 与配对结果统计
- [ ] 人工确认纠错、正式 gold 与版本发布

所有完整商品原文、翻译结果、历史曝光清单、原始日志放在 Git 忽略的 local/ 下，不向公开 GitHub 推送。未经用户额外授权，不改 ActionSKUTracker、AmazonESBestseller、IKEASKUTracker、五个 Skills 或 knowledge/approved；不合并 main。

如本机数据缺失或 Codex 运行受阻，结论必须写 NOT_RUN/BLOCKED，不允许用合成商品代替真实的30条。