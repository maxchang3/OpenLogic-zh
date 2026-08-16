#!/usr/bin/env python3
"""机械校验：每个 content/<rel> 与 locale/zh/content/<rel> 的令牌完全一致。

用法：python3 scripts/check-tokens.py [--quiet]
- 折叠空白后统计完整令牌（冠词变体 + 键名）：!!{formula}、!!a{formula}、
  !!^{formula}、!!^a{formula} 互不相同，英文源与译文必须一一对应
  （POLICY：冠词变体空/a/^/^a 必须与英文原文一一对应）。
- 注意：英文令牌可跨行（!!{signed\\n formula}），必须先折叠空白再匹配。
- 退出码：0 = 全部一致；1 = 有差异。
"""
import re, glob, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tokens(text):
    flat = re.sub(r'\s+', ' ', text)
    return Counter(re.findall(r'!!(\^?[a-zA-Z])?\{([a-z ]+)\}', flat))

def show(c):
    """把 (prefix, key) 计数渲染为可读的 !!a{key}: n 形式。"""
    return {f'!!{p or ""}{{{k}}}': n for (p, k), n in c.items()}

def main():
    quiet = '--quiet' in sys.argv
    diffs = []
    for en in sorted(glob.glob(os.path.join(ROOT, 'content', '**', '*.tex'), recursive=True)):
        rel = os.path.relpath(en, os.path.join(ROOT, 'content'))
        zh = os.path.join(ROOT, 'locale', 'zh', 'content', rel)
        if not os.path.exists(zh):
            continue
        ec, zc = tokens(open(en, encoding='utf-8').read()), tokens(open(zh, encoding='utf-8').read())
        if ec != zc:
            miss = {k: ec[k]-zc.get(k, 0) for k in ec if ec[k] > zc.get(k, 0)}
            extra = {k: zc[k]-ec.get(k, 0) for k in zc if zc[k] > ec.get(k, 0)}
            diffs.append((rel, show(miss), show(extra)))
    if diffs:
        for rel, miss, extra in diffs:
            print(f'{rel}: 缺 {miss or "-"} | 多 {extra or "-"}')
        print(f'FAIL: {len(diffs)} 个文件令牌不一致')
        return 1
    if not quiet:
        print('OK: 全部文件的令牌（含冠词变体）计数一致')
    return 0

if __name__ == '__main__':
    sys.exit(main())
