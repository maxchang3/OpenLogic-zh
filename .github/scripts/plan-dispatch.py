#!/usr/bin/env python3
"""按改动文件规划组装仓库的构建派发，供 notify workflow 调用。

规则（fail-open：宁可多建，不可漏建）：
- 共享 TeX、参考文献、图片和语言表改动影响所有消费者，直接全派发；
- content/<path> 或 locale/zh/content/<path> 落在某本书的导入闭包内则派发该书；
- consumer 闭包或其他共享 locale 元数据变化时全派发，以免依赖范围变化漏检；
- 其余路径（文档、脚本、翻译状态等）不影响构建，不派发。

闭包清单与各书实际编译闭包一致，路径相对 content/：
- B&D：locale/zh/consumers/boxes-and-diamonds-zh.txt
- SLC：locale/zh/consumers/sets-logic-computation-zh.txt

两份闭包清单都是派发器的必需输入；缺失时直接失败。
"""
from __future__ import annotations

import argparse
from pathlib import Path

CONSUMERS = ("bd", "slc")

# 这些前缀下的改动是两本书共用的排版与素材层。
SHARED_PREFIXES = ("sty/", "bib/", "include/", "assets/")

# 顶层和 locale 层的可执行 TeX 配置。
SHARED_TEX = {
    "open-logic-config.sty",
    "open-logic-envs.sty",
    "open-logic-locale.sty",
    "locale/zh/open-logic-config.sty",
    "locale/zh/open-logic-envs.sty",
    "locale/zh/open-logic-locale.sty",
}


def read_closure(path):
    """读取相对 content/ 的路径清单。"""
    closure = Path(path)
    if not closure.is_file():
        raise FileNotFoundError(f"missing consumer closure: {closure}")
    paths = set()
    for raw in closure.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            paths.add(line)
    return paths


def content_relative(changed):
    for prefix in ("content/", "locale/zh/content/"):
        if changed.startswith(prefix):
            return changed[len(prefix):]
    return None


def is_shared(changed):
    if changed in SHARED_TEX:
        return True
    if changed.startswith(SHARED_PREFIXES):
        return True
    if changed.startswith("locale/zh/") and not changed.startswith("locale/zh/content/"):
        return True
    return False


def plan(changed_files, bd_closure, slc_closure):
    affected = set()
    for changed in changed_files:
        changed = changed.strip()
        if not changed:
            continue
        if is_shared(changed):
            affected.update(CONSUMERS)
            continue
        relative = content_relative(changed)
        if relative is None:
            continue
        if relative in bd_closure:
            affected.add("bd")
        if relative in slc_closure:
            affected.add("slc")
    return affected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed", required=True, help="每行一个改动路径")
    parser.add_argument("--bd-closure", required=True)
    parser.add_argument("--slc-closure", required=True)
    parser.add_argument("--all", action="store_true", help="无法判定影响面时派发所有消费者")
    parser.add_argument("--github-output")
    args = parser.parse_args()

    changed_files = Path(args.changed).read_text(encoding="utf-8").splitlines()
    if args.all:
        affected = set(CONSUMERS)
    else:
        try:
            bd_closure = read_closure(args.bd_closure)
            slc_closure = read_closure(args.slc_closure)
        except FileNotFoundError as exc:
            raise SystemExit(str(exc)) from exc
        affected = plan(changed_files, bd_closure, slc_closure)

    print(f"changed files: {len([c for c in changed_files if c.strip()])}")
    for name in CONSUMERS:
        hit = name in affected
        print(f"  {name}: {'dispatch' if hit else 'skip'}")

    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as handle:
            for name in CONSUMERS:
                handle.write(f"{name}={'true' if name in affected else 'false'}\n")


if __name__ == "__main__":
    main()
