"""
Which file ranks #1 for each test question?

This is the extra measurement for the unit 2 improvement. My five criteria were
all MET before the fix, so they can't show whether hybrid search helped. The
diagnosis was about rank: the withdrawal question's #1 chunk was the wrong
policy. This prints the #1 chunk for every question so before and after can be
compared directly.

    AI201_HYBRID=0 python check_top1.py     # before: vector search only
    python check_top1.py                    # after: hybrid search
"""
import questions as qs
import store

# The file each question's answer lives in, decided before running this.
EXPECTED = {
    "Is the housing lottery random for juniors and seniors?":
        "admin_housing_lottery.txt",
    "How long is the wait at Kestrel Commons during the lunch rush?":
        "dining_kestrel_commons",            # main review or followup both count
    "What do I need to withdraw from a course after the drop deadline has passed?":
        "admin_withdrawal_deadline.txt",
    "Where on campus can I get real espresso?":
        "dining_the_ridgeway_cafe",
    "How much does it cost to dry a load of laundry in Morrow House?":
        "housing_morrow_house",
}

print(f"Hybrid search: {'ON' if store.HYBRID else 'OFF'}\n")
correct = 0
for item in qs.answered():
    q = item["question"]
    top = store.search(q)[0]
    ok = top.source.startswith(EXPECTED.get(q, "?"))
    correct += ok
    print(f"{'✅' if ok else '❌'}  #1 = {top.label:<40} (distance {top.distance:.3f})  {q}")

print(f"\nTop-ranked chunk is the right file: {correct} of {len(qs.answered())}")
