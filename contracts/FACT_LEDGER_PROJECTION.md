# 事实唯一来源与目标投影扩展 amazon-r3-v1

用于兼容清单、代际/数量或多字段合成的商品。扩展基础翻译契约，不替换原始source，不是批准知识或新的Skill。不依赖local脚本或独立翻译引擎；Codex原生生成并回读实际JSON，离线检查器只验证绑定。

## 1. 先源、后译、再投影

从完整source按字段先登记事实，再生成中文。执行分段中的半个词/型号应与相邻片段在完整源中闭合；只有源本身的省略、`Ver más`或缺尾才是未知内容。先判断实际语言，明确西语正文可含品牌、技术代码和借词；完整英文主体不作为本语向译文。

`retained_facts[]`为唯一中文事实来源，每项含：

- `fact_id`、`source_field`、`source_span={quote,occurrence,start,end}`（未知偏移null，但引文必须真实可定位）；
- `role`和`scope`：事实类型及对象/部件/所选变体/条件，不能以数字替代角色；
- `action`、`zh`及可选`label_zh`；明确事实有具体中文，待核槽`zh=null`并写uncertainties/conflicts，噪声/去重另留来源账本；
- `target_fields`：所有实际目标JSON Pointer。多个源重复项可指向同一事实，但不能吞掉独有后缀、否定、比较条件或角色。

允许清楚且同作用域的事实合句；任何局部疑点须先拆槽，不null掉同句其他已明确事实。`reason/meaning/notes`中的文字不算中文译文。

每项规范中文的引文须覆盖其中全部主张，不能从其他字段偷带未登记的事实，也不把整块混合属性当作一个technical_spec事实。`uncertainties[].fact_ids`只引用实际未确认、中文为null的槽；可见兼容前缀继续保留，未知尾部可用空fact_ids及真实截断位置描述，不能把已保留清单整体挂成未确认事实。疑点仅写旁注而确定目标仍存在，不能算隔离。

## 2. 兼容对象逐项闭合

兼容清单另列`compatibility_lists[]`，包括完整原字段位置、可见项目、否定/限制/版本或连接器条件、末尾截断状态。每个可见项目有`source_literal`、`qualifier`、`fact_id`和`disposition=RETAINED/REVIEW_REQUIRED`。登记源字面缩写，不擅自展开未知前缀或补出截断后的型号。

品牌/型号代码原样保护，但普通西语限定必须译为实际中文：`conector Lightning`、`generación`、`con estuche de carga`、主动降噪、英寸等不是可原样贴整段的型号代码。有这类条件时`qualifier`登记原限定，`qualifier_zh`登记实际中文且须出现在对应规范中文中；不能所有项目都写qualifier=null，也不能用中文前缀加整份西语清单冒充翻译。源字面清单保留在账本，中文目标同时保留代码与译出的限定。

每个明确项目在事实中文中实际出现，再指向可解析目标；不能用“多种手机”“AirPods系列”等总称代替清单。`AirPods Max`不覆盖带`conector Lightning`限定的项目。相同主型号的连接器/代际/后缀差异不得粗略去重。QC、PD等协议、接口两端方向和设备兼容对象分开登记，不能互相替代。

缺官网或未来型号不构成删除源明确兼容声明的理由；作为“源文标称适用于……”保留，独立审查实际适配未知。不同非排他清单可互补；同条件明确兼容与不兼容才是冲突。异常模板字段按归属单独待核。

## 3. 代际是角色，数量是另一角色

`Generación/segunda generación/2.ª generación`等表达登记`role=generation`，中文为第几代；不得落到`item_count/package_count/unit_count`或写“几个单位”。品牌型号中的数字、`5 en 1`功能组合也不作件数。

确有`Número de artículos/Número de paquetes/Contenido de la caja`时分别保存数量、包装层次和组成。数字相同不能合并角色。`numeric_role_checks[]`记录源键、原值、事实ID、`dimension`和候选中文，逐项核对；没有原证据的槽不补造。

## 4. 合成只复用事实，不重写数值

先审查事实表，后生成title/specifications/bullets/description/details/categories/brand。`projection_map[]`逐个列出实际字符串目标的`target_path`、`fact_ids`、`part=zh/label_zh`和`joiner`。实际目标必须等于所引规范事实文字的原样拼接；同一事实不得在另一目标自由改写数字、单位、对象或限定。需要自然表达时先改规范事实，再更新全部引用并重新审查。

目标可选择不同事实，但所有重要源事实必须有去向；缩短标题不代表删除正文事实。规范事实待核后，其所有目标和去重别名同步去掉该确定值；不能在conflicts里注明100g/110g，标题仍确定100g。重量标签若不能确认净重/商品重/包装重关系，登记作用域不明，不武断声称源数值一定互斥。

不得写另一份无投影依据的合成中文作为额外`summary`、嵌套备份或备注成品。平台metadata/标识按基础契约单独保存实际值和来源，不因缺少某个原生导出对象就把已经正确的中文事实判错。

## 5. 原生交付与独立检查

交付基础契约规定的完整实际对象（含translation_zh、identifiers、research_metadata、field_alignment、protected_identifiers、retained_facts、账本、疑点、review和run_metadata），扩展字段`contract_extension=amazon-r3-v1`、`compatibility_lists`、`numeric_role_checks`、`projection_map`。不可只交事实表并称完整原生契约通过。明确源不可恢复时FAILED；其余候选保持REVIEW_REQUIRED，人工确认不自动产生。

独立Reviewer先保存完整源事实，再读取所有实际目标、规范事实及投影。分别判断：源清单漏登、登记后未译、投影不一致、原事实本身译错、过度隔离、结构导出缺口。只有投影一致不能证明规范事实正确；尤其复核型号后缀、2cm/20mm的对象和单位、代际与件数、负载与包装层次。任何工程检查通过都不等于真实质量或训练准入通过。
