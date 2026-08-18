# OpenLogic-Zh 翻译与校验工作流

每个文件由一个 worker 负责；批次控制在 3–5 个。worker 开始前读 `README.md`、`POLICY.md`、`terminology/terms.json`（按需用 jq 过滤 `module`），再读 `content/<相对路径>`，把完整译文写入 `locale/zh/content/<同路径>`。

worker 必须保留宏、数学、token、标签和 `\olfileid[zh]` 规则；返回空值视为失败，必须检查目标文件真实存在且不是未经翻译的英文副本，不能只依据返回消息判断成功。

未覆盖术语先查通行译法并在交付报告登记；协调者把尚未确认的项目写入 `pending.md`，不要直接在多个文件中采用互相冲突的译法。确认后的术语必须回填 `terminology/terms.json`，并检查可执行 locale 映射是否一致。**术语定案或修改后立即 grep 全部译文同步替换旧译名**（曾发生定案「逆良基的/全称量化/原子公式」后译文仍残留旧译名「反良基/普遍量化/原子命题」多处的案例）。

每批完成后先在 `OpenLogic-Zh/` 运行 `python3 scripts/check-tokens.py` 做令牌计数机械校验、`python3 scripts/check-names.py` 做人名覆盖校验、`python3 scripts/check-name-refs.py` 做同姓人名指代校验（如 C. I. Lewis 与 David K. Lewis 的张冠李戴），再（缺/多均需修到 0），再在兄弟仓库 `boxes-and-diamonds-zh/` 至少运行一次 `make check`；失败时优先检查花括号、数学模式、`!!{token}` 键、`\tagitem` 嵌套和 `\olfileid[zh]` 参数。用 `pdftotext` 抽查目录、章节标题和关键术语，并用 `git diff --check` 检查空白。**任何 LLM 批量修改（翻译、审计修复、重构）后都必须重跑 `check-tokens.py` 并清零**——修复类 worker 曾把普通词加成 `!!{token}`、把 token 改回普通词、改动 token 键，只有机械校验能兜底。

审计与修复 worker 的要求：
- 提示词必须包含：`!!{...}` 原样保留、不得改动 token 键、不得把普通词改写为 token（或反之）、每处修改用最小 diff；
- worker 加载 `terms.json`（避免把已定译名当错报）与 `../notes/tex-traps.md` 的上游疑点清单（避免把忠实照搬当错报）；
- 审计报告的行号仅供参考（LLM 统计易错位），复核以 EN/ZH 内容匹配为准；
- 大批次数据（文件清单、问题清单）写入临时文件由 worker 自行读取，不要内嵌进调度参数（曾发生内嵌 JSON 错乱导致批次丢失）。
- 审计时注意上下文敏感的普通数学词，不得因术语表存在某一译法就机械逐词替换；遇到 `identity`、`part` 等词须结合其句法功能和数学对象判断。

人名处理：有通行译名的人名在译文中写 `\zhFirst{原名}{译名}`（音译表见 `terms.json` 人名条目），不要手工判断首次出现位置或手工加括号；无通行译名的人名保留原文。

OpenLogic-Zh 自身的 `make`/`make all` 仍构建上游英文文档；中文排版验证由 B&D 组装器完成。同步上游前先检查差异，只合并必要提交，不改写上游源文件或远程配置。

JavaScript 调度 prompt 不要把 TeX 的两个反引号引号对直接放入模板字符串；需要时用文字描述或字符串数组拼接。并发失败后先检查文件状态，再补跑失败文件。

视觉排版问题先渲染目标 PDF 页面为 PNG（`pdftoppm -png -r 150 file.pdf out`，图片放在工作区内），再交由视觉模型提出具体字号、行距和颜色建议；视觉建议不能代替实际 XeLaTeX 构建与文本检查。

视觉模型的调用方式（DSH workflow，provider/model 覆盖）：用 workflow 工具跑单个 agent，`agent(prompt, { provider: 'opencode-go', model: 'minimax-m3' })`，prompt 里给出图片路径（工作区内）并让 agent 用 `read_image` 看图、逐项回答具体问题。注意：视觉模型对字符间空隙的观察不可全信——花体/斜体字形（如 `\mathcal{L}_0`）的视觉重心偏移会被误读为「间距大」，且与 TeX 宽度测量可能矛盾；精确间距以 `\hbox` 宽度测量（`\the\wd0`）为准，视觉仅作交叉验证。中文与数学/英文之间的 `~` 和普通空格都会被 xeCJK 吸收，不产生额外间距，无需为对齐而添加。
