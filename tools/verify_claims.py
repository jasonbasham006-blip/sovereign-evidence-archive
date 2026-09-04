#!/usr/bin/env python3
"""verify_claims.py — self-contained integer re-verifier for the Sovereign
Evidence Archive claims registry. Run before trusting; run before adding.
Stdlib only. Exit 0 = all checks pass."""
import math
import sys

FAILS = []


def ck(name, ok):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILS.append(name)


def psd(l, s=0, d=0):
    return l * 240 + s * 12 + d


# --- C-004: the 18460 identities ---------------------------------------------
ck("18460: 1420x13", 1420 * 13 == 18460)
ck("18460: 923x20", 923 * 20 == 18460)
ck("18460: /13000 = 1.42 = 71/50", abs(18460 / 13000 - 1.42) < 1e-12 and 71 / 50 == 1.42)
ck("18460: 71-rail", 18460 == 71 * 260)

# --- C-018: CRT block ---------------------------------------------------------
X = 3398738
ck("CRT residues", X % 49 == 0 and X % 1118 == 18 and X % 79 == 0 and X % 107 == 97)
ck("CRT dependent witness 158", X % 158 == 0)
ck("CRT product", 49 * 1118 * 79 * 107 == 463072246)
ck("CRT factorization", X == 2 * 7 ** 2 * 79 * 439)

# --- C-019: mass constants ----------------------------------------------------
ck("923 factors", 923 == 13 * 71)
ck("1118 factors", 1118 == 2 * 13 * 43)
ck("1118/923 = 86/71", 1118 * 71 == 923 * 86)
ck("mass residues mod49", (923 % 49, 1118 % 49, (923 + 1118) % 49) == (41, 40, 32))

# --- C-020: vessel weights ----------------------------------------------------
ck("commission 230 dwt", 11 * 20 + 10 == 230)
ck("scratch 238 dwt", 11 * 20 + 18 == 238)
ck("238 god seal", 238 % 49 == 42)
ck("238 hebrew sum", 238 == 119 + 119)
ck("238 factors", 238 == 2 * 7 * 17)
ck("delta 8 dwt", 238 - 230 == 8)

# --- C-021: 7s/oz rate lock ---------------------------------------------------
ck("avery candlesticks 29oz -> £10-3-0", 29 * 7 == 203 == psd(10, 3, 0) // 12)
ck("shattuck sugar 14:2 -> £4-18-8", abs(14.1 * 7 - psd(4, 18, 8) / 12) < 0.05)
ck("shattuck coffee 40:2 -> £14-0-8", abs(40.1 * 7 - psd(14, 0, 8) / 12) < 0.05)
ck("tracy goblets 38:2 -> £13-6-8", abs(38.1 * 7 - psd(13, 6, 8) / 12) < 0.05)
ck("saunders large 24:10 -> £8-11-6", abs(24.5 * 7 - psd(8, 11, 6) / 12) < 0.05)
ck("saunders tea 5:10 -> £1-18-6", abs(5.5 * 7 - psd(1, 18, 6) / 12) < 0.05)

# --- identifier components ----------------------------------------------------
ck("identifier 111118 mod49 = 35", 111118 % 49 == 35)
ck("identifier 306 mod49 = 12", 306 % 49 == 12)
ck("identifier 923 mod49 = 41", 923 % 49 == 41)

# --- tally-page arithmetic (W-06 ledger wave) ---------------------------------
tally = [(3,0,0),(6,10,0),(2,5,0),(4,0,0),(19,10,0),(54,0,0),(4,6,0),(10,10,0),
         (9,2,6),(3,5,0),(3,5,0),(20,0,0),(7,0,0),(8,0,0),(11,2,0),(19,0,0),
         (2,5,0),(9,0,0),(5,0,0),(10,0,0),(10,0,0),(4,10,0),(46,0,0),(13,0,0)]
ck("tally computed £284-10-6", sum(psd(*e) for e in tally) == psd(284, 10, 6))
ck("tally delta vs written £250-10-0", psd(284, 10, 6) - psd(250, 10, 0) == psd(34, 0, 6))
ck("running total £274-0-0", psd(250, 10, 0) + psd(7, 10, 0) + psd(12, 0, 0) + psd(4, 0, 0) == psd(274, 0, 0))

print()
if FAILS:
    print(f"verify_claims: FAIL ({len(FAILS)}): {FAILS}")
    sys.exit(1)
print(f"verify_claims: ALL CHECKS PASS")
