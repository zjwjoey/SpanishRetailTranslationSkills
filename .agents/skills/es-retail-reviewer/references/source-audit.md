# SOURCE_AUDIT 操作规则

适用契约 `1.0.0-foundation`。此模式不翻译最终中文，只对完整源的内容去向作候选决定。

## 输入、定位与覆盖

确认商品与快照hash对应、字段映射可回查，再合并类目与术语结果。类目不足时不要凭首词确定商品主体；保护品牌、系列、型号的候选仍应保留。只把完整英文主体标为超出西译中方向，英文品牌、型号及合法专名不自动污染。

source_field指向不可变输入的精确叶字段，如 `source.title`、`source.bullets[1]`、`source.details[0].value`。每个span含精确原文quote、从1起的occurrence及start/end；偏移已核算时为Unicode码点半开区间，否则二者null，以quote+occurrence定位。不要用UTF-16代码单元偏移冒充码点；不能将不同字段的同句合并成一个定位。若quote非精确子串或occurrence不存在，该决定不可执行。

逐个源字段检查实质片段覆盖：每段有效事实有TRANSLATE/PRESERVE或待核动作，所有转出/排除/去重内容有账本。允许纯标点不单列，禁止用“其他内容”一笔带过未审段落。未提供字段标缺失，不生成猜测内容；保留所有源字段或不可变source_archive引用。

## 六个动作

|action|何时用|需要的证明与目标|
|---|---|---|
|TRANSLATE|明确商品主体、功能、材质、规格、数量、配置、用途及限定|对应中文字段路径；保留数值及限定的原证据；不输出最终译文|
|PRESERVE|品牌、系列、型号、ASIN/GTIN/零件号等不可随意改写标识|identifiers或合适目标内保存实际原串、类型及来源；加入账本|
|METADATA|评分、排名、评论、上架日期等研究元数据|research_metadata/identifiers内实际原值、单位/类目/时点；加入账本，不能只写“已转出”|
|DEDUPLICATE|同商品同语义槽中已证实无独有事实的完全重复或等价重述|canonical_decision_id指向可追溯保留项；记录等价理由、保留目标及事实引用|
|EXCLUDE_FROM_DESCRIPTION|纯网页操作提示等不进入商品描述|target_field=source_archive并保留源；含疑似截断迹象时另建REVIEW_REQUIRED|
|REVIEW_REQUIRED|事实冲突、截断、归属/语义/去留未明|定位问题槽与证据，目标为待核槽或source_archive；不输出确定替代值|

所有decision共有 `decision_id/item_id/source_field/source_span/action/reason/target_field/review_status`，review_status只为PROPOSED或REVIEW_REQUIRED。带去重动作的decision额外记录canonical_decision_id。

所有非TRANSLATE动作逐项进入preservation_ledger，包含decision_id/source_field/source_span/disposition/target_field/retained_fact_refs。disposition说明“原样保留/转元数据/保留canonical/归档/隔离待核”等实际处置，不构造第七种action。retained_fact_refs指向有实际值的目标/源或被保留事实，不能全部空数组敷衍。目标采用可解析路径；同一输出内路径风格一致。引用input source时明确是原始不可变引用，不假装已写入新字段。

PRESERVE可与标题翻译范围重叠，但应说明该子串是受保护标识、不是第二份商品数量。对QP2734/30中的数字不做件数抽取，不将系列360改成数量或角度事实。

## 去重与元数据

先比事实槽、对象、单位、范围与限定，再比文字。两个字段都写“1 pieza”但分别描述机身和附件时不能去重；2件与2×500ml也不是等价。重复标题中增加的材质、型号后缀、兼容对象或否定必须保留。近似、同义不明或源值矛盾时待核而非去重。

同一句完全重复按occurrence分别定位，后一项指向第一保留项。canonical必须存在且本身保留事实，不允许A去重到B、B又指回A。品牌重复可在描述中去重显示，但identifiers必须仍有原串和全部来源。评分/排名脱离商品描述后仍保留类别、数值与来源，不能把“排名1”写成“销量第一”的独立商品承诺。

## 截断、冲突与局部隔离

`Ver más/查看更多/…`先作展示残留判断，再问字段是否缺失后文。不能仅剔除提示便认为正文完整；含义不完整或是否缺文无法判断则truncations记录span、受影响范围、理由，status=REVIEW_REQUIRED。完整可读的前文事实可继续TRANSLATE。

冲突先核对是否同一语义槽：两处明确“总包装内刀片2片/1片”形成冲突；“有两刀片”与“机身已装1片”未必冲突，未明确是否包含时归属待审。`5 en 1`是功能/档位表达，`60 minutos`是时长，型号30不是包装数，不可混槽比较。

conflicts列fact_slot、两侧原字段/span、不同值、归属解释与受影响目标。只隔离该槽：确定的品牌、型号、梳头功能、续航仍能保留；包装刀片数量及受其影响的总配置不取任意一侧。明确需要人工确认的具体问题，不写泛化“请检查全商品”。任何未决冲突/截断令整件REVIEW_REQUIRED，但不得清空未受影响字段。

## 输出闭合检查

按SOURCE_AUDIT契约输出身份/快照/版本、decisions/preservation_ledger/conflicts/truncations/status；同时提供动作所需的identifiers、research_metadata及不可变source_archive引用等实际目标。每个转出动作沿账本找到值或canonical；每个canonical沿回源；每个冲突/截断可定位。无未决问题可PASSED（仅源筛选），缺完整原文或身份无法确认FAILED。明确的AI动作review_status=PROPOSED，待核动作review_status=REVIEW_REQUIRED，均不自行签发人工批准。
