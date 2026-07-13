from pathlib import Path
import time
import nbformat
import pandas as pd
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
EXECUTED_DIR = ROOT / "validation" / "executed_notebooks"
EXECUTED_DIR.mkdir(parents=True, exist_ok=True)

pipeline = [
    "00_Setup_and_Configuration.ipynb",
    "01_Corpus_Validation.ipynb",
    "02_Corpus_Cleaning_and_Normalization.ipynb",
    "03_Keyword_Analysis.ipynb",
    "04_Scientific_Knowledge_Extraction.ipynb",
    "05_Temporal_Trends_and_Emerging_Topics.ipynb",
    "06_Sources_Authors_Institutions_Countries.ipynb",
    "07_Citation_and_Related_Work_Selection.ipynb",
    "08_VOSviewer_Preparation.ipynb",
    "09_Figures_Report_and_QA.ipynb",
]

rows = []
for name in pipeline:
    source = NOTEBOOK_DIR / name
    destination = EXECUTED_DIR / name.replace(".ipynb", "_executed.ipynb")
    start = time.time()
    status = "PASS"
    message = ""
    try:
        nb = nbformat.read(source, as_version=4)
        client = NotebookClient(nb, timeout=1200, kernel_name="python3", resources={"metadata": {"path": str(NOTEBOOK_DIR)}})
        client.execute()
        nbformat.write(nb, destination)
    except Exception as exc:
        status = "FAIL"
        message = str(exc)
    rows.append({"Notebook": name, "Status": status, "Seconds": round(time.time() - start, 2), "Message": message})
    print(name, status)
    if status == "FAIL":
        break

log = pd.DataFrame(rows)
log.to_csv(ROOT / "validation" / "pipeline_execution_log.csv", index=False, encoding="utf-8-sig")
print(log)
if (log["Status"] == "FAIL").any():
    raise SystemExit(1)
