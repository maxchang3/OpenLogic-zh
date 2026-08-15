# 《盒子与钻石》翻译规范与术语对照（v4）

本文件是翻译工作流的唯一权威输入：每个翻译 worker 开工前必须通读。术语译法以《模态逻辑教程》（文学锋，主题索引 393–410 页）为准。

格式约定：段落一行一段、列表一项一行（不手动折行），表格与代码块按正常 markdown 结构书写。

## 0. 翻译原则

1. 括号原文是自动的，译者不要手动加：术语表机制（见 §0b）让每个 `!!{token}` 令牌在全书首次出现处自动渲染为"中文（English）"，之后无痕；译者只负责把令牌原样保留。
2. 只翻散文：`\begin{defn}` 等环境、`\ollabel`、`\olref`、`\olimport`、`\olsection`、`\olfileid`、`\tagitem`、`\indcase`、`\iftag` 等全部原样保留。
3. 数学不动：`$...$`、`$$...$$`、`\begin{equation}` 内内容逐字符保留，包括 `!A`、`\Box`、`\mSat{M}{!A}[w]` 等；数学周围的中文标点按中文习惯调整。
4. 令牌不动：`!!{formula}`、`!!a{derivation}`、`!!^a{formula}` 等占位符原样保留，不要手工展开。
5. 裸英文术语必须翻译：正文中直接书写的英文术语（negation、valid、world、branch 等，不在令牌内）按 §2/§2b/§2c 对照表翻译；表中没有的按通行逻辑术语译法，并在交付报告里登记，以便补入对照表。
6. 标点：正文英文标点转中文（逗号、句号、分号），数学/宏参数内保持英文；引号：英文引号对（TeX 源中的 ``...'' 或 "..."）译为「...」，嵌套内层用『...』；`\emph{...}` 照译并保留包裹；`\iftag{...}{\ycomma $\lnot$ (negation)}{}` 这类宏参数内的英文术语照译（如 `$\lnot$（否定）`），`\ycomma` 等控制序列保留。
7. 人名/系统名：Kripke、Leibniz、Brouwer、Dummett、Stalnaker、Lewis、Barcan、Gentzen、Henkin、Lindenbaum、S4、S5、K、T、B、GL 等保留原文，不音译。
8. 章节标题照译；`\usetoken{P}{tableau}` 保持原样（术语表自动输出中文）。
9. 习题 `\begin{prob}` 题干照译。
10. 文件头 `% Part: ...` 等注释保留；`\begin{editorial}` 建议译。
11. 数字、页码、节号、`\olref{...}` 参数、标签名一律不动。
12. 输出只含完整 .tex 内容（含 `\documentclass` 头与 `\end{document}`），不输出解释文字。
13. 英语语言形式保留原文：讨论英语语言形式本身的文字（英语构式、语法例句，如「if \dots then \dots」构式、「if it were the case that \dots then it would be the case that \dots」虚拟式例句）保留英文原文，不翻译（讨论对象就是英语形式本身）；作为内容的例句（如「如果管家做了这件事，那么园丁是无辜的」）照常翻译。
14. 未覆盖术语流程：TERMINOLOGY.md 未覆盖的逻辑/哲学术语，先用 web_search 查证中文通行译法，自行定译并在交付报告中登记（英文→中文）；协调者汇总后交用户确认，确认后补入本表成为唯一权威；未确认前译法为暂定，多 worker 译法冲突时以本表为准。
15. 不折行：译文正文段落一行一段，不手动折行（与英文源文件的行结构无关）。

0b. 括号原文由术语表自动完成（`locale/zh/open-logic-config.sty` 的 `\zhToken[English]{key}{中文}`），目录与书签始终无括号。

0c. 术语依据标注：本表词条来源分三类——（1）文学锋《模态逻辑教程》索引/正文有据（如 表列、可靠性、合式公式、矢列演算、正规模态逻辑、真性）；（2）学界通行译法（如 反事实条件句、球面模型、最小变化语义、空真地、未消去的、项模型、公共知识、主算子、超矢列、群体知识、带符号公式——2026-08-15 经用户确认定案）；（3）worker 登记后补入（见 TRANSLATION-POLICY.md G 节）。operator（逻辑算子，含模态算子）与 connective（命题联结词）是 OLP 中的两个独立概念，分别译「算子」与「联结词」，不统一。

