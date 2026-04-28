# Phase B — Mini Scoping Run Results

> **Run date**: 2026-04-28  
> **API**: OpenAlex (free tier, polite pool)  
> **Purpose**: Validate corpus density target (40–80 papers) and identify nearest existing SLRs

---

## 1. Hit Count Summary

| Variant | Query Label | All (2010–2026) | Articles | Reviews / SLRs | Recent (2018+) |
|---|---|---|---|---|---|
| `S1` | Core ML + Public Finance Fraud | 5,917 | 4,370 | 308 | 4,270 |
| `S2` | Corruption Detection + IS | 8,991 | 5,853 | 190 | 4,667 |
| `S3` | Village Fund / Dana Desa | 60 | 57 | 0 | 57 |
| `S4` | Feature Engineering + Corruption Typology | 515 | 249 | 11 | 194 |
| `S5` | Decentralized Fund Audit Analytics | 897 | 642 | 68 | 639 |
| `S6` | Procurement Fraud ML | 4,655 | 3,310 | 167 | 3,177 |
| `S7` | SLR Existing Reviews (novelty check) | 11,060 | 7,763 | 646 | 7,482 |

## 2. Corpus Density Assessment

- **Largest raw pool (articles)**: 5,853 from S1/S5 combined domain
- **Conservative filter pass rate**: ~8–25% (IC/EC + quality threshold)
- **Estimated included corpus**: 468–1463 papers
- **Verdict**: ⚠️ **Corpus may be too large.** Narrow search or accept higher filter attrition.

## 3. Sample Titles by Variant

### S1 — Core ML + Public Finance Fraud

> *Rationale*: Primary scope: ML methods + public sector financial fraud

- [2024] **Enhancing fraud detection in accounting through AI: Techniques and case studies** — *Finance & Accounting Research Journal* (cited: 26, OA)
- [2020] **Cybersecurity data science: an overview from machine learning perspective** — *Journal Of Big Data* (cited: 705, OA)
- [2014] **Toward Scalable Systems for Big Data Analytics: A Technology Tutorial** — *IEEE Access* (cited: 1091, OA)
- [2020] **A Survey on Machine Learning Techniques for Cyber Security in the Last Decade** — *IEEE Access* (cited: 495, OA)
- [2020] **A Survey on the Internet of Things (IoT) Forensics: Challenges, Approaches, and Open Issues** — *IEEE Communications Surveys & Tutorials* (cited: 821, OA)
- [2022] **Financial Fraud Detection Based on Machine Learning: A Systematic Literature Review** — *Applied Sciences* (cited: 338, OA)
- [2020] **Data governance: Organizing data for trustworthy Artificial Intelligence** — *Government Information Quarterly* (cited: 622, OA)
- [2022] **Is artificial intelligence improving the audit process?** — *Review of Accounting Studies* (cited: 351, OA)

### S2 — Corruption Detection + IS

> *Rationale*: IS framing + corruption: direct RQ1 alignment

- [2013] **Global health 2035: a world converging within a generation** — *The Lancet* (cited: 1213, OA)
- [2020] **A country level analysis measuring the impact of government actions, country preparedness and socioeconomic factors on COVID-19 mortality and related health outcomes** — *EClinicalMedicine* (cited: 460, OA)
- [2012] **Understanding China's Growth: Past, Present, and Future** — *The Journal of Economic Perspectives* (cited: 583, OA)
- [2012] **Government auditing and corruption control: Evidence from China’s provincial panel data** — *China Journal of Accounting Research* (cited: 163, OA)
- [2023] **Examining the interconnectedness of green finance: an analysis of dynamic spillover effects among green bonds, renewable energy, and carbon markets** — *Environmental Science and Pollution Research* (cited: 320, OA)
- [2017] **Shadow Economy: Estimation Methods, Problems, Results and Open questions** — *Open Economics* (cited: 193, OA)
- [2018] **Leveraging Blockchain Technology to Enhance Supply Chain Management in Healthcare:** — *Blockchain in Healthcare Today* (cited: 233, OA)
- [2014] **Big Data: Survey, Technologies, Opportunities, and Challenges** — *The Scientific World JOURNAL* (cited: 535, OA)

### S3 — Village Fund / Dana Desa

> *Rationale*: Specific context — RQ3 applicability boundary

