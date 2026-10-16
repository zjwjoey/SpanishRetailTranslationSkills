# 合成行为场景

全部 `is_synthetic=true`，为手工构造的机制演练，不是用户历史商品、人工gold、批准词库或盲测。生产ASIN未知时保持null，不编假ASIN。公开例子不携真实货盘位置或快照。

| 场景 | 合成输入片段 | 预期判断与交接 |
| --- | --- | --- |
| 正常/触发 | 清洁用品；`Cepillo para limpiar botellas` | cepillo候选“清洁刷”，用途来自para limpiar botellas；可PASSED，知识依据为语义候选而非批准 |
| 跨类多义 | 美发；`Cepillo para el cabello` | 候选“发刷”，不套用上一清洁刷候选；记录美发用途 |
| 歧义/异常 | 仅`Banco`，类别与用途均缺 | 列出长凳/工作台等备选，REVIEW_REQUIRED，不给确定主体 |
| 未知词 | `Accesorio xylovex` | 保留xylovex原词，不能仅因位置认定品牌；REVIEW_REQUIRED，索取用途或可核查词义 |
| 保护和数量 | `PHILIPS OneBlade 360 QP2734/30; 2 Cuchillas 360; Peine-Guía Ajustable 5 en 1; 60 minutos` | 品牌、系列、型号原串保护；刀片数2、组合5合1、时长60分钟分开，不解释为5件；这只是合成串，不代表真实在售配置 |
| 首词边界 | `Cepillo suave para ropa`，brand未提供 | Cepillo为主体候选，不能删作品牌；未提供品牌保持缺失 |
| 代码冲突 | specifications=`USB-6`，description=`puerto USB-C` | 两串分别保护并保留源位置，REVIEW_REQUIRED，不把6改C；交Reviewer源问题 |
| 失败 | 相同item_id出现不同source_snapshot，无法判明该项输入版本 | FAILED，拒绝复用旧术语；请求确定快照，不从另一商品借值 |
| 非触发 | “删除重复标题并批准整件中文” | 路由Reviewer；术语Skill不能输出整段删除或终审结论 |

独立调用时，最小缺口只阻塞受影响术语；无歧义词与已定位标识仍可输出。整件保留REVIEW_REQUIRED，不因局部候选可读就整体放行。
