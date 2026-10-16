# 第三轮预登记比较协议

本文件在本轮生成前登记。A为b751ee8工作树有效版本（第二轮已回退）；B为第三轮Translator与Reviewer候选，其他三个Skill、契约、approved知识不变。第二轮失败补丁不应用。快照和逐文件hash保存在local/tuning-round-03；formal gold=0，Train/Validation/Holdout均0。本轮为共享目录、独立上下文的开发性验证，不是权限隔离盲测。

先对11个暴露回归case测试（7真实case/6唯一ASIN，4合成）；回归失败保留原件与修订。随后冻结候选与同一任务，用12件全新商品（Action6/Amazon6）分别在两个新上下文运行A/B，各给一次同范围自查。选样排除146个既有身份、已知parent家族及近重复标题。未参与生成的QA先只读完整源，冻结事实清单后才读两臂全部结果。源清单不是中文gold。共享目录仅行为限制，模型/设置不可观测写unknown，成本/token/可靠耗时null。

两臂共同任务沿用第二轮紧凑表示（不冒称完整原生输出schema验证），同源、同字段、同执行条件；明确源类目与研究类目，保护标识及关系、逐字段证据、前审动作/账本、局部待核与完整实际中文。生成后冻结FINAL及hash；首次输出和自查修订都保留，不挑最佳结果。后审修改另存，不改变原始统计。

QA从源逐条核对重要声明、对象/属性角色、数值/单位、用途、适用人群、否定/限定/条件、包装层次和完整兼容对象；也检查中文新增主张。引用存在不证明语义覆盖。相同事实跨字段只计一个根因；不同事实分别计数。固定分母为Action6、Amazon6、总12，漏审不得从分母剔除。

每项finding列item_id、arm、issue_key、fact_slot、severity、layer、source_field/quote、target_field/quote、reason、affected_fields、certainty与paired_status。层分semantic P0/P1、false_block P2、mechanical/style P2，互不抵消；UNCERTAIN及UNRESOLVED_DISAGREEMENT单列，不计确定错误或改进。真实源冲突独立记录，保留双方证据并局部隔离；明确兼容源声明与现实适配验证分开。正式事实覆盖率仅在完整原子清单逐项核查时报告，不能拿引用数当分母。

任一未处理P0、关键配置退化、新且未解释P1阻止候选升级，保存失败补丁/回退证据。即使观察P1为0也仅为本次AI审查范围，不证明生产级、V1或人工准确率。无法确认的目标槽排除，保留原始候选和排除理由；不得用排除后结果重算原始A/B分数。正式Learning仍EVIDENCE_BLOCKED/proposed_changes=[]。普通Codex本轮NOT_RUN，上游NOT_COMPARABLE，不冒称三方对比。

原始workbook只读，完整源与逐条中文留ignored local/，仅提交自己编写的规则、协议、汇总及测试证据。仅本地阶段提交，不push、merge或Release。
