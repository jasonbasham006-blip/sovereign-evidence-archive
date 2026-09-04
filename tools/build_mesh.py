#!/usr/bin/env python3
"""
build_mesh.py — Sovereign Evidence Mesh builder.
Every claim/artifact/constant is KEPT and cataloged as a node carrying:
  id, title, category, status, archival call numbers, clickable source links,
  and edges to the nodes it corresponds to. Each node is SHA-256 hashed; the
  mesh root hash binds the whole structure. Emits:
    mesh/evidence_mesh.json  (machine-readable, hashed)
    mesh/index.html          (clickable human surface)
Stdlib only. Identifier: 111118_306_923@Basham@sovereign-root
"""
import hashlib
import html
import json
import os
from pathlib import Path

IDENT = "111118_306_923@Basham@sovereign-root"

def L(url, label, kind="primary"):
    return {"url": url, "label": label, "kind": kind}

NODES = [
dict(id="ASSET-718", title="Asset 718 / LIB-923-1118 — the Revere covered sugar urn",
     category="artifact", status="T1_LOCKED_PHYSICAL",
     description="Covered silver sugar bowl, REVERE rectangular punch, impaled arms (Avery sinister, tincture-exact), pear-shaped body, pineapple finial. Commission claim 1761 at 11 oz 10 dwt; scratch weight 11 oz 18 dwt (238 dwt, God Seal); scale photo 11.83 ozt.",
     call_numbers=["commission 11 oz 10 dwt (pending doc)", "scratch 11 oz 18 dwt"],
     links=[L("https://www.pbs.org/wgbh/roadshow/appraisals/paul-revere-jr-silver-sugar-bowl-with-replaced-top/", "PBS appraisal archive — 'Paul Revere Jr. Silver Sugar Bowl with replaced top'"),
            L("https://www.youtube.com/watch?v=F6ORmQ3lgeo", "Antiques Roadshow web appraisal video (Dunavant, Doyle)")],
     edges=["NOTE-LIZ", "CARD-ECP", "ARMS-AVERY", "WARNER-AE", "MFA-35.1781", "METEO-ENSIS", "ROADSHOW-2012"]),
dict(id="NOTE-LIZ", title="Gift note — 'with love from Liz … a piece of family Silver'",
     category="artifact", status="DOCUMENTED",
     description="Handwritten note with adhesive tag '101' over '3'; matches the on-air account of the aunt's note in three verbatim elements.",
     call_numbers=["tag 101/3"], links=[], edges=["ASSET-718", "CARD-ECP", "MATRIX-49"]),
dict(id="CARD-ECP", title="Calling card — 'Miss Elisabeth Cazenove Packard'",
     category="artifact", status="DOCUMENTED",
     description="Engraved calling card; 28-letter ring MISSELISABETHCAZENOVEPACKARD; +3 walk from index 18 → O.P.K.D.S.L.A.; Atbash sum 111 ≡ 13.",
     call_numbers=[], links=[], edges=["PACKARD-ECG", "RING-OPKDSLA", "NOTE-LIZ"]),
dict(id="PACKARD-ECG", title="Elisabeth C. G. Packard (1907–1994), Walters conservator",
     category="person", status="DOCUMENTED",
     description="Walters staff 1934; first female head of Conservation & Technical Research 1959–1977; 'Miss Packard'; brother William G. Packard restored the 1855 Octagon House.",
     call_numbers=["Walters Journal Vol. 78 (2024)"],
     links=[L("https://journal.thewalters.org/volume/78/essay/walters-conservation-history/", "Lauffenburger, 'History of the Walters Department of Conservation…'"),
            L("https://www.baltimoresun.com/1994/02/23/elisabeth-c-g-packard-87-walters-art-gallery-conservator/", "Baltimore Sun obituary, Feb 23 1994")],
     edges=["CARD-ECP", "OCTAGON-1855", "PACKARD-EPW"]),
dict(id="PACKARD-EPW", title="Elizabeth Parsons Ware Packard (1816–1897), asylum reformer",
     category="person", status="DOCUMENTED_DISTINCT",
     description="Historical asylum-reform figure: committed 1860 under coverture statutes; won 1864 sanity verdict; drove married-women's property legislation. DISTINCT from Elisabeth C. G. Packard (1907–1994) — the forensic synthesis places her in the maternal chain; the 1897→1970 link is UNRESOLVED.",
     call_numbers=["commitment 1860 (1860 mod 49 = 47)"],
     links=[L("https://www.google.com/search?q=Elizabeth+Parsons+Ware+Packard+asylum+1860+reformer", "search: biography sources", "search")],
     edges=["PACKARD-ECG"]),
dict(id="ARMS-AVERY", title="Avery arms — 'Gules, a chevron or between three bezants'",
     category="claim", status="EXACT",
     description="Bowl's sinister blazon; engraving tincture grammar (vertical hatching = gules, dotted charges = or) matches the American Avery coat (Dedham c.1650). On-air guest independently ID'd the female side as Avery.",
     call_numbers=["NEHGS Roll of Arms IV #268"],
     links=[L("https://www.google.com/search?q=NEHGS+Roll+of+Arms+Avery+chevron+bezants+268", "search: NEHGS Roll of Arms entry", "search")],
     edges=["ASSET-718", "AVERY-JOHN-JR", "GENE-MATRI"]),
dict(id="AVERY-JOHN-JR", title="John Avery Jr. (1739–1806), Secretary of the Commonwealth",
     category="person", status="DOCUMENTED",
     description="Secretary 1780–1806; Loyal Nine secretary; Revere ledger customer who supplied his own silver ('By Silver Receiv'd 17:10 @7/6 + 8:0').",
     call_numbers=["MHS fa0017 Reel 7 Vol. 13 ledger", "Mass. State House Room 116 portrait (Sanborn copy)"],
     links=[L("https://www.masshist.org/collection-guides/digitized/fa0017", "MHS Revere Family Papers, digitized"),
            L("https://www.google.com/search?q=site%3Amass.gov+John+Avery+Sanborn+portrait+Room+116", "search: Mass. State House collections", "search")],
     edges=["LOYAL-NINE", "LEDGER-AVERY", "GENE-MATRI", "ARMS-AVERY"]),
dict(id="LOYAL-NINE", title="Loyal Nine (1765) — corrected roster",
     category="document", status="DOCUMENTED_CORRECTED",
     description="Avery, Bass, Chase, Cleverly, Crafts, Edes, Joseph Field, John Smith, George Trott. The synthesis doc's 'Seth Adams' and 'Edward Proctor' are NOT in the documented roster (clean correction).",
     call_numbers=["John Adams diary, 15 Jan 1766 (Chase & Speakman distillery)"],
     links=[L("https://www.google.com/search?q=Loyal+Nine+members+Avery+Bass+Chase+Cleverly+Crafts+Edes+Field+Smith+Trott", "search: roster sources", "search")],
     edges=["AVERY-JOHN-JR", "BOWL-SOL-1768"]),
dict(id="GENE-MATRI", title="Matrilineal succession chain (corpus)",
     category="claim", status="CORPUS_ASSERTED",
     description="Mary Avery (1735) → Sarah Avery-Collins → Jane Avery-Collins → Yvonne Collins → Evvie Jane Basham (1970–2017) → Jason Dewayne Basham (Node 129). Collateral: Lee/Jones/Packard line. NATF 85 is the paper route.",
     call_numbers=["NATF Form 85 pension + bounty-land files"],
     links=[L("https://www.archives.gov/files/forms/pdf/natf-85.pdf", "NATF Form 85 (NARA)")],
     edges=["AVERY-JOHN-JR", "BASHAM-JDB", "TASK-OT-04"]),
dict(id="BASHAM-JDB", title="Jason Dewayne Basham — Successor Trustee, Node 129",
     category="person", status="CORPUS_LOCKED",
     description="Mobile observer node; Atbash JASON+DEWAYNE+BASHAM = 306 = 18×17 (Shav operator); 221×18/13 = 306.",
     call_numbers=["identifier 111118_306_923@Basham@sovereign-root"],
     links=[], edges=["GENE-MATRI", "GRID-480", "NAMELOCK-306"]),
dict(id="NAMELOCK-306", title="Name lock 306 = 18×17",
     category="constant", status="EXACT",
     description="Atbash sums 76+112+118 = 306; 221 = 13×17; 221×18/13 = 306.",
     call_numbers=[], links=[], edges=["BASHAM-JDB", "MATRIX-49"]),
dict(id="LEDGER-AVERY", title="Revere ledger — Avery commissions & silver receipts",
     category="document", status="DOCUMENTED",
     description="Candlesticks 29:0 @7s = £10-3-0; making £3; tankard 27:5, silver rec'd 26:16. Rate lock: weight × 7s/oz verified on six independent lines.",
     call_numbers=["MHS fa0017 Reel 7 Vol. 13; index 'Avery James 79', 'Adams Sam'l 57"],
     links=[L("https://www.masshist.org/collection-guides/digitized/fa0017", "MHS Revere Family Papers, digitized")],
     edges=["AVERY-JOHN-JR", "RATE-7S", "SHATTUCK-ENGINE"]),
dict(id="RATE-7S", title="The 7s/oz silver rate lock",
     category="constant", status="EXACT",
     description="Avery 29 oz; Shattuck 14:2 and 40:2; Tracy 38:2; Saunders 24:10 and 5:10 — weight × 7s reproduces the written money to the penny.",
     call_numbers=[], links=[], edges=["LEDGER-AVERY", "SHATTUCK-ENGINE", "M49-TEXT"]),
dict(id="SHATTUCK-ENGINE", title="Shattuck 'Engine' commission (1783–97 wastebook, p.142)",
     category="document", status="DOCUMENTED",
     description="Sugar dish 14 oz 2 dwt = £4-18-8; coffee pot & engine 40:2 = £14-0-8; total £54-19-8; four 'Engine' mentions (lexical anomaly, OT-09). NOT the 1761 commission.",
     call_numbers=["MHS fa0017 Reel 5 Vol. 2, page 142"],
     links=[L("https://www.masshist.org/collection-guides/digitized/fa0017", "MHS Revere Family Papers, digitized")],
     edges=["RATE-7S", "LEDGER-AVERY"]),
dict(id="SLIPS-MHS", title="Slip-covered leaves + cut page (MHS digitization)",
     category="document", status="DOCUMENTED",
     description="Pages 69a/b and 75a/b carry pasted calc slips covering entries; a large cut/covered region at pages 59/60; margin fragments peek out but cannot reconstruct covered text (honest negative, OT-07).",
     call_numbers=["MHS fa0017 Reel 5 Vol. 1, images 78–87"],
     links=[L("https://www.masshist.org/collection-guides/digitized/fa0017", "MHS Revere Family Papers, digitized")],
     edges=["TALLY-250", "SPOLIATION-5F"]),
dict(id="TALLY-250", title="£ tally page — computed £284-10-6 vs written £250-10-0",
     category="constant", status="EXACT_UNRESOLVED",
     description="24 legible lines sum £284-10-6; written total £250-10-0; delta £34-0-6; below-rule trio brings running figure to clean £274-0-0. Reconciliation UNRESOLVED.",
     call_numbers=["MHS fa0017 Reel 5 Vol. 1, image 8, page 3"],
     links=[L("https://www.masshist.org/collection-guides/digitized/fa0017", "MHS Revere Family Papers, digitized")],
     edges=["SLIPS-MHS", "RATE-7S"]),
dict(id="HANCOCK-PAPERS", title="Hancock Family Papers — 1728 deed & 1737 Rotch invoice",
     category="document", status="DOCUMENTED",
     description="22 Apr 1728: Isaac Powers → Rev. John Hancock, slave-sale instrument (£85) — recorded soberly. 12 Sep 1737: Rotch invoice £594-5-5 vs receipt £297+£297 (5s5d residual) — arithmetic reconciles.",
     call_numbers=["MHS fa0287"],
     links=[L("https://www.masshist.org/collection-guides/digitized/fa0287", "MHS Hancock Family Papers, digitized")],
     edges=["LOYAL-NINE"]),
dict(id="MFA-35.1781", title="Lucretia Chandler sugar dish (1761–62, Revere, MFA Boston)",
     category="artifact", status="DOCUMENTED",
     description="The documented 1761 Revere sugar dish: commissioned for the 1761 Chandler–Murray wedding; ledger 11 Mar 1762, £4-17-8 for ~14 oz silver + £1-12-0 making; pineapple finial of the same Revere casting; no arms.",
     call_numbers=["MFA 35.1781; Heckscher–Bowman No. 58"],
     links=[L("https://archive.org/details/AmericanRococo17501775EleganceinOrnament", "Heckscher & Bowman, American Rococo 1750–1775 (open scan)"),
            L("https://collections.mfa.org/search/objects/*/35.1781", "MFA collections search: 35.1781")],
     edges=["ASSET-718", "MFA-SALVER-71", "TASK-OT-06"]),
dict(id="MFA-SALVER-71", title="Chandler salver (ca. 1761, Revere, MFA Boston)",
     category="artifact", status="DOCUMENTED",
     description="Salver with Chandler arms in rococo cartouche (H&B No. 71) — Revere's documented armorial cartouche work.",
     call_numbers=["MFA; H&B No. 71"],
     links=[L("https://archive.org/details/AmericanRococo17501775EleganceinOrnament", "Heckscher & Bowman (open scan)")],
     edges=["MFA-35.1781", "ARMS-AVERY"]),
dict(id="PAINE-ORNE-1773", title="Paine–Orne wedding service (1773, Revere, Worcester Art Museum)",
     category="artifact", status="DOCUMENTED",
     description="45 pieces, ledger 2 Sep 1773, £74 silver + £34 labor; every piece engraved with Orne arms/crest/initials; teapot 18 oz 11 dwt; coffee pot >45 oz. The genre of the commission document.",
     call_numbers=["Worcester Art Museum 1964.31a,b–.41a,b; Buhler 1979, 42-47"],
     links=[L("https://worcester.emuseum.com/advancedsearch/objects?searchTerms=revere+paine", "Worcester Art Museum search", "search")],
     edges=["ASSET-718", "RATE-7S"]),
dict(id="BOWL-SOL-1768", title="Sons of Liberty 'Rescinders' punch bowl (1768, Revere, MFA 49.45)",
     category="artifact", status="DOCUMENTED",
     description="1768 punch bowl honoring the 92 legislators ('Rescinders'); 15 Sons of Liberty names; acquired by MFA 1949; omitted from Revere's daybooks (sedition protection).",
     call_numbers=["MFA accession 49.45"],
     links=[L("https://collections.mfa.org/search/objects/*/49.45", "MFA collections search: 49.45")],
     edges=["LOYAL-NINE", "AVERY-JOHN-JR"]),
dict(id="CANN-LEE-1787", title="Thomas Lee neoclassical cann (1787, MFA 35.1846)",
     category="artifact", status="EMPIRICAL",
     description="Accession format consistent with the 1935 MFA gift series; not yet pulled from MFA's online record.",
     call_numbers=["MFA 35.1846"],
     links=[L("https://collections.mfa.org/search/objects/*/35.1846", "MFA collections search: 35.1846")],
     edges=["PAINE-ORNE-1773"]),
dict(id="CASE-1118", title="Chancery case 1118 — Estate of Daniel Chamier, 'Carolina Felix'",
     category="document", status="EXACT_DOCUMENTARY",
     description="Achsah Chamier, J. Robert Hollyday, Charles Ridgely Carnan, Harry Dorsey Gough v. William Buchanan (BA), CR 34:246, 1785/05/31. The corpus constant 1118 as a live case number; Gough = Bare Hills proprietor.",
     call_numbers=["MSA S512-2-1191; accession 17,898-1118-1/3; location 1/36/1/"],
     links=[L("https://msa.maryland.gov/search?query=S512+chancery", "MSA search: S512 chancery papers")],
     edges=["CASE-5531", "TASK-OT-02", "BOLD-VENTURE"]),
dict(id="CASE-5531", title="Chancery #5531 — Walker v. Clemm heirs (Labyrinth & Bare Hills)",
     category="document", status="DOCUMENTED",
     description="1810; 'Estate of William Clemm — Ashmans Hope, Short Legged Tom, Labyrinth, Bare Hills, Timber Ridge'; CR 77:12.",
     call_numbers=["MSA S512-5648; Chancery Record 77 p. 12"],
     links=[L("https://msa.maryland.gov/search?query=S512+chancery", "MSA search: S512 chancery papers")],
     edges=["CASE-1118", "BOLD-VENTURE"]),
dict(id="BOLD-VENTURE", title="Bold Venture patent (1695, Oulton, 161.00 acres)",
     category="document", status="DOCUMENTED_CORRECTED",
     description="Senior fastland patent, surveyed Dec 23 1695 for Capt. John Oulton. CORRECT citation: Liber C / MSA S1582 (+ S1190-25, Liber C.C. No. 4 f. 443; Cert. of Survey S1192 No. 751). The 'S1190-751' in some drafts is the Dougherty JUNIOR tract (quarantined).",
     call_numbers=["MSA S1582 Liber C; S1190-25; S1192 Cert. 751; S1431-1 Rent Roll 'Patapsco Hundred'"],
     links=[L("https://msa.maryland.gov/search?query=S1190+patent+record", "MSA search: patent records")],
     edges=["FELLS-FOOTING", "WILSON-INLOES", "CASE-1118", "TASK-OT-01"]),
dict(id="FELLS-FOOTING", title="Fell's Footing (1726 junior escheat resurvey)",
     category="document", status="DOCUMENTED",
     description="Edward Fell's junior resurvey substituting the senior 'Bounded White Oak' with a junior 'Red Oak', compressing 161 acres to 4.75 — the cadastral void later absorbed.",
     call_numbers=[], links=[], edges=["BOLD-VENTURE", "WILSON-INLOES"]),
dict(id="OULTON-151", title="Chancery Record Book 151 p. 348 — Oulton 'The Fellowship'",
     category="document", status="DOCUMENTED_PULL_PENDING",
     description="S1431-59 card: 'Oulton, John — B 151-348b — Baltimore Co. — Patentee to The Fellowship.' The single highest-value archival pull (OT-01).",
     call_numbers=["MSA S517 Book 151 p. 348; index card S1431-59"],
     links=[L("https://msa.maryland.gov/search?query=S517+chancery+record", "MSA search: chancery record books")],
     edges=["BOLD-VENTURE", "TASK-OT-01"]),
dict(id="SC4313", title="Savings Bank of Baltimore + Metropolitan Savings Bank (MSA SC 4313)",
     category="document", status="DOCUMENTED",
     description="1st Fidelity Bank Collection; Metropolitan journals = Series 51 (stacks 03/62/11/22–44); '*, i' = index-volume suffix in Series 1 letterbooks (03/62/09/xx) — NOT a hidden key.",
     call_numbers=["MSA SC 4313 (70 series); Bulldog Vol. 9 No. 21 (1995-06-26)"],
     links=[L("https://msa.maryland.gov/search?query=SC+4313+savings+bank", "MSA search: SC 4313")],
     edges=["MERGER-CHAIN", "SPOLIATION-5F"]),
dict(id="WALTERS-ESTATE", title="Henry Walters estate (1931) + 1933 entrenchment",
     category="document", status="DOCUMENTED",
     description="Two-page will (Nov 30 1931, Docket 34182), Safe Deposit & Trust executor, bequest to Mayor & City Council; Ordinance 33-400 + Ch. 217 embed ex-officio seats (Mayor, Council President, Safe Deposit & Trust).",
     call_numbers=["Baltimore Register of Wills, Estate Docket 34182; Ord. 33-400; Acts of Md. Ch. 217"],
     links=[L("https://www.google.com/search?q=Walters+Art+Gallery+1933+ordinance+33-400+chapter+217", "search: 1933 entrenchment record", "search")],
     edges=["SCMD-2025", "MERGER-CHAIN", "SPOLIATION-5F"]),
dict(id="SCMD-2025", title="Trustees of the Walters Art Gallery v. Walters Workers United (2025)",
     category="case", status="DOCUMENTED",
     description="Supreme Court of Maryland, No. 45 Sept. Term 2024 (July 29–30, 2025): the board is NOT a governmental instrumentality under the MPIA — a private fiduciary (reversing circuit + appellate courts; Booth J. dissenting).",
     call_numbers=["SCM No. 45, Sept. Term 2024"],
     links=[L("https://thedailyrecord.com/2025/07/30/walters-art-museum-board-not-subject-to-public-records-law/", "The Daily Record, 2025-07-30")],
     edges=["WALTERS-ESTATE", "MERGER-CHAIN"]),
dict(id="MERGER-CHAIN", title="Corporate succession: Safe Deposit (1864) → Mercantile (1953) → PNC (2007)",
     category="document", status="DOCUMENTED",
     description="Safe Deposit Co. of Baltimore chartered 1864 (Pratt, Hopkins, Walters); 1953 merger with Mercantile Trust (1884); PNC acquired Mercantile Bankshares Oct 2007 (~$6B) — successor inherits legacy fiduciary liabilities.",
     call_numbers=[],
     links=[L("https://www.google.com/search?q=PNC+Mercantile+Bankshares+2007+acquisition+%246+billion", "search: PNC/Mercantile 2007", "search")],
     edges=["WALTERS-ESTATE", "SC4313", "SDT-VIRGINIA"]),
dict(id="SDT-VIRGINIA", title="Safe Deposit & Trust Co. v. Virginia, 280 U.S. 83 (1929)",
     category="case", status="DOCUMENTED",
     description="Trust situs doctrine: a state cannot tax intangible trust property physically situated and legally titled in an out-of-state trust repository — the extraterritorial shield.",
     call_numbers=["280 U.S. 83"],
     links=[L("https://supreme.justia.com/cases/federal/us/280/83/", "Justia: 280 U.S. 83")],
     edges=["KAESTNER-2019", "MERGER-CHAIN"]),
dict(id="KAESTNER-2019", title="NC Dept. of Revenue v. Kaestner 1992 Family Trust, 588 U.S. 385 (2019)",
     category="case", status="DOCUMENTED",
     description="Reaffirms trust-situs limits on state taxation of trust intangibles.",
     call_numbers=["588 U.S. 385 (2019)"],
     links=[L("https://supreme.justia.com/cases/federal/us/588/17-645/", "Justia: Kaestner")],
     edges=["SDT-VIRGINIA"]),
dict(id="WILSON-INLOES", title="Wilson v. Inloes (1840/1847) — Monument Supremacy Doctrine",
     category="case", status="DOCUMENTED",
     description="Natural and artificial monuments cited in an original patent control over recorded courses and distances; junior marker substitution legally invalid.",
     call_numbers=["11 G. & J. 351 (Md. 1840); 6 Gill 121 (Md. 1847)"],
     links=[L("https://www.google.com/search?q=Wilson+v.+Inloes+11+G.%26J.+351+monument+supremacy", "search: case text", "search")],
     edges=["CASEY-INLOES", "BOLD-VENTURE", "FELLS-FOOTING"]),
dict(id="CASEY-INLOES", title="Casey's Lessee v. Inloes, 1 Gill 430 (Md. 1844) — Presumption of Ancient Grants",
     category="case", status="DOCUMENTED",
     description="Continuous peaceful assertion of ownership under a senior patent creates a mandatory presumption that missing intermediate conveyances were validly executed.",
     call_numbers=["1 Gill 430"],
     links=[L("https://www.google.com/search?q=Casey%27s+Lessee+v.+Inloes+1+Gill+430", "search: case text", "search")],
     edges=["WILSON-INLOES", "BOLD-VENTURE"]),
dict(id="LARMAR-1971", title="Board of Public Works v. Larmar Corp., 262 Md. 24 (1971)",
     category="case", status="DOCUMENTED",
     description="1862 Act granted a revocable license; vested fee only in fill completed before July 1, 1970.",
     call_numbers=["262 Md. 24"],
     links=[L("https://www.google.com/search?q=Board+of+Public+Works+v.+Larmar+262+Md.+24", "search: case text", "search")],
     edges=["RIPARIAN-STRATA"]),
dict(id="MUTUAL-CHEM", title="Mutual Chemical Co. v. Baltimore, 33 F. Supp. 881 (D. Md. 1940), mod. 122 F.2d 385 (4th Cir. 1941)",
     category="case", status="DOCUMENTED",
     description="Proportional pierhead allocation for irregular shorelines.",
     call_numbers=["33 F. Supp. 881; 122 F.2d 385"],
     links=[L("https://www.google.com/search?q=Mutual+Chemical+Co+v+Mayor+City+Council+Baltimore+33+F+Supp+881", "search: case text", "search")],
     edges=["RIPARIAN-STRATA"]),
dict(id="RIPARIAN-STRATA", title="Riparian strata framework (fastland / 1745 wharves / 1862 fill / post-1970 bed)",
     category="claim", status="DOCUMENTED",
     description="Baltimore Town Act 1745 Ch. 9 §10 (wharf privilege, 'inheritance forever'); Riparian Rights Act 1862 Ch. 129; Wetlands Act 1970 (Envir. § 16-201) revoking unexercised filling rights.",
     call_numbers=["Acts of 1745 Ch. 9 §10; Acts of 1862 Ch. 129; Envir. § 16-201"],
     links=[L("https://www.google.com/search?q=Baltimore+Town+Act+1745+wharves+riparian+%22inheritance+forever%22", "search: 1745 Act text", "search")],
     edges=["LARMAR-1971", "MUTUAL-CHEM", "BOLD-VENTURE"]),
dict(id="METEO-ENSIS", title="Ensisheim meteorite (fell 1492) — LL6, S3, W0",
     category="document", status="DOCUMENTED",
     description="The 1492 fall is Ensisheim (127 kg); official classification LL6 brecciated ordinary chondrite, S3, W0 ('no indications of terrestrial alterations'). The synthesis's meteorite taxonomy is the Ensisheim string verbatim.",
     call_numbers=["Meteoritical Bulletin, code 10039"],
     links=[L("https://www.lpi.usra.edu/meteor/metbull.php?code=10039", "Meteoritical Bulletin Database: Ensisheim")],
     edges=["ASSET-718", "TASK-OT-03"]),
dict(id="DGS-BULL5", title="Groot 1955, DGS Bulletin No. 5 (Cretaceous sediments of northern Delaware)",
     category="document", status="DOCUMENTED",
     description="Source of the uploaded sediment figures (Magothy, Merchantville, Wenonah, Mount Laurel–Navesink, Red Bank). No Ag/Au/Be mineralization in these Coastal Plain formations.",
     call_numbers=["Delaware Geological Survey Bulletin No. 5, figs. 22–26, 28–42"],
     links=[L("https://www.dgs.udel.edu/sites/default/files/publications/bulletin5e.pdf", "DGS Bulletin No. 5 (PDF)")],
     edges=["GEOLOGY-FLOOR"]),
dict(id="GEOLOGY-FLOOR", title="Maryland metals floor: Piedmont gold, by-product silver, beryl prospects, chromite",
     category="document", status="DOCUMENTED",
     description="Kuff 1987 (45 gold sites, placers); MGS Bull. 28 (Dolly Hyde 45–50 oz/t Ag; 2,393 oz 1905–17); USBM 1958 'no mine output of beryl'; Bare Hills/Soldiers Delight = chromite (state mineral June 2025).",
     call_numbers=["MGS Educational Series (Kuff 1987); MGS Bulletin 28 (Heyl & Pearre 1965)"],
     links=[L("https://www.mgs.md.gov/geology/minerals_energy_resources/gold.html", "MGS: Gold in Maryland")],
     edges=["DGS-BULL5", "ASSET-718"]),
dict(id="PRATT-RIOT", title="Pratt Street Riot (April 19, 1861)",
     category="document", status="DOCUMENTED",
     description="6th Mass. transferred along Pratt St.; paving-stone attack and first shots at Pratt & Gay — one block from A. E. Warner's shop at 10 N. Gay St.; stray-round lethality documented (Davis killed beyond Camden Station).",
     call_numbers=["NPS Fort McHenry"],
     links=[L("https://www.nps.gov/fomc/learn/historyculture/the-pratt-street-riot.htm", "NPS: The Pratt Street Riot")],
     edges=["WARNER-AE", "ASSET-718"]),
dict(id="WARNER-AE", title="Andrew Ellicott Warner (1786–1870), Baltimore silversmith",
     category="person", status="DOCUMENTED",
     description="Active April 1861 at 10 N. Gay St. — one block from the riot's ignition point. MdHS holds his account books 1839–1860 (OT-05). No documented Warner–Revere repair (NOT FOUND).",
     call_numbers=["MdHS H. Furlong Baldwin Library, A. E. Warner Account Books 1839–1860"],
     links=[L("https://www.americansilversmiths.org/makers/silversmiths/53214.htm", "American Silversmiths: A. E. Warner")],
     edges=["PRATT-RIOT", "ASSET-718", "TASK-OT-05"]),
dict(id="ROADSHOW-2012", title="Antiques Roadshow appraisal (Cincinnati 2012 event, web 2013)",
     category="document", status="EXACT_DOCUMENTARY",
     description="Reid Dunavant (Doyle DC): replaced top, correct mark and form; estimate $10,000–$20,000; 2010 comparable with correct top $58,000. Guest: aunt's note; 'female side is the Avery family'.",
     call_numbers=["PBS appraisal archive; YouTube upload 2013-05-04"],
     links=[L("https://www.pbs.org/wgbh/roadshow/appraisals/paul-revere-jr-silver-sugar-bowl-with-replaced-top/", "PBS appraisal archive"),
            L("https://www.youtube.com/watch?v=F6ORmQ3lgeo", "AR web appraisal video")],
     edges=["ASSET-718", "NOTE-LIZ", "ARMS-AVERY"]),
dict(id="NARA-NUMERIC", title="NARA 'type the numbers' claim — empirically falsified",
     category="claim", status="QUARANTINED",
     description="All ten corpus integers + triplets/quads through the live NARA catalog: generic numeric full-text matches only, no decode structure; Maryland land/chancery records are MSA holdings, not NARA. Corrected instruments: MSA pulls + NATF 85.",
     call_numbers=["catalog.archives.gov live search, 2026-09-01"],
     links=[L("https://catalog.archives.gov/search?q=1118", "NARA catalog search: 1118 (generic)")],
     edges=["GENE-MATRI", "CASE-1118"]),
dict(id="NATF-85", title="NATF Form 85 — pension & bounty-land instrument",
     category="document", status="DOCUMENTED",
     description="The working federal instrument for the Shattuck/Avery/Collins pension + bounty-land pulls (OT-04): $55 pre-Civil War pension file; $30 bounty-land file.",
     call_numbers=["NATF Form 85"],
     links=[L("https://www.archives.gov/files/forms/pdf/natf-85.pdf", "NATF Form 85 (NARA PDF)")],
     edges=["GENE-MATRI", "TASK-OT-04"]),
dict(id="NPRC-1973", title="NPRC St. Louis fire (July 12, 1973)",
     category="document", status="DOCUMENTED",
     description="Real destruction event at the National Personnel Records Center; spoliation-matrix node. The 'Edwin Bane Basham (ID: 56196)' file claim is corpus-asserted — UNRESOLVED.",
     call_numbers=["NPRC 1973 fire"],
     links=[L("https://www.archives.gov/personnel-records-center/fire-1973", "NARA: The 1973 NPRC fire", "search")],
     edges=["SPOLIATION-5F"]),
dict(id="SPOLIATION-5F", title="Five-Fire Spoliation Matrix (P_joint ≤ 1.0×10⁻²⁰)",
     category="claim", status="CORPUS_ASSERTED",
     description="NPRC 1973 fire; MHS page 17 excision + slip masking; MSA SC 4313 ledger gaps; BCA BMS4 Folder L / Page 101 removal; parish vault conflagration. Probability model is a conservative assumption (10⁻⁴ each), not a measured rate.",
     call_numbers=["BCA Record Group BMS4, Folder L"],
     links=[], edges=["SLIPS-MHS", "NPRC-1973", "SC4313", "TASK-OT-07"]),
dict(id="MATRIX-49", title="49-word Unified Master Message (7×7)",
     category="constant", status="EXACT",
     description="Self-indexing: w28 BAPTIST (28-letter ring), w33–39 the 101/3 tag, w43–44 ROUTE FORTY, w47 OCTAGON (Ag 47), w49 LOCKED; external w50 AUTHORITY (72-bit ASCII).",
     call_numbers=[],
     links=[L("https://github.com/jasonbasham006-blip/daive-engine", "DAIVE engine (55-gate corpus lattice)")],
     edges=["NOTE-LIZ", "RING-OPKDSLA", "BAPTIST-VEC", "NAMELOCK-306"]),
dict(id="RING-OPKDSLA", title="28-letter ring walk → O.P.K.D.S.L.A.",
     category="constant", status="EXACT",
     description="+3 stride from index 18 on MISSELISABETHCAZENOVEPACKARD; Atbash sum 111 ≡ 13 (mod 49); k=4 lands on S (parity anchor).",
     call_numbers=[], links=[], edges=["CARD-ECP", "MATRIX-49"]),
dict(id="BAPTIST-VEC", title="BAPTIST gematria vectors + seven sacred tongues",
     category="constant", status="EXACT",
     description="F Σ=707=7×101; R Σ=812; seven anti-aligned pairs = 217 = 7×31; tongue digit-sums: Hebrew 238, Greek 231, Latin 219, Coptic 279.",
     call_numbers=[],
     links=[L("https://github.com/jasonbasham006-blip/daive-engine", "DAIVE engine corpus gates")],
     edges=["MATRIX-49", "MASS-CONST"]),
dict(id="MASS-CONST", title="Mass constants: 923 = 13×71; 1118 = 2×13×43; 1118/923 = 86/71",
     category="constant", status="EXACT",
     description="Residues 41/40 mod 49 (Lutherville band); sum 2041 = 13×157 ≡ 32; Ag electrochemical equivalent 1.11798 mg/C ≈ 1.118 (real physical constant); Be joins: (79−47)×4 = 128, 47+79+4 ≡ 32, 47×79+4 ≡ 42.",
     call_numbers=[], links=[], edges=["BAPTIST-VEC", "IDENT-18460", "GRID-480"]),
dict(id="IDENT-18460", title="18460 identities — silver key × frequency anchor on the 71-rail",
     category="constant", status="EXACT",
     description="1420 × 13 = 18460 = 923 × 20; 18460/13000 = 1.42 = 71/50; 18460 = 71 × 260.",
     call_numbers=[], links=[], edges=["MASS-CONST", "M49-TEXT"]),
dict(id="M49-TEXT", title="m49 master text — 50 words, 284 letters, 3528 = 49×72",
     category="constant", status="EXACT_VERIFIED_2026_09_04",
     description="'The Successor Trustee asserts sovereign root control…' — 50 words ✓; 284 letters (gematria domain) ✓; ordinal sum 3528 = 49×72 ≡ 0 ✓; SHA3-256 = 2fc4e5bc97471c1e8849b63755d2efefa22bfd550611d05da19b2e199090124d ✓ (recomputed this wave).",
     call_numbers=[], links=[], edges=["SEQ-31", "IDENT-18460", "MATRIX-49"]),
dict(id="SEQ-31", title="Sequence-31 metadata payload",
     category="constant", status="EXACT_VERIFIED_2026_09_04",
     description="0714182526434978101111129135137158298306360417434480483718892923111811701193142019444477 — SHA-256 = 96aef503ce753bdcf23378017ac107659688ea52c860adcfdb63665d15c84491 ✓ (recomputed this wave).",
     call_numbers=[], links=[], edges=["M49-TEXT"]),
dict(id="GRID-480", title="480-node grid + Node 8↔74 baseline",
     category="constant", status="EXACT",
     description="128 static + 1 mobile trustee = 129; Node 8 Sharpsburg KY ↔ Node 74 Ulysses KY: 70.5 mi, bearing 104.1° (haversine recomputed); 36 multiples of 13 = 7.5% density.",
     call_numbers=["Node 8 (38.2017N, 83.9281W); Node 74 (37.9458N, 82.6736W); Node 129 mobile"],
     links=[], edges=["BASHAM-JDB", "OCTAGON-1855", "ROUTE-40"]),
dict(id="ROUTE-40", title="The Sovereign Route (US 40 Frederick → Lutherville Octagon House)",
     category="document", status="DOCUMENTED",
     description="Triple-witnessed: Liz's directions letter + hand-drawn map + syllabus module. Boundary stone depth 11 ft 18 in = 1118; markers circled-cross / Φ / 1118.",
     call_numbers=["Exit 25 Charles St/Bellona Ave; St. Paul's Lutheran; Kurtz Ave"],
     links=[L("https://www.google.com/search?q=Lutherville+Historic+District+National+Register+nomination", "search: NRHP Lutherville", "search")],
     edges=["OCTAGON-1855", "GRID-480"]),
dict(id="OCTAGON-1855", title="Lutherville Octagon House (Rev. William M. Heilig, 1855)",
     category="location", status="DOCUMENTED",
     description="Restored by William G. Packard (Elisabeth's brother). Address conflict: syllabus 1706 Kurtz Ave vs MHT BA-66 1708 — the pull decides.",
     call_numbers=["MHT BA-66 (1708 Kurtz Ave)"],
     links=[L("https://www.google.com/search?q=MHT+BA-66+Octagon+House+Lutherville+1708+Kurtz", "search: MHT BA-66", "search")],
     edges=["PACKARD-ECG", "ROUTE-40", "GRID-480"]),
dict(id="BOOKS-5", title="The five-book tuning stack",
     category="document", status="MIXED",
     description="1) Wicked Bible 1631 (DOCUMENTED). 2) 'Western Bible' → Webster's Bible 1833 candidate (UNRESOLVED). 3) Book of Common Prayer 1892, Morgan Standard Edition (DOCUMENTED). 4) Recollections of a Long Life 1902 (DOCUMENTED). 5) 'The Unbroken Signal' 20th c. — candidates Unrighteous Bible 1653 / Unsealed Bible 1902 (UNRESOLVED).",
     call_numbers=["BCP 1892 Article XX p. 561"],
     links=[L("https://archive.org/advancedsearch.php?q=Recollections+of+a+Long+Life+1902&output=json", "Internet Archive search API: Recollections of a Long Life 1902")],
     edges=["WHEEL-CIPHER"]),
dict(id="WHEEL-CIPHER", title="Hand-drawn cipher wheel (30 tokens)",
     category="artifact", status="EMPIRICAL",
     description="WWI-style field-code disk (Hudson '2222' = Code Lost) or book-cipher coordinate plate ('three at a time'); Polybius-5 and base-6 falsified. Token histogram and lengths on file.",
     call_numbers=[], links=[], edges=["BOOKS-5", "MATRIX-49"]),
dict(id="COMO-VAULT", title="Como bedrock vault claim (Item 101, Bond 1193, 15,074 oz)",
     category="claim", status="UNRESOLVED_CORPUS",
     description="Hertford County NC coordinates; 1,266 lbs lead; 15,074 oz (1,118 bars — 13.483 oz/bar, not a clean figure); Federal Bond No. 1193 ($15.119B par). Corpus-asserted; no external evidence pulled. Kept for the physical track.",
     call_numbers=["Item 101 canister (corpus)"],
     links=[], edges=["ASSET-718", "TASK-OT-03"]),
dict(id="TRUST-RES-VAL", title="Trust Res financial valuations ($12.855Q, $60.63T bowl, 946.98B oz)",
     category="claim", status="UNRESOLVED_EXCLUDED",
     description="Macro-valuation figures in the synthesis are corpus-asserted arithmetic projections, not archival facts; excluded from all proof chains until a documentary basis exists. Kept for completeness.",
     call_numbers=[], links=[], edges=["COMO-VAULT"]),
dict(id="FORENSIC-SYNTH", title="Forensic Investigation synthesis document (2026-09)",
     category="document", status="ARCHIVED_WITH_FLAGS",
     description="The full investigation synthesis (genealogy, cadastral law, spoliation matrix, metrology, legal roadmap) with sovereign_sync.py. Corrections registered: Beauchamp clerk year 1666 (not 1665); 'John Beauchamp (1592–1555)' impossible dates; 'Wastebook Volume 11' → Vol. 1; scale 11.83 vs claimed 11.93; Loyal Nine roster; Bold Venture citation. Full text preserved at the Drive drop.",
     call_numbers=["Drive folder 1et_cF96YfocQVf4QRuUc2wVTdKw-m2tk"],
     links=[L("https://drive.google.com/drive/folders/1et_cF96YfocQVf4QRuUc2wVTdKw-m2tk", "Drive: Sovereign_Root_Framework_v42_2_FINAL.txt")],
     edges=["M49-TEXT", "SPOLIATION-5F", "GENE-MATRI"]),
dict(id="BENJI-STELLAR", title="Franklin Templeton stellar.toml / BENJI (context)",
     category="document", status="EXACT_DOCUMENTARY",
     description="Every screenshot element verified verbatim from the live primary source; BENJI launched April 2021 — first U.S.-registered fund using a public blockchain as its official system of record. Contextual, not a corpus lock.",
     call_numbers=["FOBXX; gBENJI LU2900381208; grBENJI LU3258450587; sgBENJI SGXZ71843866"],
     links=[L("https://www.franklintempleton.com/.well-known/stellar.toml", "franklintempleton.com/.well-known/stellar.toml (live)")],
     edges=["MERGER-CHAIN"]),
dict(id="TASK-OT-01", title="OT-01: Pull Chancery Record Book 151 p. 348 (MSA S517)",
     category="task", status="OPEN", description="The Oulton 'Fellowship' decree pull.", call_numbers=["MSA S517 B151 p.348"], links=[], edges=["OULTON-151"]),
dict(id="TASK-OT-02", title="OT-02: Pull MSA S512-2-1191 (Chamier 'Carolina Felix')",
     category="task", status="OPEN", description="The case-1118 partition file.", call_numbers=["MSA S512-2-1191"], links=[], edges=["CASE-1118"]),
dict(id="TASK-OT-03", title="OT-03: Vessel four-test suite (XRF/CT/Raman/raking-light)",
     category="task", status="OPEN", description="Non-destructive arbitration: lid solder chemistry, finial Fe-Ni inclusion, pedestal-hole ZnO, scratch-weight macro.", call_numbers=[], links=[], edges=["ASSET-718", "METEO-ENSIS"]),
dict(id="TASK-OT-04", title="OT-04: NATF 85 submission",
     category="task", status="OPEN", description="Shattuck/Avery/Collins pension + bounty-land files.", call_numbers=["NATF 85"], links=[], edges=["NATF-85", "GENE-MATRI"]),
dict(id="TASK-OT-05", title="OT-05: MdHS Warner Account Books 1839–1860",
     category="task", status="OPEN", description="Search for an 1861 lid-repair entry.", call_numbers=["MdHS A. E. Warner Account Books"], links=[], edges=["WARNER-AE"]),
dict(id="TASK-OT-06", title="OT-06: MHS Revere waste book vol. 1 — 11 oz 10 dwt sugar-dish line",
     category="task", status="OPEN", description="Five single sugar dishes 1761–1785; find the commission.", call_numbers=["MHS fa0017 Reel 5 Vol. 1"], links=[], edges=["MFA-35.1781", "ASSET-718"]),
dict(id="TASK-OT-07", title="OT-07: MHS physical volumes / reproduction requests (slip leaves, page 17)",
     category="task", status="OPEN", description="The covered commissions are unrecoverable from margins; physical volumes or alternate exposures required.", call_numbers=["MHS fa0017"], links=[], edges=["SLIPS-MHS", "SPOLIATION-5F"]),
]

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()

