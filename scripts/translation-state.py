#!/usr/bin/env python3
import argparse
import difflib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
STATE = Path(".agents/translation/state.json")
TERMS = Path(".agents/translation/terminology/terms.json")
SCHEMA = 1
OID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
_MANIFEST_MODULE = None


def load_json(path):
    def reject_duplicate_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r}")
            result[key] = value
        return result

    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def manifest_paths(root):
    global _MANIFEST_MODULE
    path = Path(root) / "locale" / "zh" / "manifest.txt"
    if _MANIFEST_MODULE is None:
        module_path = Path(__file__).with_name("check-zh-manifest.py")
        spec = importlib.util.spec_from_file_location("check_zh_manifest", module_path)
        _MANIFEST_MODULE = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_MANIFEST_MODULE)
    return _MANIFEST_MODULE.manifest_paths(path)


def strip_tex_comments(text):
    return _MANIFEST_MODULE.strip_tex_comments(text)


def canonical_path(rel, manifest):
    if not isinstance(rel, str) or not rel:
        return None
    path = PurePosixPath(rel)
    if (
        path.is_absolute()
        or path.as_posix() != rel
        or "\\" in rel
        or any(part in ("", ".", "..") for part in path.parts)
        or path.suffix != ".tex"
        or rel not in manifest
    ):
        return None
    return rel


def load_state(root, manifest):
    path = Path(root) / STATE
    problems = []
    try:
        document = load_json(path)
    except FileNotFoundError:
        return {}, [f"missing translation state: {path}"]
    except (OSError, ValueError) as exc:
        return {}, [f"cannot read translation state {path}: {exc}"]

    if not isinstance(document, dict):
        problems.append("translation state root must be an object")
        return {}, problems
    if set(document) != {"schema", "pairs"}:
        problems.append("translation state must contain only schema and pairs")
    if type(document.get("schema")) is not int or document["schema"] != SCHEMA:
        problems.append(f"translation state schema must be integer {SCHEMA}")
    pairs = document.get("pairs")
    if not isinstance(pairs, dict):
        problems.append('translation state "pairs" must be an object')
        return {}, problems

    valid_pairs = {}
    for rel, pair in pairs.items():
        if canonical_path(rel, manifest) is None:
            problems.append(f"translation state pair path is not in manifest: {rel!r}")
            continue
        if not isinstance(pair, dict) or set(pair) != {"source", "translation"}:
            problems.append(
                f"translation state pair {rel!r} must contain only source and translation OIDs"
            )
            continue
        if any(type(pair[key]) is not str or not OID.fullmatch(pair[key]) for key in pair):
            problems.append(
                f"translation state pair {rel!r} has invalid source or translation OID"
            )
            continue
        valid_pairs[rel] = pair
    return {"schema": document.get("schema"), "pairs": valid_pairs}, problems


def git(root, *args):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def file_oid(root, path, write=False):
    args = ["hash-object"]
    if write:
        args.append("-w")
    result = git(root, *args, "--", str(path))
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"cannot hash {path}: {detail or 'git hash-object failed'}")
    return result.stdout.decode("ascii").strip()


def blob_type(root, oid):
    result = git(root, "cat-file", "-t", oid)
    if result.returncode != 0:
        return None
    return result.stdout.decode("ascii", "replace").strip()


def read_blob(root, oid):
    if blob_type(root, oid) != "blob":
        raise RuntimeError(f"Git object {oid} is missing or is not a blob")
    result = git(root, "cat-file", "blob", oid)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"cannot read Git blob {oid}: {detail or 'git cat-file failed'}")
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"Git blob {oid} is not UTF-8 text: {exc}") from exc


def check_blob_objects(root, state):
    problems = []
    for rel, pair in sorted(state.get("pairs", {}).items()):
        for role in ("source", "translation"):
            oid = pair[role]
            if blob_type(root, oid) != "blob":
                problems.append(
                    f"translation state pair {rel!r} {role} OID is not a readable Git blob: {oid}"
                )
    return problems


def check_state(root=ROOT):
    root = Path(root)
    manifest, problems = manifest_paths(root)
    state, state_problems = load_state(root, manifest)
    problems.extend(state_problems)
    problems.extend(check_blob_objects(root, state))
    for rel, pair in sorted(state.get("pairs", {}).items()):
        for role, relative in (
            ("source", Path("content") / rel),
            ("translation", Path("locale/zh/content") / rel),
        ):
            try:
                current = file_oid(root, relative)
            except RuntimeError as exc:
                problems.append(str(exc))
                continue
            if current != pair[role]:
                problems.append(
                    f"translation state pair {rel!r} {role} changed: "
                    f"recorded {pair[role]}, current {current}"
                )
    return problems