- [2021] **Organizational culture as moderating the influence of internal control and community participation on fraud prevention in village fund management during the COVID-19 pandemic** — *Linguistics and Culture Review* (cited: 18, OA)
- [2021] **An analysis on fraud tendency of village government officials** — *Jurnal Akuntansi & Auditing Indonesia* (cited: 6, OA)
- [2022] **Fraud Prevention of Village Fund Management** — *International Journal of Islamic Business and Management Review* (cited: 6, OA)
- [2022] **Fraud Prevention Efforts In Managing Village Funds In Accordance With Aspects of Human Resource Management with Transparency Principles** — *International Journal of Economics Business and Entrepreneurship* (cited: 4, OA)
- [2024] **Development of integrated village fund governance model with siberas public service application** — *Edelweiss Applied Science and Technology* (cited: 4, OA)
- [2023] **Supervision of Village Financial Management: will it be in Parallel with the Development of Village Officials? (a Study of North Sumatra Province)** — *Journal of Law and Sustainable Development* (cited: 4, OA)
- [2020] **Prevention and Detection of Fraud in Village Fund Supervision in Barito Kuala District** — *Assets Jurnal Akuntansi dan Pendidikan* (cited: 3, OA)
- [2023] **Recognising and detecting patterns of village corruption in Indonesia** — *Integritas Jurnal Antikorupsi* (cited: 3, OA)

### S4 — Feature Engineering + Corruption Typology

> *Rationale*: RQ2 operationalization gap — typology to signal

- [2019] **Artificial Intelligence (AI): Multidisciplinary perspectives on emerging challenges, opportunities, and agenda for research, practice and policy** — *International Journal of Information Management* (cited: 3885, OA)
- [2015] **Audit Culture Revisited** — *Current Anthropology* (cited: 456, OA)
- [2016] **Organised Cybercrime or Cybercrime that is Organised? An Assessment of the Conceptualisation of Financial Cybercrime as Organised Crime** — *European Journal on Criminal Policy and Research* (cited: 105, OA)
- [2023] **The landscape of public procurement research: a bibliometric analysis and topic modelling based on Scopus** — *Journal of Public Procurement* (cited: 91, OA)
- [2021] **Countering money laundering and terrorist financing: A case for bitcoin regulation** — *Research in International Business and Finance* (cited: 91, paywalled)
- [2021] **Exploring the application of blockchain to humanitarian supply chains: insights from Humanitarian Supply Blockchain pilot project** — *International Journal of Operations & Production Management* (cited: 108, OA)
- [2016] **Organizing the finances for and the finances from transnational corporate bribery** — *European Journal of Criminology* (cited: 40, OA)
- [2024] **Cybercriminal Networks and Operational Dynamics of Business Email Compromise (BEC) Scammers: Insights from the “Black Axe” Confraternity** — *Deviant Behavior* (cited: 43, OA)

### S5 — Decentralized Fund Audit Analytics

> *Rationale*: Broadened S1: includes audit analytics + decentralized governance

- [2021] **IoT for Smart Cities: Machine Learning Approaches in Smart Healthcare—A Review** — *Future Internet* (cited: 655, OA)
- [2017] **Converging blockchain and next-generation artificial intelligence technologies to decentralize and accelerate biomedical research and healthcare** — *Oncotarget* (cited: 468, OA)
- [2018] **Chained Anomaly Detection Models for Federated Learning: An Intrusion Detection Case Study** — *Applied Sciences* (cited: 315, OA)
- [2023] **Re-Thinking Data Strategy and Integration for Artificial Intelligence: Concepts, Opportunities, and Challenges** — *Applied Sciences* (cited: 568, OA)
- [2022] **AI-big data analytics for building automation and management systems: a survey, actual challenges and future perspectives** — *Artificial Intelligence Review* (cited: 463, OA)
- [2018] **From Intrusion Detection to Attacker Attribution: A Comprehensive Survey of Unsupervised Methods** — *IEEE Communications Surveys & Tutorials* (cited: 208, OA)
- [2023] **A Survey of Explainable Artificial Intelligence for Smart Cities** — *Electronics* (cited: 176, OA)
- [2020] **Big Data for Energy Management and Energy-Efficient Buildings** — *Energies* (cited: 157, OA)

### S6 — Procurement Fraud ML

> *Rationale*: Procurement sub-domain — often overlaps Dana Desa irregularities

