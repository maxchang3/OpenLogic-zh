#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TERMS = ROOT / ".agents" / "translation" / "terminology" / "terms.json"
TOKENS = ROOT / ".agents" / "translation" / "terminology" / "tokens.json"
STY = ROOT / "locale" / "zh" / "open-logic-config.sty"
INDEX = ROOT / ".agents" / "translation" / "references" / "wenxuefeng-index.json"


def reject_duplicate_json_keys(pairs):
    """避免重复键被后出现的值静默覆盖。"""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_json_keys)


def strip_tex_comments(text):
    """删除未转义的 TeX 注释，避免注释中的伪调用进入术语映射。"""
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


ZH_TOKEN_CALL = re.compile(
    r"^\s*\\zhToken(?:\[(?P<english>[^]\r\n]*)\])?"
    r"\{(?P<key>[^{}\r\n]*)\}\{(?P<zh>[^{}\r\n]*)\}\s*$"
)


def parse_sty_tokens(sty, source=STY):
    """行首限制用于避开宏定义和拼接文本。"""
    problems = []
    token_map = {}
    for line_number, line in enumerate(strip_tex_comments(sty).splitlines(), 1):
        if not re.match(r"^\s*\\zhToken\b", line):
            continue
        match = ZH_TOKEN_CALL.match(line)
        if match is None:
            problems.append(
                f"{source}:{line_number}: malformed \\zhToken; "
                "expected optional English, key, and Chinese value"
            )
            continue
        key = f"!!{{{match.group('key')}}}"
        if key in token_map:
            problems.append(f"{source}:{line_number}: duplicate \\zhToken definition for {key}")
        else:
            token_map[key] = match.group("zh")
    return token_map, problems


def compare_token_maps(json_tokens, sty_tokens):
    problems = []
    json_keys = set(json_tokens)
    sty_keys = set(sty_tokens)
    only_json = json_keys - sty_keys
    only_sty = sty_keys - json_keys
    if only_json:
        problems.append(f"tokens.json has keys absent from sty: {sorted(only_json)}")
    if only_sty:
        problems.append(f"sty has \\zhToken keys absent from tokens.json: {sorted(only_sty)}")
    for key in sorted(json_keys & sty_keys):
        if json_tokens[key] != sty_tokens[key]:
            problems.append(
                f"token mapping mismatch for {key}: "
                f"tokens.json={json_tokens[key]!r}, sty={sty_tokens[key]!r}"
            )
    return problems


def validate_terms(path=TERMS):
    problems = []
    try:
        doc = load_json(path)
    except FileNotFoundError:
        return [f"{path} not found (run from OpenLogic-Zh root?)"], 0
    except ValueError as exc:
        return [f"{path}: invalid JSON ({exc})"], 0

    if not isinstance(doc, dict):
        return [f"{path}: root must be an object"], 0
    terms = doc.get("terms", [])
    if not isinstance(terms, list) or not terms:
        problems.append('terms.json: "terms" missing or empty')
        terms = []
    valid_terms = []
    for i, term in enumerate(terms):
        if not isinstance(term, dict):
            problems.append(f"terms[{i}]: entry must be an object")
            continue
        valid_terms.append(term)
    en_counts = Counter(
        term.get("en") for term in valid_terms if isinstance(term.get("en"), str)
    )
    for en, count in en_counts.items():
        if count > 1:
            for term in valid_terms:
                if term.get("en") == en and "note" not in term:
                    problems.append(
                        f'homograph {en!r} x{count}: entry "{term.get("zh")}" lacks context note'
                    )
    for i, term in enumerate(terms):
        if not isinstance(term, dict):
            continue
        for field in ("en", "zh", "module"):
            value = term.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append(f"terms[{i}]: empty or non-string {field}")
        if isinstance(term.get("en"), str) and term["en"].startswith("!!"):
            problems.append(
                f'terms[{i}]: token key {term["en"]!r} must live in tokens.json, not terms.json'
            )
        if "note" in term and not isinstance(term["note"], str):
            problems.append(f"terms[{i}]: note not string")
    for module in {
        term.get("module") for term in valid_terms if isinstance(term.get("module"), str)
    }:
        if module not in ("core", "modal-logic"):
            problems.append(f"unexpected module: {module!r}")
    if not isinstance(doc.get("context"), dict):
        problems.append('terms.json: "context" missing or not object')
    return problems, len(terms)


def validate_tokens(tokens_path=TOKENS, sty_path=STY):
    problems = []
    try:
        doc = load_json(tokens_path)
    except FileNotFoundError:
        return [f"{tokens_path} not found"], 0
    except ValueError as exc:
        return [f"{tokens_path}: invalid JSON ({exc})"], 0

    if not isinstance(doc, dict):
        return [f"{tokens_path}: root must be an object"], 0
    tokens = doc.get("tokens", {})
    if not isinstance(tokens, dict):
        return [f'{tokens_path}: "tokens" must be an object'], 0
    for key, value in tokens.items():
        if not re.fullmatch(r"!!\{[^{}\r\n]+\}", key):
            problems.append(f"{tokens_path}: invalid token key {key!r}")
        if not isinstance(value, str) or not value.strip():
            problems.append(
                f"{tokens_path}: token {key!r} has an empty or non-string Chinese value"
            )
    try:
        sty = sty_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        problems.append(f"{sty_path} not found")
        return problems, len(tokens)
    sty_tokens, sty_problems = parse_sty_tokens(sty, sty_path)
    problems.extend(sty_problems)
    problems.extend(compare_token_maps(tokens, sty_tokens))
    return problems, len(tokens)


def validate_index(path=INDEX):
    problems = []
    try:
        doc = load_json(path)
    except FileNotFoundError:
        return [f"{path} not found"], 0
    except ValueError as exc:
        return [f"{path}: invalid JSON ({exc})"], 0

    if not isinstance(doc, dict):
        return [f"{path}: root must be an object"], 0
    if "entries" not in doc:
        return [f'{path}: "entries" missing'], 0
    entries = doc["entries"]
    if not isinstance(entries, list):
        return [f'{path}: "entries" must be a list'], 0

    seen_entries = {}
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            problems.append(f"index[{i}]: entry must be an object")
            continue
        for field in ("line", "zh", "en", "pages", "sub"):
            if field not in entry:
                problems.append(f"index[{i}]: missing field {field}")
        if "line" in entry:
            if type(entry["line"]) is not int or entry["line"] <= 0:
                problems.append(f"index[{i}]: line must be a positive integer")
        for field in ("zh", "en", "pages"):
            if field in entry and not isinstance(entry[field], str):
                problems.append(f"index[{i}]: {field} must be a string")
        if "sub" in entry and not isinstance(entry["sub"], bool):
            problems.append(f"index[{i}]: sub not bool")
        key = json.dumps(entry, ensure_ascii=False, sort_keys=True)
        if key in seen_entries:
            problems.append(
                f"index[{i}]: duplicate entry of index[{seen_entries[key]}]"
            )
        else:
            seen_entries[key] = i
    return problems, len(entries)


def validate():
    problems = []
    term_problems, term_count = validate_terms()
    token_problems, _ = validate_tokens()
    index_problems, index_count = validate_index()
    problems.extend(term_problems)
    problems.extend(token_problems)
    problems.extend(index_problems)
    return problems, term_count, index_count


def main():
    problems, term_count, index_count = validate()
    if problems:
        print("FAIL")
        for problem in problems:
            print(f" - {problem}")
        return 1
    print(f"OK: terms.json {term_count} terms, index {index_count} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