## 1. 令牌术语表（31 个）

| 令牌 | 中文 | 令牌 | 中文 |
|---|---|---|---|
| `!!{formula}` | 公式 | `!!{propositional variable}` | 命题变元 |
| `!!{sentence}` | 语句 | `!!{language}` | 语言 |
| `!!{operator}` | 算子 | `!!{main operator}` | 主算子 |
| `!!{constant}` | 常元 | `!!{predicate}` | 谓词 |
| `!!{function}` | 函数 | `!!{element}` | 元素 |
| `!!{structure}` | 结构 | `!!{domain}` | 论域 |
| `!!{value}` | 值 | `!!{truth}` | 真 |
| `!!{falsity}` | 假 | `!!{conditional}` | 条件句 |
| `!!{biconditional}` | 双条件 | `!!{injective}` | 单射的 |
| `!!{derivation}` | 推演 | `!!{derive}` | 推演出 |
| `!!{derivable}` | 可推演的 | `!!{derivability}` | 可推演性 |
| `!!{nonderivability}` | 不可推演性 | `!!{undischarged}` | 未消去的 |
| `!!{complete}` | 完全的 | `!!{tableau}` | 表列 |
| `!!{relational model}` | 关系模型 | `!!{valuation}` | 赋值 |
| `!!{signed formula}` | 带符号公式 | `!!{denumerable}` | 可数的 |

## 2. 核心概念对照表（散文固定译法）

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| modal logic | 模态逻辑 | normal modal logic | 正规模态逻辑 |
| sound / soundness | 可靠的 / 可靠性 | complete / completeness | 完全的 / 完全性 |
| valid / validity | 有效的 / 有效性 | satisfiable | 可满足的 |
| satisfiability relation | 可满足关系 | satisfaction | 满足 |
| consequence | 后承 | entail | 衍推 |
| accessibility relation | 可及关系 | possible world | 可能世界 |
| frame | 框架 | Kripke frame/model | Kripke 框架/模型 |
| relational semantics | 关系语义 | canonical model | 典范模型 |
| canonical | 典范的 | filtration | 过滤 |
| bisimulation | 双模拟 | maximal consistent | 极大一致的 |
| consistent / inconsistent | 一致的 / 不一致的 | tautology | 重言式 |
| substitution | 代入 | rule of necessitation | 必然化规则 |
| truth lemma | 真值引理 | Lindenbaum lemma | Lindenbaum 引理 |
| theory | 理论 | extension | 扩张 |
| dual | 对偶 | countermodel | 反模型 |
| decidable / undecidable | 可判定的 / 不可判定的 | branch | 支 |
| closed tableau | 闭的表列 | open branch | 开放的支 |
| intuitionistic logic | 直觉主义逻辑 | constructive | 构造性的 |
| counterfactual conditional | 反事实条件句 | strict conditional | 严格条件句 |
| material conditional | 实质条件句 | antecedent / consequent | 前件 / 后件 |
| alethic | 真性的 | epistemic | 认知的 |
| doxastic | 信念的 | deontic | 道义的 |
| temporal | 时态的 | group knowledge | 群体知识 |
| common knowledge | 公共知识 | public announcement | 公开宣告 |
| reflexive | 自反的 | transitive | 传递的 |
| symmetric | 对称的 | Euclidean | 欧性的 |
| serial | 持续的 | irreflexive | 禁自反的 |
| axiom / rule | 公理 / 规则 | derivable rule | 导出规则 |
| soundness theorem | 可靠性定理 | completeness theorem | 完全性定理 |
| decidability | 可判定性 | finite model property | 有穷模型性 |
| frame definability | 框架可定义性 | definable | 可定义的 |
| characteristic | 特征 | schema | 模式 |
| world | 世界 | actual world | 现实世界 |
| truth at a world | 在世界处为真 | true in a model | 在模型中为真 |
| valid on a frame | 在框架上有效 | generalized | 广义的 |
| induction | 归纳 | case | 情形 |
| exercise | 习题 | prove | 证明 |

