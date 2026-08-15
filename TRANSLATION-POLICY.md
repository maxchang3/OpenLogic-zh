# 翻译定性清单（Translation Policy）

本文件是全部翻译决策的登记处：✅ 已定 · ❓ 待定（附建议值，建议以《模态逻辑教程》文学锋为准）。与 TERMINOLOGY.md（术语对照）配套：TERMINOLOGY 管"怎么译"，本文件管"译不译/叫什么/什么风格"。不手动折行。

## A. 专名与机构（保留原文）

- ✅ Open Logic Project（OLP）保留英文，不译——用户定案。
- ✅ Open Logic Text → 《开放逻辑读本》（OLT）。
- ✅ 人名全部保留原文：Kripke、Leibniz、Brouwer、Dummett、Stalnaker、Lewis、Barcan、Gentzen、Henkin、Lindenbaum、Carnap、Prior、Heyting、Antonelli 等；不音译。
- ✅ 逻辑系统名保留：K、T、B、D、S4、S5、GL、K4、KB、K45 等。
- ❓ 机构名（University of Calgary、Taylor Institute of Teaching and Learning、ABOER Initiative、Alberta government）：建议保留英文（版权页致谢中出现）。
- ✅ 引书书名用通行中文译名并保留原名：Principia Mathematica《数学原理》、Begriffsschrift《概念文字》、Meaning and Necessity《意义与必然性》、De Interpretatione《解释篇》。
- ✅ BHK interpretation → BHK 解释；Kripke semantics → Kripke 语义（Kripke 保留）。

## B. 书名与封面

- ✅ 主书名：《盒子与钻石》（用户定案；与 □（box=盒子）、◇（diamond=钻石）字面呼应）。
- ❓ 副标题 An Open Introduction to Modal Logic → 建议《模态逻辑导论》。
- ✅ 封面书名呈现：纯中文——书名"盒子与钻石"、副标"模态逻辑导论"（用户 2026-08-15 定案：不要双语；双语版曾由 minimax-m3 视觉评审调整比例/行距/颜色后废弃）；肖像组图保留。全书（版权页/扉页）用中文。
- ❓ 作者名 Richard Zach：建议保留原文（数学书惯例）。
- ❓ 版本号 Fall 2025 → 建议"2025 年秋季版"；修订信息（revision hash）保留。
- ❓ 前言/导论标题：Preface → 前言、Introduction → 导论（建议）。

## C. 模态类型（正文出现的五类，建议值均出自教材）

- ✅ alethic → 真性（教材正文 7 次"真性"；通行另有"真势"，不采用）。
- ✅ epistemic → 认知的（认知模态）。
- ✅ doxastic → 信念的（信念模态）。
- ✅ deontic → 道义的（道义模态）。
- ✅ temporal → 时态的（时态模态）；tense logic → 时态逻辑。
- ✅ modality / modalities → 模态（文学锋教材调研 2026-08-15：理论层"模态"——道义模态 deontic modality、典型模态 stereotypical modality、叠加模态 iterated modality；□◇ 算子 → "模态算子"——差异模态算子 difference modality；"模态词"专指自然语言副词：必然/可能/知道/相信（真性/时间/道义/认知模态词）。旧记录"教材 107 次用模态词指 □◇ 算子"有误，已更正。innermost modality → 最内层的模态算子（对齐教材 5066 行"所有叠加模态算子都可归约为最内层的模态算子"）；iterated modality → 叠加模态（教材定义 5.1.10）。
- ❓ 形容词 metaphysical / logical / physical（模态分类）→ 建议"形而上学的 / 逻辑的 / 物理的"。

## D. 术语与风格（已定见 TERMINOLOGY.md；此处列关键拍板项）

