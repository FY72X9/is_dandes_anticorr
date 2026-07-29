# Chapter 2: Related Work

> **Draft Status**: July 2026 (Aligned with IEEE references [1]–[32])  
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Target**: ~850 words  
> **Citation Format**: IEEE (continuous numbering per references.md)  

---

## 2. Related Work

### 2.1 Corruption Typology Frameworks

Understanding the target of unsupervised detection requires a precise, domain-grounded taxonomy of corruption forms. Bussell [1-book] proposes a pragmatic two-dimensional typology distinguishing corruption by access type (monetary vs. preferential) and governance level (bureaucratic vs. political), establishing the foundational analytical axes. Graycar's TASP framework—Types, Activities, Sectors, Places—extends this by asserting that anti-corruption mechanisms must specify not merely what form of corruption occurs, but within which specific public programme activity and geographic locus it manifests [7].

For Indonesia's *Dana Desa* context, Siregar and Aminudin [13] provide the primary empirical classification: a multi-case study of East Java village fund fraud identifying five recurring modus operandi—unit price mark-up of goods and services, fictitious budget items (*proyek fiktif*), double budgeting, procurement manipulation, and misuse of personnel honoraria. Kartadinata et al. [14] extend this taxonomy through systematic analysis of over 200 KPK prosecution cases (2015–2020), confirming mark-up (*penggelembungan*) and fictitious projects as the dominant physical corruption moduses. Recent empirical work by Medan et al. [15] in East Nusa Tenggara documents that these exact modus operandi patterns persist into contemporary fiscal periods, validating the requirement for typology-grounded detection rules in automated screening artifacts.

### 2.2 Fraud Diamond and Principal-Agent Foundations

The Fraud Triangle (Cressey, 1953) [17], operationalised in rural governance by Hidajat [6], models fraud via three conditions: Pressure (rigid statutory disbursement timetables), Opportunity (structural absence of competitive bidding and auditor reach), and Rationalisation (normative acceptance of budget diversion). Wolfe and Hermanson's Fraud Diamond extends this model by incorporating **Capability**—the individual authority, digital access, and technical competence required to execute and conceal financial manipulation [17b]. In Siskeudes execution, Capability resides in the Village Head (*Kepala Desa*) and Financial Officer (*Kaur Keuangan*), who maintain exclusive digital authorization credentials and bank withdrawal signatures.

Opportunity is structurally driven by procurement method selection. Dataset audit reveals that **98.8% of all village fund activities** in Jambi Province are executed through self-managed procurement (*Swakelola*), completely bypassing open competitive bidding. This empirical dominance confirms Søreide's [9] procurement corruption theory: the structural absence of market competition removes natural price-discovery mechanisms, enabling local officials to select favored vendors or inflate invoices without external challenge.

Principal-Agent Theory [25], applied to local governance by Groenendijk and Sutarna & Subandi, frames the village head as an Agent possessing severe information asymmetry relative to the Principal (district APIP inspectorate, BPKP, KPK). The Agent operates on-site with private knowledge of true material purchasing costs and physical progress, while the Principal observes only computerised financial entries in Siskeudes. Unexplained statistical deviations in unit costs, tranche disbursement progress ratios, and procurement categories constitute proximate empirical traces of moral hazard and information asymmetry exploitation [25, 9].

### 2.3 Anomaly Detection Paradigms in Public Financial Data

The anomaly detection literature applied to public financial management has converged on three methodologically distinct paradigms as complementary rather than substitutable:
1. **Global Sparsity Partitioning**: Isolation Forest (Liu et al. [18, 19]) measures random partitioning path length in tree ensembles, performing optimally against globally extreme multi-feature outliers.
2. **Local Density Ratio Estimation**: Local Outlier Factor (LOF, Breunig et al. [24]) evaluates local reachability density ratios relative to $k$-nearest neighbors. LOF isolates records that are locally sparse relative to their specific activity peer group (e.g., within a specific output code `Kode_Output`), capturing within-group price inflation that global partitioning methods structurally miss [24].
3. **Neural Reconstruction Error**: Deep Autoencoders (Zhou & Paffenroth [32]) learn compressed latent representations of normal financial behaviour. Records exhibiting anomalously high Mean Squared Error (MSE) at reconstruction signal non-linear feature interaction distortions.

Chandola et al. [23] confirm in their survey that multi-paradigm ensembles consistently achieve superior detection coverage compared to any single algorithm, because each paradigm isolates a fundamentally distinct statistical signature of anomalous behaviour. Prior studies on Indonesian public financial data have not yet combined local density isolation and deep neural reconstruction into a unified Dual-Path framework applied to longitudinal activity-level expenditure records [12, 16].

### 2.4 Information Systems Success Grounding

The DeLone and McLean IS Success Model [10]—in its updated formulation incorporating Service Quality alongside Information Quality and System Quality—provides the theoretical justification for deploying an automated anomaly detection artifact as an institutional intervention. In this framework, the artifact's processed outputs (dual-path consensus flags, typology mappings, village priority tiers) represent the **Information Quality** dimension. High Information Quality directly drives **Individual Impact** (reducing auditor search space and providing XAI audit checklists) and **Organizational Impact** (enabling targeted APIP inspection and state financial loss recovery).

Mutungi et al. [5] further demonstrate that digital anti-corruption tools fail in practice when their algorithmic design does not map directly to specific administrative interaction points. This insight validates the present study's feature-engineering protocol, which maps each detector construct to documented corruption modus operandi under the Design Science Research (DSR) framework (Hevner et al. [10]).