## 2b. 补充对照表（正文 `\emph` 术语：71 条教材索引命中 + 人工定译）

元理论性质：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| soundness | 可靠性 | completeness | 完全性 |
| unsatisfiable | 不可满足的 | consistent / inconsistent | 一致的 / 不一致的 |
| consistency | 一致性 | axiomatic | 公理化的 |
| deductively closed | 演绎封闭的 | non-constructive | 非构造性的 |
| compactness | 紧致性 | decision procedure | 判定程序 |
| unique readability | 唯一可读性 | formation sequence | 形成序列 |
| inductive definition | 归纳定义 | substitution instance | 代入特例 |
| tautological instance | 重言式特例 | valid / invalid schemas | 有效 / 无效模式 |

模态逻辑概念：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| modal propositions | 模态命题 | modal-free | 无模态的 |
| modally closed | 模态封闭的 | modal system | 模态系统 |
| necessarily / necessarily true | 必然地 / 必然真 | iterated | 叠置的（叠加模态） |
| tense logic | 时态逻辑 | epistemic possibility | 认知可能性 |
| knowledge and belief | 知识与信念 | epistemic propositions | 认知命题 |
| necessitation (rule) | 必然化（规则） | rule of inference | 推理规则 |
| modus ponens | 分离规则（肯定前件） | prefixed tableau | 带前缀的表列 |
| prefixes | 前缀 | hypersequent | 超矢列 |
| term model | 项模型 | standard translation | 标准翻译 |
| modal degree | 模态度 | truth-functional | 真值函项的 |

条件句：

| 英文 | 中文 |
|---|---|
| counterfactual conditionals | 反事实条件句 |
| subjunctive conditionals | 虚拟条件句 |
| indicative (conditionals) | 直陈的（直陈条件句） |
| material conditional | 实质条件句 |
| strict conditional | 严格条件句 |
| sphere model / system of spheres | 球面模型 / 球面系统 |
| centered / nested / innermost | 中心的 / 嵌套的 / 最内层的 |

关系与框架性质：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| relational structures | 关系结构 | transitive closure | 传递闭包 |
| reflexive transitive closure | 自反传递闭包 | reflexive closure | 自反闭包 |
| equivalence relation / class | 等价关系 / 等价类 | quotient | 商集 |
| partial order | 偏序 | preorder | 预序 |
| total order / linear order | 全序 / 线性序 | strict order | 严格序 |
| strict total order | 严格全序 | order relation | 序关系 |
| well-ordered | 良序的 | least element | 最小元 |
| initial segment | 初始段 | successor / predecessor | 后继点 / 前驱点 |
| weakly dense | 弱稠密的 | weakly connected | 弱连通的 |
| weakly directed | 弱有向的 | partially functional | 部分函数的 |
| universal relation | 全域关系 | empty relation | 空关系 |
| identity relation | 恒等关系 | inverse | 逆关系 |
| relative product | 相对积 | binary relation | 二元关系 |
| ordered pair | 有序对 | cartesian product | 卡氏积 |
| power set | 幂集 | disjoint | 不相交的 |
| set difference | 差集 | comprehension | 概括（原则） |
| non-self-membered | 非自属的 | | |

图与树：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| directed graph | 有向图 | graph | 图 |
| vertices / edges | 顶点 / 边 | tree | 树 |
| root | 根 | children / parent | 子节点 / 父节点 |
| subtree | 子树 | ancestor | 祖先 |
| finitely branching | 有穷分支的 | infinite binary tree | 无穷二叉树 |

直觉主义与拓扑：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| topological space | 拓扑空间 | open sets | 开集 |
| topological model | 拓扑模型 | interior | 内部 |
| prime (formula) | 素的 | constructive reasoning | 构造性推理 |
| BHK interpretation | BHK 解释 | | |

时态/认知：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| possible histories model | 可能历史模型 | linear (time) | 线性的 |
| dense (time) | 稠密的 | unbounded (past/future) | 无界的（过去/未来） |
| precedes | 先于 | updates / events | 更新 / 事件 |

