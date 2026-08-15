#!/usr/bin/env python3
"""Mechanical validation for terminology data files.

Checks:
- terminology/terms.json: structure, empty fields, homograph context notes
- terminology/tokens.json: keys consistent with locale/zh/open-logic-config.sty
- references/wenxuefeng-index.json: entry fields, line coverage

Exits 1 on any problem. Run from the OpenLogic-Zh repo root:
    python3 scripts/check-terms.py
"""
import json
import re
import sys
from collections import Counter

TERMS = '.agents/translation/terminology/terms.json'
TOKENS = '.agents/translation/terminology/tokens.json'
STY = 'locale/zh/open-logic-config.sty'
INDEX = '.agents/translation/references/wenxuefeng-index.json'

problems = []

# ---- terms.json ----
try:
    doc = json.load(open(TERMS, encoding='utf-8'))
except FileNotFoundError:
    problems.append(f'{TERMS} not found (run from OpenLogic-Zh root?)')
    doc = None

if doc is not None:
    terms = doc.get('terms', [])
    if not isinstance(terms, list) or not terms:
        problems.append('terms.json: "terms" missing or empty')
    en_counts = Counter(t.get('en', '') for t in terms)
    for en, n in en_counts.items():
        if n > 1:
            # homographs are allowed only with an explicit context note
            for t in terms:
                if t.get('en') == en and 'note' not in t:
                    problems.append(f'homograph {en!r} x{n}: entry "{t.get("zh")}" lacks context note')
    for i, t in enumerate(terms):
        for field in ('en', 'zh', 'module'):
            if not t.get(field, '').strip():
                problems.append(f'terms[{i}]: empty {field}')
        if t.get('en', '').startswith('!!'):
            problems.append(f'terms[{i}]: token key {t["en"]!r} must live in tokens.json, not terms.json')
        if 'note' in t and not isinstance(t['note'], str):
            problems.append(f'terms[{i}]: note not string')
    mods = {t.get('module') for t in terms}
    for m in mods:
        if m not in ('core', 'modal-logic'):
            problems.append(f'unexpected module: {m!r}')
    if 'context' not in doc or not isinstance(doc.get('context'), dict):
        problems.append('terms.json: "context" missing or not object')

# ---- tokens.json vs open-logic-config.sty ----
try:
    tok = json.load(open(TOKENS, encoding='utf-8'))
    keys = set(tok.get('tokens', {}))
    sty = open(STY, encoding='utf-8').read()
    # keys are bare ("formula") in sty, "!!{formula}" in tokens.json; skip comments
    sty_code = '\n'.join(l for l in sty.split('\n') if not l.strip().startswith('%'))
    sty_keys = {'!!{' + k + '}' for k in re.findall(r'\\zhToken(?:\[[^\]]*\])?\{([^}]*)\}', sty_code)}
    if keys != sty_keys:
        only_json = keys - sty_keys
        only_sty = sty_keys - keys
        if only_json:
            problems.append(f'tokens.json has keys absent from sty: {sorted(only_json)}')
        if only_sty:
            problems.append(f'sty has \\zhToken keys absent from tokens.json: {sorted(only_sty)}')
except FileNotFoundError:
    problems.append(f'{TOKENS} or {STY} not found')

# ---- wenxuefeng-index.json ----
# Lines 521-768 gaps are symbol-index headers/blank pages/standalone glyphs
# (e.g. "本⻚为空白⻚！", "符号索引" page headers), not subject-index entries.
INDEX_GAP_WHITELIST = {521, 522, 528, 579, 587, 650, 652, 662, 703, 705, 706, 714, 724, 725, 751, 768}
try:
    idx = json.load(open(INDEX, encoding='utf-8'))
    entries = idx.get('entries', [])
    lines = Counter(e.get('line') for e in entries)
    missing = [i for i in range(1, 816) if i not in lines]
    missing = [i for i in missing if i not in INDEX_GAP_WHITELIST]
    if missing:
        problems.append(f'index: missing lines {missing}')
    for i, e in enumerate(entries):
        for field in ('line', 'zh', 'en', 'pages', 'sub'):
            if field not in e:
                problems.append(f'index[{i}]: missing field {field}')
        if not isinstance(e.get('sub'), bool):
            problems.append(f'index[{i}]: sub not bool')
except FileNotFoundError:
    problems.append('references/wenxuefeng-index.json not found')

if problems:
    print('FAIL')
    for p in problems:
        print(' -', p)
    sys.exit(1)
print(f'OK: terms.json {len(terms)} terms, index {len(entries)} entries')
