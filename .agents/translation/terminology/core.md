# OpenLogic-Zh 核心术语

本表收录跨模块通用的逻辑、数学与证明术语，以及目前已经定案但尚不足以单建模块包的非模态术语；它不包含模态逻辑专用词。令牌键是 TeX 接口的一部分，必须按原文保留；普通散文术语按语境和下表统一。某一非模态领域的术语增长到需要独立加载时，再从本表迁入有实际内容的模块包。

## 可执行令牌对照

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
| `!!{complete}` | 完全 | `!!{tableau}` | 表列 |
| `!!{relational model}` | 关系模型 | `!!{valuation}` | 赋值 |
| `!!{signed formula}` | 带符号公式 | `!!{denumerable}` | 可数的 |

`!!{complete}` 的可执行映射刻意使用「完全」：源文中的 `!!{complete}的` 组合为「完全的」，避免 token 自带「的」后重复渲染。

## 句法、公式和语义

| English | 中文 | English | 中文 |
|---|---|---|---|
| syntax / syntactic | 句法 / 句法的 | semantics / semantic | 语义 / 语义的 |
| formula / sentence | 公式 / 语句 | language | 语言 |
| propositional variable | 命题变元 | variable | 变元 |
| constant / individual constant | 常元 / 个体常元 | predicate / predicate symbol | 谓词 / 谓词符号 |
| function / function symbol | 函数 / 函数符号 | operator / propositional operator | 算子 / 命题算子 |
| main operator | 主算子 | connective / logical connective | 联结词 / 逻辑联结词 |
| negation | 否定 | conjunction | 合取 |
| disjunction | 析取 | implication | 蕴含 |
| subformula | 子公式 | schema | 模式 |
| instance / substitution instance | 特例 / 代入特例 | truth table | 真值表 |
| truth value | 真值 | formation sequence | 形成序列 |
| unique readability | 唯一可读性 | inductive definition | 归纳定义 |
| interpretation | 解释 | assignment | 指派 |
| object language | 对象语言 | meta-language | 元语言 |
| meta-linguistic expression | 元语言表达式 | standard translation | 标准翻译 |
| well-formed formula | 合式公式 | metavariable | 元变元 |
| uniform substitution | 统一代入 | iterated substitution | 迭代代入 |

## 模型、真值和元理论

| English | 中文 | English | 中文 |
|---|---|---|---|
| model | 模型 | structure | 结构 |
| domain | 论域 | element | 元素 |
| value | 值 | truth / falsity | 真 / 假 |
| valuation | 赋值 | satisfaction | 满足 |
| satisfiable / unsatisfiable | 可满足的 / 不可满足的 | satisfiability relation | 可满足关系 |
| valid / validity | 有效的 / 有效性 | invalid | 无效的 |
| consequence | 后承 | entail / entailment | 衍推 |
| sound / soundness | 可靠的 / 可靠性 | complete / completeness | 完全的 / 完全性 |
| consistency / consistent | 一致性 / 一致的 | inconsistent | 不一致的 |
| tautology | 重言式 | counterexample | 反例 |
| countermodel | 反模型 | truth lemma | 真值引理 |
| compactness | 紧致性 | finite model property | 有穷模型性 |
| decision procedure | 判定程序 | decidable / decidability | 可判定的 / 可判定性 |
| undecidable | 不可判定的 | deductively closed | 演绎封闭的 |
| non-constructive | 非构造性的 | axiomatic | 公理化的 |
| characteristic | 特征的 | definable | 可定义的 |
| generalized | 广义的 | | |

## 证明系统和推理

| English | 中文 | English | 中文 |
|---|---|---|---|
| derivation / derive | 推演 / 推演出 | derivable / derivability | 可推演的 / 可推演性 |
| non-derivability | 不可推演性 | proof / prove | 证明 |
| provable / provability | 可证明的 / 可证明性 | rule | 规则 |
| rule of inference / rules of inference | 推理规则 | axiom | 公理 |
| axiomatic system | 公理系统 | derivable rule | 导出规则 |
| hypothesis / assumption | 假设 | premise | 前提 |
| conclusion | 结论 | induction / induction hypothesis | 归纳 / 归纳假设 |
| case | 情形 | deduction | 演绎 |
| deduction theorem | 演绎定理 | natural deduction | 自然演绎 |
| sequent calculus | 矢列演算 | tableau | 表列 |
| closed tableau | 闭的表列 | open branch | 开放的支 |
| branch | 支 | closure | 闭合 |
| modus ponens | 分离规则（肯定前件） | rule of necessitation | 必然化规则 |
| substitution | 代入 | uniform substitution | 统一代入 |
| tautological instance | 重言式特例 | valid / invalid schema | 有效 / 无效模式 |
| undischarged | 未消去的 | complete | 完全 |

## 集合、关系、函数和图

