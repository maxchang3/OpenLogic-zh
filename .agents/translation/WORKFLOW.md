# OpenLogic-Zh 翻译与校验工作流

每个文件由一个 worker 负责；批次控制在 3–5 个。worker 开始前读 `README.md`、`POLICY.md`、`terminology/core.md` 和适用的模块术语包，再读 `content/<相对路径>`，把完整译文写入 `locale/zh/content/<同路径>`。

worker 必须保留宏、数学、token、标签和 `\olfileid[zh]` 规则；返回空值视为失败，必须检查目标文件真实存在且不是未经翻译的英文副本，不能只依据返回消息判断成功。

未覆盖术语先查通行译法并在交付报告登记；协调者把尚未确认的项目写入 `pending.md`，不要直接在多个文件中采用互相冲突的译法。确认后的术语必须回填术语包，并检查可执行 locale 映射是否一致。

每批完成后先在 `OpenLogic-Zh/` 运行 `python3 scripts/check-tokens.py` 做令牌计数机械校验（缺/多均需修到 0），再在兄弟仓库 `boxes-and-diamonds-zh/` 至少运行一次 `make check`；失败时优先检查花括号、数学模式、`!!{token}` 键、`\tagitem` 嵌套和 `\olfileid[zh]` 参数。用 `pdftotext` 抽查目录、章节标题和关键术语，并用 `git diff --check` 检查空白。

OpenLogic-Zh 自身的 `make`/`make all` 仍构建上游英文文档；中文排版验证由 B&D 组装器完成。同步上游前先检查差异，只合并必要提交，不改写上游源文件或远程配置。

JavaScript 调度 prompt 不要把 TeX 的两个反引号引号对直接放入模板字符串；需要时用文字描述或字符串数组拼接。并发失败后先检查文件状态，再补跑失败文件。

视觉排版问题先渲染目标 PDF 页面为 PNG，再交由视觉模型提出具体字号、行距和颜色建议；视觉建议不能代替实际 XeLaTeX 构建与文本检查。
