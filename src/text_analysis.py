from __future__ import print_function

import re
from itertools import combinations

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from core import combined_text, normalize_keyword, split_semicolon


def explode_keywords(df, source_column, keyword_type, corrections=None):
    base_columns = [column for column in [
        "EID", "DOI", "Title", "Year", "Source title normalized"
    ] if column in df.columns]
    temp = df[base_columns + [source_column]].copy()
    temp["Keyword original"] = temp[source_column].map(split_semicolon)
    temp = temp.explode("Keyword original")
    temp["Keyword original"] = temp["Keyword original"].fillna("").astype(str).str.strip()
    temp = temp[temp["Keyword original"].ne("")].copy()
    temp["Keyword normalized"] = temp["Keyword original"].map(
        lambda value: normalize_keyword(value, corrections=corrections)
    )
    temp["Keyword type"] = keyword_type
    return temp.drop(columns=[source_column]).reset_index(drop=True)


def document_frequency(keyword_df, keyword_column="Keyword normalized"):
    identifier = "EID" if "EID" in keyword_df.columns else "Title"
    return (
        keyword_df.drop_duplicates([identifier, keyword_column])
        .groupby(keyword_column)[identifier]
        .nunique().sort_values(ascending=False)
        .rename("Documents").reset_index()
    )


def keyword_variant_audit(keyword_df):
    variants = (
        keyword_df.groupby("Keyword normalized")["Keyword original"]
        .agg(lambda values: sorted(set(values))).reset_index()
    )
    variants["Number of variants"] = variants["Keyword original"].map(len)
    variants["Variants"] = variants["Keyword original"].map(" | ".join)
    return (
        variants[variants["Number of variants"] > 1]
        .drop(columns=["Keyword original"])
        .sort_values(["Number of variants", "Keyword normalized"], ascending=[False, True])
        .reset_index(drop=True)
    )


def taxonomy_statistics(df, taxonomy, text_columns=None):
    text = combined_text(df, text_columns)
    stats_rows = []
    detail_frames = []
    for family, concepts in taxonomy.items():
        for concept, patterns in concepts.items():
            pattern = "|".join("(?:{})".format(item) for item in patterns)
            mask = text.str.contains(pattern, regex=True, na=False)
            stats_rows.append({
                "Family": family,
                "Concept": concept,
                "Documents": int(mask.sum()),
                "Percentage": round(float(mask.sum()) / len(df) * 100, 2)
            })
            details = df.loc[mask, [column for column in [
                "EID", "Title", "Year", "Authors", "Source title normalized", "Cited by", "DOI"
            ] if column in df.columns]].copy()
            details["Family"] = family
            details["Concept"] = concept
            detail_frames.append(details)
    stats = pd.DataFrame(stats_rows).sort_values(["Family", "Documents", "Concept"], ascending=[True, False, True])
    details = pd.concat(detail_frames, ignore_index=True) if detail_frames else pd.DataFrame()
    return stats, details


def discover_ngrams(df, min_df=2, max_features=3000):
    text = combined_text(df, ["Title", "Abstract"]).fillna("")
    vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 3), min_df=min_df,
        max_df=0.85, max_features=max_features, token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9-]{1,}\b"
    )
    matrix = vectorizer.fit_transform(text)
    features = vectorizer.get_feature_names_out()
    tfidf_sum = np.asarray(matrix.sum(axis=0)).ravel()
    doc_frequency = np.asarray((matrix > 0).sum(axis=0)).ravel()
    result = pd.DataFrame({
        "Term": features,
        "Documents": doc_frequency.astype(int),
        "TF-IDF sum": tfidf_sum.round(6)
    })
    result["Words"] = result["Term"].str.count(" ") + 1
    return result.sort_values(["TF-IDF sum", "Documents"], ascending=[False, False]).reset_index(drop=True)


def extract_model_candidates(df):
    text = combined_text(df, ["Title", "Abstract"])
    patterns = [
        r"\bYOLO(?:v?\d+|11|12|26)?(?:-[A-Za-z0-9]+)?\b",
        r"\b(?:RT-)?DETR(?:-[A-Za-z0-9]+)?\b",
        r"\b(?:Mask|Faster)?\s*R-?CNN\b",
        r"\b(?:ResNet|DenseNet|EfficientNet|MobileNet|ConvNeXt|Swin|ViT|U-Net|DeepLab|SegFormer)[A-Za-z0-9+./-]*\b",
        r"\b(?:SAM2?|DINOv2?|GroundingDINO|CLIP|OWL-ViT|Florence-2)\b"
    ]
    counts = {}
    for document in text:
        found = set()
        for pattern in patterns:
            for match in re.findall(pattern, document, flags=re.IGNORECASE):
                value = match if isinstance(match, str) else "".join(match)
                value = value.strip()
                if value:
                    found.add(value)
        for value in found:
            key = value.lower()
            counts[key] = counts.get(key, 0) + 1
    return pd.DataFrame([
        {"Model candidate": key, "Documents": value}
        for key, value in counts.items()
    ]).sort_values("Documents", ascending=False) if counts else pd.DataFrame(columns=["Model candidate", "Documents"])


def extract_dataset_candidates(df):
    text = combined_text(df, ["Title", "Abstract"])
    pattern = re.compile(r"\b([A-Z][A-Za-z0-9_-]{2,}(?:\s+[A-Z][A-Za-z0-9_-]{2,}){0,3})\s+(?:dataset|database)\b")
    counts = {}
    for document in text:
        for match in pattern.findall(document):
            candidate = match.strip()
            if candidate.lower() not in {"the", "this", "our", "image", "training", "test"}:
                counts[candidate] = counts.get(candidate, 0) + 1
    return pd.DataFrame([
        {"Dataset candidate": key, "Mentions": value}
        for key, value in counts.items()
    ]).sort_values("Mentions", ascending=False) if counts else pd.DataFrame(columns=["Dataset candidate", "Mentions"])


def keyword_cooccurrence(keyword_df, minimum_occurrences=3, fractional=False):
    frequency = document_frequency(keyword_df)
    allowed = set(frequency.loc[frequency["Documents"] >= minimum_occurrences, "Keyword normalized"])
    edge_weights = {}
    for _, group in keyword_df[keyword_df["Keyword normalized"].isin(allowed)].groupby("EID"):
        items = sorted(set(group["Keyword normalized"]))
        if len(items) < 2:
            continue
        contribution = 1.0 / (len(items) - 1) if fractional and len(items) > 1 else 1.0
        for left, right in combinations(items, 2):
            edge_weights[(left, right)] = edge_weights.get((left, right), 0.0) + contribution
    edges = pd.DataFrame([
        {"Source": left, "Target": right, "Weight": round(weight, 6)}
        for (left, right), weight in edge_weights.items()
    ])
    if not edges.empty:
        edges = edges.sort_values("Weight", ascending=False)
    nodes = frequency[frequency["Keyword normalized"].isin(allowed)].copy()
    return nodes, edges
