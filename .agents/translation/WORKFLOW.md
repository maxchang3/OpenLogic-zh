# OpenLogic-Zh 翻译与校验工作流

## 批次与状态

每个文件由一个 worker 负责；批次控制在 3–5 个。worker 开始前读 `README.md`、`POLICY.md`、`terminology/terms.json`（按需用 jq 过滤 `module`），再读 `content/<相对路径>`，把完整译文写入 `locale/zh/content/<同路径>`。

先用 `python3 scripts/translation-state.py status --consumer <名称>` 选取待办，再对每个文件运行 `brief`。未译文件的 brief 给出英文位置、目标译文位置、整篇命中术语和门禁；已有确认基线的文件只列英文增量。完成翻译和审查后运行 `confirm --write`，最后按批次运行 `make check-zh`。`confirm` 内部执行静态门禁，只记录通过门禁的当前英文和中文 Git blob，不自动判断翻译语义。

worker 遵守 `POLICY.md` 的 TeX 不变量；返回空值视为失败，必须检查目标文件真实存在且不是未经翻译的英文副本，不能只依据返回消息判断成功。

## 术语与审查

未覆盖术语先查通行译法并在交付报告登记；协调者把尚未确认的项目写入 `pending.md`，不要直接在多个 worker 中采用互相冲突的译法。确认后的术语必须回填 `terminology/terms.json`，并检查可执行 locale 映射是否一致。术语定案或修改后，立即检索并同步替换全部译文中的旧译名。

每批完成后在 `OpenLogic-Zh/` 运行 `make check-zh`，检查译文范围、路径与 `\olfileid`、术语和令牌映射、人名及人名指代。失败时优先检查花括号、数学模式、`!!{token}` 键、`\tagitem` 嵌套和 `\olfileid[zh]` 参数；任何批量修改后都要重跑本门禁，并用 `git diff --check` 检查空白。

审计与修复 worker 的要求：
- 明确保留 `!!{...}`、token 键、普通词与 token 的边界；每处修改保持最小 diff；
- 加载 `terms.json`（避免把已定译名当错报）与 `../notes/tex-traps.md` 的上游疑点清单（避免把忠实照搬当错报）；
- 审计报告的行号仅供参考，复核以 EN/ZH 内容匹配为准；
- 大批次数据（文件清单、问题清单）写入临时文件由 worker 自行读取，不要内嵌在任务参数中；
- 审计时注意上下文敏感的普通数学词，不得因术语表存在某一译法就机械逐词替换；遇到 `identity`、`part` 等词须结合其句法功能和数学对象判断。

人名处理：有通行译名的人名在译文中写 `\zhFirst{原名}{译名}`（音译表见 `terms.json` 人名条目），不要手工判断首次出现位置或手工加括号；无通行译名的人名保留原文。

## 构建与视觉验收

OpenLogic-Zh 自身的 `make`/`make all` 仍构建上游英文文档。正文批次形成完整章节后，在受影响的组装仓库做中文试编译、`pdftotext` 抽查和必要的页面渲染；SLC 整书未齐时运行 `make zh-chapter`。共享章节要验证所有消费它的书，共享 TeX 改动要回归两书；整书中文目标仍不允许英文回退。

视觉排版问题先渲染目标 PDF 页面为 PNG（`pdftoppm -png -r 150 file.pdf out`，图片放在工作区内）。视觉核验只作辅助，不能代替实际 XeLaTeX 构建与文本检查；字符间空隙可能受字形视觉重心影响，精确间距以 `\hbox` 宽度测量（`\the\wd0`）和实际构建为准。中文与数学/英文之间的 `~` 和普通空格会被 xeCJK 吸收，不要为对齐盲目补空格。
