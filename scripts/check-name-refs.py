#!/usr/bin/env python3
"""Check zh name-macro keys against EN source name references.

Person names with the same surname (e.g. C. I. Lewis vs David K.
Lewis) are easy to mix up in translation. This script checks every
translated file in three layers:

1. Same-file contradiction: if the EN file contains a full name of
   person A (e.g. "C. I. Lewis") but the zh translation uses a macro
   key for person B with the same surname (e.g. David K. Lewis)
   without B's full name ever appearing in that EN file, the zh key
   is wrong. (This catches the paradoxes-material case.)
2. Knowledge base: some passages only use a bare surname in EN, so no
   automatic referent can be derived; KNOWLEDGE records passages whose
   referent is historically fixed (e.g. "Lewis introduced the strict
   conditional" = C. I. Lewis). A mismatch there is an error.
3. Unresolved: everything else is reported as info (exit 0) for human
   review, not as a failure.

Run from the OpenLogic-Zh repo root:
    python3 scripts/check-name-refs.py
"""
import glob
import json
import os
import re
import sys


def norm(s):
    """Fold whitespace, ~, and common LaTeX escapes so name matching works."""
    s = s.replace('~', ' ')
    s = s.replace(r'\"o', 'ö').replace(r'\"a', 'ä').replace(r'\"u', 'ü')
    s = s.replace(r"\'e", 'é').replace(r"\'a", 'á')
    s = re.sub(r'\\[a-zA-Z]+', '', s)  # drop remaining macros
    s = s.replace('{', ' ').replace('}', ' ')
    s = re.sub(r'\s+', ' ', s)
    return s


def surname_of(full):
    return full.split()[-1].rstrip('.')


# ambiguous surname groups: surname -> {full name -> normalized form}
terms = json.load(open('.agents/translation/terminology/terms.json', encoding='utf-8'))
groups = {}
for t in terms['terms']:
    en = t['en']
    if '人名' not in t.get('note', ''):
        continue
    if ' ' not in en:
        continue
    groups.setdefault(surname_of(en), {})[en] = norm(en)

# 知识库：EN 只用裸姓、但指代由历史/上下文固定的段落。
# 键为 (相对路径, 归一化 EN 片段子串)；值为该处应有的全名宏键。
# 命中且 zh 宏键不符 → 报错；相符 → 静默通过（不再报"未定"）。
# 新增此类场景时在此登记。
KNOWLEDGE = {
    # 严格条件句由 C. I. Lewis 引入（1918），非 David K. Lewis
    ('counterfactuals/introduction/strict-conditional.tex',
     'Lewis introduced the strict conditional'): 'C. I. Lewis',
    # 批评实质条件句、与 Whitehead/Russell 同时代的是 C. I. Lewis
    ('counterfactuals/introduction/paradoxes-material.tex',
     'C. I. Lewis'): 'C. I. Lewis',
}
# 安全默认：反事实条件句语境中的裸姓 Lewis/Stalnaker 是 David K.
# Lewis / Robert Stalnaker（两人共同开创最小变化语义）。命中即静默通过。
SAFE_DEFAULT = [
    ('counterfactuals', 'Lewis', 'David K. Lewis'),
    ('counterfactuals', 'Stalnaker', 'Robert Stalnaker'),
]

MACRO = re.compile(r'\\zh(?:First|FullName)\{([^{}]*)\}')