其他：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| vacuously | 空真地 | closed under subformulas | 对子公式封闭 |
| balanced | 平衡的 | assumptions | 假设 |
| in parallel | 并行地 | finest / coarsest | 最细的 / 最粗的 |
| partitions | 划分 | first / second-order definable | 一阶 / 二阶可定义的 |
| symbolic logic | 符号逻辑 | state description | 状态描述 |
| word / finite strings | 词 / 有穷字符串 | principia mathematica | 《数学原理》（保留原文） |
| begriffsschrift | 《概念文字》（保留原文） | meaning and necessity | 《意义与必然性》（保留原文） |
| de interpretatione | 《解释篇》（保留原文） | | |

## 2c. 高频裸词对照表（正文中直接书写、不在令牌内的英文术语；翻译时必须翻译）

逻辑联结词与公式结构：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| negation | 否定 | disjunction | 析取 |
| propositional connectives | 命题联结词 | operator（令牌） | 算子 |
| main operator（令牌） | 主算子 | | |
| conjunction | 合取 | implication | 蕴含 |
| connective | 联结词 | logical connective | 逻辑联结词 |
| subformula | 子公式 | instance | 特例 |
| schema | 模式 | truth table | 真值表 |
| truth value | 真值 | formation sequence | 形成序列 |

元理论：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| valid | 有效的 | validity | 有效性 |
| invalid | 无效的 | satisfiable | 可满足的 |
| unsatisfiable | 不可满足的 | satisfaction | 满足 |
| sound | 可靠的 | soundness | 可靠性 |
| complete | 完全的 | completeness | 完全性 |
| consistent | 一致的 | inconsistent | 不一致的 |
| consistency | 一致性 | entail / entailment | 衍推 |
| consequence | 后承 | decidable | 可判定的 |
| undecidable | 不可判定的 | decidability | 可判定性 |
| compactness | 紧致性 | deduction | 演绎 |
| deduction theorem | 演绎定理 | deductive | 演绎的 |
| provable | 可证明的 | provability | 可证明性 |
| proof / prove | 证明 | counterexample | 反例 |
| countermodel | 反模型 | purported counterexample | 所谓反例 |

证明系统：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| rule | 规则 | rules of inference | 推理规则 |
| rule of necessitation | 必然化规则 | axiom | 公理 |
| axiomatic system | 公理系统 | modus ponens | 分离规则 |
| hypothesis | 假设 | induction hypothesis | 归纳假设 |
| assumption | 假设 | premise | 前提 |
| conclusion | 结论 | | |

模态：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| modal | 模态的 | modality | 模态 |
| modal logic | 模态逻辑 | normal modal logic | 正规模态逻辑 |
| regular | 正则的 | necessity | 必然性 |
| possibility | 可能性 | necessary | 必然的 |
| possible | 可能的 | necessarily true | 必然真 |
| possible world | 可能世界 | world | 世界 |
| frame | 框架 | model | 模型 |
| relational | 关系的 | canonical | 典范的 |
| canonical model | 典范模型 | filtration | 过滤 |
| bisimulation | 双模拟 | dual | 对偶 |
| characteristic | 特征的 | iterated | 叠置的 |
| modal degree | 模态度 | Kripke frame | Kripke 框架 |

语义与语言：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| semantics | 语义 | semantic | 语义的 |
| syntax | 句法 | syntactic | 句法的 |
| interpretation | 解释 | assignment | 指派 |
| object language | 对象语言 | meta-language | 元语言 |

集合与关系：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| set | 集合 | subset | 子集 |
| proper subset | 真子集 | union | 并 |
| intersection | 交 | set difference | 差集 |
| relation | 关系 | binary relation | 二元关系 |
| equivalence relation | 等价关系 | equivalence class | 等价类 |
| transitive closure | 传递闭包 | reflexive | 自反的 |
| transitive | 传递的 | symmetric | 对称的 |
| antisymmetric | 反对称的 | asymmetric | 禁对称的 |
| irreflexive | 禁自反的 | Euclidean | 欧性的 |
| serial | 持续的 | partial order | 偏序 |
| total order | 全序 | preorder | 预序 |
| well-ordered | 良序的 | linear | 线性的 |
| dense | 稠密的 | tree | 树 |
| graph | 图 | directed graph | 有向图 |
| vertex | 顶点 | edge | 边 |
| branch | 支 | root | 根 |
| subtree | 子树 | ancestor | 祖先 |
| child | 子节点 | parent | 父节点 |
| finitely branching | 有穷分支的 | infinite binary tree | 无穷二叉树 |
| finite | 有穷的 | infinite | 无穷的 |
| countable | 可数的 | uncountable | 不可数的 |
| ordered pair | 有序对 | cartesian product | 卡氏积 |
| power set | 幂集 | disjoint | 不相交的 |
| comprehension | 概括 | quotient | 商集 |
| successor | 后继 | predecessor | 前驱 |
| least element | 最小元 | initial segment | 初始段 |
| injective | 单射的 | surjective | 满射的 |
| bijection | 双射 | partial function | 部分函数 |
| codomain | 目标域 | identity | 同一性 |
| equality | 相等 | | |

