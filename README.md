# Beneath The Shard

A grim-dark solo pen-and-paper RPG for Planet Terramyr. The books are written in XeLaTeX and compile to printable PDFs.

| Book | Source | Output |
|------|--------|--------|
| Core rules | `rules.tex` | `rules.pdf` |
| Bestiary | `bestiary.tex` | `bestiary.pdf` |
| Journey Encounters | `encounters.tex` | `encounters.pdf` |
| Intro adventure — *The Ledger Gate* | `adventure.tex` | `adventure.pdf` |
| Party sheet (XeLaTeX) | `party-sheet.tex` | `party-sheet.pdf` |
| Party sheet (HTML alt.) | `party-sheet.html` | `party-sheet-alt.pdf` |

A themed download page lives at [`index.html`](index.html).

## Requirements

- **XeLaTeX** (TeX Live or MiKTeX) with KOMA-Script (`scrartcl`)
- Packages used by [`preamble.tex`](preamble.tex): `fontspec`, `tcolorbox`, `tabularray`, `tikz`, `fontawesome5`, `imakeidx`, `xcolor`, `geometry`, `booktabs`, `longtable`, `tabularx`, `scrlayer-scrpage`, `ebgaramond`
- **Fonts**
  - [Forum](https://fonts.google.com/specimen/Forum) as `Forum-Regular.otf` (title face; must be findable by `fontspec`)
  - EB Garamond (body)
  - DejaVu Sans Condensed (UI / keywords)
- **JDK 21+** and **Maven 3.8+** (only when regenerating catalog tables from YAML)
- **WeasyPrint** (only for the HTML party-sheet alternative)

On Debian/Ubuntu-style systems:

```bash
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-extra \
  fonts-ebgaramond fonts-dejavu openjdk-21-jdk-headless maven
# Install Forum Regular into ~/.local/share/fonts and run: fc-cache -fv
```

## Regenerate tables (optional)

Catalog data lives in [`generators/src/main/resources/data/*.yaml`](generators/src/main/resources/data/). The Maven module [`generators/`](generators/) maps those files to TeX with Jackson (YAML module):

```bash
./generators/generate.sh
# or: ./scripts/generate.sh
# or: (cd generators && mvn -q exec:java)
```

That rebuilds:

- `chapters/classes/{warrior,rogue,mage}.tex` from `classes.yaml`
- `tables/equipment.tex` and `tables/relics.tex` from `equipment.yaml`
- `tables/spells.tex` from `spells.yaml`
- `tables/monsters-bestiary.tex` from `monsters.yaml`
- `tables/encounters-book.tex` from `encounters.yaml`
- `chapters/hexmap-grid.tex` from `hexmap.yaml`

Edit the YAML, regenerate, then recompile the affected book(s).

## Build the PDFs

From the repository root, compile each book **twice** so the TOC and index settle. Indexing is handled by `imakeidx` / `makeindex` during the XeLaTeX pass.

```bash
for book in rules bestiary encounters adventure party-sheet; do
  xelatex -interaction=nonstopmode "$book.tex"
  xelatex -interaction=nonstopmode "$book.tex"
done
```

Or build a single volume:

```bash
xelatex -interaction=nonstopmode rules.tex
xelatex -interaction=nonstopmode rules.tex
```

The party sheet is a one-page photocopy extra (no second pass needed):

```bash
xelatex -interaction=nonstopmode party-sheet.tex
```

HTML alternative (WeasyPrint):

```bash
./scripts/build-party-sheet-html.sh
# → party-sheet-alt.pdf
```

With `latexmk` (if installed):

```bash
latexmk -xelatex rules.tex bestiary.tex encounters.tex adventure.tex party-sheet.tex
```

Outputs land next to the `.tex` roots: `rules.pdf`, `bestiary.pdf`, `encounters.pdf`, `adventure.pdf`, `party-sheet.pdf`.

## Suggested reading order

1. **Rules** — campaign loop, hexploration, pools, character creation, combat
2. **The Ledger Gate** — short intro delve (no companion books required)
3. **Journey Encounters** / **Bestiary** — road tables and monster stat blocks for a full campaign

## Repository layout

```
rules.tex / bestiary.tex / encounters.tex / adventure.tex   # book roots
party-sheet.tex / party-sheet.html                          # single-page photocopy extras
scripts/build-party-sheet-html.sh                           # HTML → PDF via WeasyPrint
preamble.tex                                                # shared style
chapters/                                                   # prose chapters (+ party-sheet-form)
tables/                                                     # generated catalogs
scripts/generate.sh                                        # thin wrapper → generators/
generators/                                                 # Maven module (Jackson + YAML data)
index.html                                                  # web download page
```

## Licence / status

Work in progress on branch `feature/update1`. Treat rules and catalogs as draft until a release is tagged.
