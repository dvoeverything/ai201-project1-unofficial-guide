# Criterion 5 runs — before

Produced by `python app.py ask` with caching off (`AI201_CACHE=0` for runs 2
and 3; run 1 was the first call for this prompt, so nothing was cached yet).
Chunks from `chunker.py::split_documents`, top-k 5, cutoff 0.6.

Kestrel Commons and Morrow House come from `results/run_2026-09-30_1927_before.md`
(three runs each, produced by `run_eval.py`). This file holds the Calder Annexe runs.

### How much does laundry cost in Calder Annexe? — run 1

  (best distance 0.175, cutoff 0.6)

Laundry in Calder Annexe costs $2.00 to wash and $1.75 to dry (housing_calder_annexe.txt and housing_calder_annexe_laundry.txt).

Sources retrieved: housing_aldridge_hall.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt, housing_old_brewhouse.txt

1 model calls this session, 479 tokens (434 in, 45 out)

### How much does laundry cost in Calder Annexe? — run 2

  (best distance 0.175, cutoff 0.6)

Laundry in Calder Annexe costs $2.00 for a wash and $1.75 for a dryer. 

Sources: `housing_calder_annexe.txt` and `housing_calder_annexe_laundry.txt`

Sources retrieved: housing_aldridge_hall.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt, housing_old_brewhouse.txt

1 model calls this session, 488 tokens (434 in, 54 out)

### How much does laundry cost in Calder Annexe? — run 3

  (best distance 0.175, cutoff 0.6)

Laundry in Calder Annexe costs $2.00 for a wash and $1.75 for a dry. 

This information came from the documents `housing_calder_annexe.txt` and `housing_calder_annexe_laundry.txt`.

Sources retrieved: housing_aldridge_hall.txt, housing_calder_annexe.txt, housing_calder_annexe_laundry.txt, housing_old_brewhouse.txt

1 model calls this session, 492 tokens (434 in, 58 out)