条件句：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| counterfactual | 反事实的 | counterfactual conditional | 反事实条件句 |
| subjunctive | 虚拟的 | indicative | 直陈的 |
| material | 实质的 | strict | 严格的 |
| antecedent | 前件 | consequent | 后件 |
| sphere model | 球面模型 | system of spheres | 球面系统 |
| centered | 中心的 | nested | 嵌套的 |
| innermost | 最内层的 | vacuously | 空真地 |
| admitting sphere | 容纳球面（$p$-容纳球面：包含使 $p$ 为真之世界的球面） | closest worlds | 最接近的世界 |
| strata | 分层 | opposite（图题） | 颠倒式 |
| agglomeration / agglomerates | 聚合 | antecedent strengthening | 前件强化 |
| contrapositive | 逆否命题 | chain rule | 链规则 |
| contingent | 偶然的 | monotonic | 单调的 |
| symbolize | 符号化 | capture | 刻画 |

应用模态：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| public announcement | 公开宣告 | group knowledge | 群体知识 |
| common knowledge | 公共知识 | knowledge | 知识 |
| agent | 主体（教材：认知主体） | multi-agent / single-agent | 多主体 / 单主体 |
| epistemic logic | 认知逻辑（教材：认知（epistemic）用法） | dynamic epistemic logic | 动态认知逻辑 |
| informational state | 信息状态 | announcement operator | 宣告算子 |
| box operator | 盒子算子（呼应书名） | Veridicality | 真实性 |
| Positive / Negative Introspection | 正内省 / 负内省 | KK principle | KK 原则 |
| correspondence theory | 对应理论 | computational path | 计算路径 |
| future contingent | 未来偶然命题 | open future | 开放的未来 |
| determinist | 决定论者 | validities | 有效式 |
| since / until（时态算子读法） | 自从 / 直到 | excluded middle | 排中律 |
| node / arrow（图示） | 节点 / 箭头 | renaming | 重命名 |
| modal model | 模态模型 | meta-linguistic expression | 元语言表达式 |
| Symbolic Logic（书名） | 《符号逻辑》 | | |
| belief | 信念 | epistemic possibility | 认知可能性 |
| update | 更新 | event | 事件 |
| possible histories | 可能历史 | linear time | 线性时间 |
| dense time | 稠密时间 | unbounded | 无界的 |
| precedes | 先于 | | |

表列：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| closed | 闭的 | open | 开的 |
| closure | 闭合 | prefix | 前缀 |
| labelled | 加标的 | prefixed | 带前缀的 |

杂项：

| 英文 | 中文 | 英文 | 中文 |
|---|---|---|---|
| definition | 定义 | example | 例 |
| exercise | 习题 | theorem | 定理 |
| lemma | 引理 | proposition | 命题 |
| corollary | 推论 | intuitionistic | 直觉主义的 |
| constructive | 构造性的 | variable | 变元 |
| constant | 常元 | predicate | 谓词 |
| operator | 算子 | function | 函数 |

## 3. 句式处理

- iff → 当且仅当
- i.e. → 即；e.g. → 例如；viz. → 亦即
- Note that ... → 注意，……；Recall that ... → 回顾，……
- Suppose ... → 设……；Then ... → 则……；Hence / Thus → 因此 / 于是
- It is easy to see that ... → 容易看出，……
- The following proposition ... → 如下命题……
- 定义中的 iff 句型：`!A ∈ Γ 当且仅当 ...`
