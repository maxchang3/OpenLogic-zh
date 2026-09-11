#!/usr/bin/env python3
"""从 LaTeX recorder 输出校验或刷新消费者正文闭包。"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REVISION = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
METADATA_KEYS = (
    "driver",
    "tag-config",
    "consumer-revision",
    "openlogic-revision",
)


def load_manifest_module():
    path = Path(__file__).with_name("check-zh-manifest.py")
    spec = importlib.util.spec_from_file_location("check_zh_manifest", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_paths(fls_path, openlogic_root):
    """提取指向 OpenLogic content 或中文 locale content 的 .tex 输入。"""
    fls_path = Path(fls_path).resolve()
    openlogic_root = Path(openlogic_root).resolve()
    roots = (
        openlogic_root / "content",
        openlogic_root / "locale" / "zh" / "content",
    )
    paths = set()
    for raw in fls_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.startswith("INPUT "):
            continue
        value = Path(raw[6:])
        resolved = (
            value.resolve()
            if value.is_absolute()
            else (fls_path.parent / value).resolve()
        )
        for content_root in roots:
            try:
                relative = resolved.relative_to(content_root)
            except ValueError:
                continue
            if relative.suffix == ".tex":
                paths.add(relative.as_posix())
            break
    return sorted(paths)


def read_metadata(path):
    metadata = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"# ([a-z-]+): (.+)", raw)
        if match:
            metadata[match.group(1)] = match.group(2)
    return metadata


def metadata_problems(metadata, driver, tag_config):
    problems = []
    for key in METADATA_KEYS:
        if key not in metadata:
            problems.append(f"consumer closure is missing metadata: {key}")
    expected = {"driver": driver, "tag-config": tag_config}
    for key, value in expected.items():
        if key in metadata and metadata[key] != value:
            problems.append(
                f"consumer closure {key} is {metadata[key]!r}, expected {value!r}"
            )
    for key in ("consumer-revision", "openlogic-revision"):
        if key in metadata and REVISION.fullmatch(metadata[key]) is None:
            problems.append(f"consumer closure has invalid {key}: {metadata[key]!r}")
    return problems


def git_revision(root):
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git rev-parse failed"
        raise RuntimeError(f"cannot determine revision for {root}: {detail}")
    return result.stdout.strip()


def write_closure(
    path, consumer, paths, driver, tag_config, consumer_root, openlogic_root
):
    metadata = {
        "driver": driver,
        "tag-config": tag_config,
        "consumer-revision": git_revision(consumer_root),
        "openlogic-revision": git_revision(openlogic_root),
    }
    lines = [
        f"# {consumer} 的完整正文导入闭包；路径相对 content/。",
        "# 由 LaTeX recorder 输出生成；译文完整性由组装仓库判定。",
        *(f"# {key}: {metadata[key]}" for key in METADATA_KEYS),
        *paths,
    ]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer", required=True)
    parser.add_argument("--fls", required=True)
    parser.add_argument("--driver", required=True)
    parser.add_argument("--tag-config", required=True)
    parser.add_argument("--consumer-root", default=".")
    parser.add_argument("--openlogic-root", default=str(ROOT))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    openlogic_root = Path(args.openlogic_root).resolve()
    consumer_root = Path(args.consumer_root).resolve()
    closure = openlogic_root / "locale" / "zh" / "consumers" / f"{args.consumer}.txt"
    fls = Path(args.fls)
    for label, relative in (("driver", args.driver), ("tag config", args.tag_config)):
        source = consumer_root / relative
        if not source.is_file():
            print(f"错误: missing {label}: {source}", file=sys.stderr)
            return 2
    if not fls.is_file():
        print(f"错误: missing recorder output: {fls}", file=sys.stderr)
        return 2
    try:
        actual = extract_paths(fls, openlogic_root)
    except OSError as exc:
        print(f"错误: cannot read recorder output {fls}: {exc}", file=sys.stderr)
        return 2
    if not actual:
        print(f"错误: no OpenLogic content inputs found in {fls}", file=sys.stderr)
        return 2

    if args.write:
        try:
            write_closure(
                closure,
                args.consumer,
                actual,
                args.driver,
                args.tag_config,
                consumer_root,
                openlogic_root,
            )
        except (OSError, RuntimeError) as exc:
            print(f"错误: {exc}", file=sys.stderr)
            return 2
        print(f"OK: wrote {len(actual)} paths to {closure}")
        return 0

    manifest = load_manifest_module()
    if not closure.is_file():
        print(f"错误: missing consumer closure: {closure}", file=sys.stderr)
        return 2
    expected, problems = manifest.read_consumer_list(closure)
    problems.extend(
        metadata_problems(read_metadata(closure), args.driver, args.tag_config)
    )
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing:
        problems.append("recorder output is missing listed paths:")
        problems.extend(f"  - {path}" for path in missing)
    if extra:
        problems.append("recorder output contains unlisted paths:")
        problems.extend(f"  - {path}" for path in extra)
    if problems:
        print("FAIL")
        for problem in problems:
            print(f" - {problem}")
        return 1
    metadata = read_metadata(closure)
    print(
        f"OK: {args.consumer} recorder closure matches {len(expected)} paths "
        f"({metadata['consumer-revision']} / {metadata['openlogic-revision']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
