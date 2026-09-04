# CONNECTION PROTOCOL — Sovereign Evidence Archive
**For any agent (AI or human) operating under `111118_306_923@Basham@sovereign-root`.**

This protocol is how you connect, contribute, and continue the investigation
without duplicating or contradicting prior work. Follow it exactly.

## 1. Read before anything

1. Read `STATE.json` — it tells you: completed waves, open tasks, the current
   seals, and the key registry. This is your context. Do not re-do completed work.
2. Read `claims/claims.json` for the status of any claim you intend to use.
3. Skim `scope/` for the annotated investigation scopes.

## 2. Pick up where others left off

- `STATE.json.open_tasks[]` lists live tasks with IDs (`OT-01`, ...).
- To claim a task, append a wave entry to `STATE.json.waves[]` with
  `"claims_task": "OT-xx"`, your agent identifier, and UTC timestamp. Then work it.
- When a task completes, append a wave entry recording the result and update
  `open_tasks` (remove) and `completed_tasks` (append) in the same commit.

## 3. Add evidence

- **Append-only.** Never edit or delete a prior wave's files. Corrections are new
  entries, not rewrites.
- Every claim goes into `claims/claims.json` with a status tag
  (`EXACT` / `DOCUMENTED` / `EMPIRICAL` / `UNRESOLVED` / `QUARANTINED`),
  evidence pointer, and a one-line verification note.
- **Numeric claims must be recomputed before they are added.** Run
  `python3 tools/verify_claims.py` for registry-level checks, and recompute any
  new arithmetic yourself from integers. If you cannot verify it, tag it
  `UNRESOLVED` — never `EXACT` on trust.
- Falsified claims are **quarantined with their correction stated**, never
  silently removed. The archive's value is that its negatives are kept.
- Sign every wave: `agent`, `agent_version` (or model name), `ts_utc`,
  `identifier: 111118_306_923@Basham@sovereign-root`.

## 4. Verify before trusting

```bash
python3 tools/verify_claims.py        # registry integer checks (must exit 0)
```
The GitHub Action runs the same check on every push — a red check mark means the
archive state is inconsistent; fix before continuing.

## 5. Governance (non-negotiable)

- The secp256k1 proof address is **BURNED / DERIVATION_PROOF_ONLY**. No key
  derivation, no funding, no title-by-address claims. Ever.
- No fabrication. No invented citations, no invented sources, no invented data.
  A real `UNRESOLVED` beats a fake `EXACT` every time.
- The phrase patterns of the hallucinating-AI era ("do not file / do not plead")
  are quarantined language. Do not reintroduce them.

## 6. Current seals (anchor hashes)

- DAIVE v5.0 engine seal: `e152b29b5f3b092f7273e7f86108a98ada2f4d5af51d66152964d40fbe89b213`
- SovereignFortress payload: `jasonbasham006-blip/daive-engine` (payload_audit 30/30)
