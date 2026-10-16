# 能力复用矩阵（V3，五 Skills）

日期 2026-10-16。固定来源 SHA 见 [来源清单](SOURCE_MANIFEST.json)。REUSE=可采用的通用工程做法或许可明确内容；ADAPT=需改商品语境/运行时；REFERENCE=仅设计参考；REJECT=不进入正式流程。以下均是能力决策，未声明已复制第三方正文。

| 来源 / 能力 | 决策 | 五 Skills 对应 | 处理与限制 |
|---|---|---|---|
| Claude：翻译/术语/独立审校职责分开 | ADAPT | terminology、translator、reviewer | Codex 实际执行者按批次/风险分工，非每商品固定四角色 |
| Claude：任务依赖与文件所有权 | REUSE | 五者开发协作 | 通用工程做法写入 AGENTS；不增加正式 Skill |
| Claude：术语 context、sources、不确定性 | ADAPT | terminology、learning | 加类目、适用/排除语境、批准版本；置信度不等于 VERIFIED |
| Claude：按原词单键去重术语 | REJECT | terminology | 同词不同类目/用途保留多条，冲突待复核 |
| Claude：根据来源数量产生可信度 | REFERENCE | terminology | 权威性、独立性、适用范围优先；人工确认决定本项目训练准入 |
| Claude：双向核对新增与遗漏 | ADAPT | reviewer | 后置审查完整源、SOURCE_AUDIT日志和译文，检查误删 |
| Claude：文档结构 manifest | ADAPT | reviewer、translator | 改为商品字段/事实/去向证明，行号只定位，不对齐商品 |
| Claude：按10页/50词切分 | REJECT | translator、reviewer | 按复杂度、商品组、上下文预算实测批次，不拆变体事实 |
| Claude：TeamCreate/Sonnet/Opus/env/textutil | REJECT | 五者运行环境 | 运行时不可直接移植；不用虚构 Codex 工具模拟成功 |
| Claude：强制DOCX+PDF | REJECT | translator | 商品字段交付依契约，按需输出研究结果 |
| Claude：Bash结构测试 | REFERENCE | reviewer | 实跑有早退缺陷，不进入正式运行依赖 |
| Codex：原生入口和简洁元数据 | REFERENCE | 五者 | 按本项目规范独立创作，未明许可内容不复制 |
| Codex：源块/对齐稿/阅读版分开 | REFERENCE | translator、reviewer | 借鉴通用可追溯思想；独立定义商品片段证据与字段去向 |
| Codex：四角色强制完整文档流程 | REJECT | 五者调度 | 零售短字段按需，长字段/高风险才深审，调度由AGENTS负责 |
| Codex：建包与PDF脚本 | REJECT | translator | 无明确许可且不需论文流程，不成为Skills依赖 |
| Codex：VALID作为准确性通过 | REJECT | reviewer | 无关译文能通过，仅是包结构检查 |
| Codex：术语先行、完整源独立核查 | REFERENCE | terminology、reviewer | 通用方法独立表述；不继承其未经核验词表 |
| game：占位符不被改写 | ADAPT | terminology、translator、reviewer | 扩到品牌/系列/型号/ASIN/GTIN/零件号，检查字面与出现范围 |
| game：单次执行与明确结束 | ADAPT | 五者任务执行 | 依据真实产物结束，规则优化最多三轮，不以exit0代替交付 |
| game：参考译文自动提词 | REJECT | learning、terminology | RAW历史译文不能直接晋级正式知识 |
| game：翻译/QA/批量程序 | REJECT | translator、reviewer | 实现为空或文件不存在，不能作为基线 |
| game：长度50%-150% | REJECT | reviewer | 西中长度比例不能代表事实质量 |
| 项目V3：source片段六动作 | ADAPT | reviewer、translator | 独立设计 SOURCE_AUDIT，不假称从上游代码复用 |
| 项目V3：类别与术语初判合并 | ADAPT | category、terminology | 类别定语境，术语定含义/保护清单；不决定删整段 |
| 项目V3：人工纠错→候选规则→回归 | ADAPT | learning | 只读已确认纠错，不能自行改正式库或签发升级 |

## 五者的统一协作

category 给出平台源类目与研究建议；terminology 提供词义/品牌型号保护。两者可并行初判，有歧义时合并再定稿。reviewer 在必要时 SOURCE_AUDIT，translator 根据审查与语境生成候选，reviewer 后置读取完整源和动作日志检查误删。learning 在人工确认纠错后离线提案。

SOURCE_AUDIT 的去重/元数据转出不是删除原文；任何独有事实和不确定重复均保留并待核。以上流程是本项目政策，不能代替真实效果测试。