def derive_status(root, rel, pair):
    source = file_oid(root, Path("content") / rel)
    translation = file_oid(root, Path("locale/zh/content") / rel)
    if pair is None:
        return "unconfirmed"
    source_changed = source != pair["source"]
    translation_changed = translation != pair["translation"]
    if source_changed and translation_changed:
        return "both-changed"
    if source_changed:
        return "source-changed"
    if translation_changed:
        return "translation-changed"
    return "confirmed"


def status_entries(root=ROOT, requested=None):
    root = Path(root)
    manifest, problems = manifest_paths(root)
    state, state_problems = load_state(root, manifest)
    problems.extend(state_problems)
    problems.extend(check_blob_objects(root, state))
    if requested is None:
        paths = manifest
    else:
        paths = []
        for rel in requested:
            if canonical_path(rel, manifest) is None:
                problems.append(f"path is not a manifest .tex path: {rel!r}")
            elif rel not in paths:
                paths.append(rel)
    entries = []
    if not problems:
        for rel in paths:
            try:
                state_name = derive_status(root, rel, state["pairs"].get(rel))
            except RuntimeError as exc:
                problems.append(str(exc))
                continue
            entries.append({"path": rel, "status": state_name})
    return entries, problems


def load_terms(root):
    document = load_json(Path(root) / TERMS)
    if not isinstance(document, dict) or not isinstance(document.get("terms"), list):
        raise ValueError('terms.json must contain a "terms" list')
    terms = []
    for index, term in enumerate(document["terms"]):
        if not isinstance(term, dict) or not isinstance(term.get("en"), str):
            raise ValueError(f"terms.json entry {index} has no string en field")
        terms.append(term)
    return terms


def term_matches(text, term):
    matches = []
    for variant in term["en"].split(" / "):
        variant = variant.strip()
        if not variant:
            continue
        pattern = re.compile(
            r"(?<![A-Za-z])" + re.escape(variant) + r"(?![A-Za-z])", re.IGNORECASE
        )
        if pattern.search(text):
            matches.append(variant)
    return matches


def matching_terms(root, source_text):
    matches = []
    for term in load_terms(root):
        variants = term_matches(source_text, term)
        if variants:
            item = {
                key: term[key]
                for key in ("en", "zh", "module", "note")
                if key in term
            }
            item["matched"] = variants
            matches.append(item)
    return sorted(matches, key=lambda term: (term["en"].casefold(), term["en"]))


def changed_source_text(previous, current):
    return "\n".join(
        line[2:]
        for line in difflib.ndiff(previous.splitlines(), current.splitlines())
        if line.startswith(("- ", "+ "))
    )


def brief(root, rel):
    root = Path(root)
    manifest, problems = manifest_paths(root)
    if canonical_path(rel, manifest) is None:
        problems.append(f"path is not a manifest .tex path: {rel!r}")
        return "", problems
    state, state_problems = load_state(root, manifest)
    problems.extend(state_problems)
    if problems:
        return "", problems
    source_path = root / "content" / rel
    translation_path = root / "locale" / "zh" / "content" / rel
    try:
        current_source = source_path.read_text(encoding="utf-8")
        translation_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return "", [f"cannot read translation pair {rel!r}: {exc}"]
    pair = state["pairs"].get(rel)
    try:
        status_name = derive_status(root, rel, pair)
    except RuntimeError as exc:
        return "", [str(exc)]

    lines = [
        f"EN: content/{rel}",
        f"ZH: locale/zh/content/{rel}",
        f"状态: {status_name}",
        "",
        "英文变化:",
    ]
    if pair is None:
        lines.append(
            "[unconfirmed；没有确认基线，未生成增量 diff；请直接读取上述 EN/ZH 文件]"
        )
        term_source = strip_tex_comments(current_source)
    else:
        try:
            previous_source = read_blob(root, pair["source"])
        except RuntimeError as exc:
            return "", [str(exc)]
        term_source = strip_tex_comments(
            changed_source_text(previous_source, current_source)
        )
        diff = list(
            difflib.unified_diff(
                previous_source.splitlines(keepends=True),
                current_source.splitlines(keepends=True),
                fromfile=f"confirmed/content/{rel}",
                tofile=f"content/{rel}",
            )
        )
        if diff:
            lines.extend(line.rstrip("\n") for line in diff)
        else:
            lines.append("（无英文变化）")

    try:
        terms = matching_terms(root, term_source)
    except (OSError, ValueError) as exc:
        return "", [f"cannot read terms.json: {exc}"]
    lines.extend(["", "命中的术语:"])
    if terms:
        for term in terms:
            matched = ", ".join(term["matched"])
            note = f"；{term['note']}" if "note" in term else ""
            lines.append(
                f"- {term['en']} → {term['zh']} ({term['module']}; 命中: {matched}){note}"
            )
    else:
        lines.append("（无）")
    lines.extend(
        [
            "",
            "门禁:",
            "- make check-zh-static",
            f"- python3 scripts/translation-state.py confirm --write {rel}",
            "- make check-zh",
        ]
    )
    return "\n".join(lines) + "\n", []


