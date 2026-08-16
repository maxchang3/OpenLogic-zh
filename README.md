# OpenLogic-Zh

本仓库旨在完整翻译 [OpenLogicProject/OpenLogic](https://github.com/OpenLogicProject/OpenLogic)。

中文内容放在 `locale/zh/`，目前仅按需翻译了部分内容。

**现阶段的译文全部由 AI 生成**，使用 DeepSeek Harness（DeepSeek V4 Flash 0731，思考强度 Max），并经过术语统一、TeX 结构检查和 PDF 审校；尚未进行大规模人工校验。

翻译规范入口位于 `.agents/translation/`：先读 `README.md`、`POLICY.md` 和 `terminology/core.md`，再按模块读取术语包；可执行的令牌映射仍在 `locale/zh/open-logic-config.sty`。

## 构建

由于译文尚未覆盖完整上游内容，本仓库的 `make` 和 `make all` 继续构建上游英文文档；已经本地化的组件供下游项目按需使用。

## 基于本项目的相关项目

[_Boxes and Diamonds_ 中文版](https://github.com/maxchang3/boxes-and-diamonds-zh)

## 同步上游

```sh
git remote add upstream https://github.com/OpenLogicProject/OpenLogic.git
git fetch upstream
git log --oneline HEAD..upstream/master
```

Actions 分别运行上游英文构建和中文 locale 结构检查。

## Upstream project

The Open Logic Project is an open source, open access collection of materials on advanced logic, aimed mainly at philosophers, but also suitable for computer scientists and mathematicians. The text can be rearranged and remixed into custom textbooks. It is written in LaTeX.

For more information, see the [project website](https://openlogicproject.org/), the [Open Logic wiki](https://github.com/OpenLogicProject/OpenLogic/wiki), and the [official PDF builds](https://builds.openlogicproject.org/).

Author(s): The Open Logic Project

The Open Logic Text is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
