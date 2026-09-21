# Reference Formatting Consistency Plan

**Status:** Executed (2026-09-21). See the "Outcome" section at the end.

## Problem

The thesis bibliography renders 449 cited entries from five `.bib` files that originated in four separate papers.
The entries come from three sources with different conventions---verbatim DBLP exports, hand-written Google-Scholar-style entries, and hand-written web resources---and biblatex's `numeric` style prints each entry as it finds it.
The result is a visibly inconsistent reference list.

## Audit (2026-09-21)

All counts are over the 449 cited entries after building `main.tex`.

| Inconsistency | Extent | Where it comes from |
|---|---|---|
| Conference venues | 82 of 121 `booktitle` values are DBLP long form ("…Conference…, SANER 2020, London, ON, Canada, February 18-21, 2020"); the rest carry only the venue name; one is "Proc. of NDSS" | DBLP exports vs. hand entries |
| Journal names | 52 abbreviated ("IEEE Trans. Software Eng.", "Empir. Softw. Eng.") vs. 131 spelled out | DBLP abbreviates; hand entries do not |
| Title casing | 292 Title Case vs. 133 sentence case, 13 mixed | DBLP uses Title Case; Google Scholar exports use sentence case |
| arXiv preprints | four renderings: "In: CoRR abs/… . arXiv: … . url: …" (14), "In: arXiv abs/…" (23), "In: arXiv preprint arXiv:…" (2), `@unpublished` with `note={arXiv preprint …}` (4) | DBLP `journal={CoRR}`, edited DBLP `journal={arXiv}`, Scholar `journal={arXiv preprint …}`, tutorial `@unpublished` |
| Web resources | 77 entries; 73 use `lastaccessed`, which biblatex does not know and silently drops, so no access date is printed; 4 use `note={Accessed …}`; 43 have no author, so the entry starts with the title ("AI \| 2024 Stack Overflow Developer Survey. 2025. url: …") | pinning, fake-stars, cursor bibs vs. tutorial bib |
| DOI + URL redundancy | 125 entries print both `doi: 10.…` and `url: https://doi.org/10.…` | DBLP exports carry both fields |
| Missing metadata | 62 journal articles without a DOI; 8 conference papers without pages; 3 stray ISBNs | hand entries |
| Duplicates | 7 papers cited under two keys (see below); the two Renovate entries point at the same page | the same paper cited from different chapters |
| Housekeeping noise | 181 entries carry `timestamp`, `biburl`, `bibsource` (not printed, but clutter) | DBLP exports |

### Duplicate pairs (same paper, two keys)

| Paper | Key A (file) | Key B (file) | Keep |
|---|---|---|---|
| He et al., Cursor study | `DBLP:journals/corr/abs-2511-04427` (references.bib) | `DBLP:conf/msr/HeMAKV26` (tutorial) | MSR'26 key |
| Peng et al., Copilot RCT | `peng2023impact` (tutorial, `@unpublished`) | `DBLP:journals/corr/abs-2302-06590` (cursor) | DBLP key |
| Becker et al., METR study | `becker2025measuring` (tutorial) | `DBLP:journals/corr/abs-2507-09089` (cursor) | DBLP key |
| Cui et al., three field experiments | `cui2025effects` (tutorial, Management Science) | `cui2024effects` (cursor, SSRN) | published version |
| Paradis et al. | `DBLP:conf/icse-seip/ParadisGMNMMZFC25` (tutorial) | `DBLP:journals/corr/abs-2410-12944` (cursor) | ICSE-SEIP key |
| Card & Krueger, minimum wage | `card1994minimum` (tutorial) | `card1993minimum` (cursor) | verify year; AER 1994 is the journal version |
| de Chaisemartin & D'Haultfœuille, TWFE | `dechaisemartin2020two` (tutorial) | `de2020two` (cursor) | one key, Title Case title |
| Renovate pinning docs | `renovate-discussion` (pinning) | `renovate-pinning` (pinning) | one entry |

## Target Conventions

Decide these once and record them in `AGENTS.md` so future entries follow them.

