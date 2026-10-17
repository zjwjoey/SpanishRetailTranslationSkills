---
name: es-retail-terminology
description: Resolve Spanish retail terms into Simplified Chinese by product category and use, and protect brands, series, models and technical identifiers for Action, Amazon.es or IKEA Spain. Use for terminology decisions; exclude general prose, other language directions, whole-field filtering and final translation approval.
---

# 西语零售术语与标识保护

版本 `0.2.6-candidate-amazon-r3`；工程候选，尚非真实数据训练或质量验收结果。独立完成术语判断，不代替整件翻译、分类或审校。

## 输入和适用范围

读取 [商品输入](../../../contracts/ITEM_INPUT_CONTRACT.md)、[交接](../../../contracts/SKILL_HANDOFF.md) 和 [已批准知识政策](../../../knowledge/approved/KNOWLEDGE_POLICY.md) 及其 [manifest](../../../knowledge/approved/manifest.json)，记录实际版本。异常严重度遵循 [质量契约](../../../contracts/QUALITY_AND_SEVERITY.md)。

输入为 `item_id/platform/product_id/source_snapshot/source/source_locations`；可附同一源快照的 `category_context`。保留完整源或不可变引用、有序重复属性和变体信息，不用历史中文补造西语事实。仅给名称可以部分处理并列出缺口；稳定身份或快照无法确定、源不可访问、JSON重复key导致丢值时，停止该项定稿并报 `FAILED`。

触发例：“结合清洁用品语境判断西语 cepillo 并保护型号”。非触发例：“删除Amazon重复段落”“批准中文整件译文”“翻译德语文章”；说明边界并交回调度，不为非适用请求制造商品通过记录。

兼容对象型号后缀/连接器、产品代际和件数须按[事实唯一来源与目标投影](../../../contracts/FACT_LEDGER_PROJECTION.md)分槽：明确Generación为第几代，禁止因数值为2而译作2件；兼容品牌和协议不是本商品制造品牌或件数。

## 判断流程

材质、表面属性、织物或携带部件歧义须读[材质维度与部件角色](references/material-dimensions-and-parts.md)。不把上一轮示例词做成全局替换表。

1. 从原名称、类目、用途、规格及详情识别主体、材质、功能、适配对象的术语，保留每次出现的精确位置。类别只提供语境：原类目与实际用途冲突时不能盲从标签。
2. 按类目、适用及排除条件匹配正式知识。只有实际批准条目覆盖当前语境和字段时才引用其ID/版本。当前批准术语数为0，仍可依西语语义提出候选；不得声称人工批准、`VERIFIED` 或编造证据编号。
3. 无适用词条时提出有原文依据的中文候选，说明用途和排除解释。未识别词、不明品牌归属、影响主体或用途的多义词保留备选并报 `REVIEW_REQUIRED`。可并行初判；消歧需要类别时向调度列出最小缺口，合并语境后再判断，不递归调用分类Skill。
4. 识别并逐字保护品牌、系列、型号、ASIN、GTIN、零件号及技术代码；记录全部出现位置与目标路径。兼容对象品牌也保护，不能当成本商品品牌。首词或大写不等于品牌，不机械删首词；可疑代码原串保留，不擅自纠正。
5. 数量和限定词按语义槽理解：`5 en 1` 表示组合功能/配置而非5件；`2 x 500 ml` 分开记录件数与单件容量。型号数字不作包装数。原串一致不代表数量语义正确。同语境保持一致，跨语境不机械一词一译。
6. 核对冲突、未知术语及保护遗漏；原词冲突不能靠较长字段或常见解释覆盖。术语结论不决定整段去留；重复、噪声、截断和数量归属争议携原证据交Reviewer，不自行删除或输出源筛选动作。

## 输出和交接

按 [输出字段](references/output.md) 生成 `terminology_decisions`、`protected_identifiers`、缺口和冲突。所有交接带 `item_id/source_snapshot/contract_version/knowledge_version`，不可套用不同hash的类别或旧术语结果；源和快照不改写。

运行状态仅 `PASSED/REVIEW_REQUIRED/FAILED`：`PASSED` 仅表示已检查范围的术语与保护判断无未决问题，候选仍非人工批准；有未知词、语义/源冲突、必要语境缺失则 `REVIEW_REQUIRED`；无法可靠定位身份或源则 `FAILED`。数据核验状态与运行状态分开。

把完整源、候选依据和保护清单交Reviewer.SOURCE_AUDIT或Translator；未决问题不得伪装已解决。学习所需人工确认由后续流程处理，本Skill不写正式知识库。按需读 [合成场景](references/cases.md) 核对正常、异常、失败与跨Skill边界。

IKEA家具、部件、聚合物或染色工艺歧义须读取[IKEA材质与部件消歧](references/ikea-material-role.md)。
