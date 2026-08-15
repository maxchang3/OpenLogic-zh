#!/usr/bin/env python3
"""机械校验：每个 content/<rel> 与 locale/zh/content/<rel> 的 !!{token} 计数一致。

用法：python3 scripts/check-tokens.py [--quiet]
- 折叠空白后统计令牌键名（!!{formula}、!!a{formula}、!!^{formula}、!!^a{formula} 键名均为 formula）。
- 注意：英文令牌可跨行（!!{signed\\n formula}），必须先折叠空白再匹配。
- 退出码：0 = 全部一致；1 = 有差异。
"""
import re, glob, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tokens(text):
    flat = re.sub(r'\s+', ' ', text)
    return Counter(re.findall(r'!!(?:\^?[a-zA-Z])?\{([a-z ]+)\}', flat))

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
            diffs.append((rel, miss, extra))
    if diffs:
        for rel, miss, extra in diffs:
            print(f'{rel}: 缺 {miss or "-"} | 多 {extra or "-"}')
        print(f'FAIL: {len(diffs)} 个文件令牌不一致')
        return 1
    if not quiet:
        print('OK: 全部文件的令牌键名计数一致')
    return 0

if __name__ == '__main__':
    sys.exit(main())