1. **Venues.** Conference `booktitle` in the data is the proceedings name followed by the acronym and year (DBLP's location-and-dates tail may stay); a source map in `main.tex` renders it as "27th IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER 2020)". Journal names are spelled out in full, by a source map for the DBLP abbreviations.
2. **Titles.** Title Case for all titles, with acronyms and proper nouns brace-protected. Title Case is the existing majority (DBLP) and needs no lowercasing of unprotected proper nouns, which is the failure mode of the alternative (`\MakeSentenceCase*`).
3. **arXiv preprints.** One shape in the data, the one DBLP exports: `@article` with `journal={CoRR}` (or `{arXiv}`), `volume={abs/NNNN.NNNNN}`, `eprinttype={arXiv}`, `eprint={NNNN.NNNNN}`, and `year`; a source map in `main.tex` renders every such entry as "Title. 2023. arXiv: 2302.06590" and drops the redundant `10.48550/arXiv...` DOI. A preprint that has since been published is cited by its published version.
4. **Web resources.** `@online` with `author` (the organization or site as a corporate author, e.g. `author={{Stack Overflow}}`), `title`, `year`, `url`, and `urldate={YYYY-MM-DD}`. Rendered with `urldate=iso` as "(visited on 2024-07-09)". This replaces both `lastaccessed` and `note={Accessed …}`; update the `AGENTS.md` example accordingly.
5. **Identifiers.** Print DOIs; print URLs only for `@online` entries; never print ISBNs. Every journal article and conference paper carries a DOI when one exists.
6. **Keys and files.** Unchanged: DBLP keys for CS publications, Scholar-style keys otherwise, one `.bib` per chapter plus `references.bib` for entries cited from more than one chapter.

## Approach

Most of the visible inconsistency can be fixed at the style level in `main.tex`, without touching 449 entries, using biblatex options and `\DeclareSourcemap`.
The remainder is a data-level cleanup done by script with manual review, verified by an audit script.

### Phase A: style-level fixes in `main.tex` (about 2 hours)

- [x] Set options: `maxbibnames=999` (done), `isbn=false`, `url=false`, `doi=true`, `eprint=true`, `urldate=iso`, `giveninits=false`.
- [x] Re-enable URLs for web resources only: `\ExecuteBibliographyOptions[online]{url=true}` (the `url` option is settable per entry type; the `@online` driver goes through the same `doi+eprint+url` macro as every other type, so a global `url=false` alone would hide web URLs too).
- [x] Add a `\DeclareSourcemap` that expands DBLP journal abbreviations to full names via a lookup table (`IEEE Trans. Software Eng.` → `IEEE Transactions on Software Engineering`, `ACM Trans. Softw. Eng. Methodol.` → `ACM Transactions on Software Engineering and Methodology`, `Empir. Softw. Eng.` → `Empirical Software Engineering`, `IEEE Softw.` → `IEEE Software`, `Proc. ACM Softw. Eng.` → `Proceedings of the ACM on Software Engineering`, etc.). Enumerate the 52 abbreviated values from the audit script before writing the table.
- [x] Add a sourcemap step that strips the DBLP location-and-date tail from `booktitle` (regex on `, <City>, <Country>, <Month> <D>-<D>, <YYYY>$` variants). Check the 82 long-form entries afterwards; hand-fix the ones the regex misses.
- [x] Add a sourcemap step that normalizes arXiv entries: when `journal` is `CoRR` or `arXiv` and `volume` matches `^abs/(.+)$`, set `eprinttype=arXiv`, `eprint=\1`, and clear `journal`, `volume`, `url`. Handle the `journal={arXiv preprint arXiv:NNNN}` and `note={arXiv preprint arXiv:NNNN}` shapes the same way.
- [x] Rebuild and confirm: no `url: https://doi.org`, no `In: CoRR`, no ISBNs, full journal names, and web entries still show their URL.

### Phase B: data-level cleanup in the `.bib` files (about 1 day)

- [x] Merge the 8 duplicate pairs above: keep the key in the "Keep" column, update `\cite` keys in the `.tex` files, delete the other entry, and move entries cited from more than one chapter into `references.bib`.
- [x] Convert `lastaccessed={Month D, YYYY}` (73 entries) and `note={Accessed YYYY-MM-DD}` (4 entries) to `urldate={YYYY-MM-DD}` by script; parse the three date formats in use (`December 10, 2023`, `Apr 20, 2025`, ISO).
- [x] Add a corporate `author` to the 43 authorless `@online` entries (the site or organization), so entries no longer begin with the title.
- [x] Fill missing DOIs for the 62 journal articles and missing pages for the 8 conference papers, querying DBLP first and Crossref (title search) second; leave a `% no DOI` comment for entries that genuinely have none (e.g., blog posts filed as articles, which should become `@online`).
- [x] Convert the 133 sentence-case titles to Title Case by script, with brace protection of acronyms and proper nouns; review the diff by hand since automated casing gets small words and hyphenated compounds wrong.
- [x] Strip `timestamp`, `biburl`, `bibsource` from DBLP entries (optional; not printed, but keeps the files readable and diffs small). Keep the DBLP-verbatim rule in `AGENTS.md` for `author`, `title`, `booktitle`, `year`, `doi` only.
- [x] Fix the `@unpublished` and `journal={Available at SSRN …}` entries by citing the published versions found during duplicate merging.
- [x] Update `AGENTS.md`: replace the `note={Accessed …}` example with `urldate`, add the venue, title-case, and arXiv conventions above.

### Phase C: verification (about 1 hour)

- [x] Check in an audit script (`bib-audit.py`, a cleaned-up version of the one used for this audit) that parses the five `.bib` files, restricts to keys in `main.bcf`, and reports: duplicate titles/DOIs, `lastaccessed`, `@online` without `author` or `urldate`, `journal` abbreviations still present, DBLP long-form `booktitle`, arXiv entries not in the canonical shape, articles without DOI, and sentence-case titles.
- [x] Run `biber --validate-datamodel main` and resolve every warning (this is what would have flagged `lastaccessed`).
- [x] Rebuild, extract the bibliography text, and confirm all audit counts are zero.
- [x] Spot-check 20 random entries against DBLP or Crossref for author, title, venue, year, and DOI.
- [x] Commit in three steps (Phase A, Phase B, Phase C) so the style-level changes can be reviewed on their own.

## Notes

- The `numeric` style stays. Switching to `ieee` or `acm` styles would not remove the data-level inconsistencies and would change in-text citation formatting across the whole thesis.
- The pinning chapter's "Chapter Summary" carries the label `sec:data-availability`; the tutorial chapter now uses `sec:tutorial-data-availability`. Unrelated to references, but noticed during the audit.

## Outcome (2026-09-21)

- Phase A landed in `main.tex`: biblatex options (`isbn=false`, `url=false` with `url=true` re-enabled for `@online`, `doi=true`, `eprint=true`, `urldate=iso`) and source maps for journal expansion, DBLP venue reduction, and arXiv normalization. Two facts about `\regexp` matter for anyone editing the maps: it strips spaces (write `\x{20}`), and a raw `&` breaks the XML control file (write `\x26`, and expand ampersand journals in the data instead).
- Phase B rewrote 376 cited entries by script (`lastaccessed`/`note` to `urldate`, DBLP housekeeping fields dropped, corporate or personal authors added to 43 web resources, 66 DOIs and 8 page ranges added, 31 shortened venue names restored, 8 duplicate pairs merged with 23 citation keys renamed in the chapters, 135 titles converted to Title Case). Every DOI, journal name, venue, arXiv id, and web author was checked against Crossref, the arXiv API, or the page itself; DBLP was unreachable to scripts (bot shield), so DBLP-keyed corrections were verified through Crossref by DOI.
- Corrections found along the way: the Nocera et al. MSR 2026 DOI pointed at a different paper; Nakasai et al. is IEEE Software 2019, not 2018; Cui et al. appeared in Management Science in 2026; Ambati et al. was filed under the wrong conference; Wang et al. ICSE 2025 had wrong pages; Wu et al. had a typo in the author list; two web sources (Modulecounts, Phylum) are offline and now cite Wayback Machine copies.
- Phase C: `bib-audit.py` reports zero problems for the cited entries; `biber --validate-datamodel` reports only `publisher` on `@article` entries, which the Google-Scholar convention in `AGENTS.md` deliberately keeps and biblatex never prints. A 20-entry random Crossref spot-check matched on title, first author, year, and pages.
- Not changed: the Reddit post (`cursor-reddit-survey`) has no verifiable author, so it carries `organization={Reddit, r/cursor}` instead; `windsurf.com` now redirects to Devin, and no archived copy exists.
