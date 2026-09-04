# Sovereign Evidence Archive
**Operator identifier:** `111118_306_923@Basham@sovereign-root`

The shared, append-only evidence store for the Sovereign Root investigation. Any
agent or human working under the operator identifier can **read the full record,
add verified evidence, and pick up where any previous agent left off** — without
asking anyone for context. The state of the investigation is machine-readable in
[`STATE.json`](STATE.json). The connection protocol is
[`protocol/CONNECT.md`](protocol/CONNECT.md). Start there.

## What lives here

| Path | Contents |
|---|---|
| `STATE.json` | Machine-readable investigation state: completed waves, open tasks, seals, key registry — read this first |
| `claims/claims.json` | Every claim as a registry entry with a status tag and verification note |
| `scope/` | Investigation scope documents, annotated with verification verdicts |
| `tools/verify_claims.py` | Self-contained integer re-verifier for the registry's numeric claims — run before trusting, run before adding |
| `protocol/CONNECT.md` | The full protocol: how to read, add, correct, and continue |

## Status tags (mandatory on every claim)

`EXACT` — recomputed from integers, passes bit-exact. `DOCUMENTED` — verified
against a primary external source (URL cited). `EMPIRICAL` — observed, plausible,
not independently confirmed. `UNRESOLVED` — open question. `QUARANTINED` — proven
false; kept with its correction, never silently deleted.

## Governance

The secp256k1 proof address `19UdRsPi5LMQo9a78n2f9QUDz4wJ4pptt4` is
**BURNED / DERIVATION_PROOF_ONLY**. Nothing in this archive derives keys, funds
wallets, or treats address derivation as title evidence. No monetary claims live
here — evidence and verification only.

## Sister repositories

- `jasonbasham006-blip/daive-engine` — the verification engine (clone-and-verify: its seal must reproduce).
- `jasonbasham006-blip/sovereign-mesh-network-v42` — the P2P mesh node (private).
