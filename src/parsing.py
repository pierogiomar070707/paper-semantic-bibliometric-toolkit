from __future__ import print_function

import re
from itertools import combinations

import pandas as pd
import pycountry

from core import normalize_spacing, normalize_title, split_semicolon

COUNTRY_ALIASES = {
    "usa": "United States", "u.s.a.": "United States", "us": "United States",
    "united states of america": "United States", "pr china": "China",
    "people's republic of china": "China", "p.r. china": "China",
    "england": "United Kingdom", "scotland": "United Kingdom", "wales": "United Kingdom",
    "uk": "United Kingdom", "south korea": "South Korea", "republic of korea": "South Korea",
    "korea": "South Korea", "russian federation": "Russia", "türkiye": "Turkey",
    "hong kong": "Hong Kong", "taiwan": "Taiwan", "iran": "Iran",
    "viet nam": "Vietnam", "czechia": "Czech Republic"
}

INSTITUTION_PRIORITY = [
    ("university", 10), ("universidad", 10), ("université", 10), ("universita", 10),
    ("academy", 9), ("institute", 9), ("institut", 9),
    ("research center", 8), ("research centre", 8), ("research council", 8),
    ("key laboratory", 7), ("laboratory", 7), ("laboratoire", 7),
    ("college", 6), ("ministry", 5), ("department", 2), ("faculty", 2),
]


def parse_author_full_names(value):
    rows = []
    for item in split_semicolon(value):
        match = re.match(r"^(.*?)\s*\((\d+)\)\s*$", item)
        if match:
            rows.append({"Author full name": match.group(1).strip(), "Author ID": match.group(2)})
        else:
            rows.append({"Author full name": item.strip(), "Author ID": ""})
    return rows


def parse_affiliations(value):
    return split_semicolon(value)


def extract_country_from_affiliation(affiliation):
    text = normalize_spacing(affiliation)
    if not text:
        return ""
    last_segment = text.split(",")[-1].strip().lower()
    if last_segment in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[last_segment]
    for country in pycountry.countries:
        candidates = [country.name]
        if hasattr(country, "official_name"):
            candidates.append(country.official_name)
        if hasattr(country, "common_name"):
            candidates.append(country.common_name)
        for candidate in candidates:
            if last_segment == candidate.lower():
                return country.name
    lowered = text.lower()
    for alias, canonical in COUNTRY_ALIASES.items():
        if re.search(r"(?<![a-z])" + re.escape(alias) + r"(?![a-z])", lowered):
            return canonical
    return ""


def extract_institution_candidate(affiliation):
    text = normalize_spacing(affiliation)
    if not text:
        return ""
    segments = [segment.strip() for segment in text.split(",") if segment.strip()]
    scored = []
    for index, segment in enumerate(segments):
        lowered = segment.lower()
        score = 0
        for token, token_score in INSTITUTION_PRIORITY:
            if token in lowered:
                score = max(score, token_score)
        if score > 0:
            scored.append((score, len(segment), -index, segment))
    if scored:
        scored.sort(reverse=True)
        return scored[0][-1]
    return segments[0] if segments else text


def build_pair_edges(document_to_items, item_a="Source", item_b="Target"):
    weights = {}
    for _, items in document_to_items.items():
        unique_items = sorted(set(item for item in items if item))
        for left, right in combinations(unique_items, 2):
            key = (left, right)
            weights[key] = weights.get(key, 0) + 1
    rows = [{item_a: key[0], item_b: key[1], "Weight": weight} for key, weight in weights.items()]
    return pd.DataFrame(rows).sort_values("Weight", ascending=False) if rows else pd.DataFrame(columns=[item_a, item_b, "Weight"])
