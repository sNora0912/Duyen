#!/usr/bin/env python3
"""
Reproduce the numbers in Tables 3-5 and Section 4.1 of
"Duyen: Measuring Pragmatic Naturalness in Vietnamese LLM Output" (VTCA 2026).

Usage (from the repository root):   python3 scripts/reproduce_tables.py
Reads data/annotation_30.csv, data/scenarios.csv and data/outputs.csv. Standard library only.

Conventions: NONE is the empty label set; the eight labels used for per-label presence are the
seven error types plus OTHER. "Exact" means identical label sets. "Error vs. NONE" compares only
whether an item carries any label at all.
"""
import csv, os, re
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
TYPES = ["PR1", "PR2", "PR4", "PF1", "PF2", "FP1", "FP2"]
LABELS8 = TYPES + ["OTHER"]

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def S(s):
    s = (s or "").strip()
    return frozenset() if s in ("", "NONE") else frozenset(x.strip() for x in s.split(";") if x.strip())

def frac(a, b):
    return f"{a}/{b} ({100 * a / b:.1f}%)" if b else "n/a"

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

def agree(rows, a, b):
    exact = sum(S(r[a]) == S(r[b]) for r in rows)
    flag = sum(bool(S(r[a])) == bool(S(r[b])) for r in rows)
    pooled = sum((l in S(r[a])) == (l in S(r[b])) for r in rows for l in LABELS8)
    return exact, flag, pooled

def main():
    ann = load("annotation_30.csv"); scen = {s["item_id"]: s for s in load("scenarios.csv")}
    samp = [r for r in ann if r["is_control"] == "no"]; ctrl = [r for r in ann if r["is_control"] == "yes"]
    assert len(samp) == 25 and len(ctrl) == 5

    print("== Table 3: errors per designed opportunity, 25 sampled outputs, curator labels")
    outside = []
    for t in TYPES + ["OTHER"]:
        opp = [r for r in samp if t in scen[r["item_id"]]["designed_opportunities"].split(";")]
        err = [r for r in opp if t in S(r["curator_labels"])]
        print(f"  {t}: opportunities {len(opp):2d}  errors {len(err)}")
        outside += [(r["item_id"], t) for r in samp if t in S(r["curator_labels"]) and r not in opp]
    print(f"  labels outside designed opportunities (not counted above): {outside}")
    core = ["PR2", "PF1", "FP1"]
    for who in ("curator_labels", "a2_labels"):
        print(f"  core-type labels, {who}: {[(r['item_id'], sorted(S(r[who]) & set(core))) for r in ann if S(r[who]) & set(core)]}")

    flagged = [r for r in samp if S(r["curator_labels"])]
    print(f"\n== Section 4.1: {len(flagged)} of 25 sampled outputs carry a problem (curator)")
    for st in ("base", "adversarial"):
        n = sum(r["stratum"] == st for r in samp); k = sum(r["stratum"] == st for r in flagged)
        print(f"  {st}: {k} of {n}")
    for g in sorted({r["generator"] for r in samp}):
        n = sum(r["generator"] == g for r in samp); k = sum(r["generator"] == g for r in flagged)
        print(f"  {g}: {k} of {n}")
    for r in flagged:
        print(f"  {r['item_id']} [{r['generator']}] curator={r['curator_labels']}")

    print("\n== Table 4: second annotator (A2) vs curator")
    for name, rows in (("sampled", samp), ("controls", ctrl)):
        e, f, p = agree(rows, "curator_labels", "a2_labels"); n = len(rows)
        print(f"  {name}: exact {frac(e, n)} | error vs NONE {frac(f, n)} | pooled presence {frac(p, 8 * n)}")
    lo, hi = wilson(*agree(samp, "curator_labels", "a2_labels")[:1], 25)
    print(f"  95% Wilson interval for sampled exact agreement: {100 * lo:.0f}%-{100 * hi:.0f}%")
    both_none = sum(not S(r["curator_labels"]) and not S(r["a2_labels"]) for r in samp)
    both_other = sum(S(r["curator_labels"]) == S(r["a2_labels"]) == {"OTHER"} for r in samp)
    thr = [r for r in samp if not S(r["curator_labels"]) and S(r["a2_labels"])]
    rev = [r for r in samp if S(r["curator_labels"]) and not S(r["a2_labels"])]
    typ = [r for r in samp if S(r["curator_labels"]) and S(r["a2_labels"]) and S(r["curator_labels"]) != S(r["a2_labels"])]
    print(f"  both NONE {both_none}, both OTHER {both_other}")
    print(f"  A2 flags / curator accepts: {len(thr)} -> {[r['a2_labels'] for r in thr]}")
    print(f"  curator flags / A2 accepts: {len(rev)} -> {[r['item_id'] for r in rev]}")
    print(f"  type disagreements: {len(typ)} -> {[(r['item_id'], r['curator_labels'], r['a2_labels']) for r in typ]}")
    base = [r for r in samp if r["stratum"] == "base"]
    print(f"  base stratum flagged: A2 {sum(bool(S(r['a2_labels'])) for r in base)} of {len(base)}, "
          f"curator {sum(bool(S(r['curator_labels'])) for r in base)}")

    print("\n== Table 5: AI judge vs curator (human-human exact in last column)")
    groups = [("sampled, all", samp)] + [(g, [r for r in samp if r["generator"] == g])
                                         for g in sorted({r["generator"] for r in samp})] + [("controls", ctrl)]
    for name, rows in groups:
        e, f, _ = agree(rows, "curator_labels", "judge_labels"); hh = agree(rows, "curator_labels", "a2_labels")[0]
        print(f"  {name:16s} n={len(rows):2d}  exact {e}/{len(rows)}  error-vs-NONE {f}/{len(rows)}  human-human {hh}/{len(rows)}")
    jf = [r for r in samp if S(r["judge_labels"])]
    print(f"  judge flagged {len(jf)} of 25; curator-flagged items also flagged by judge: "
          f"{sum(bool(S(r['judge_labels'])) for r in flagged)} of {len(flagged)}")
    print(f"  judge additions: {[(r['item_id'], r['judge_labels']) for r in jf if not S(r['curator_labels'])]}")

    print("\n== Controls")
    for r in ctrl:
        print(f"  {r['item_id']}: curator={r['curator_labels']:6s} A2={r['a2_labels']:6s} judge={r['judge_labels']}")

    print("\n== Particle counts across all outputs (word-boundary matches)")
    outs = load("outputs.csv")
    for w in ("nha", "nhé", "ạ"):
        n = sum(len(re.findall(rf"(?<!\w){w}(?!\w)", o["output_vi"], flags=re.IGNORECASE)) for o in outs)
        print(f"  {w}: {n} occurrences in {len(outs)} outputs")

if __name__ == "__main__":
    main()
