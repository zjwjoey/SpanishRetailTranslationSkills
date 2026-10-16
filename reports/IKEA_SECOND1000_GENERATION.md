# IKEA第二个1000 SKU生成记录

2026-10-16；规则冻结提交 `b310f69`。本轮已实际生成第二个1000个唯一SKU，10批×100，每批10个分段。与首1000及首轮验证20条重叠为0，来自964个系列。输入按来源大类/系列确定性轮转选择，不根据中文答案筛选；这不是正式隔离Holdout。

生成前修改了Translator、Terminology和Reviewer中的旋钮/拉手、洗碗机自动洗涤/机器维护和倍数总量/增量规则。5条真实失败案例及8条synthetic回归保留了两次尝试和独立审查记录；不明倍率继续隔离，门禁仅为CANDIDATE_PLUS_QUARANTINE。Translator/Reviewer版本为`1.0.4-candidate-ikea02a2`，Terminology为`0.2.2-candidate-ikea02a2`，Category/Learning未改。17项基础检查及5个Skill校验通过。

所有生成执行者请求模型`gpt-5.6-luna`；后端实际型号不可观测，记录unknown。生成期间31个冻结文件保持不变，不逐SKU启动五个Agent。固定紧凑中间件字段类型，未声称通过完整原生输出契约。

## 真实失败与重做

初始整批执行者中，有执行者违反协议，用词面替换词典生成中西文混杂甚至乱码。原先身份/类型检查没有发现该语义性失败。根审查拒收了360条SKU尝试：003/004/005整批及001后六段，保留原输出、程序和拒收依据，撤销其完成状态；这些尝试不计入最终1000。

随后把执行者任务缩小到10/20条，要求直接逐件生成中文JSON，禁止翻译脚本/replace词典/模板。业务批次仍为100条。相同源SKU全部重新生成，没有换成更容易的商品。增加混杂文本机械检查，用三组实际失败输出作负对照，均被拦住；检查通过本身不证明翻译正确。

源hash抄写错误、规格数组和排除原因缺失等机械问题保留原attempt后纠正。源缺失和仅制造商落款的三条排除原因由根按原源补齐，没有改变翻译值。

## 生成交付与当前门禁

- 实际1000，稳定8位SKU、系列及源hash全部匹配；10个FINAL及实际100条载荷均存在并校验hash。
- 原始实际中文汇总SHA256：`27490d6b0eab1d823fdf3268287005f0d8be55d7b91cc8b1361e027d3161a284`。
- 当前生成查看版隔离97个字段槽；包括模型明确列出的排除和uncertainties对应字段，均置null，原候选另存。最终语义审查可能修正隔离范围。
- 源工作簿SHA256仍为`28a76574e836036fb11fe8b6dc0c42b95742f64f0fd28ca102a4b4f59c38eb74`；原工作簿、首1000原始候选、冻结31文件及approved知识未变。
- 全量独立语义审核已在1000生成完成后启动。生成检查不能代替语义核对，此记录不宣称1000全部质量通过。
- 人工确认数0，IKEA可信Training/Validation/Holdout均为0；Learning正式知识准入仍EVIDENCE_BLOCKED，不自动写approved。

本地完整证据位于Git忽略的`local/ikea-run-02/`：`inputs/`完整源及原表行/hash映射、`runs/batch-001..010/`实际输出/元数据/FINAL、`outputs/all-actual-candidates.jsonl`实际1000、`outputs/generation-review-view.jsonl`隔离查看版、`outputs/generation-field-exclusions.jsonl`、`verification/`、`regression/`及`rejected/word-replacement/`。`AUDIT_PROTOCOL.md`限定独立审查范围与source-first步骤；审核结果和根裁定另行保存。

分支`feature/foundation-v1`，仅本地分阶段提交，未推送、未合并main、未发布Release，也未上传完整货盘。
