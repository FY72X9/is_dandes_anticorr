# Full Spoken Presentation Script (ICDEES 2026) — Calm Pace Edition

**Slide Deck:** `1571349783_ICDEES2026_Presentation.pdf` (12 Slides)  
**Total Word Count:** ~630 words (Designed specifically for a relaxed **80–90 words per minute** speaking pace)  
**Total Target Time:** Exactly 7:30 – 8:00 (Includes comfortable 1–2 second breathing pauses on every slide)  
**Presenter:** Farrell Yodihartomo  
**Style:** Academic Conference Presentation (Formal, Empirical, Objective; **Not a Pitch**)  
**Language Level:** Plain, Fluent, and Accessible English (IELTS Band 4–5 syntax, simple words, short sentences)  

---

### [0:00 – 0:35] Slide 1: Title & Author Block
*(~45 words | ~35 seconds)*

`[SLIDE 1 ON SCREEN]`

"Good morning, session chairs and fellow colleagues. 

My name is **Farrell Yodihartomo**, from Bina Nusantara University, Indonesia. 

On behalf of our research team from BINUS and the Corruption Eradication Commission, **KPK**, I present our study: 

*'Unsupervised Dual-Path Consensus Machine Learning for Village Fund Expenditure Anomaly Detection.'* `[PAUSE]`

Thank you for having me."

`[NEXT SLIDE]`

---

### [0:35 – 1:15] Slide 2: 01 / Problem Background — Rural Oversight Deficit
*(~60 words | ~40 seconds)*

`[SLIDE 2 ON SCREEN]`

"Under fiscal decentralization, Indonesia sends **71 trillion Rupiah** every year to over **75,000 villages**. 

However, local inspectorates only have **5 to 15 auditors** to oversee up to **250 villages**. 

Furthermore, **98.8 percent** of village projects use self-managed spending without competitive bidding. `[PAUSE]`

Because oversight is manual, corruption cases are usually discovered **two to five years late**, after funds are already lost."

`[NEXT SLIDE]`

---

### [1:15 – 1:55] Slide 3: 02 / Literature Gaps (2022–2026)
*(~55 words | ~40 seconds)*

`[SLIDE 3 ON SCREEN]`

"We identified **three core research gaps** in the recent literature. `[PAUSE]`

First, **subspace cancellation**: standard majority voting erases local density outliers. 

Second, **missing policy mapping**: outlier scores are not connected to statutory audit rules. 

Third, **geographic cost distortion**: remote mountain logistics naturally inflate unit costs, misleading standard models. 

Our research was designed to solve all three issues."

`[NEXT SLIDE]`

---

### [1:55 – 2:35] Slide 4: 03 / Design Science Research (DSR) Pipeline
*(~55 words | ~40 seconds)*

`[SLIDE 4 ON SCREEN]`

"Following the **Design Science Research** framework, we built a four-stage pipeline. `[PAUSE]`

First, we cleaned **96,778 real transactions** across 1,363 villages in Jambi Province. 

Second, we engineered **27 features** centered by regional baseline z-scores. 

Third, we run three orthogonal anomaly engines in parallel. 

Finally, we convert neural reconstruction errors into actionable field inspection checklists."

`[NEXT SLIDE]`

---

### [2:35 – 3:15] Slide 5: 04 / Algorithm & Feature Design (RQ1)
*(~60 words | ~40 seconds)*

`[SLIDE 5 ON SCREEN]`

"To answer **Research Question 1**, we formulate three distinct engines: `[PAUSE]`

**Isolation Forest** isolates global spending sparsity using 200 trees. 

**Local Outlier Factor** measures density compared to twenty neighboring villages in a sub-district. 

And an **8-layer Reconstruction Autoencoder** compresses the 27 features down to an 8-dimension bottleneck. 

Each engine evaluates transactions from a completely different statistical perspective."

`[NEXT SLIDE]`

---

### [3:15 – 4:00] Slide 6: 05 / Ensemble Innovation (RQ2) — Dual-Path Consensus
*(~65 words | ~45 seconds)*

`[SLIDE 6 ON SCREEN]`

"For **Research Question 2**, we compare ensemble architectures. 

