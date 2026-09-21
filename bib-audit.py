#!/usr/bin/env python3
"""Audit the thesis bibliography for deviations from the conventions in AGENTS.md.

Usage:  python3 bib-audit.py            # audit entries cited by main.tex (needs main.bcf from a build)
        python3 bib-audit.py --all      # audit every entry in the .bib files

Reports, per convention: duplicate titles or DOIs across files, web resources without an author or
access date, the obsolete `lastaccessed` field, `note={Accessed ...}`, arXiv preprints not in the
DBLP shape, journal articles without a DOI, sentence-case titles, DBLP housekeeping fields, and
`and others` in author lists. Exit status is 1 when anything is reported.
"""
import re, sys, collections, os

FILES = ['references.bib', 'references-tutorial.bib', 'references-pinning.bib',
         'references-fake-stars.bib', 'references-cursor.bib']
ROOT = os.path.dirname(os.path.abspath(__file__))


def entries(path):
    txt = open(path, encoding='utf-8').read()
    prev_end = 0
    for m in re.finditer(r'@(\w+)\s*\{\s*([^,\s]+)\s*,', txt):
        if m.group(1).lower() in ('comment', 'string', 'preamble'):
            continue
        comment = ' '.join(l.strip() for l in txt[prev_end:m.start()].splitlines() if l.strip().startswith('%'))
        i = m.end(); d = 1; j = i
        while j < len(txt) and d > 0:
            d += (txt[j] == '{') - (txt[j] == '}'); j += 1
        body = txt[i:j - 1]; fields = {}
        for fm in re.finditer(r'(\w+)\s*=\s*(\{(?:[^{}]|\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})*\}|"[^"]*"|[^,\n]+)', body):
            v = fm.group(2).strip()
            if v[:1] in '{"':
                v = v[1:-1]
            fields[fm.group(1).lower()] = ' '.join(v.split())
        prev_end = j
        yield dict(file=os.path.basename(path), type=m.group(1).lower(), key=m.group(2), fields=fields, comment=comment)


def cited_keys():
    bcf = os.path.join(ROOT, 'main.bcf')
    if not os.path.exists(bcf):
        sys.exit('main.bcf not found; build the thesis first or pass --all')
    return set(re.findall(r'<bcf:citekey[^>]*>([^<]+)</bcf:citekey>', open(bcf, encoding='utf-8').read()))


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', re.sub(r'[{}\\]', '', s).lower())


def sentence_case(title):
    words = [w for w in re.findall(r'\b[A-Za-z][a-z]+\b', re.sub(r'\{[^}]*\}', '', title))[1:] if len(w) > 3]
    return bool(words) and sum(w[0].isupper() for w in words) / len(words) < 0.5


def main():
    only = None if '--all' in sys.argv else cited_keys()
    E = [e for f in FILES for e in entries(os.path.join(ROOT, f)) if only is None or e['key'] in only]
    problems = collections.defaultdict(list)
    by_title = collections.defaultdict(list); by_doi = collections.defaultdict(list)
    for e in E:
        f = e['fields']; k = f"{e['file']}:{e['key']}"
        first = norm(f.get('author', '').split(' and ')[0].split(',')[0])
        if 'title' in f: by_title[norm(f['title'])[:60]].append((k, f.get('year', ''), first))
        if 'doi' in f: by_doi[f['doi'].lower()].append(k)
        if 'lastaccessed' in f: problems['lastaccessed field (use urldate)'].append(k)
        if re.search(r'Accessed\s+\d{4}', f.get('note', '')): problems['note={Accessed ...} (use urldate)'].append(k)
        if any(x in f for x in ('timestamp', 'biburl', 'bibsource')): problems['DBLP housekeeping fields'].append(k)
        if 'and others' in f.get('author', ''): problems['"and others" in author list'].append(k)
        if e['type'] in ('online', 'misc'):
            if 'author' not in f and 'organization' not in f: problems['web resource without author'].append(k)
            if 'urldate' not in f: problems['web resource without urldate'].append(k)
            if 'url' not in f: problems['web resource without url'].append(k)
        j = f.get('journal', ''); n = f.get('note', '')
        if 'arxiv preprint' in j.lower() or 'arxiv preprint' in n.lower() or e['type'] == 'unpublished':
            problems['arXiv preprint not in DBLP shape (journal=CoRR/arXiv, volume=abs/..., eprint)'].append(k)
        if j in ('CoRR', 'arXiv') and not f.get('volume', '').startswith('abs/'):
            problems['arXiv entry without volume=abs/...'].append(k)
        is_arxiv = j in ('CoRR', 'arXiv')
        no_doi_ok = re.search(r'no doi', e['comment'], re.I)
        if e['type'] == 'article' and not is_arxiv and 'doi' not in f and not no_doi_ok:
            problems['journal article without DOI (add one, or a "% No DOI" comment above the entry)'].append(k)
        if e['type'] == 'inproceedings' and 'pages' not in f and 'doi' not in f and 'url' not in f:
            problems['conference paper without pages, DOI, or URL'].append(k)
        if e['type'] not in ('online', 'misc') and 'title' in f and sentence_case(f['title']):
            problems['sentence-case title'].append(k)
        if 'url' in f and re.search(r'^https?://(dx\.)?doi\.org/', f['url']) and 'doi' in f:
            pass  # harmless: URLs are not printed for non-web entries
    for t, ks in by_title.items():
        # the same title in different years by different first authors is a replication, not a duplicate
        if len(ks) > 1 and (len({y for _, y, _ in ks}) < len(ks) or len({a for _, _, a in ks}) < len(ks)):
            problems['same title under several keys'].append(' == '.join(k for k, _, _ in ks))
    for d, ks in by_doi.items():
        if len(ks) > 1: problems['same DOI under several keys'].append(' == '.join(ks))
    total = 0
    for name, ks in sorted(problems.items()):
        total += len(ks)
        print(f'[warn] {name}: {len(ks)}')
        for k in ks: print('       ', k)
    print(f'{len(E)} entries audited, {total} problems')
    sys.exit(1 if total else 0)


if __name__ == '__main__':
    main()
