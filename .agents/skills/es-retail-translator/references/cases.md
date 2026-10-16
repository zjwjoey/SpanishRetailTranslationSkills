# Synthetic 行为案例

全部为手工构造的 `is_synthetic=true` 测试，不来自历史货盘，不提供人工gold。输入须补齐ITEM_INPUT_CONTRACT的身份、source_snapshot和synthetic定位；生产ASIN未知时不用假ASIN，测试用product_id明确写synthetic标识。

|请求|预期路由|
|---|---|
|“把这批Action西语商品名称译成中文”|触发；短而明确时直接候选，不固定启用五Agent|
|“$es-retail-translator 翻译这条Amazon西语规格”|显式触发|
|“把中文品名译成西班牙语”|非触发，超出方向|
|“中文描述润色一下”|非触发，无西语商品翻译|
|“独立审查这条已有中文是否漏掉配置”|交Reviewer.TRANSLATION_AUDIT|

## 正常：包装层次与小数

title=`Botellas reutilizables, 2 x 500 ml`，specifications有序条目 `Altura: 21,5 cm`。允许候选“可重复使用水瓶（2个装，每个500毫升）”，规格“高度：21.5厘米”。保留2件、单件500ml与21.5cm三个事实，不能新增材质/密封性。status=REVIEW_REQUIRED，结论awaiting_post_audit；source_audit=null及skip_reason=short_clear_fields。

## 异常：长字段、保护词和局部配置冲突

synthetic商品，brand=`PHILIPS`；title=`PHILIPS OneBlade 360 QP2734/30, afeitadora híbrida, 2 Cuchillas 360`；bullets包含`Incluye 2 Cuchillas 360 y Peine-Guía Ajustable 5 en 1`及`Contenido de la caja: 1 Cuchilla 360`；description=`PHILIPS OneBlade 360 QP2734/30. Recorta, perfila y afeita. Ver más…`；platform_metadata单列`rating: 4,5`与排名。没有真实ASIN。

读完整源及Reviewer动作。PHILIPS/OneBlade 360/QP2734/30原串保存；可译“混合式剃须刀”“修剪、塑形和剃须”“五合一可调导向梳”。“五合一”不是5把梳。两处明确包装刀片数量2与1冲突：该槽目标值null，conflicts保留两段证据；不要因型号猜配置。重复品牌或标题片段只有在无独有事实时才去重，并指回canonical来源。评分/排名的实际值转research_metadata，不塞功能描述。`Ver más…`保留源归档并记录正文可能截断，未见尾文不补写；候选整体REVIEW_REQUIRED，保留所有未受影响事实。

后审所需：完整源+动作及账本+候选中文。若后审只收到精简译文，应要求补齐；若发现品牌/型号遗漏或把数量冲突强行选2，应提出P0候选问题，不以保护词清单中有值掩盖实际目标缺失。

## 局部缺失与失败

- 仅title=`Marco A3`且身份与源快照可靠：可译“A3相框”，其他translation_zh字段null，不加29.7×42cm。列缺口，仍awaiting_post_audit。
- 两条item_id相同但属于不同商品，无法确定对应：FAILED，不任意挑一条。
- source_snapshot指向hash甲，source_audit来自hash乙：拒绝复用动作；重新获取匹配审查，候选待审，不覆盖甲源。
- 原始JSON同一对象有两个`color` key：保留原文本及两值，要求转换有序属性数组/确认映射，不能让解析器静默留下后一值。
- 关键原文不可得，仅历史中文：FAILED；不能把中文反推为西语事实。

以上是预期行为，用于载入演练。只阅读此文件不证明实际调用或质量通过。