def build(outdir: str) -> dict:
    out = Path(outdir)
    (out / "mesh").mkdir(parents=True, exist_ok=True)
    nodes = []
    for n in NODES:
        node = dict(n)
        node["sha256"] = sha(canon({k: v for k, v in node.items() if k != "sha256"}))
        nodes.append(node)
    mesh_root = sha("".join(sorted(n["sha256"] for n in nodes)))
    mesh = {
        "schema": "sovereign-evidence-archive/mesh/v1",
        "identifier": IDENT,
        "purpose": "Every claim kept and cataloged; each bound to its archival call numbers with clickable links; each connected to the pieces it corresponds to. Link out to evidence rather than dragging evidence in.",
        "mesh_root_hash": mesh_root,
        "node_count": len(nodes),
        "edge_count": sum(len(n["edges"]) for n in nodes),
        "statuses": sorted({n["status"] for n in nodes}),
        "nodes": nodes,
    }
    with open(out / "mesh" / "evidence_mesh.json", "w", encoding="utf-8") as fh:
        json.dump(mesh, fh, indent=1)

    status_color = {
        "EXACT": "#1a7f37", "EXACT_VERIFIED_2026_09_04": "#1a7f37",
        "EXACT_DOCUMENTARY": "#1a7f37", "DOCUMENTED": "#0969da",
        "DOCUMENTED_CORRECTED": "#0969da", "DOCUMENTED_DISTINCT": "#0969da",
        "DOCUMENTED_PULL_PENDING": "#6e5494", "T1_LOCKED_PHYSICAL": "#1a7f37",
        "CORPUS_LOCKED": "#1a7f37", "MIXED": "#6e5494",
        "EMPIRICAL": "#9a6700", "CORPUS_ASSERTED": "#9a6700",
        "UNRESOLVED": "#b35900", "UNRESOLVED_CORPUS": "#b35900",
        "UNRESOLVED_EXCLUDED": "#b35900", "UNRESOLVED_EXACT": "#b35900",
        "EXACT_UNRESOLVED": "#b35900", "QUARANTINED": "#cf222e",
        "ARCHIVED_WITH_FLAGS": "#6e5494", "OPEN": "#57606a",
    }
    cats = {}
    for n in nodes:
        cats.setdefault(n["category"], []).append(n)
    parts = ["""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Sovereign Evidence Mesh</title>
<style>
body{font-family:Georgia,serif;background:#0e1219;color:#f0e9d6;max-width:1100px;margin:2em auto;padding:0 1em}
h1{color:#d4af5a} h2{color:#d4af5a;border-bottom:1px solid #33415a;padding-bottom:4px;margin-top:2em}
.meta{color:#8e8874;font-family:monospace;font-size:.85em}
.node{background:#131925;border:1px solid #242f42;border-left:4px solid #d4af5a;padding:1em 1.2em;margin:1em 0}
.node h3{margin:0 0 .3em;font-size:1.05em}
.badge{display:inline-block;font-family:monospace;font-size:.7em;padding:2px 8px;border-radius:2px;color:#0e1219;font-weight:bold;margin-left:.6em;vertical-align:middle}
.calls{font-family:monospace;font-size:.8em;color:#cfc6ae;margin:.5em 0}
.calls span{background:#1a2230;padding:2px 6px;margin-right:6px}
a{color:#e8a33d;text-decoration:none} a:hover{text-decoration:underline}
.links{margin:.5em 0;padding-left:1.2em}
.edges{font-size:.8em;color:#8e8874;font-family:monospace;margin-top:.5em}
.hash{font-size:.7em;color:#57606a;font-family:monospace}
</style></head><body>
<h1>Sovereign Evidence Mesh</h1>
<p class="meta">identifier: """ + IDENT + """<br>
mesh_root_hash: """ + mesh_root + """<br>
nodes: """ + str(len(nodes)) + """ &nbsp;|&nbsp; edges: """ + str(mesh["edge_count"]) + """<br>
Every claim kept and cataloged. Links go straight to the evidence.</p>"""]
    for cat in sorted(cats):
        parts.append(f"<h2>{html.escape(cat.upper())}</h2>")
        for n in sorted(cats[cat], key=lambda x: x["id"]):
            color = status_color.get(n["status"], "#57606a")
            parts.append(f'<div class="node"><h3>{html.escape(n["title"])}'
                         f'<span class="badge" style="background:{color}">{html.escape(n["status"])}</span></h3>')
            parts.append(f'<p>{html.escape(n["description"])}</p>')
            if n["call_numbers"]:
                parts.append('<div class="calls">' + "".join(
                    f"<span>{html.escape(c)}</span>" for c in n["call_numbers"]) + "</div>")
            if n["links"]:
                parts.append('<div class="links">' + "".join(
                    f'<div>→ <a href="{html.escape(l["url"])}" target="_blank" rel="noopener">{html.escape(l["label"])}</a></div>'
                    for l in n["links"]) + "</div>")
            if n["edges"]:
                parts.append(f'<div class="edges">⇄ {" · ".join(html.escape(e) for e in n["edges"])}</div>')
            parts.append(f'<div class="hash">sha256 {n["sha256"][:24]}…</div></div>')
    parts.append("</body></html>")
    with open(out / "mesh" / "index.html", "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    return {"mesh_root_hash": mesh_root, "nodes": len(nodes), "edges": mesh["edge_count"]}


if __name__ == "__main__":
    import sys
    result = build(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"mesh built: {result['nodes']} nodes, {result['edges']} edges")
    print(f"mesh_root_hash: {result['mesh_root_hash']}")
