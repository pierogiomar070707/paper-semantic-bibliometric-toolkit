# Validation Report

- Toolkit version: 1.0.0
- Validation corpus: 272 Scopus records
- Validation date: 2026-07-12
- Notebook modules executed: 10
- Notebook execution status: PASS
- Final output QA status: PASS
- RIS-dependent VOSviewer import was not executed because the RIS was not uploaded to the chat; the notebook correctly generated an auditable RIS-status warning and all preparation files.

## Notebook results

| Notebook                                        | Status   | Executed copy                                                                          | Errors   |
|:------------------------------------------------|:---------|:---------------------------------------------------------------------------------------|:---------|
| 00_Setup_and_Configuration.ipynb                | PASS     | validation/executed_notebooks/00_Setup_and_Configuration_executed.ipynb                |          |
| 01_Corpus_Validation.ipynb                      | PASS     | validation/executed_notebooks/01_Corpus_Validation_executed.ipynb                      |          |
| 02_Corpus_Cleaning_and_Normalization.ipynb      | PASS     | validation/executed_notebooks/02_Corpus_Cleaning_and_Normalization_executed.ipynb      |          |
| 03_Keyword_Analysis.ipynb                       | PASS     | validation/executed_notebooks/03_Keyword_Analysis_executed.ipynb                       |          |
| 04_Scientific_Knowledge_Extraction.ipynb        | PASS     | validation/executed_notebooks/04_Scientific_Knowledge_Extraction_executed.ipynb        |          |
| 05_Temporal_Trends_and_Emerging_Topics.ipynb    | PASS     | validation/executed_notebooks/05_Temporal_Trends_and_Emerging_Topics_executed.ipynb    |          |
| 06_Sources_Authors_Institutions_Countries.ipynb | PASS     | validation/executed_notebooks/06_Sources_Authors_Institutions_Countries_executed.ipynb |          |
| 07_Citation_and_Related_Work_Selection.ipynb    | PASS     | validation/executed_notebooks/07_Citation_and_Related_Work_Selection_executed.ipynb    |          |
| 08_VOSviewer_Preparation.ipynb                  | PASS     | validation/executed_notebooks/08_VOSviewer_Preparation_executed.ipynb                  |          |
| 09_Figures_Report_and_QA.ipynb                  | PASS     | validation/executed_notebooks/09_Figures_Report_and_QA_executed.ipynb                  |          |

## Final output QA

| Output                          | Exists   |   Size bytes | Status   |
|:--------------------------------|:---------|-------------:|:---------|
| 00_project_summary.csv          | True     |          251 | PASS     |
| 01_corpus_validation.json       | True     |         3594 | PASS     |
| corpus_cleaned.csv              | True     |      2781367 | PASS     |
| 03_author_keyword_frequency.csv | True     |        13932 | PASS     |
| 04_theme_statistics.csv         | True     |         3027 | PASS     |
| 05_documents_by_year.csv        | True     |          481 | PASS     |
| 06_source_statistics.csv        | True     |         9749 | PASS     |
| 06_author_statistics.csv        | True     |        35259 | PASS     |
| 06_country_statistics.csv       | True     |          665 | PASS     |
| 07_related_work_candidates.csv  | True     |       186321 | PASS     |
| 08_ris_status.csv               | True     |          143 | PASS     |
