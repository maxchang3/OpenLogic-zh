#!/usr/bin/env python3
"""校验中文 locale 的消费者闭包与已译文件。

consumer 清单在 locale/zh/consumers/*.txt，各记录一个下游书籍的完整导入闭包
（路径相对 content/）。清单可以包含尚未翻译的条目；本检查只保证：
- 每个清单条目的路径合法、排序、唯一，且在 content/ 有英文对应；
- locale/zh/content 下的每个 .tex 都落在某个闭包里（没有野生译文）；
- 每个译文都带 \\olfileid[zh] 标记。

某本书是否翻译完整由该书自己的构建/CI 判定，本检查不强制。
"""
from pathlib import Path, PurePosixPath
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CONSUMERS = Path("locale/zh/consumers")


def strip_tex_comments(text):
    """去掉未转义的 TeX 注释，同时保留行边界以便报告行号。"""
    lines = []
    for line in text.splitlines():
        for i, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            j = i - 1
            while j >= 0 and line[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                line = line[:i]
                break
        lines.append(line)
    return "\n".join(lines)


def read_consumer_list(path):
    problems = []
    paths = []
    seen = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        item = PurePosixPath(line)
        if (
            raw != line
            or item.is_absolute()
            or item.as_posix() != line
            or "\\" in line
            or any(part in ("", ".", "..") for part in item.parts)
            or item.suffix != ".tex"
            or not item.parts
        ):
            problems.append(
                f"{path.name} line {line_number}: invalid relative .tex path {raw!r}"
            )
            continue
        if line in seen:
            problems.append(f"{path.name} line {line_number}: duplicate path {line}")
            continue
        seen.add(line)
        paths.append(line)
    if paths != sorted(paths):
        problems.append(
            f"{path.name}: paths are not sorted; sort the non-comment entries in dictionary order"
        )
    return paths, problems


def consumer_paths(root=ROOT):
    """返回 {消费者名: [闭包路径]}；路径相对 content/。"""
    directory = Path(root) / CONSUMERS
    problems = []
    consumers = {}
    if not directory.is_dir():
        problems.append(f"missing consumer directory: {directory}")
        return consumers, problems
    for path in sorted(directory.glob("*.txt")):
        paths, list_problems = read_consumer_list(path)
        consumers[path.stem] = paths
        problems.extend(list_problems)
        for rel in paths:
            if not (Path(root) / "content" / rel).is_file():
                problems.append(
                    f"{path.name}: no English counterpart in content/: {rel}"
                )
    if not consumers:
        problems.append(f"no consumer lists found in {directory}")
    return consumers, problems


def universe_paths(root=ROOT):
    """所有消费者闭包的并集，即可以合法出现在 locale/zh/content 的路径集合。"""
    consumers, problems = consumer_paths(root)
    union = sorted({rel for paths in consumers.values() for rel in paths})
    return union, problems


def locale_paths(locale_content):
    if not locale_content.is_dir():
        return []
    return sorted(
        path.relative_to(locale_content).as_posix()
        for path in locale_content.rglob("*.tex")
        if path.is_file()
    )


OLFILEID = re.compile(
    r"\\olfileid(?P<locale>\[[^\]\r\n]*\])?(?:\{[^{}\r\n]*\}){3}"
)


def check_file_ids(locale_content, paths):
    problems = []
    for rel in paths:
        path = locale_content / rel
        if not path.is_file():
            continue
        code = strip_tex_comments(path.read_text(encoding="utf-8"))
        for occurrence in re.finditer(r"\\olfileid", code):
            match = OLFILEID.match(code, occurrence.start())
            line = code.count("\n", 0, occurrence.start()) + 1
            if match is None:
                problems.append(
                    f"{rel}:{line}: malformed \\olfileid; expected \\olfileid[zh]{{...}}{{...}}{{...}}"
                )
            elif match.group("locale") != "[zh]":
                marker = match.group("locale") or "(missing locale marker)"
                problems.append(
                    f"{rel}:{line}: illegal \\olfileid marker {marker}; use \\olfileid[zh]"
                )
    return problems


def validate(root=ROOT):
    root = Path(root)
    locale_content = root / "locale" / "zh" / "content"
    consumers, problems = consumer_paths(root)
    universe = {rel for paths in consumers.values() for rel in paths}

    actual = locale_paths(locale_content)
    if not locale_content.is_dir():
        problems.append(f"missing locale content directory: {locale_content}")
    else:
        unlisted = sorted(set(actual) - universe)
        if unlisted:
            problems.append("locale .tex files not listed in any consumer closure:")
            problems.extend(f"  - {path}" for path in unlisted)
        problems.extend(check_file_ids(locale_content, actual))
    return problems, consumers


def main():
    problems, consumers = validate()
    if problems:
        print("FAIL")
        for problem in problems:
            print(f" - {problem}")
        return 1
    universe = {rel for paths in consumers.values() for rel in paths}
    names = ", ".join(sorted(consumers))
    print(
        f"OK: {len(consumers)} consumer closures ({names}) define {len(universe)} paths; "
        "locale files, English counterparts, and file-id markers are valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