def run_static_gate(root):
    return subprocess.run(["make", "check-zh-static"], cwd=root, check=False).returncode


def write_state(root, pairs):
    path = Path(root) / STATE
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {"schema": SCHEMA, "pairs": {key: pairs[key] for key in sorted(pairs)}}
    payload = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def confirm_paths(root, requested, write=False, run_static=True):
    root = Path(root)
    if not write:
        return ["confirm requires --write"], []
    requested = list(dict.fromkeys(requested))
    manifest, problems = manifest_paths(root)
    for rel in requested:
        if canonical_path(rel, manifest) is None:
            problems.append(f"path is not a manifest .tex path: {rel!r}")
    if problems:
        return problems, []
    state, state_problems = load_state(root, manifest)
    if state_problems:
        return state_problems, []
    if run_static and run_static_gate(root) != 0:
        return ["make check-zh-static failed; no confirmation was written"], []
    updates = {}
    try:
        for rel in requested:
            updates[rel] = {
                "source": file_oid(root, Path("content") / rel, write=True),
                "translation": file_oid(
                    root, Path("locale/zh/content") / rel, write=True
                ),
            }
    except RuntimeError as exc:
        return [str(exc)], []
    pairs = dict(state["pairs"])
    pairs.update(updates)
    write_state(root, pairs)
    return [], requested


def parser():
    command = argparse.ArgumentParser(
        description="派生 OpenLogic-Zh 翻译确认状态，不执行翻译语义判断。"
    )
    subparsers = command.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="显示译文确认状态")
    status_parser.add_argument("rel", nargs="*", help="manifest 中的相对 .tex 路径")
    status_parser.add_argument("--json", action="store_true", dest="as_json")

    subparsers.add_parser("check", help="校验确认状态和 Git blob")

    brief_parser = subparsers.add_parser("brief", help="显示单个文件的增量审阅摘要")
    brief_parser.add_argument("rel")

    confirm_parser = subparsers.add_parser("confirm", help="记录审阅后的当前内容")
    confirm_parser.add_argument("--write", action="store_true")
    confirm_parser.add_argument("rel", nargs="+", help="manifest 中的相对 .tex 路径")
    return command


def main(argv=None, root=ROOT):
    args = parser().parse_args(argv)
    if args.command == "status":
        entries, problems = status_entries(root, args.rel or None)
        if problems:
            for problem in problems:
                print(f"错误: {problem}", file=sys.stderr)
            return 1
        if args.as_json:
            print(json.dumps(entries, ensure_ascii=False, indent=2))
        else:
            for entry in entries:
                print(f"{entry['status']:18} {entry['path']}")
        return 0
    if args.command == "check":
        problems = check_state(root)
        if problems:
            print("FAIL")
            for problem in problems:
                print(f" - {problem}")
            return 1
        print("OK: translation state and recorded Git blobs are valid")
        return 0
    if args.command == "brief":
        output, problems = brief(root, args.rel)
        if problems:
            for problem in problems:
                print(f"错误: {problem}", file=sys.stderr)
            return 1
        print(output, end="")
        return 0
    problems, confirmed = confirm_paths(root, args.rel, args.write)
    if problems:
        for problem in problems:
            print(f"错误: {problem}", file=sys.stderr)
        return 2
    for rel in confirmed:
        print(f"{rel}: 记录为已确认内容")
    return 0


if __name__ == "__main__":
    sys.exit(main())
