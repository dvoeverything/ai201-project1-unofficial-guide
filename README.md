# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This system answers plain-language questions about campus life using the `campus_life` corpus: 88 short, student-written posts about courses, dining halls, residence halls, and admin rules (deadlines, housing lottery, meal plans, parking, and more). You ask something like "Is the housing lottery random?" and it retrieves the most relevant passages, answers only from them, and names the file each answer came from.

## Chunking Strategy

**Chunk size:** one paragraph per chunk, with the document's title line put
in front. That gives 183 chunks, 64 to 398 characters, 168 on average.
Produced by `chunker.py::paragraph_split`.

**Overlap:** 0.

**Why these choices:**

- **The starter's chunker never split anything.** `fallback_split` cuts
  800-character windows, but every file in `campus_life` is between 178 and
  549 characters, so 88 documents became 88 chunks. Changing the window size
  wouldn't help. The documents already have natural break points.
- **Each file is a title line plus one to four short paragraphs, and each
  paragraph is usually its own topic.** Some files cover two separate things,
  like `study_library_hours.txt` (opening hours, then where to sit) and
  `health_center.txt` (walk-in hours, then counselling). Kept whole, those
  chunks match both kinds of question only partly. Split at blank lines, each
  chunk covers one thing.
- **The subject is only named in the title.** On its own, "Expect 4 hours a
  week outside class." from `course_econ_101.txt` doesn't say which course it
  means. Putting the title in front of every paragraph keeps the course,
  dining hall, or building name in each chunk. Criterion 4 checks this.
- **Overlap is 0 because paragraph breaks never cut a sentence.** Overlap
  exists to repair sentences that a fixed window chops in half. Splitting on
  blank lines never does that, and the title prefix already carries the
  context a neighbouring chunk would have added.

**Changed my mind:** I started out thinking one file per chunk was fine,
since the starter already produced that. After reading the two-topic files,
I decided to split by paragraph instead.
**Evidence it helped:** after switching from `fallback_split` to
`split_documents`, the espresso question's best distance improved from 0.427
to 0.373, and the Morrow House main review moved up to #2 (0.206) for the
laundry question, because its laundry sentence is no longer mixed in with
the rest of the review.
## Sample Chunks

Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
On the add/drop deadline — You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

Chunk 2  |  source: course_cs_340_exams.txt#1  |  produced by: chunker.py::split_documents
CS 340 Databases — assessment — Start the term project in week three, not week eight; everyone learns this the hard way.

Chunk 3  |  source: course_phys_130_workload.txt#0  |  produced by: chunker.py::split_documents
Workload for PHYS 130 Mechanics — People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

Chunk 4  |  source: dining_verrill_street_grill_followup.txt#1  |  produced by: chunker.py::split_documents
Re: Verrill Street Grill — Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.

Chunk 5  |  source: housing_morrow_house.txt#1  |  produced by: chunker.py::split_documents
Morrow House — what it's actually like — The good: cheapest housing tier by about $900 a year, and the singles are real singles.

## Sample Answer



**Question:** Is the housing lottery random for juniors and seniors?
**Answer:**


#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.1494     admin_housing_lottery.txt        On the housing lottery — The housing lottery is not ...
2   0.6833     housing_aldridge_hall.txt        Aldridge Hall — what it's actually like — I lived he...
3   0.6901     housing_morrow_house.txt         Morrow House — what it's actually like — The good: c...
4   0.7015     advising_registration.txt        Registration and your adviser — Registration times a...
5   0.7049     admin_parking_permits.txt        On the parking permits — Student permits for the wes...

Gate: best distance 0.149 is under the 0.6 cutoff

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.