Standard majority voting fails because model agreement is near zero—Cohen's Kappa is only **0.041**. 

As a result, majority voting cancels out **3,940 high-risk local outliers**. `[PAUSE]`

Therefore, we designed **Dual-Path Consensus**. 

Path 1 preserves local LOF density outliers directly. 

Path 2 requires joint agreement between Isolation Forest and the Autoencoder. 

This completely eliminates mutual cancellation."

`[NEXT SLIDE]`

---

### [4:00 – 4:45] Slide 7: 06 / Experimental Evaluation (RQ2) — Ablation Study
*(~65 words | ~45 seconds)*

`[SLIDE 7 ON SCREEN]`

"Slide 7 presents our **ablation study results**. `[PAUSE]`

On our benchmark of 10,000 transactions with 500 injected frauds: 

Standard majority voting achieved an F1-score of only **56.8%**. It missed nearly half the fraud! 

In contrast, our **Dual-Path Protocol 2** achieved an F1-score of **84.6%** and an AUC of **0.912**. 

In real Jambi data, it identified **7,153 anomalies**, uncovering **642 billion Rupiah** in realization risk."

`[NEXT SLIDE]`

---

### [4:45 – 5:25] Slide 8: 07 / Operational Policy Mapping (RQ3) — Typology Shift
*(~60 words | ~40 seconds)*

`[SLIDE 8 ON SCREEN]`

"Answering **Research Question 3**, our policy layer maps anomalies into corruption typologies. `[PAUSE]`

Compared to majority voting: 

**Ghost Activities** increased by **436 percent**, capturing over 4,100 uncompleted projects. 

**Procurement Irregularities** under uncompetitive spending increased to over 2,300 records. 

By protecting local density signals, Dual-Path reveals hidden non-linear spending tricks that standard voting misses entirely."

`[NEXT SLIDE]`

---

### [5:25 – 6:05] Slide 9: 08 / XAI Error Drivers & Village Persistence
*(~55 words | ~40 seconds)*

`[SLIDE 9 ON SCREEN]`

"Slide 9 displays our **Explainable AI feature attribution**. `[PAUSE]`

Category cost deviation and unit price inflation explain **75 percent** of the neural reconstruction error. 

Longitudinally, **702 villages** showed persistent anomalies across all three fiscal years. 

Geographically, **Batanghari Regency** showed the highest risk density, with nearly 16 percent of transactions flagged, representing **115 billion Rupiah** at risk."

`[NEXT SLIDE]`

---

### [6:05 – 6:40] Slide 10: 09 / Information Systems Success Impact
*(~50 words | ~35 seconds)*

`[SLIDE 10 ON SCREEN]`

"Under the **DeLone and McLean IS Success Model**, our system provides significant operational impact. `[PAUSE]`

It reduces the inspectorate audit search space by **92.6 percent**. 

Instead of checking nearly 100,000 records manually, the small audit team focuses on 7,153 high-risk records. 

The system automatically generates a **field inspection checklist** to guide on-site verifications."

`[NEXT SLIDE]`

---

### [6:40 – 7:20] Slide 11: 10 / Legal Governance & Limitations
*(~55 words | ~40 seconds)*

`[SLIDE 11 ON SCREEN]`

"We also address critical **legal boundaries** under Indonesian public audit law. `[PAUSE]`

Under **KUHAP Article 184**, algorithmic flags are **not** legal proof. They serve as an **Initial Investigative Lead** (*Indikasi Awal*). 

Human auditors must still verify criminal intent and actual state financial loss. 

Also, as a boundary condition, administrative ledgers cannot capture unrecorded, off-books cash kickbacks."

`[NEXT SLIDE]`

---

### [7:20 – 8:00] Slide 12: Conclusion & Key Findings
*(~50 words | ~40 seconds)*

`[SLIDE 12 ON SCREEN]`

"In conclusion, our research delivers three key contributions: `[PAUSE]`

First, **Dual-Path Consensus** overcomes mutual cancellation, reaching an **84.6% F1-score**. 

Second, it isolates **642 billion Rupiah** in real financial risk. 

Third, it reduces inspectorate search effort by **92.6 percent**. 

Thank you very much. I am happy to take your questions."

`[END OF PRESENTATION]`
