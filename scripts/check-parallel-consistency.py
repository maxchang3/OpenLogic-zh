#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""找出平行章节中「英文源相似但中文译文不一致」的段落对。

原理：OpenLogic 上游有大量复制修改的平行章节（如 normal-modal-logic/tableaux
与 intuitionistic-logic/tableaux）。英文源段落相似度高于阈值、而对应中文
译文段落相似度明显更低时，说明两边译法可能不一致，输出候选供人工/子代理裁决。

用法：python3 scripts/check-parallel-consistency.py [min_ratio]
"""
import difflib
import glob
import os
import re
import sys

ZH_ROOT = 'locale/zh/content'
EN_ROOT = 'content'
MIN_EN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.75
MIN_DROP = 0.15  # 中文相似度至少比英文低这么多才算候选

def fold(s: str) -> str:
    """折叠空白：段落内换行/缩进 -> 空格，去掉多余空格。"""
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def paras(path: str):
    """按空行分块，折叠空白；跳过纯注释/结构块。"""
    if not os.path.exists(path):
        return []
    text = open(path, encoding='utf-8').read()
    out = []
    for blk in text.split('\n\n'):
        blk = fold(blk)
        if not blk or blk.startswith('%'):
            continue
        # 跳过纯结构块（如只有 \begin{document}）
        if re.match(r'^\\(begin|end|documentclass|olfileid|olsection)', blk):
            continue
        out.append(blk)
    return out

def ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def main():
    zh_files = sorted(glob.glob(f'{ZH_ROOT}/**/*.tex', recursive=True))
    zh_files = [f for f in zh_files if 'wo/empty' not in f]
    # 同名文件分组
    by_name = {}
    for f in zh_files:
        name = os.path.basename(f)
        by_name.setdefault(name, []).append(f)

    candidates = []
    seen_pairs = set()
    for name, group in by_name.items():
        if len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                fa, fb = group[i], group[j]
                key = tuple(sorted((fa, fb)))
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                en_a = paras(os.path.join(EN_ROOT, os.path.relpath(fa, ZH_ROOT)))
                en_b = paras(os.path.join(EN_ROOT, os.path.relpath(fb, ZH_ROOT)))
                zh_a = paras(fa)
                zh_b = paras(fb)
                n = min(len(en_a), len(en_b), len(zh_a), len(zh_b))
                for k in range(n):
                    er = ratio(en_a[k], en_b[k])
                    if er < MIN_EN:
                        continue
                    zr = ratio(zh_a[k], zh_b[k])
                    if er - zr >= MIN_DROP:
                        candidates.append((er, zr, fa, fb, k, en_a[k], zh_a[k], zh_b[k]))

    candidates.sort(key=lambda c: -(c[0] - c[1]))
    print(f'候选不一致段落对：{len(candidates)}（英文相似 >= {MIN_EN}，中文落差 >= {MIN_DROP}）\n')
    for er, zr, fa, fb, k, en, za, zb in candidates:
        print('=' * 100)
        print(f'EN sim {er:.2f} / ZH sim {zr:.2f}  段 {k}')
        print(f'  A: {fa}')
        print(f'  B: {fb}')
        print(f'  EN: {en[:160]}')
        print(f'  ZH A: {za[:160]}')
        print(f'  ZH B: {zb[:160]}')

if __name__ == '__main__':
    main()
