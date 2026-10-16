# 许可证与复制边界审查（V3）

日期 2026-10-16。任务 R1 实时核对三个远端 HEAD，均与已读固定提交相同；git ls-tree 全树和本地文件哈希一致。本报告记录工程复用边界，不推断仓库外另有授权。

| 仓库及 Commit | 实际许可核验 | 结论 | 本项目使用范围 |
|---|---|---|---|
| [translation-quality-codex](https://github.com/WenhaoLiu0218/translation-quality-codex/tree/fb3be31df931a0e71fe8955e25a12245dbf29453) @ fb3be31df931a0e71fe8955e25a12245dbf29453 | 固定树无LICENSE/COPYING/NOTICE；README未授予新增代码/文档明确许可 | LICENSE_UNCONFIRMED | 只读研究，借鉴通用工作流思想后独立表述；不复制其新增SKILL、脚本、README或元数据 |
| [claude-translation-skill](https://github.com/senshinji/claude-translation-skill/tree/42d6c8a2a07b77f085d6cafe6d4102d36aeafd02) @ 42d6c8a2a07b77f085d6cafe6d4102d36aeafd02 | 根LICENSE为MIT；Copyright (c) 2026 senshinji | LICENSE_CONFIRMED_MIT | 可在许可通知条件下复制/修改；当前独立写零售规则与契约，无需搬入Claude依赖 |
| [game-localization-skill](https://github.com/tokyboop/game-localization-skill/tree/bccaac8abde17bcd9e507a9c729e259ae1750251) @ bccaac8abde17bcd9e507a9c729e259ae1750251 | 根LICENSE为MIT；Copyright (c) 2026 tokyboop | LICENSE_CONFIRMED_MIT | 许可允许不代表功能已实现；只参考结构保护/明确结束思想，不复用空翻译模板 |

## 复制、改写与独立实现

- 若复制 MIT 上游源代码或实质性文档段落，须保留其版权及完整许可通知，并标明来源版本和改动；只放 URL 不足以替代许可通知。
- 当前 research/ 只保存本项目独立审查、文件哈希、来源链接和设计决策；没有第三方源码或大段原文。第三方正文仅留既有、被忽略的 upstream/checkouts/；本轮未提交或重新分发 clone。
- 缺许可证的 Codex 仓库不能因公开可读或声明改编自 MIT 项目，就自动视为整仓 MIT。其五份 Markdown references 与 senshinji 同名文件哈希相同；若将来需要这些文本，应从许可明确的 senshinji 固定提交取用并携带该 MIT 通知，仍不能推定 Codex 新增部分获许可。
- 同类通用流程，如角色分工、独立读源、双向覆盖核对、证据账本和有限循环，可以独立设计。本项目将 SOURCE_AUDIT 六动作与五 Skills 分工明确归因于用户 V3 规范，不标为复制上游实现。
- 上游案例、游戏数据及术语示例没有经过本项目人工核验，不作为 VERIFIED，也没有因 MIT 自动成为用户商品标准答案。

## 基线与门槛

当前没有经过证明、可合法且在本环境原样同条件运行的上游 B，比较状态 NOT_COMPARABLE。MIT Claude 工作流可考虑做明确标识的 Codex 适配；须先实际运行并记录模型、工具、依赖和改动，再确定可比性。game 空脚本不能当作质量很差的真实 B；Codex 未明许可部分不拿来复制执行正式基线。

LICENSE_GATE=PASSED_FOR_INDEPENDENT_AUTHORING：可独立创作恰好五个专业 Skills，不表示已允许公开发布第三方正文，也不意味着已完成模型调用、数据训练、独立质量验收或正式版本发布。
