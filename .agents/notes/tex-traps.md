# OpenLogic-Zh TeX 排雷记录

本文件只记录 OpenLogic-Zh locale 与译文文件的长期约束；B&D 的封面、构建产物和 release 问题归下游仓库。

- TeX Live 2026 的 babel caption 宏进入 `hyperref` URL 时可能触发递归；`open-logic-locale.sty` 在 `\AtBeginDocument` 中覆盖进入 `\href` 的名称宏，而且必须在 `\selectlanguage` 之后执行。
- cleveref 不识别本 fork 的 `chinese` 选项；语言名称和交叉引用格式由 locale 的 `\Crefname`/`\crefformat` 显式设置。
- 首次出现括号原文的标记必须使用可保护的宏、全局 `\csname` 标记和目录/书签开关；不能把 `\ifcsname` 当作有副作用的初始化机制，也不能让 `\write` 展开出 `\def\relax`。
- 书签环境不支持正文中的首次检测逻辑；在 `\pdfstringdefDisableCommands` 中让 token 只展开为中文，避免书签显示英文键名或消耗正文首次标记。
- 中文令牌不区分英语冠词形态；`!!a{token}`、`!!^a{token}` 的输出不能保留原英文实现中的 tie 空格，否则会在 CJK 与令牌之间产生多余空隙。
- 令牌键必须保持英文原样，不能把 `!!{formula}` 等键翻译成中文或在令牌后手工保留英文复数 `s`。
- 数学宏必须留在数学模式内；`\text{...}` 中的普通文字可按 POLICY 翻译，但不能移动变量、关系符号或数学命令。
- `\iftag{FOL}` 等门控内容是否出现由上游 tag 配置决定；缺少某段输出不应直接判断为翻译遗漏。

## 上游原文疑点（zh 照搬，不主动修改；如需修正须在 diff 中注明偏离）

- `nml/tableaux/soundness.tex`（EN 31 / zh 25）：逆否命题证明写 `but $\mSat{M}{!A}[w]$`，缺否定，应为 $\mSat/{M}{!A}[w]$。PDF 可见。
- `nml/completeness/complete-consistent-sets.tex`（EN 84 / zh 55）：「而若 $!A \notin \Gamma$，则因 $\Gamma$ 是完全 $\Sigma$-一致的，故 $!A \in \Gamma$」自相矛盾，应为 $\lnot!A \in \Gamma$。PDF 可见。
- 同文件（EN 122 / zh 65）：prvIff 逆否「反之，设 $!A \lif !B \notin \Gamma$」应为 $\liff$；被 `\tagfalse{prvIff}` 门控，PDF 不可见。
- `nml/tableaux/completeness.tex`（EN 80 / zh 63）：命题称「每条分支都是完成的」，证明末句却写「每条分支都是闭的」，应为「完成的」。PDF 可见。
- `counterfactuals/minimal-change-semantics/transitivity.tex`（EN 60 / zh 36）：`$\mSat/{M}{q \lif r}$ is true at all worlds in it` 记号与真值矛盾（$q \lif r$ 在 $S'$ 的所有世界为真，应为 $\mSat{M}$）；zh 照搬（译文中删除了译员添加的冗余括注「即 $q \lif r$」，其余与上游一致）。
- `intuitionistic-logic/tableaux/soundness.tex`（EN 22-23 / zh 20）：`$\mSat{M}{!A}[w]$` 缺否定，应为 $\mSat/{M}{!A}[w]$（反模型要求 !A 在 w 不成立）。
- `normal-modal-logic/filtrations/introduction.tex`（EN 13）：句子末尾缺右括号（`2^{n^2}。`）。

## 术语易混点（2026 审计批次）

- `anti-symmetric`＝反对称的（偏序用），`asymmetric`＝禁对称的（严格序用）；两者不可互换。
- `functional`＝函数的（从每个世界恰好一个可及），`partially functional`＝部分函数的（至多一个）；functional 蕴含 serial。
- `p-admitting sphere`＝$p$-容纳球面（不要写成「容许/允许/可容纳 $p$ 的球面」）。
- 中文术语后不要手工补英文括注（首次出现由 token 机制自动呈现原文）。
- 人名勿张冠李戴：C.~I. Lewis（严格条件句、实质条件句批评者）≠ David K. Lewis（反事实条件句、最小变化语义）；`check-name-refs.py` 会校验。

- 术语定案/改名后必须立即同步全部译文：曾发生定案「逆良基的/全称量化/原子公式/逆否律」后，`first-order-definability.tex` 仍残留 5 处「反良基」、「bhk-interpretation.tex」仍用「原子命题」；定案即 grep 全文替换。
- 修复/审计类 LLM worker 会把普通词加成 `!!{token}`、把 token 改回普通词或改键（6 文件案例）；任何批量修改后跑 `scripts/check-tokens.py` 兜底，比对 EN/ZH 的 token 序列定位（勿信行号）。
