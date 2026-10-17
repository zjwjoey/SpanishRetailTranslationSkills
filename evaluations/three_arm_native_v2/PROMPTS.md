# 三臂正式提示词（冻结前须保存原字节 hash）

## COMMON_TASK：A / B / C 完全相同
将随输入提供的西班牙语零售商品原始信息翻译成适合中文内部商品研究使用的简体中文。忠实于提供的数据，不查外部网页，不补造原文没有的商品事实。按统一结构输出每条商品的中文商品名称、中文平台原类目、规格、卖点、描述及详情。原来就有的商品 ID、品牌/型号标识字段照原样保存；原文不明确时可以把受影响的中文值设为 null，并在 issues 记录原因。不要修改 source 或 source_sha256。只输出要求的 JSON 对象，不要讲解。

输入商品集合及统一 OUTPUT_SCHEMA 在调用时作为结构化数据注入。务必为每个 item_id 返回唯一记录，保持商品顺序。

## EXPERT_APPENDIX：只给 B
按西班牙零售商品专业翻译规程工作：
1. 每个商品先定位实际主体、变体及原平台类目；不要把研究建议类目冒充原类目。多用途/混合套装不得凭第一项排除其他。
2. 保护品牌、系列、ASIN/SKU、型号和部件号，分清商品制造品牌与“兼容品牌”。
3. 完整保留源文的规格数值、单位、尺寸轴、用途、材质/加工工艺、配件、包装清单；特别区分单件数量、套装件数、商品代际、价格参照数量和“多合一”功能数。
4. 把每条兼容对象、接口方向、协议、限制、适用/不适用条件完整准确表达，不得因为一项不明便丢失整份清单。
5. 长字段中分清商品事实、重复、平台元数据、广告残留；不删除独有功能或安全/安装重要说明。其他语言品牌/型号可原样保护，但正常可译的西班牙语必须中文化。
6. 遇到源文矛盾/截断，只隔离确实受影响的事实槽，不误删附近已确认信息；不能用常识强行纠正源的容量、尺寸或材质。
7. 生成后独立从完整源文逐项回查：是否遗漏重要事实、合成标题与结构字段数值是否互相矛盾、是否虚构内容，保证 issues 和被置 null 的实际中文字段一致。

## C 原生条件
C 的**用户输入必须与 A 的 COMMON_TASK 完全一致**，不拼接 EXPERT_APPENDIX，不额外要求“逐句调用五个Skill”。仅通过隔离工作区按当前 Codex 原生机制提供冻结的 .agents/skills 五入口与 references/、contracts/、approved manifest。由客户端自行发现，Codex 按任务需要读取。真实读取原始日志是计入“Native”组的门槛；发现失败不得全文注入或把 Skill 规则改写进 C 的用户提示词。

## 所有组统一 OUTPUT_SCHEMA（等价结构即可，不能对某臂独有）
- item_id, platform, product_id, source_sha256 （与输入一一对应）
- title_zh: string|null
- translated_source_categories_zh: array|string|null
- specifications_zh: array of {key_zh,value_zh}，按原顺序
- bullets_zh: array of string|null
- description_zh: string|null
- details_zh: array of {key_zh,value_zh}
- protected_identifiers: array of {kind,value,role}
- issues: array of {source_field,source_quote,reason,target_field}

生成任务使用同一外层 JSON envelope {items:[...]}；不在统一 Schema 中强制全部填满与额外 source-audit 内部账本，避免以输出格式抬高任一组对照门槛。QA 从完整原始记录建立事实清单，而不是仅依赖任一组 self-reported issues。
