#!/usr/bin/env python3
from pathlib import Path, PurePosixPath
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


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


def manifest_paths(manifest):
    problems = []
    if not manifest.is_file():
        problems.append(f"missing locale manifest: {manifest}")
        return [], problems

    paths = []
    seen = set()
    for line_number, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        path = PurePosixPath(line)
        if (
            raw != line
            or path.is_absolute()
            or path.as_posix() != line
            or "\\" in line
            or any(part in ("", ".", "..") for part in path.parts)
            or path.suffix != ".tex"
            or not path.parts
        ):
            problems.append(
                f"manifest line {line_number}: invalid relative .tex path {raw!r}"
            )
            continue
        if line in seen:
            problems.append(f"manifest line {line_number}: duplicate path {line}")
            continue
        seen.add(line)
        paths.append(line)

    if paths != sorted(paths):
        problems.append(
            "manifest paths are not sorted; sort the non-comment entries in dictionary order"
        )
    return paths, problems


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
    content = root / "content"
    locale_content = root / "locale" / "zh" / "content"
    manifest_path = root / "locale" / "zh" / "manifest.txt"
    manifest, problems = manifest_paths(manifest_path)
    actual = locale_paths(locale_content)

    if not locale_content.is_dir():
        problems.append(f"missing locale content directory: {locale_content}")
    else:
        listed_but_missing = sorted(set(manifest) - set(actual))
        unlisted = sorted(set(actual) - set(manifest))
        if listed_but_missing:
            problems.append(
                "manifest entries missing from locale/zh/content (restore or remove the stale line):"
            )
            problems.extend(f"  - {path}" for path in listed_but_missing)
        if unlisted:
            problems.append(
                "locale .tex files not listed in manifest (review and add the path):"
            )
            problems.extend(f"  - {path}" for path in unlisted)

        no_counterpart = sorted(
            path
            for path in set(manifest) | set(actual)
            if not (content / path).is_file()
        )
        if no_counterpart:
            problems.append("locale paths without an English counterpart in content/:")
            problems.extend(f"  - {path}" for path in no_counterpart)

        problems.extend(check_file_ids(locale_content, actual))
    return problems, manifest


def main():
    problems, manifest = validate()
    if problems:
        print("FAIL")
        for problem in problems:
            print(f" - {problem}")
        return 1
    print(
        f"OK: manifest covers {len(manifest)} Chinese locale .tex files; "
        "paths, English counterparts, and file-id markers are valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