**My relevance cutoff:** 0.6 (the starter's default, kept after measuring)

I ran my five test questions and the five `OUT_OF_SCOPE` questions through
`python app.py retrieve` and recorded the best distance for each. The two
groups don't overlap:

- **In corpus:** 0.149 to 0.416. The worst is the withdrawal question, where
  the add/drop file (0.416) and the withdrawal file (0.424) came back almost
  tied, because the two policies are worded so similarly.
- **Out of scope:** 0.795 to 0.916. The closest is "What is the capital of
  Mongolia?", which matched HIST 118 Modern World History.

The gap runs from 0.416 to 0.795, and 0.6 sits roughly in the middle of it:
about 0.18 above my worst real question and 0.19 below my closest off-topic
one. What 0.6 would get wrong: a real question worded very differently from
its document could land above 0.6 and be refused. The espresso question
(0.373) shows how far wording alone can push a real question up.

I expected the ibuprofen question to be the borderline case because the
corpus has a `health_center.txt`, but it never matched that file. Its
closest chunk was The Ridgeway Café's hours at 0.847.

| Question                                                                     | In corpus? | Best distance |
|------------------------------------------------------------------------------|------------|---------------|
| Is the housing lottery random for juniors and seniors?                       | Yes        | 0.149         |
| How long is the wait at Kestrel Commons during the lunch rush?               | Yes        | 0.176         |
| What do I need to withdraw from a course after the drop deadline has passed? | Yes        | 0.416         |
| Where on campus can I get real espresso?                                     | Yes        | 0.373         |
| How much does it cost to dry a load of laundry in Morrow House?              | Yes        | 0.175         |
| What is the capital of Mongolia?                                             | No         | 0.795         |
| How do I change the oil in a diesel engine?                                  | No         | 0.916         |
| Who won the 1994 World Cup?                                                  | No         | 0.859         |
| What is the recommended dosage of ibuprofen for a headache?                  | No         | 0.847         |
| How do I write a for loop in Rust?                                           | No         | 0.865         |

## How I Used AI

## How I Used AI

**1. Writing the chunker.** I decided to split each file on its blank lines
and put the title line in front of every paragraph, so a chunk like "Expect
4 hours a week outside class" still says which course it's about. I asked
Claude to write that function. The first version (`paragraph_split`) took a
single string and returned plain strings, but the starter's `split_documents`
receives a list of `Document` objects and has to return `Chunk` objects, so
it would have crashed on `python app.py index`. I pasted my `chunker.py` back
to Claude, and it rewrote the logic inside `split_documents` itself so it
returns `Chunk` objects with `produced_by="chunker.py::split_documents"`. I
kept `fallback_split` for comparison, re-indexed, and checked the summary
line: 183 chunks, 64 to 398 characters, average 168.

**2. Writing criterion 4 (chunks).** My first draft was "No chunk is shorter
than 178 characters or longer than 549 characters." When I asked Claude for
a reason to go with it, it pointed out that 178 and 549 were just the
starter's own output from `python app.py index`, so the criterion described
what had already happened and couldn't fail. I rewrote it around what a bad
chunk actually looks like in this corpus: one that loses its course, dining
hall, or building name. I first wrote "all but one" chunk, and picked the
ECON 101 line as the one I'd allow to fail. Claude showed me that a chunker
that drops the title from one course drops it from all nine at once, so a
single failure wasn't realistic. I changed the target to "every chunk."

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

## Run Log — Before

Criteria 1–3 from `results/run_2026-09-30_1927_before.md` (`run_eval.py::main`).
Criterion 4 from `check_criterion4.py`. Criterion 5 from the run_eval file
(Kestrel, Morrow) and `results/criterion5_before.md` (Calder).

| Criterion                                                     | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---------------------------------------------------------------|--------|-------|-------|-------|---------|
| 1. Retrieved chunk contains the answer                        | 4 of 5 | 5/5   | 5/5   | 5/5   |         |
| 2. Every answer names a source                                | 5 of 5 | 5/5   | 5/5   | 5/5   |         |
| 3. Gate stops out-of-corpus questions                         | 4 of 5 | 5/5   | 5/5   | 5/5   |         |
| 4. Chunks from course/dining/housing files name their subject | every chunk | 147/147 | 147/147 | 147/147 |       |
| 5. Place-naming questions cite a file about that place        | 2 of 3 | 3/3   | 3/3   | 3/3   |          |

Criteria 3 and 4 are single deterministic measurements (the gate is a fixed
comparison; the chunks don't change between runs), so the same number goes
in all three columns.

### Real output

**Criterion 1 — retrieval** (`store.py::search`), withdrawal question, run 1:
```
Best distance: 0.4160 (passed the gate)
Sources retrieved: admin_add_drop_deadline.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_withdrawal_deadline.txt, advising_registration.txt
```

**Criterion 2 — answer with source** (`generate.py::answer_from_chunks`), housing lottery, run 1:
```
No, the housing lottery is not entirely random for juniors and seniors. They are ordered by accumulated credit hours first, and random drawing is used only as a tie-breaker (admin_housing_lottery.txt).
```

**Criterion 3 — gate** (`run_eval.py::check_out_of_scope`):
```
| What is the capital of Mongolia? | 0.795 | refused |
| How do I change the oil in a diesel engine? | 0.916 | refused |
| Who won the 1994 World Cup? | 0.859 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.847 | refused |
| How do I write a for loop in Rust? | 0.865 | refused |
Refused 5 of 5.
```

**Criterion 4 — chunks** (`check_criterion4.py`, using `chunker.py::split_documents`):
```
Files checked: 62 (course, dining, housing)
Chunks checked: 147
Chunks that name their subject: 147 of 147
```

**Criterion 5 — right place cited** (`app.py ask`), Calder Annexe, run 2:
```
Laundry in Calder Annexe costs $2.00 for a wash and $1.75 for a dryer.
Sources: `housing_calder_annexe.txt` and `housing_calder_annexe_laundry.txt`
```

## Verdicts

## Verdicts

| # | Criterion                                        | Verdict | How I decided                                                                                |
|------------------------------------------------------|---------|----------------------------------------------------------------------------------------------|
| 1 | Retrieved chunk contains the answer (4 of 5)     | MET     | 5/5 in all three runs. I checked that the file holding each answer was in the "Sources retrieved" list. It was closest for the withdrawal question: `admin_add_drop_deadline.txt` came back first (0.416) and the correct `admin_withdrawal_deadline.txt` was only 4th, but it was there, so it counts. |
| 2 | Every answer names a source (5 of 5)             | MET     | All 15 answers name at least one file, in three different formats (inline brackets, a "Source:" line, a bulleted list). This criterion only checks that a file is named, not that it is the right one; criterion 5 covers that. |
| 3 | Gate stops out-of-corpus questions (4 of 5)      | MET     | All five were refused. The closest was "capital of Mongolia" at 0.795, still 0.195 above the 0.6 cutoff. One deterministic pass, so the same 5/5 goes in every column. |
| 4 | Every chunk from course/dining/housing files names its subject | MET | `check_criterion4.py` checked all 147 chunks from the 62 files against the name in each file's title: 147 of 147. The chunks don't change between runs, so one measurement covers all three. |
| 5 | Place-naming questions cite the right place (2 of 3) | MET | 3/3 in every run. The Calder question, the one I expected to fail, cited `housing_calder_annexe...` files every time, and Fenwick's identical laundry file was never even retrieved. |
|

## Diagnoses

## Diagnoses

**No criterion was missed.** All five met their target in all three runs.

**Why my predicted failures didn't happen.** I expected two failures: the
Morrow House dryer question being crowded out by seven near-identical laundry
files (criterion 1), and the Calder Annexe question citing Fenwick Court's
identical laundry file (criterion 5). Neither happened. Morrow's laundry file
ranked #1 (0.175), and Fenwick was never retrieved for the Calder question.
Both have the same cause, at the **chunking** stage: `split_documents` puts
each file's title ("Laundry in Morrow House", "Laundry in Calder Annexe") in
front of every chunk, so the one word that differs between near-identical
files, the building name, is in the text the embedding sees.

**Near-miss: withdrawal vs. drop (retrieval).** For "What do I need to
withdraw from a course after the drop deadline has passed?",
`admin_add_drop_deadline.txt` ranked first (0.416) and the correct
`admin_withdrawal_deadline.txt` ranked only 4th. The two policies use almost
the same vocabulary (course, drop, deadline, week), so in embedding space
they are near neighbours and meaning alone can't separate them. Criterion 1
passed only because top-k is 5; at top-k 3 this question would have failed.

**Near-miss: the test, not the system.** The 'expects' phrase for the
withdrawal question is "adviser signature", but all three answers say
"adviser's signature". An exact-match scorer would fail a correct answer.
This is a flaw in my test question, not in any pipeline stage.

**Were my targets set low? Yes.** Criterion 5 was the safest: two of its
three questions were also test questions, and each named its place exactly
as the file title does, so the title prefix made it nearly impossible to
miss. Criterion 3's out-of-scope questions were all from unrelated worlds,
so they were easy to refuse. The one I'd tighten first is **criterion 1**:
"For at least 4 of 5 questions, the top-ranked chunk contains the
answer." Under that version the withdrawal question fails today, so it would
be an honest target rather than a safe one.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