- [2022] **Data Quality Barriers for Transparency in Public Procurement** — *Information* (cited: 26, OA)
- [2024] **Enhancing fraud detection in accounting through AI: Techniques and case studies** — *Finance & Accounting Research Journal* (cited: 26, OA)
- [2023] **Algorithmic Integrity: A Predictive Framework for Combating Corruption in Public Procurement through AI and Data Analytics** — *Journal of Frontiers in Multidisciplinary Research* (cited: 17, OA)
- [2024] **Digital Procurement 4.0: Redesigning Government Contracting Systems with AI-Driven Ethics, Compliance, and Performance Optimization** — *International Journal of Scientific Research in Computer Science Engineering and Information Technology* (cited: 16, OA)
- [2014] **Big Data: New Tricks for Econometrics** — *The Journal of Economic Perspectives* (cited: 1515, OA)
- [2024] **Performance Variability of Machine Learning Models using Limited Data for Collusion Detection: A Case Study of the Brazilian Car Wash Operation** — *—* (cited: 2, OA)
- [2019] **Blockchain technology: implications for operations and supply chain management** — *Supply Chain Management An International Journal* (cited: 922, OA)
- [2020] **The Impact of Artificial Intelligence and Blockchain on the Accounting Profession** — *IEEE Access* (cited: 325, OA)

## 4. Nearest Existing SLRs — Novelty Gap Analysis

> These are candidate SLRs retrieved from OpenAlex type:review. Review each title to confirm it is a genuine SLR and assess the gap this study fills.

| Year | Title | Journal | Citations | OA | Potential Gap |
|---|---|---|---|---|---|
| 2023 | Interpreting Black-Box Models: A Review on Explainable Artificial Intelligence | Cognitive Computation | 1560 | OA | Broader domain; this SLR adds village-level IS framing |
| 2021 | Artificial Intelligence and Business Value: a Literature Review | Information Systems Frontiers | 843 | OA | Broader domain; this SLR adds village-level IS framing |
| 2021 | Data Science and Analytics: An Overview from Data-Driven Smart Computing, Decision-Making  | SN Computer Science | 504 | OA | Broader domain; this SLR adds village-level IS framing |
| 2023 | Exploring the Full Potentials of IoT for Better Financial Growth and Stability: A Comprehe | Sensors | 493 | OA | Broader domain; this SLR adds village-level IS framing |
| 2020 | A comprehensive survey of AI-enabled phishing attacks detection techniques | Telecommunication Systems | 394 | OA | Broader domain; this SLR adds village-level IS framing |
| 2024 | A Review on Large Language Models: Architectures, Applications, Taxonomies, Open Issues an | IEEE Access | 639 | OA | Broader domain; this SLR adds village-level IS framing |
| 2022 | Cyber risk and cybersecurity: a systematic review of data availability | The Geneva Papers on Risk and Insurance  | 311 | OA | Broader domain; this SLR adds village-level IS framing |
| 2023 | Smarter eco-cities and their leading-edge artificial intelligence of things solutions for  | Environmental Science and Ecotechnology | 472 | OA | Broader domain; this SLR adds village-level IS framing |
| 2020 | Security and the smart city: A systematic review | Sustainable Cities and Society | 286 | OA | Broader domain; this SLR adds village-level IS framing |
| 2018 | A Systematic Review on Healthcare Analytics: Application and Theoretical Perspective of Da | Healthcare | 273 | OA | Broader domain; this SLR adds village-level IS framing |
| 2021 | Enabling Technologies for Urban Smart Mobility: Recent Trends, Opportunities and Challenge | Sensors | 355 | OA | Broader domain; this SLR adds village-level IS framing |
| 2020 | Mitigation of emerging implications of climate change on food production systems | Food Research International | 364 | OA | Broader domain; this SLR adds village-level IS framing |

## 5. Notes & Decisions

- Scopus, IEEE Xplore, and WoS searches must be run manually with institutional access.
  Use string variants S1–S6 from `search_strings.md` with database-specific field tags.
- OpenAlex hit counts are indicative; actual includable papers depend on IC/EC filter outcomes.
- Combine S1 + S2 + S4 + S6 as the primary search string set for Scopus.
- S3 (Dana Desa) expected sparse — treat results as specialty supplementary corpus.
- **Recommendation**: Proceed to Phase C. Target combined retrieval of 150–400 raw records across all databases.
