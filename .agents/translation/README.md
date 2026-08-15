# OpenLogic-Zh 翻译规范入口

本目录是 OpenLogic-Zh 翻译工作的规范入口；它只约束本仓库中的英文正文与 `locale/zh/` 译文，不约束下游组装器的封面、版本信息或发行流程。

每次翻译或审校先读本文件、`POLICY.md` 和 `terminology/core.md`，再按当前文件所属主题读取相应术语包；模态逻辑、反事实、时态逻辑和认知逻辑使用 `terminology/modal-logic.md`，其他模块暂时只加载核心术语，确有新领域术语时再建立有内容的模块包。

规范的优先顺序是：用户已经确认的决定，其次是 `POLICY.md` 中的共同不变量与决策记录，再次是 `terminology/core.md` 和当前模块术语包；`pending.md` 只记录尚未定案的候选译法，不得作为规范引用。

`locale/zh/open-logic-config.sty` 是可执行的术语映射，必须与核心术语和模块术语包保持一致；若实现与文档冲突，应报告并同步修正，不应在 worker 中自行创造隐式覆盖。术语包之间没有默认覆盖关系，语境不同的同形英文词必须在条目中明确语境。

`references/` 记录术语来源和适用范围；文学锋《模态逻辑教程》是模态逻辑术语的重要参考，不是整个 OpenLogic-Zh 的唯一来源或自动覆盖规则。

翻译执行细节见 `WORKFLOW.md`；改动 TeX 或 locale 机制前先读 `../notes/tex-traps.md`。未决术语按 `pending.md` 流程登记，确认后移入对应术语包并从 pending 删除。