def check_file(rel):
    en_raw = open('content/' + rel, encoding='utf-8').read()
    zh = open('locale/zh/content/' + rel, encoding='utf-8').read()
    en_paras = [norm(p) for p in re.split(r'\n\s*\n', en_raw) if p.strip()]
    zh_paras = [p for p in re.split(r'\n\s*\n', zh) if p.strip()]
    errors, infos = [], []
    en_joined = ' '.join(en_paras)

    # 层 1：同文件矛盾 —— EN 中出现全名 A，zh 却用同姓 B 且 B 全名未出现
    if len(en_paras) == len(zh_paras):
        current = {}  # surname -> full name
        for i, (ep, zp) in enumerate(zip(en_paras, zh_paras)):
            for surname, fulls in groups.items():
                for fn, fn_n in fulls.items():
                    if fn_n in ep:
                        current[surname] = fn
            for m in MACRO.finditer(zp):
                key = m.group(1).strip()
                surname = surname_of(key)
                if surname not in groups or key in BARE_OK:
                    continue
                if key not in groups[surname]:
                    continue
                cur = current.get(surname)
                if cur is None:
                    # 只有同姓多人组（如 Lewis）的未定项才需要人工复核；
                    # 单姓人名（Stalnaker/Kripke…）EN 只用姓氏是正常现象。
                    if len(groups[surname]) > 1:
                        infos.append((rel, i + 1, key, '未定',
                                      '同姓多人组，EN 该文件内无全名先例，需人工复核指代'))
                elif cur != key:
                    errors.append((rel, i + 1, key, cur, '同文件指代矛盾'))
    else:
        # 段落数不一致时的文件级回退
        en_fullnames = set()
        for surname, fulls in groups.items():
            for fn, fn_n in fulls.items():
                if fn_n in en_joined:
                    en_fullnames.add(fn)
        for i, zp in enumerate(zh_paras, 1):
            for m in MACRO.finditer(zp):
                key = m.group(1).strip()
                surname = surname_of(key)
                if surname not in groups or key in BARE_OK:
                    continue
                if key not in groups[surname]:
                    continue
                if key not in en_fullnames:
                    if len(groups[surname]) > 1:
                        infos.append((rel, i, key, '未定',
                                      '同姓多人组，段落数不一致且 EN 无该全名，人工复核'))

    # 层 2：知识库（错误）与安全默认（静默）
    if len(en_paras) == len(zh_paras):
        for i, zp in enumerate(zh_paras, 1):
            for m in MACRO.finditer(zp):
                key = m.group(1).strip()
                surname = surname_of(key)
                for (krel, frag), expect in KNOWLEDGE.items():
                    if krel == rel and frag in en_joined and surname == surname_of(expect):
                        if key != expect:
                            errors.append((rel, i, key, expect, '知识库：该处应为 ' + expect))
                        else:
                            infos = [x for x in infos if not (x[0] == rel and x[1] == i and x[2] == key)]
                # KNOWLEDGE 锁定的姓氏（如 paradoxes-material 的 Lewis=C. I.）不受 SAFE_DEFAULT 干扰
                kb_locked = any(krel == rel and frag in en_joined and surname == surname_of(expect)
                                for (krel, frag), expect in KNOWLEDGE.items())
                for (krel, frag, expect) in SAFE_DEFAULT:
                    if krel in rel and surname == surname_of(expect) and not kb_locked:
                        if key == expect:
                            infos = [x for x in infos if not (x[0] == rel and x[1] == i and x[2] == key)]
                        else:
                            errors.append((rel, i, key, expect, '安全默认：该处应为 ' + expect))
    return errors, infos


# single-surname keys that are fine as bare zhFirst keys
BARE_OK = {'Kripke', 'Lewis', 'Stalnaker', 'Langford', 'Brouwer', 'Heyting',
           'Kolmogorov', 'Russell', 'Hilbert', 'Frege', 'Gödel', 'Tarski',
           'Cantor', 'Carnap', 'Hintikka', 'Skolem', 'Leibniz', 'Whitehead',
           'Dummett', 'Prior', 'Goethe', 'Warren', 'Wiener', 'Kuratowski',
           'Bishop', 'Beth', 'Smullyan', 'Antonelli', 'Yap', 'Kratzer',
           'Beezie', 'Adams', 'Dana', 'Oswald', 'Kennedy', 'Hoover',
           'Jaakko', 'Evert', 'Raymond', 'Alfred', 'Bertrand', 'Michael',
           'Robert', 'David', 'Rudolf', 'Saul', 'Arthur', 'Richard',
           'Audrey', 'Edgar', 'Harvey', 'John', 'Lee', 'Ruth', 'Kurt',
           'C.', 'I.', 'K.', 'L.', 'E.', 'J.', 'F.', 'A.', 'P.', 'R.',
           'M.', 'N.', 'O.', 'S.', 'H.', 'Bernays', 'Fraenkel',
           'Zermelo', 'Peano', 'Dedekind', 'Kleene', 'Post', 'Church',
           'Gentzen', 'Turing', 'Lindenbaum', 'Clarence', 'Irving',
           'Ernest', 'Gottlob', 'L. E. J.'}


def main():
    errors, infos = [], []
    for zh in sorted(glob.glob('locale/zh/content/**/*.tex', recursive=True)):
        if 'wo/empty' in zh:
            continue
        rel = zh.replace('locale/zh/content/', '')
        if not os.path.exists('content/' + rel):
            continue
        e, i = check_file(rel)
        errors += e
        infos += i
    if errors:
        print('人名指代错误（必须修正）：')
        for rel, para, key, ref, why in errors:
            print(f'  {rel}: 段落 {para} | 宏键 {key} | 应为 {ref} | {why}')
        sys.exit(1)
    if infos:
        print('人名指代待人工复核（信息，不阻断）：')
        for rel, para, key, ref, why in infos:
            print(f'  {rel}: 段落 {para} | 宏键 {key} | {why}')
    print('OK: 无同文件指代矛盾')


if __name__ == '__main__':
    main()
