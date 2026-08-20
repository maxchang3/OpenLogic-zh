# OpenLogic-Zh 工作说明

本仓库是 OpenLogicProject/OpenLogic 的中文 fork，也是实际翻译工作的归属仓库；B&D 只从这里取 `locale/zh/` 内容进行组装。

开始工作先读 `.agents/translation/README.md`、`POLICY.md` 和 `.agents/translation/terminology/terms.json`，再按 `module` 字段加载当前主题术语；改动 TeX 或 locale 机制前再读 `.agents/notes/tex-traps.md`，批量 worker 与校验细节见 `.agents/translation/WORKFLOW.md`。

英文源文件在 `content/`，译文在 `locale/zh/content/`；保持相同相对路径，默认不修改英文源。`locale/zh/open-logic-config.sty` 是可执行 token 映射，必须与 `.agents/translation/terminology/tokens.json` 一致；`open-logic-locale.sty` 负责语言与交叉引用，文档规范必须与它们一致。

保持上游友好的最小改动：不要擅自修改 remote、分支或推送；同步前查看 `git log HEAD..upstream/master`（具体 remote 名称以本地配置为准），只合并必要上游提交，不重写上游历史。

OpenLogic-Zh 的 `make`/`make all` 构建上游英文文档；中文译文的最小完整验证在兄弟目录 `boxes-and-diamonds-zh/` 执行 `make check`，再用 `pdftotext` 抽查中文目录、标题和术语。
