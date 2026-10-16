# 数据集与核验 1.0.0-foundation

本机原始Action/Amazon可访问，不标DATA_BLOCKED；可信人工答案为0，标HUMAN_VERIFICATION_BLOCKED；正式train/validation/holdout各0。
已有候选72条来自先前真实审计，但未经人工确认且已暴露给开发者；其group_id和dataset_split尚未完成正式划分。不把它们自动升级或凑齐600条。
每条保留完整源、历史中文、候选修改、差异与风险、两侧文件hash/sheet/行/字段、核验人和时间、已核验字段。schema见schemas。人工核验清单仅保存在local，不能上传完整原始货盘。
先连接稳定SKU/ASIN、父子变体、同SKU跨快照、跨平台同款和近重复组，核验冲突后按组约60/20/20分train/validation/holdout。版本改变不能借用旧中文真值；分组不明保持unassigned。
同一共享本机没有答案权限隔离，指令、隐藏目录、worktree不构成盲测。普通保留集与真正盲测须明确区分；已暴露样本不能冒称未见盲测。真实Holdout需独立访问控制保管，本轮无证据则BLOCKED。
人工确认部分字段只能用于这些字段，不能当整件商品答案。没有可靠标准答案时不计算正式质量正确率，不发布稳定V1。
