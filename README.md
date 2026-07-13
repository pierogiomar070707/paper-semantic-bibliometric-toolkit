# Paper Semantic Bibliometric Toolkit v1.0.0

A reproducible, auditable workflow for Scopus bibliometric analysis, scientific knowledge extraction, VOSviewer preparation, Related Work discovery, and paper-ready evidence.

## What is included

Ten independent notebooks executed in order:

1. `00_Setup_and_Configuration.ipynb`
2. `01_Corpus_Validation.ipynb`
3. `02_Corpus_Cleaning_and_Normalization.ipynb`
4. `03_Keyword_Analysis.ipynb`
5. `04_Scientific_Knowledge_Extraction.ipynb`
6. `05_Temporal_Trends_and_Emerging_Topics.ipynb`
7. `06_Sources_Authors_Institutions_Countries.ipynb`
8. `07_Citation_and_Related_Work_Selection.ipynb`
9. `08_VOSviewer_Preparation.ipynb`
10. `09_Figures_Report_and_QA.ipynb`

The unified Master Notebook will be created only after these ten modules are validated on the user's computer.

## Current corpus

The validated Scopus CSV with 272 documents is already included at `data/scopus_272.csv`.

The RIS was not uploaded to this chat and therefore is not included. Copy the complete Scopus RIS to:

`data/scopus_export.ris`

The analytical notebooks run without the RIS; it is required only for the final VOSviewer procedure.

## Installation on Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Open the full folder in VS Code and select `.venv` as the Jupyter kernel.

## Execution

Run notebooks 00 through 09 in numerical order. No notebook-code changes are required for the included corpus.

## Reuse with another Scopus corpus

The notebooks remain unchanged. Replace the CSV and update only the data-oriented values in `config.json` and the domain dictionaries under `config/` when the new scientific domain differs.

## Scientific safeguards

- No documents are removed automatically.
- Journal, institution, country, and keyword transformations remain auditable.
- A low-frequency concept is not automatically declared a research gap.
- Automated Related Work ranking never replaces reading the papers.
- Illustrator may improve typography and composition, but must not alter scientific links in VOSviewer networks.
