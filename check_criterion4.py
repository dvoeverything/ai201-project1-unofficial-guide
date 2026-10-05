"""
Criterion 4 check: every chunk that comes from the 62 course, dining, and
housing files names the course, dining hall, or building it is about.

Run from the project folder:  python check_criterion4.py
"""
from chunker import split_documents
from ingest import load_documents

# The name each file's chunks must contain, worked out from the file name.
# course_cs_210_exams.txt -> "CS 210"; housing_calder_annexe_noise.txt -> "Calder Annexe"
SUFFIXES = ("_exams", "_workload", "_followup", "_laundry", "_noise")


def expected_name(source: str) -> str | None:
    stem = source.rsplit(".", 1)[0]
    for s in SUFFIXES:
        if stem.endswith(s):
            stem = stem[: -len(s)]
    kind, _, rest = stem.partition("_")
    words = rest.split("_")
    if kind == "course":
        return f"{words[0].upper()} {words[1]}"            # "CS 210"
    if kind in ("dining", "housing"):
        if words[0] == "the":
            words = words[1:]
        return " ".join(w.capitalize() for w in words[:2])  # "Ridgeway Cafe" -> checked loosely below
    return None


def names_subject(text: str, name: str) -> bool:
    # Compare case-insensitively, and treat "é" as "e" so "Café" matches "Cafe".
    t = text.lower().replace("é", "e")
    return name.lower() in t


chunks = split_documents(load_documents())
in_scope = [c for c in chunks if expected_name(c.source)]
failures = [c for c in in_scope if not names_subject(c.text, expected_name(c.source))]

files = {c.source for c in in_scope}
print(f"Files checked: {len(files)} (course, dining, housing)")
print(f"Chunks checked: {len(in_scope)}")
print(f"Chunks that name their subject: {len(in_scope) - len(failures)} of {len(in_scope)}")
for c in failures:
    print(f"  MISSING NAME  {c.label}  expected '{expected_name(c.source)}'")
    print(f"    {c.text[:100]}")