| English | 中文 | English | 中文 |
|---|---|---|---|
| set | 集合 | subset / proper subset | 子集 / 真子集 |
| union / intersection | 并 / 交 | set difference / relative difference | 差集 / 相对差集 |
| relation / binary relation | 关系 / 二元关系 | equivalence relation / class | 等价关系 / 等价类 |
| identity relation | 恒等关系 | inverse | 逆关系 |
| transitive closure | 传递闭包 | reflexive closure | 自反闭包 |
| reflexive transitive closure | 自反传递闭包 | | |
| quotient | 商集 | comprehension | 概括（原则） |
| ordered pair | 有序对 | cartesian product | 卡氏积 |
| power set | 幂集 | disjoint | 不相交的 |
| partial order | 偏序 | preorder | 预序 |
| total order / linear order | 全序 / 线性序 | strict order | 严格序 |
| strict total order | 严格全序 | order relation | 序关系 |
| well-ordered | 良序的 | least element | 最小元 |
| initial segment | 初始段 | successor / predecessor | 后继点 / 前驱点 |
| weakly dense | 弱稠密的 | weakly connected | 弱连通的 |
| weakly directed | 弱有向的 | partially functional | 部分函数的 |
| universal relation | 全域关系 | empty relation | 空关系 |
| non-self-membered | 非自属的 | connected | 连通的 |
| function | 函数 | injective / surjective / bijection | 单射的 / 满射的 / 双射 |
| partial function | 部分函数 | domain / codomain | 定义域 / 目标域 |
| identity / equality | 同一性 / 相等 | | |
| directed graph / graph | 有向图 / 图 | vertices / edges | 顶点 / 边 |
| tree | 树 | root | 根 |
| children / parent | 子节点 / 父节点 | subtree | 子树 |
| ancestor | 祖先 | finitely branching | 有穷分支的 |
| infinite binary tree | 无穷二叉树 | finite / infinite | 有穷的 / 无穷的 |
| countable / uncountable | 可数的 / 不可数的 | | |

## 直觉主义、拓扑和其他 OpenLogic 模块

| English | 中文 | English | 中文 |
|---|---|---|---|
| intuitionistic logic | 直觉主义逻辑 | intuitionistic | 直觉主义的 |
| constructive / constructive reasoning | 构造性的 / 构造性推理 | | |
| topological space | 拓扑空间 | open sets | 开集 |
| topological model | 拓扑模型 | interior | 内部 |
| prime (formula) | 素的 | | |
| BHK interpretation | BHK 解释 | | |
| atomic formula | 原子公式 | | |
| excluded middle | 排中律 | Law of Excluded Middle | 排中律 |
| state description | 状态描述 | symbolic logic | 符号逻辑 |
| word / finite strings | 词 / 有穷字符串 | | |

## 通用书籍和句式

| English | 中文 | English | 中文 |
|---|---|---|---|
| definition | 定义 | example | 例 |
| exercise | 习题 | theorem / lemma | 定理 / 引理 |
| proposition | 命题 | corollary | 推论 |
| note | 注 | convention | 约定 |
| suppose | 设 | then | 则 |
| hence / thus | 因此 / 于是 | note that | 注意，…… |
| recall that | 回顾，…… | it is easy to see that | 容易看出，…… |
| the following proposition | 如下命题 | iff | 当且仅当 |
| i.e. / e.g. / viz. | 即 / 例如 / 亦即 | prove | 证明 |

定义中的 `iff` 句型统一写作「`!A ∈ Γ` 当且仅当……」。数学或宏参数内的变量、标签和控制序列不随中文句式改变。

## 其他通用语境

| English | 中文 | English | 中文 |
|---|---|---|---|
| relational structures | 关系结构 | relative product | 相对积 |
| partitions | 划分 | first / second-order definable | 一阶 / 二阶可定义的 |
| balanced | 平衡的 | in parallel | 并行地 |
| finest / coarsest | 最细的 / 最粗的 | assumptions | 假设 |
| closed | 闭的 | open | 开的 |
| labelled | 加标的 | prefixed | 带前缀的 |
| principia mathematica | 《数学原理》（保留原文） | begriffsschrift | 《概念文字》（保留原文） |
| meaning and necessity | 《意义与必然性》（保留原文） | de interpretatione | 《解释篇》（保留原文） |

## 元理论补充

| English | 中文 | English | 中文 |
|---|---|---|---|
| soundness theorem | 可靠性定理 | completeness theorem | 完全性定理 |
| decidability | 可判定性 | theory | 理论 |
| extension | 扩张 | Lindenbaum lemma | Lindenbaum 引理 |
| truth-functional | 真值函项的 | deductive | 演绎的 |
| purported counterexample | 所谓反例 | closed under subformulas | 对子公式封闭 |

## 不翻译与语境边界

Open Logic Project 保留英文；Open Logic Text 在中文散文中写作《开放逻辑读本》。项目链接、GitHub 链接、DOI、逻辑系统名（K、T、B、D、S4、S5、GL、K4、KB、K45 等）、公理模式名、文献引用和人名保留原文；其他书名若有通行中文译名，可保留原名并附中文名。

`operator`（逻辑算子）与 `connective`（命题联结词）是两个独立概念，分别译「算子」与「联结词」；`syntax/syntactic` 在逻辑学语境译「句法/句法的」，自然语言或程序语言的 `grammar` 才译「语法」。
