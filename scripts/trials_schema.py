"""Shared schema for data/trials.csv. Imported by validate.py and build_json.py."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "trials.csv"
JSON_PATH = ROOT / "data" / "trials.json"

# Column order is part of the schema. Changing it is a deliberate, documented change.
COLUMNS = [
    "tumour", "subsite", "setting", "line", "subgroup", "trial", "phase",
    "population", "intervention", "results", "comment", "pe", "pm", "rf",
    "extra", "link", "src", "flags",
]

# A blank required field is an error unless the row's `flags` cell records an open issue.
REQUIRED = ["tumour", "trial", "population", "intervention", "results", "src"]

TUMOURS = {
    "Bladder Cancer", "Breast Cancer", "CLL", "CML", "Colorectal Cancer",
    "Endometrial and Cervical Cancer", "Gastric Cancer", "Head and Neck",
    "Hepatobiliary", "Indolent Lymphoma", "Kidney Cancer", "Lung Cancer",
    "Lymphoma - DLBCL", "Lymphoma - Hodgkin", "MPN", "Melanoma", "Myeloid",
    "Myeloma", "Neuroendocrine", "Ovarian Cancer", "Prostate Cancer", "Sarcoma",
    "Supportive Care", "Thrombosis", "Tissue Agnostic",
}

PHASES = {
    "Phase 1", "Phase 1b", "Phase 1b/2", "Phase 1/2", "Phase 2", "Phase 2/3",
    "Phase 3", "Meta-analysis",
}


def read_rows(path=CSV_PATH):
    """Return (header, rows) where rows are lists of raw cell strings."""
    import csv

    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        return header, list(reader)
