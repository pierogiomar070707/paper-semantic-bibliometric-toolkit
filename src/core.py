from __future__ import print_function

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

DASH_TRANSLATION = str.maketrans({
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    "“": '"', "”": '"', "‘": "'", "’": "'",
})


def find_project_root(start=None):
    current = Path(start or Path.cwd()).resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / "config.json").exists():
            return candidate
    raise FileNotFoundError("No se encontró config.json en la carpeta actual ni en sus carpetas superiores.")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_config(root):
    return read_json(Path(root) / "config.json")


def ensure_directories(root):
    for folder in ["data", "outputs", "figures", "reports", "thesaurus", "validation"]:
        (Path(root) / folder).mkdir(parents=True, exist_ok=True)


def load_scopus_csv(root, config):
    path = Path(root) / config["input_csv"]
    if not path.exists():
        raise FileNotFoundError("No se encontró el CSV configurado: {}".format(path))
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)


def load_clean_corpus(root):
    path = Path(root) / "outputs" / "corpus_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError("Ejecuta primero 02_Corpus_Cleaning_and_Normalization.ipynb")
    return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)


def normalize_spacing(value):
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = text.translate(DASH_TRANSLATION)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_identifier(value):
    return normalize_spacing(value).lower()


def normalize_title(value):
    text = normalize_spacing(value).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_keyword(value, corrections=None):
    text = normalize_spacing(value).lower()
    text = re.sub(r"\s*-\s*", "-", text)
    text = re.sub(r"\s+", " ", text).strip(" .;,:")
    if corrections:
        for _ in range(4):
            replacement = corrections.get(text, text)
            if replacement == text:
                break
            text = replacement
    return text


def split_semicolon(value):
    text = normalize_spacing(value)
    if not text:
        return []
    return [part.strip() for part in re.split(r"\s*;\s*", text) if part.strip()]


def frequency_table(df, column, top_n=None):
    if column not in df.columns:
        return pd.DataFrame(columns=[column, "Documents"])
    values = df[column].fillna("").astype(str).str.strip()
    values = values[values.ne("")]
    counts = values.value_counts()
    if top_n is not None:
        counts = counts.head(top_n)
    return counts.rename_axis(column).reset_index(name="Documents")


def save_csv(df, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def save_json(data, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def markdown_table(df, rows=20):
    if df is None or df.empty:
        return "_No data available._"
    return df.head(rows).to_markdown(index=False)


def combined_text(df, columns=None):
    if columns is None:
        columns = ["Title", "Abstract", "Author Keywords", "Index Keywords"]
    available = [column for column in columns if column in df.columns]
    return df[available].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
