#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把中文译文正文段落重排为一段一行（POLICY 第 6 条），并清理中文之间的多余空格。

规则：
- 按空行分块；块内只有散文行时折叠为一行（换行折叠为空格）。
- 结构行原样保留：\\begin/\\end、数学块（\\[ \\] $$）、\\item/\\intertext/\\tagitem、
  注释行（行首 %）、含行尾 % 的行（折叠会破坏 % 注释）。
- 折叠后清理「中文/中文标点」与「中文/宏/令牌/数学」之间的多余空格；
  英文单词之间的空格、~ 硬空格保留。

用法：python3 scripts/reflow-paragraphs.py [file.tex ...]   （默认全部 locale/zh/content）
"""
import glob
import re
import sys

CJK = r'\u4e00-\u9fff'
CJK_PUNCT = r'\u3001\u3002\uff0c\uff1b\uff1a\uff1f\uff01\uff09\u300d\u300f\u3011'  # 、。，；：？！）」』】
CJK_OPEN = r'\u300c\u300e\u3010\uff08\u300a\u3008'  # 「『【（《〈

# 中文与中文/标点/宏/令牌/数学之间的多余空格
CLEANUPS = [
    re.compile(rf'(?<=[{CJK}{CJK_PUNCT}]) +(?=[{CJK}{CJK_PUNCT}{CJK_OPEN}\\!!$])'),
    re.compile(rf'(?<=[{CJK}]) +(?=[{CJK}{CJK_PUNCT}{CJK_OPEN}])'),
    re.compile(r' +$'),
]

STRUCT_RE = re.compile(
    r'^\s*(%|\\(begin|end)\{|\item\b|\intertext|\tagitem|\[$|\]|$$|\olsection|\caption)'
)

def is_struct(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith('%'):
        return True
    if STRUCT_RE.match(s):
        return True
    # 行尾 % 注释（非行首）会破坏折叠，作为结构行保留
    stripped = re.sub(r'\\%', '', s)
    if re.search(r'[^\\]%.+$', stripped):
        return True
    return False

def clean(text: str) -> str:
    for rx in CLEANUPS:
        text = rx.sub('', text)
    return text

def reflow(path: str) -> str:
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    buf = []
    def flush():
        nonlocal buf
        if not buf:
            return
        if len(buf) == 1:
            out.append(clean(buf[0].strip()))
        else:
            joined = ' '.join(l.strip() for l in buf)
            out.append(clean(joined))
        buf = []
    for line in lines:
        if line.strip() == '':
            flush()
            out.append('')
        elif is_struct(line):
            flush()
            out.append(line)
        else:
            buf.append(line)
    flush()
    return '\n'.join(out) + '\n'

def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = glob.glob('locale/zh/content/**/*.tex', recursive=True)
    files = [f for f in files if 'wo/empty' not in f]
    for f in files:
        new = reflow(f)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        print(f'reflowed {f}')

if __name__ == '__main__':
    main()
