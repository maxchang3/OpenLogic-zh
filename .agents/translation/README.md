# OpenLogic-Zh 翻译规范入口

本目录是 OpenLogic-Zh 翻译工作的规范入口；它只约束本仓库中的英文正文与 `locale/zh/` 译文，不约束下游组装器的封面、版本信息或发行流程。

每次翻译或审校先读本文件、`POLICY.md` 和 `terminology/terms.json`。`terms.json` 是术语的单一数据源（只含可翻译词条），条目带 `module` 字段（`core` 为跨模块通用、`modal-logic` 为模态逻辑模块包）；查词示例：`jq -r '.terms[] | select(.en=="bisimulation") | .zh' terminology/terms.json`，按模块过滤加 `.module=="modal-logic"`。**`!!{...}` 令牌是 TeX 接口键（对照见 `terminology/tokens.json`），翻译时必须原样保留，严禁替换为中文**。其他模块暂时只加载核心术语，确有新领域术语时再增加 `module` 值。

规范的优先顺序是：用户已经确认的决定，其次是 `POLICY.md` 中的共同不变量与决策记录，再次是 `terminology/terms.json`；`pending.md` 只记录尚未定案的候选译法，不得作为规范引用。

`locale/zh/open-logic-config.sty` 中的 token 映射必须与 `terminology/tokens.json` 保持一致；`terms.json` 是可翻译词条的数据源，二者职责不同。若实现与对应数据冲突，应报告并同步修正，不应在 worker 中自行创造隐式覆盖。术语条目之间没有默认覆盖关系，语境不同的同形英文词必须在条目中明确语境（`note` 字段）。

`references/` 记录术语来源和适用范围；文学锋《模态逻辑导论》是模态逻辑术语的重要参考，不是整个 OpenLogic-Zh 的唯一来源或自动覆盖规则。

翻译执行细节见 `WORKFLOW.md`；改动 TeX 或 locale 机制前先读 `../notes/tex-traps.md`。未决术语按 `pending.md` 流程登记，确认后移入 `terms.json` 并从 pending 删除。文学锋《模态逻辑导论》的完整中英索引见 `references/wenxuefeng-index.json`（jq 可查，如 `jq -r '.entries[] | select(.zh|contains("良基"))' references/wenxuefeng-index.json`）。
