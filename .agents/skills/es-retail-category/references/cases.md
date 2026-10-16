# Category 合成工程场景

全部 `is_synthetic=true`，人为编写，无真实SKU/ASIN、历史中文、货盘hash或商品详情。不是VERIFIED、真实训练或盲测样本。以下“预期”是开发验收条件，不是实际模型运行结果。

## 合成输入

每项遵循ITEM_INPUT_CONTRACT。item_id/product_id均用 `synthetic-category-<编号>`，platform=action，明确非生产SKU。source_snapshot.label=`synthetic-category-v3`，sha256对完整source规范UTF-8 JSON实际计算，captured_at=null。source_locations对已提供字段用 `{synthetic:"cases/<编号>/<字段>"}`。生产ASIN未知不填假值，未提供字段null，group_id=null、dataset_split=unassigned。

输出保留相同item_id/source_snapshot、contract_version/knowledge_version及完整source或不可变引用。category_context五项及evidence严格遵循入口，证据不能引用开发者预期。研究建议始终未批准。

## 正常 N1：清晰单类

title=`Cepillo para lavar platos`，categories=`["Hogar","Cocina"]`，description=`Para limpiar platos y vasos.`

预期：保留原路径；中文候选“家居→厨房”；研究建议可提“家居清洁→餐具清洁工具”，明确候选。引用 `platos y vasos`，不发明抗菌、刷毛材质或耐温值。分类检查可PASSED；样本与整件译文未批准。

## 异常 A1：疑似错类目

title=`Mascarilla hidratante para manos`，categories=`["Cuidado personal","Cuidado facial"]`，description=`Para hidratar las manos.`

预期：来源不变，来源中文可为“个人护理→面部护理”；研究建议“个人护理→手部护理”另列。引用 `para manos` 和 `Cuidado facial` 标不协调待核实，REVIEW_REQUIRED。不确认平台有错，不以研究建议覆盖源路径。

## 异常 A2：跨类双用途

title=`Taburete plegable con caja de almacenamiento`，categories=`["Hogar","Muebles"]`，description=`Sirve como asiento y para guardar juguetes.`

预期：保留家具路径及中文候选；研究建议可覆盖座凳/收纳，证据 `asiento` 与 `guardar juguetes`。不把玩具当包装内容，不推定儿童适用或承重。明确双用途不是自动冲突；不能无证据强定唯一研究主类。

## 异常 A3：低可信多义语境

title=`Banco`，categories=null，其余商品内容缺失。

预期：来源及中文来源类目均null，研究建议可空；保留家具/工作台等备选语境与原文 `Banco`，不确定成银行/长凳。REVIEW_REQUIRED；向术语交接缺用途/类目的问题，不编材质。

## 异常 A4：缺级/污染

title=`Caja para guardar herramientas`，categories=`["Bricolaje","待补充"]`。

预期：两个源节点均保留，中文可为 `["DIY/家装",null]`；第二级SOURCE_ISSUE问题；不能把猜测“工具收纳”冒充平台二级。若提研究建议需引用标题并分列。REVIEW_REQUIRED。

## 失败 F1：身份缺失/重复/换源

取N1但删product_id、同批重复item_id或源hash改变仍尝试复用。预期缺身份/不确定身份FAILED；换hash必须重判，不直接复用。不能以行号/标题补生产键；批次不能吞失败、重复或少返回。

## 失败 F2：无法回查源

取N1但source_snapshot/source_locations不可取得，或JSON同名key冲突覆盖类目。预期FAILED，列输入缺口，不静默修复原数据、不输出确定替代类别。

## 触发与非触发

|请求|预期路由|
|---|---|
|理解Action西语原分类并交给术语判断|触发Category|
|给Amazon.es西语商品提独立研究类目|触发Category，不继承父ASIN属性|
|翻译法语商品|不触发，方向不符|
|删除西语描述中的重复段落|不是Category工作，交Reviewer.SOURCE_AUDIT|
|给软件bug分类|不触发，非零售商品分类|

## 交接不变量

Category→Terminology保持item_id/source_snapshot/contract_version/knowledge_version；待复核语境不作为确定术语证据；研究建议不是批准词条。给Reviewer时仍保留完整source。Category不输出删减动作，也不批准整件译文；PASSED不能解释为VERIFIED。
