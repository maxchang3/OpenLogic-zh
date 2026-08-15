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