- ✅ soundness → 可靠性（教材 93 次；不用"健全性"）。
- ✅ well-formed formula → 合式公式（教材 4 次；不用"良构公式"）。
- ✅ natural deduction → 自然演绎（教材）。
- ✅ sequent calculus → 矢列演算（教材 6 次"矢列"；不用"相继式演算"）。
- ✅ tautology → 重言式；iff → 当且仅当。
- ✅ metavariable → 元变元；meta-language → 元语言；object language → 对象语言。
- ✅ propositional variable → 命题变元；individual constant → 个体常元。
- ✅ "the box" / "the diamond"（□◇ 的读法）→ 建议"盒子"与"钻石"（与书名呼应；待正文首次出现处确认）。
- ✅ "system K" 等 → 教材惯例"K 系统"（K 在前，8 处；"S4 和 S5 系统中的规则"；强调公理化时"公理系统 K"），全书无"系统 K"。B&D 译文保持裸 K（与教材混合用法一致），语境需要时用"K 系统"。
- ✅ 定理环境名：定理/引理/命题/推论/习题/例/注/公理/约定（已实现于 locale）。
- ✅ 数学 \text{...} 内的英文要译（葡语先例：\text{ and } → \text{ 且 }）。
- ✅ syntactic → 句法（文学锋教材调研：30 次"句法"全为逻辑学 syntactic——句法后承/句法证明/句法版本；6 次"语法"全为 grammar 语境——自然语言/程序设计语言语法。译文 16 处已改；grammar 语境"语法"保留）。
- ✅ uniform substitution → 统一代入（教材"US 称为（统一）代入规则"；不用"同一代入/一致代入"）。
- ✅ iterated substitution → 迭代代入（通行译法，教材无此术语）。

## E. 句法与风格（待定，建议值）

- ❓ "we show / we prove / we define" → 建议：数学书中文惯例用无主句（"下面证明……""由归纳法可得"），"we" 多数省略；需要语气处保留"我们"。
- ❓ 英文被动句 → 建议优先转为中文主动/无主句，避免"被"字滥用。
- ✅ 标点：正文中文标点；数学与宏参数内英文标点（已定）。
- ✅ 引号：中文引号「」或""——建议用""（与教材一致；待确认）。
- ❓ 破折号/插入语：英文 "--" 或 "---" → 中文破折号"——"（建议）。

## F. 排版（待定）

- ❓ 中文字体：当前 fontset=fandol（跨平台）；最终可换 macOS 系统字体（宋体/黑体）或思源宋体。
- ✅ 公式、表列（oltableau）、tikz 图全部保留原样。
- ✅ 封面肖像图保留（OpenLogicProject/portraits，CC-BY-NC）。
- ❓ 版权页致谢/许可文字：建议全文翻译（机构名保留英文），CC-BY 4.0 许可名用官方中文译名"知识共享署名 4.0 国际许可协议"。

## Fb. 术语定案记录（2026-08-15）
- ✅ 反事实条件句、球面模型/球面系统、最小变化语义、空真地、未消去的、演绎封闭的、唯一可读性、弱稠密/弱连通/弱有向的、项模型、公共知识、逆否命题 等学界通行译法定案（用户确认）。
- ✅ main operator 主算子（用户确认；operator 算子、connective 联结词为 OLP 两个独立概念，不统一）。
- ✅ hypersequent 超矢列、group knowledge 群体知识、signed formula 带符号公式（按建议定案，可改）。
- ✅ agent → 主体（认知逻辑语境 = 认知主体，知识/信念的持有者；**不是 AI 领域的「智能体」**；用户确认；教材依据「每个认知主体 a」「多主体的知识逻辑」）。multi-agent → 多主体、single-agent → 单主体、认知主体同此。

## G. 不翻译清单（明确保留英文的位置）

- ✅ 英语语言形式（构式名、语法例句，如 if...then 构式、if it were the case that...）保留英文原文；内容性例句照常翻译（用户确认）。
- ✅ 未覆盖术语流程：worker 先 web_search 查证通行译法 → 定译并在交付报告登记（暂定）→ 用户确认后补入 TERMINOLOGY.md 成为唯一权威（用户确认）。


- Open Logic Project、Open Logic Text 链接、github 链接、DOI。
- 逻辑系统名、公理模式名（K、T、S4...；Dual 等环境内名）。
- 文献引用（作者-年份，如 Kripke 1963）。
- 人名及带人名的术语（Kripke 框架、Lindenbaum 引理、Barcan 公式）。
- 代码/命令层面：\olref 标签、\ollabel、文件路径、% 注释中的文件名。

## 待定项速览（请逐条拍板）

1. 副标题：《模态逻辑导论》？
2. ✅ 封面：纯中文（盒子与钻石 / 模态逻辑导论）。已定案。
3. 作者名：保留 Richard Zach？
4. 版本号：2025 年秋季版？
5. ✅ modality：模态（理论层）/ 模态算子（□◇ 算子语境）/ 模态词（自然语言副词）。已定案。
6. ✅ 系统名：教材惯例"K 系统"（K 在前）；译文保持裸 K。已定案。
7. 句式：无主句（建议）还是保留"我们"？

9. 中文字体：fandol（当前）还是系统字体？
10. 机构名保留英文？（建议保留）
