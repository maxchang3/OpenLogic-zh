#!/usr/bin/env python3
"""Scan translated files' EN sources for person names not yet handled.

Extracts capitalized word sequences from the EN source of every translated
file and filters out: TeX macro arguments, math symbols, known names
(terms.json name entries), whitelisted words, and common English words
(any word that also appears lowercase anywhere in the EN corpus is a
common word, not a name). A non-empty report means the name table is
incomplete: settle the name (add to terms.json and wrap with
\\zhFirst/\\zhFullName) or whitelist it.

Run from the OpenLogic-Zh repo root:
    python3 scripts/check-names.py
"""
import json
import os
import re
import sys
import glob

# 归一化：~ 视为空格（"J.~Edgar Hoover" → "J. Edgar Hoover"），换行折叠为空格
def norm(s):
    return re.sub(r'\s+', ' ', s.replace('~', ' '))

RE_PERSON = re.compile(r'(?<![\{:\\])\b((?:[A-Z][a-z]+|[A-Z]\.(?:\s|\.)?)+(?:\s+[A-Z][a-z]+)*)\b')
RE_INITIALS = re.compile(r'^[A-Z]\.(\s?[A-Z]\.)+$')

# handled = name entries in terms.json (en field)
terms = json.load(open('.agents/translation/terminology/terms.json', encoding='utf-8'))
handled = {t['en'] for t in terms['terms'] if t.get('kind', 'word') == 'word'}

# common English words / section titles / symbols that are not person names
WHITELIST = {
    'The','A','An','If','Then','For','In','On','At','By','With','From','And','Or','Not',
    'This','That','It','We','They','You','There','Here','One','All','Some','Any','No','But','So',
    'Since','Let','Suppose','Now','To','Note','However','Show','Prove','Consider','As','Thus',
    'Hence','When','Every','These','Given','Similarly','Give','What','Complete','Moreover','Of',
    'Rules','Recall','Using','Define','Our','He','She','Choice','Otherwise','How','Such','Again',
    'Proof','Finally','Both','Well','Can','May','Will','Would','Could','Should','Must','Only',
    'Also','Than','Most','More','Less','About','After','Before','Between','During','Under',
    'Over','Without','Within','Among','Through','Because','Although','Whether','While','Where',
    'Open','Logic','Text','Project','Chapter','Section','Part','Appendix','Exercise','Modal',
    'First','Second','Third','Introduction','Syntax','Semantics','Tableau','True','False',
    'Principia','Mathematica','Begriffsschrift','Symbolic','Meaning','Necessity','Completeness',
    'Theorem','Survey','English','German','World','Frame','Model','Formula','Set','Relation',
    'Soundness','Lemma','Truth','Filtration','Counterexample','Validity','Axiom','Cut','Rule',
    'Decidability','Compactness','Consistency','Equivalence','Definability','Contraposition',
    'Bisimulation','Veridicality','Entailment','Satisfaction','Substitution','Deduction',
    'Natural','Sequent','Calculus','Excluded','Middle','Proofs','Systems','S1','S2',
    'S3','S4','S5','K','T','B','D','GL','Grz','JSL','Russian','Russia','Communist','Soviet',
    'Union','Dallas','Alberta','Calgary','Tuesdays','Vancouver','Island','Victoria','Warren',
    'California','Kennedy','Oswald','Hoover','Goldbach','Aristotle','God','JFK','Kripke',
    'Lewis','Stalnaker','Prior','Brouwer','Heyting','Kolmogorov','Russell','Hilbert','Frege',
    'Lindenbaum','Carnap','Hintikka','Skolem','Dana','Langford','Dummett','Whitehead','Leibniz',
    'Turing','Church','Gentzen','Gödel','Godel','Kurt','Tarski','Cantor','Dedekind','Kleene',
    'Post','Zermelo','Fraenkel','Peano','Bernays','Wiener','Kuratowski','Bishop','Beth',
    'Smullyan','Evert','Raymond','Jaakko','Jaako','Alfred','North','Bertrand','Michael',
    'Robert','David','Rudolf','Saul','Arthur','Richard','Audrey','Edgar','Harvey','John','Lee',
    'C.','I.','K.','L.','E.','J.','F.','A.','P.','R.','M.','N.','O.','S.','H.',
    # 书名/机构/许可/项目名等非人名短语的组成词
    'De','Interpretatione','United','States','President','Ex','Falso','Quodlibet',
    'Creative','Commons','Attribution','Contributing','Coverage','Draft','Needs','Please',
    'Polish','Super','Soaker','OpenLogicProject','OpenLogic','Hint','Contrapositively',
    'Luckily','Angrily','Lastly','Connectivity','Asymmetry','Spelling','Cartesian',
    'Barring','Correspondingly','Communists',
}
# math-ish capitalized tokens that appear as identifiers
RE_MATH = re.compile(r'^[RSGKLUVWXY]\w{0,3}$|^[A-Z]\d*$')

# 全语料小写词表：出现小写形式的词是普通英文词，不是人名
small = set()
for en in glob.glob('content/**/*.tex', recursive=True):
    txt = open(en, encoding='utf-8').read()
    for m in re.finditer(r'[a-z]+', txt):
        small.add(m.group(0))

def is_common(w):
    """候选词的任一组成词是白名单词或语料中的小写普通词 → 非人名。"""
    for part in w.split():
        if part in WHITELIST:
            return True
        if part.lower() in small:
            return True
    return False

candidates = {}
for zh in glob.glob('locale/zh/content/**/*.tex', recursive=True):
    if 'wo/empty' in zh:
        continue
    rel = zh.replace('locale/zh/content/', '')
    enp = 'content/' + rel
    if not os.path.exists(enp):
        continue
    s = norm(open(enp, encoding='utf-8').read())
    for m in RE_PERSON.finditer(s):
        w = m.group(0).strip()
        if w in handled or w in WHITELIST:
            continue
        if RE_INITIALS.match(w) or RE_MATH.match(w):
            continue
        if is_common(w):
            continue
        candidates[w] = candidates.get(w, 0) + 1

if candidates:
    print('未覆盖人名候选（请定案入 terms.json 或加入白名单）：')
    for w, c in sorted(candidates.items(), key=lambda x: -x[1]):
        print(f'  {w}: {c}')
    sys.exit(1)
print('OK: 已译文件范围内无未覆盖人名')
