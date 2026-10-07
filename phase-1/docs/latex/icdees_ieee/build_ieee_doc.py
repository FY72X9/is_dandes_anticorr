"""
Build IEEE Conference Paper in Word format (.docx and .doc)
matching conference-template-a44.docx exactly from icdees_v6_humanized.tex
and references_v03.bib with:
1. No duplicate numberings in headers, subheaders, and captions (leveraging template automatic numbering)
2. Native MS Word equations (<m:oMath>) for all LaTeX formulas
3. Non-bold headers (Heading 1, Heading 2, Heading 3, Heading 5) matching template
4. Header font size 10pt; table content and references font size 8pt
"""

import os
import re
import copy
import subprocess
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def extract_omaths():
    equations = [
        r"\mathrm{InfoAsymmetry} = \mathcal{I}_{\mathrm{Agent}}(\mathrm{Realization}, \mathrm{TrueCost}) - \mathcal{I}_{\mathrm{Principal}}(\mathrm{SiskeudesReport})",
        r"z_{i,c,k,t} = \frac{x_{i,c,k,t} - \mu_{c,k,t}}{\sigma_{c,k,t} + \epsilon}",
        r"y_{i, \mathrm{IF}} = \mathbf{1}\left(s(x_i, n) \ge \mathrm{Quantile}_{0.90}(s)\right)",
        r"\mathrm{LOF}_k(p) = \frac{1}{|N_k(p)|} \sum_{o \in N_k(p)} \frac{\mathrm{lrd}_k(o)}{\mathrm{lrd}_k(p)}",
        r"y_{i, \mathrm{LOF}} = \mathbf{1}\left(\mathrm{LOF}_k(x_i) \ge \mathrm{Quantile}_{0.95}(\mathrm{LOF})\right)",
        r"E_i = \sum_{f=1}^{d} (x_{i,f} - \hat{x}_{i,f})^2, \quad e_{i,f} = \frac{(x_{i,f} - \hat{x}_{i,f})^2}{E_i}",
        r"y_{i, \mathrm{RDA}} = \mathbf{1}\left(E_i \ge \mathrm{Quantile}_{0.95}(E)\right)",
        r"y_{i, \mathrm{consensus}} = y_{i, \mathrm{LOF}} \lor \left(y_{i, \mathrm{IF}} \land y_{i, \mathrm{RDA}}\right)"
    ]
    tex_snippets = []
    for i, eq in enumerate(equations, 1):
        tex_snippets.append(f"% EQ {i}\n$${eq}$$\n")

    os.makedirs("scratch", exist_ok=True)
    temp_tex = "scratch/temp_all_eqs.tex"
    temp_docx = "scratch/temp_all_eqs.docx"
    with open(temp_tex, "w", encoding="utf-8") as f:
        f.write("\n".join(tex_snippets))

    subprocess.run(["pandoc", temp_tex, "-o", temp_docx], check=True)
    eq_doc = docx.Document(temp_docx)
    omaths = eq_doc._body._element.xpath(".//m:oMath")
    print(f"Extracted {len(omaths)} native MS Word oMath elements.")
    return omaths

def set_cell_margins(cell, top=30, bottom=30, left=40, right=40):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_booktabs_borders(table, num_header_rows=1):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
            f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
            f'<w:insideH w:val="none"/>'
            f'<w:insideV w:val="none"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)
    
    for r_idx in range(num_header_rows):
        for cell in table.rows[r_idx].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)

def add_paragraph_runs(doc, runs, style="Body Text", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=Pt(0), space_after=Pt(1.0), line_spacing=0.96):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    p.paragraph_format.space_before = space_before
    p.paragraph_format.space_after = space_after
    p.paragraph_format.line_spacing = line_spacing
    
    for r in runs:
        if isinstance(r, str):
            p.add_run(r)
        else:
            txt, b, it = r[0], r[1] if len(r) > 1 else False, r[2] if len(r) > 2 else False
            run = p.add_run(txt)
            if b: run.bold = True
            if it: run.italic = True
    return p

def add_heading_1(doc, text):
    """
    Heading 1 in template: automatic Roman numbering (I. ), Small Caps, 10pt, NOT BOLD.
    Text passed should NOT include 'I. ', 'II. ', etc.
    """
    p = doc.add_paragraph(style="Heading 1")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4.5)
    p.paragraph_format.space_after = Pt(1.5)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.0)
    run.bold = False
    return p

def add_heading_2(doc, text):
    """
    Heading 2 in template: automatic Letter numbering (A. ), Italic, 10pt, NOT BOLD.
    Text passed should NOT include 'A. ', 'B. ', etc.
    """
    p = doc.add_paragraph(style="Heading 2")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3.5)
    p.paragraph_format.space_after = Pt(1.0)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.0)
    run.bold = False
    run.italic = True
    return p

def add_heading_3(doc, text):
    """
    Heading 3 in template: automatic numbering (1) ), Italic, 10pt, NOT BOLD.
    Text passed should NOT include '1) ', '2) ', etc.
    """
    p = doc.add_paragraph(style="Heading 3")
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2.5)
    p.paragraph_format.space_after = Pt(1.0)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.0)
    run.bold = False
    run.italic = True
    return p

def add_heading_5(doc, text):
    """
    Heading 5 in template for Acknowledgment and References:
    NO automatic numbering, Small Caps, Centered, 10pt, NOT BOLD.
    """
    p = doc.add_paragraph(style="Heading 5")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4.5)
    p.paragraph_format.space_after = Pt(1.5)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.0)
    run.bold = False
    return p

def add_native_equation(doc, omath_element, eq_num_str):
    """
    Inserts a native MS Word equation (<m:oMath>) using style 'equation'.
    Uses tab stop to center the formula and right tab to align (eq_num_str).
    """
    p = doc.add_paragraph(style="equation")
    p.paragraph_format.space_before = Pt(2.0)
    p.paragraph_format.space_after = Pt(2.0)
    
    # Run with tab to center
    r_tab1 = parse_xml(f'<w:r {nsdecls("w")}><w:tab/></w:r>')
    p._element.append(r_tab1)
    
    # Append native Word oMath
    om_copy = copy.deepcopy(omath_element)
    p._element.append(om_copy)
    
    # Run with tab to right margin and equation number
    r_tab2 = parse_xml(f'<w:r {nsdecls("w")}><w:tab/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t>({eq_num_str})</w:t></w:r>')
    p._element.append(r_tab2)
    return p

def add_figure(doc, img_path, caption_str, width_in=2.85):
    """
    Inserts centered figure and caption.
    Style 'figure caption' automatically prepends 'Fig. 1. ', 'Fig. 2. ', etc.!
    Text passed should NOT include 'Fig. X. '.
    """
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(2.5)
    p_img.paragraph_format.space_after = Pt(1.0)
    run = p_img.add_run()
    run.add_picture(img_path, width=Inches(width_in))
    
    p_cap = doc.add_paragraph(style="figure caption")
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.space_before = Pt(1.0)
    p_cap.paragraph_format.space_after = Pt(2.5)
    p_cap.paragraph_format.line_spacing = 0.94
    run_cap = p_cap.add_run(caption_str)
    run_cap.font.name = "Times New Roman"
    run_cap.font.size = Pt(8.0)
    return p_img, p_cap

def add_table_head(doc, title_str):
    """
    Style 'table head' automatically prepends 'TABLE I. ', 'TABLE II. ', etc.!
    Text passed should NOT include 'TABLE X. '.
    """
    p_th = doc.add_paragraph(style="table head")
    p_th.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_th.paragraph_format.space_before = Pt(4.0)
    p_th.paragraph_format.space_after = Pt(1.5)
    run = p_th.add_run(title_str)
    run.font.name = "Times New Roman"
    run.font.size = Pt(8.0)
    return p_th

def build_manuscript():
    print("Extracting native MS Word equations (<m:oMath>)...")
    omaths = extract_omaths()

    print("Loading transitional template...")
    doc = docx.Document("templates/transitional_template.docx")
    body = doc._body._element

    # Clear all children from body except final sectPr
    for child in list(body):
        if child.tag.endswith("sectPr"):
            continue
        body.remove(child)

    # =========================================================================
    # SECTION 1: TITLE & AUTHORS (1 Column)
    # =========================================================================
    
    # Title
    p_title = doc.add_paragraph(style="paper title")
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(8)
    run_t = p_title.add_run(
        "Unsupervised Dual-Path Consensus Machine Learning and Operational Policy Framework for Village Fund Expenditure Anomaly Detection"
    )
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(24)

    # Authors Table (2x2 layout for 4 authors)
    tbl_auth = doc.add_table(rows=2, cols=2)
    tbl_auth.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_auth.autofit = False

    authors_data = [
        [
            ("Farrell Yodihartomo", "School of Information Systems", "Bina Nusantara University", "Jakarta, Indonesia 11480", "farrell.yodihartomo@binus.ac.id"),
            ("Pandu Wicaksono", "School of Computer Science", "Bina Nusantara University", "Jakarta, Indonesia 11480", "pandu.wicaksono@binus.ac.id")
        ],
        [
            ("Humam Faiq", "Directorate of Investigation", "Corruption Eradication Commission (KPK)", "Jakarta, Indonesia", "humam.faiq@kpk.go.id"),
            ("Charlie Yen", "Business Information Technology", "Bina Nusantara University", "Jakarta, Indonesia 11480", "charlie.yen@binus.ac.id")
        ]
    ]

    for r_idx in range(2):
        for c_idx in range(2):
            cell = tbl_auth.cell(r_idx, c_idx)
            cell.width = Inches(3.4)
            set_cell_margins(cell, top=40, bottom=60, left=80, right=80)
            name, aff1, aff2, loc, email = authors_data[r_idx][c_idx]
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.05
            
            r_name = p.add_run(name + "\n")
            r_name.bold = True
            r_name.font.name = "Times New Roman"
            r_name.font.size = Pt(10.5)
            
            r_aff1 = p.add_run(aff1 + "\n")
            r_aff1.italic = True
            r_aff1.font.name = "Times New Roman"
            r_aff1.font.size = Pt(9.5)
            
            r_aff2 = p.add_run(aff2 + "\n")
            r_aff2.italic = True
            r_aff2.font.name = "Times New Roman"
            r_aff2.font.size = Pt(9.5)
            
            r_loc = p.add_run(loc + "\n")
            r_loc.font.name = "Times New Roman"
            r_loc.font.size = Pt(9.5)
            
            r_email = p.add_run(email)
            r_email.font.name = "Times New Roman"
            r_email.font.size = Pt(9.5)

    # Continuous section break to 2 columns
    p_break = doc.add_paragraph()
    p_break.paragraph_format.space_before = Pt(2)
    p_break.paragraph_format.space_after = Pt(2)
    s1_xml = (
        f'<w:sectPr {nsdecls("w")}>'
        '<w:type w:val="continuous"/>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="864" w:right="864" w:bottom="950" w:left="864" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:cols w:space="720"/>'
        '</w:sectPr>'
    )
    p_break._element.get_or_add_pPr().append(parse_xml(s1_xml))

    # =========================================================================
    # SECTION 2: MAIN BODY (2 Columns)
    # =========================================================================

    # Abstract
    abs_runs = [
        ("Abstract—", True, True),
        ("In the 2024 fiscal year, the Indonesian government allocated a budget of around Rp 71 trillion annually in 75,259 villages by utilizing the Village Fund (", False, False),
        ("Dana Desa", False, True),
        ("). Monitoring process remains mainly reactive in character that is often brought up to the judicial courts 2–5 years after the disbursed. Unsupervised machine learning is unable to give precedence to expenditure data because the administrative ledgers lack any labels of the fraud. This paper adopts Design Science Research, Agency Theory, and the Fraud Diamond to develop and evaluate an unsupervised Dual-Path Consensus protocol (Protocol 2), based on Isolation Forest, Local Outlier Factor, and eight-layer Reconstruction Dense Autoencoder model, with Operational Policy Mapping Layer on 96,778 transactions (1,363 villages, Financial Year 2023-2025) of Jambi. Through dual-path consensus, Protocol 2 reduces mutual cancellation effect in the conventional majority voting protocol due to separation of the localized density outliers and global multi-model convergence and detects 7,153 expenditure anomalies (7.39%) with the financial realization risk of Rp 642.85 billion while not labeling any entity as fraud prematurely. In the ex-ante synthetic fraud benchmark (N=10,000; 5.0% fraud), Protocol 2 achieves Precision = 0.846, Recall = 0.846, F1 = 0.846, and AUC-ROC = 0.912, whereas majority voting achieves F1 = 0.568. According to DeLone and McLean IS success model, the artifact reduces the audit search area by 92.6% and turns the neural reconstruction loss into the inspection checklists.", False, False)
    ]
    add_paragraph_runs(doc, abs_runs, style="Abstract", space_before=Pt(3), space_after=Pt(3))

    # Keywords
    kw_runs = [
        ("Keywords—", True, True),
        ("Unsupervised Anomaly Detection, Dual-Path Consensus, Design Science Research, Reconstruction Autoencoder, Explainable AI, Village Fund Governance.", False, False)
    ]
    add_paragraph_runs(doc, kw_runs, style="Keywords", space_before=Pt(1.5), space_after=Pt(6))

    # -------------------------------------------------------------------------
    # SECTION I: INTRODUCTION & RELATED WORK
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Introduction")

    p1_runs = [
        ("The Indonesian government distributes roughly Rp 71 trillion annually to 75,259 rural settlements under Law No. 6/2014 concerning villages [1]. However, the volume and velocity of these fiscal transfers have outpaced the monitoring capacity of local supervisory agencies. Indonesia Corruption Watch (ICW) documented 591 court convictions regarding village fund corruption as of 2024, representing state financial losses of Rp 598.13 billion [2]. From 2015 to 2022, the Anti-Corruption Learning Center of the Corruption Eradication Commission (ACLC KPK) recorded 851 corruption cases involving 973 village apparatus members across Rp 468.9 trillion in allocated public capital [3]. National anti-corruption agencies have instituted preventive mechanisms, including KPK Trisula [4], Desa Antikorupsi [5], Siswaskeudes [6], Stranas PK 2025–2026 [7], MCP [8], and the jaga.id portal [9]. Nevertheless, these platforms operate primarily at aggregate municipal tiers or rely on passive citizen whistleblowing, lacking automated capability to analyze transaction-level financial records submitted via Siskeudes (Village Financial System) prior to fund clearance.", False, False)
    ]
    add_paragraph_runs(doc, p1_runs)

    p2_runs = [
        ("Related Work and Research Gap (2022–2026): ", True, False),
        ("Prior work in the field of public financial oversight can be broadly classified into two streams. Qualitative studies of governance cover administrative compliance [10], [11] and types of fraud [12], [13]. Hidajat [12], for example, classified village fund corruption as theft, fake reporting, and uncompetitive procurement. Further, Medan and colleagues [14] analyzed approaches to fraud detection based on customary governance. However, their research provides post-hoc analysis of fraud types and not an automatic screening tool. Concerning the field of financial machine learning, in a recent survey by Ali et al. [15] and Gao et al. [16], the dependence on supervised classifiers that rely on labels from corporately owned data was shown. This approach does not fit the context of decentralized public administration, in which actual transactions usually do not have verified labels of fraud until the judicial process takes place. Therefore, current research moved towards unsupervised anomaly detection. Reconstruction-based approaches to anomalies with the use of autoencoders were presented by Albuquerque Filho et al. [17] and Almazroi and Ayub [18], and the effectiveness of ensembles of anomaly detectors was confirmed by Fährmann et al. [19] and Han et al. [20]. However, there are three essential gaps left in the current research. First, ", False, False),
        ("Subspace Mutual Cancellation", False, True),
        (": majority voting or score averaging will decrease the effect of local density outliers (such as zero completion transactions among peers). Indeed, such transactions will look fine when global tree splits will take place. Second, ", False, False),
        ("Absence of Operational Policy Mapping", False, True),
        (": the outliers' score is not correlated with the statutory procurement policy, thus, no investigation policies are suggested [21], [22]. Third, ", False, False),
        ("Geographical Cost Distortions", False, True),
        (": the spending metric is not centered.", False, False)
    ]
    add_paragraph_runs(doc, p2_runs)

    p3_runs = [
        ("Classification of Terms in the Study: ", True, False),
        ("In order to define terms properly for both academic and legal use, this research presents four key terms: (1) ", False, False),
        ("Statistical Anomalies", False, True),
        (" – data points mathematically out of baseline distribution range; (2) ", False, False),
        ("Administrative Irregularities", False, True),
        (" are the breach of procedure including delayed milestones and redefinition of disasters' emergency status; (3) ", False, False),
        ("Financial Risk Exposure", False, True),
        (" – total monetary amount (IDR) of anomalies which need immediate supervisory audit inspection; and (4) ", False, False),
        ("Confirmed Fraud / Corruption", False, True),
        (" is the crime which is proven by law and requires verification of the unlawful act (", False, False),
        ("Perbuatan Melawan Hukum", False, True),
        ("), ", False, False),
        ("mens rea", False, True),
        (", and state financial losses (", False, False),
        ("Kerugian Negara", False, True),
        (") by Law No. 31/1999 [23]. Since there is no Siskeudes panel with ground-truth labels of fraud cases, the algorithmic flagging in this study works as a lead for investigation (", False, False),
        ("indikasi awal", False, True),
        (") but not the final verdict. Performance metrics reported (F1 and AUC-ROC) are solely derived from an ex-ante benchmarking with fraud injection experiment.", False, False)
    ]
    add_paragraph_runs(doc, p3_runs)

    p4_runs = [
        ("Contributions and Research Questions: ", True, False),
        ("This study employs the Design Science Research (DSR) [24] methodology to devise, execute, and evaluate an unsupervised Dual-Path Consensus framework (Protocol 2) utilising 96,778 transaction records (1,363 villages, FY 2023-2025) from Jambi Province. Specifically, in Jambi Province, merely 11 citizen reports concerning corruption have been detected on the KPK jaga.id platform out of a total of 761 reports (1.4%) [9] in Indonesia, alongside notable legal cases such as Muara Hemat (Kerinci, Rp 644 million loss, 5-year delay) [25], [26], Jambi Tulo (Muaro Jambi, Rp 300 million for fraudulent projects) [27], and Pangkal Duri (Tanjung Jabung Timur, Rp 415 million loss) [28]. The contributions of this research encompass three primary facets: (1) ", False, False),
        ("Methodology", False, True),
        ("—the creation of an innovative Dual-Path Consensus mechanism that separates local density isolation from global multi-model convergence (IF ∩ RDA); (2) ", False, False),
        ("Theory", False, True),
        ("—the formulation of an integrated theoretical model encompassing Agency Theory, Fraud Diamond, and the DeLone & McLean IS Success Model; and (3) ", False, False),
        ("Practice", False, True),
        ("—a tool that reduces the search space for the district inspectorate (APIP) by 92.6%, identifies 702 persistent Tier-1 villages. This study addresses three primary Research Questions: ", False, False),
        ("RQ1", True, False),
        (": What are the most distinguishing engineering aspects of Siskeudes? ", False, False),
        ("RQ2", True, False),
        (": In what manner does the Dual-Path Consensus detector compare to the baseline detectors and the majority voting method? ", False, False),
        ("RQ3", True, False),
        (": What is the correlation between the identified anomalies and the categories of corruption, and in what manner do neural losses assist APIP field enquiries?", False, False)
    ]
    add_paragraph_runs(doc, p4_runs)

    # -------------------------------------------------------------------------
    # SECTION II: METHODOLOGY & ARTIFACT ARCHITECTURE
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Methodology and Artifact Architecture")

    add_heading_2(doc, "Theoretical Grounding and Conceptual Model")

    p_tg_runs = [
        ("The design of the artifact architecture is informed by Agency Theory, Fraud Diamond Theory, and DeLone & McLean Information Systems Success Model. In the context of the principal-agent setting, the Village Head (Kepala Desa) can be seen as an agent possessing private information which cannot be known by the principal (APIP inspectorates, BPKP, KPK):", False, False)
    ]
    add_paragraph_runs(doc, p_tg_runs)

    # Native Equation (1)
    add_native_equation(doc, omaths[0], "1")

    p_fd_runs = [
        ("There is a significant resource constraint problem with district inspectorates since only between 5 to 15 auditors work in a single regency to audit up to 250 villages [29]. Under the Fraud Diamond Theory [30], ", False, False),
        ("Pressure", True, False),
        (" comes from statutory payment deadlines which imply fast budget execution. The ", False, False),
        ("Opportunity", True, False),
        (" exists by the structural design where as much as 98.8% of the operations of village fund in Jambi use self-managed procurement (Swakelola) without bidding [31]. ", False, False),
        ("Rationalization", True, False),
        (" is the result of low audit probability perception whereas the ", False, False),
        ("Capability", True, False),
        (" is owned by Village Head and Financial Officer (Kaur Keuangan). Fig. 1 shows the conceptual model.", False, False)
    ]
    add_paragraph_runs(doc, p_fd_runs)

    add_figure(doc, "charts_ieee/ieee_conceptual_framework.png", "Integrated conceptual framework linking Agency Theory, Fraud Diamond, DSR comparative artifacts, and DeLone & McLean IS Success impact.")

    add_heading_2(doc, "Data Cleaning and Regional Baseline Z-score Calculation")

    p_dc_runs = [
        ("The original data set, which consists of 99,692 observations, was downloaded from the KPK jaga.id repository [9] where all expenditure realization (", False, False),
        ("Penyerapan", False, True),
        (") and budget ceilings (", False, False),
        ("Pagu", False, True),
        (") of FY 2023–2025 have been registered for the Jambi Province. Data cleaning removed invalid account codes, administrative duplicates, and zeros, resulting in N = 96,778 observations in 1,363 villages. In order to avoid inflated transportation costs, associated with mountainous areas (such as Kerinci district) compared to the lowlands (such as Muaro Jambi district) causing an artificial anomaly, we computed annual regional baseline z-scores as follows:", False, False)
    ]
    add_paragraph_runs(doc, p_dc_runs)

    # Native Equation (2)
    add_native_equation(doc, omaths[1], "2")

    p_rs_runs = [
        ("Continuous features were scaled using RobustScaler (median and IQR) to avoid outliers. The resulting feature matrix is composed of 27 engineered features, shown in Table I.", False, False)
    ]
    add_paragraph_runs(doc, p_rs_runs)

    # Table I
    add_table_head(doc, "ENGINEERED FEATURE CONSTRUCTS AND TARGETED ANOMALY TYPOLOGIES")

    t1_data = [
        ["Feature Construct", "Mathematical Definition", "Targeted Anomaly Modus"],
        ["cost_per_unit", "Realization_Total_i / Volume_i (RobustScaler)", "Unit price mark-up / inflation (T1)"],
        ["absorption_ratio", "Realization_Total_i / Pagu_Village_{v,t}", "Fictitious / ghost activity (T2)"],
        ["avg_completion", "1/3 * (Pct_T1_i + Pct_T2_i + Pct_T3_i)", "Progress manipulation / reporting lag"],
        ["swakelola_high_val", "1(Swakelola_i ∧ Realization_i > Q_0.75)", "Uncompetitive procurement (T5)"],
        ["cost_dev_by_cat", "z_{i,c,k,t} = (x_{i,c,k,t} - μ_{c,k,t}) / σ_{c,k,t} in (c,k,t)", "Regional price outlier (T7)"],
        ["n_stages_active", "∑_{m=1}^3 1(Real_Tm_i > 0)", "Tranche draw concentration (T4)"],
        ["activity_category", "One-Hot Encoded Kode_Output (21 cats)", "Cross-category fund dumping (T7)"]
    ]

    tbl_1 = doc.add_table(rows=len(t1_data), cols=3)
    tbl_1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_1.autofit = False
    set_booktabs_borders(tbl_1)

    t1_widths = [Inches(1.0), Inches(1.35), Inches(1.05)]
    for r_idx, row in enumerate(t1_data):
        for c_idx, val in enumerate(row):
            cell = tbl_1.cell(r_idx, c_idx)
            cell.width = t1_widths[c_idx]
            set_cell_margins(cell, top=30, bottom=30, left=35, right=35)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.0)
            if r_idx == 0:
                p.style = "table col head"
                run.bold = True
            else:
                p.style = "table copy"
                run.bold = False

    add_heading_2(doc, "Multi-Paradigm Unsupervised Detection Engines")

    p_mp_runs = [
        ("The analytical pipeline deploys three orthogonal unsupervised engines:", False, False)
    ]
    add_paragraph_runs(doc, p_mp_runs)

    # 1. IF
    add_heading_3(doc, "Isolation Forest (Global Sparsity Engine)")
    if_runs = [
        ("Features splitting occurs with T = 200 trees and ψ = 256 subsample size. The anomaly score is given by s(x, n) = 2^(-E(h(x))/c(n)) [33]. Setting contamination c = 0.10, instances meeting the 90th percentile are flagged:", False, False)
    ]
    add_paragraph_runs(doc, if_runs)
    # Native Equation (3)
    add_native_equation(doc, omaths[2], "3")

    # 2. LOF
    add_heading_3(doc, "Local Outlier Factor (Density Ratio Engine)")
    lof_runs = [
        ("LOF measures local reachability density (lrd_k) relative to k-nearest neighbors [34]:", False, False)
    ]
    add_paragraph_runs(doc, lof_runs)
    # Native Equation (4)
    add_native_equation(doc, omaths[3], "4")

    p_lof2_runs = [
        ("With the choice of k = 20, which reflects the number of typical groups in a sub-district (", False, False),
        ("kecamatan", False, True),
        ("), points exceeding the 95th quantile are considered as anomalies:", False, False)
    ]
    add_paragraph_runs(doc, p_lof2_runs)
    # Native Equation (5)
    add_native_equation(doc, omaths[4], "5")

    # 3. RDA
    add_heading_3(doc, "Reconstruction Dense Autoencoder (RDA & Neural Loss)")
    rda_runs = [
        ("The RDA employs an eight-layer symmetric dense autoencoder neural network with the configuration: [27 → 64 → 32 → 16 → 8 → 16 → 32 → 64 → 27] and hence latent feature space h of dimension 8 (compression ratio of 3.4:1) [35]. The training algorithm applies the Adam method with parameters (learning rate 10^(-3), L_2 regularization λ = 10^(-3), 50 epochs, batch size 128) and the Mean Squared Error (MSE) loss function. The overall reconstruction error for sample i is E_i, and the error fraction per feature is e_{i,f} (the definition will be continued).", False, False)
    ]
    add_paragraph_runs(doc, rda_runs)
    # Native Equation (6)
    add_native_equation(doc, omaths[5], "6")
    # Native Equation (7)
    add_native_equation(doc, omaths[6], "7")

    add_heading_2(doc, "Uniqueness of the Dual-Path Consensus Ensemble Gate")

    p_dp_runs = [
        ("In traditional unsupervised ensemble learning approaches, majority voting (∑ 1_m ≥ 2) or score averaging is used. In heterogeneous public ledger environments, however, the above techniques cannot be applied because: (1) ", False, False),
        ("Majority Voting Failure", False, True),
        (" arises due to the orthogonality of statistical subspaces (κ(IF, LOF) = 0.041; κ(LOF, RDA) = 0.083). Density outliers that are isolated (e.g., zero-completion activities amongst peer cluster groups) will show up globally as normal with regards to tree splits, thereby leading to the failure of majority voting in the sense that it eliminates 3,940 high-risk local density outliers; (2) ", False, False),
        ("Score Averaging Failure", False, True),
        (": The combination of heterogeneous score scales leads to the obscuring of local density spikes (LOF Sarle BC = 0.957).", False, False)
    ]
    add_paragraph_runs(doc, p_dp_runs)

    p_dp2_runs = [
        ("To remedy the situation, we propose the ", False, False),
        ("Dual-Path Consensus Ensemble Gate", True, False),
        (" (Protocol 2).", False, False)
    ]
    add_paragraph_runs(doc, p_dp2_runs)

    # Native Equation (8)
    add_native_equation(doc, omaths[7], "8")

    p_dp3_runs = [
        ("Path 1 (Local Density Channel)", True, False),
        (" preserves high-confidence density isolates flagged by LOF (BC = 0.957) based on a boundary score of 0.957, without requiring validation through global models. ", False, False),
        ("Path 2 (Global Convergence Channel)", True, False),
        (" requires joint intersection of Isolation Forest (global sparsity) and Reconstruction Autoencoder (nonlinear multivariate distortion), ensuring noise removal caused by individual global model influences.", False, False)
    ]
    add_paragraph_runs(doc, p_dp3_runs)

    # Algorithm 1 Box
    tbl_alg = doc.add_table(rows=1, cols=1)
    tbl_alg.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_alg.autofit = False
    tbl_alg.rows[0].cells[0].width = Inches(3.4)
    cell_alg = tbl_alg.rows[0].cells[0]
    set_cell_margins(cell_alg, top=50, bottom=50, left=70, right=70)
    
    tcPr_alg = cell_alg._tc.get_or_add_tcPr()
    tcPr_alg.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="auto"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))

    alg_lines = [
        ("Algorithm 1: Dual-Path Anomaly Detection and XAI Policy Pipeline", True, False, Pt(1), Pt(3)),
        ("Require: Panel D, c = 0.10, LOF k = 20, RDA bottleneck h = 8, q_IF = 0.90, q_LOF = q_RDA = 0.95.", False, False, Pt(1), Pt(1)),
        ("Ensure: Consensus Vector y_cons, Typologies {T_i}, XAI Checklists {C_i}.", False, False, Pt(1), Pt(3)),
        ("1: Data Hygiene & Centering: Filter invalid records; compute stratum z-score z_{i,c,k,t} = (x_i - μ_{c,k,t})/(σ_{c,k,t}+ε); scale via RobustScaler → X ∈ R^{N × 27}.", False, False, Pt(1), Pt(1)),
        ("2: Multi-Paradigm Inference: Fit IF (y_{i,IF}), LOF (y_{i,LOF}), and RDA (y_{i,RDA}).", False, False, Pt(1), Pt(1)),
        ("3: Dual-Path Gating: y_{i,cons} ← y_{i,LOF} ∨ (y_{i,IF} ∧ y_{i,RDA}).", False, False, Pt(1), Pt(1)),
        ("4: for each flagged instance x_i where y_{i,cons} = 1 do", False, False, Pt(1), Pt(1)),
        ("5:     Map T_i ∈ {T_1, T_2, T_5, T_7, Unclassified} via operational rules.", False, False, Pt(1), Pt(1)),
        ("6:     Decompose error e_{i,f} ← (x_{i,f} - x_hat_{i,f})^2 / E_i; rank descending for audit checklist C_i.", False, False, Pt(1), Pt(1)),
        ("7: end for", False, False, Pt(1), Pt(1)),
        ("8: return y_cons, {T_i}, {C_i}.", False, False, Pt(1), Pt(2))
    ]

    p_first = cell_alg.paragraphs[0]
    p_first.paragraph_format.space_before = alg_lines[0][3]
    p_first.paragraph_format.space_after = alg_lines[0][4]
    p_first.paragraph_format.line_spacing = 1.05
    r_first = p_first.add_run(alg_lines[0][0])
    r_first.font.name = "Courier New"
    r_first.font.size = Pt(7.5)
    r_first.bold = True

    for text, b, it, sp_b, sp_a in alg_lines[1:]:
        p = cell_alg.add_paragraph()
        p.paragraph_format.space_before = sp_b
        p.paragraph_format.space_after = sp_a
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(text)
        r.font.name = "Courier New"
        r.font.size = Pt(7.5)
        if b: r.bold = True
        if it: r.italic = True

    add_heading_2(doc, "Synthetic Fraud Benchmark Generation & Reproducibility")

    p_syn_runs = [
        ("As the real Siskeudes panel does not have validated fraud ground truth, the performance of the models is tested against an ex-ante synthetic fraud benchmark generation (N = 10,000). The baseline features are obtained from empirical parametric distributions calibrated with real Siskeudes expenditure. cost_per_unit ~ Lognormal(2.0, 0.5), absorption_ratio ~ Beta(5, 1), avg_completion ~ Uniform(0.70, 1.00), swakelola_high_val ~ Binomial(1, 0.25), and cost_dev_by_cat ~ N(0.0, 1.0). We injected 500 synthetic fraud instances (5.0% prevalence) across three empirical fraud moduses:", False, False)
    ]
    add_paragraph_runs(doc, p_syn_runs)

    p_m1 = [("1) Modus 1: Mark-Up (n = 200): ", True, False), ("cost_per_unit × 5.0, cost_dev + 4.5σ.", False, False)]
    add_paragraph_runs(doc, p_m1, style="bullet list")
    p_m2 = [("2) Modus 2: Ghost Activities (n = 150): ", True, False), ("absorption ≤ 0.02, completion ≤ 0.05.", False, False)]
    add_paragraph_runs(doc, p_m2, style="bullet list")
    p_m3 = [("3) Modus 3: Category Dumping (n = 150): ", True, False), ("cost_dev_by_cat + 5.0σ.", False, False)]
    add_paragraph_runs(doc, p_m3, style="bullet list")

    p_syn2_runs = [
        ("Threshold quantiles (q_IF = 0.90, q_LOF = q_RDA = 0.95) are justified by inspectorate audit capacity constraints (5–15 auditors per regency) to prevent alert fatigue. The random seed was fixed to seed = 42 for strict reproducibility.", False, False)
    ]
    add_paragraph_runs(doc, p_syn2_runs)

    # -------------------------------------------------------------------------
    # SECTION III: RESULTS & EMPIRICAL ANALYSIS
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Results and Empirical Analysis")

    add_heading_2(doc, "Anomaly Flag Counts and Temporal Consistency")

    p_res1_runs = [
        ("Fig. 2 displays the temporal stability of flagging. The LOF approach has shown stability in the flagging process in different budget periods with 4.7% in 2023, 4.6% in 2024, and 5.8% in 2025. The temporal stability for protocol 2 is seen through its consistent flagging percentage annually as 7.5% in 2023, 6.9% in 2024, and 7.7% in 2025.", False, False)
    ]
    add_paragraph_runs(doc, p_res1_runs)

    add_figure(doc, "charts_ieee/ieee_rate_consistency.png", "Year-over-year anomaly flagging rate consistency across FY 2023–2025.")

    add_heading_2(doc, "Orthogonality of Subspace and Score Distributions")

    p_res2_runs = [
        ("Figs. 3 and Table II display score distributions with annotations for Sarle Bimodality Coefficient (BC) and pair-wise Cohen's κ.", False, False)
    ]
    add_paragraph_runs(doc, p_res2_runs)

    add_figure(doc, "charts_ieee/ieee_score_distributions.png", "Score distribution histograms and bimodality threshold separations.")

    # Table II
    add_table_head(doc, "SCORE DISTRIBUTION BIMODALITY AND SUBSPACE OVERLAP MATRIX")

    t2_data = [
        ["Method / Pair", "Sarle BC", "Distribution Structure", "Shared Records", "Cohen's κ"],
        ["Isolation Forest", "0.335", "Unimodal continuous spectrum", "---", "---"],
        ["Reconstruction DA", "0.703", "Moderate bimodal (clear tail)", "---", "---"],
        ["Local Outlier Factor", "0.957", "Heavy-tailed density isolation", "---", "---"],
        ["IF ∩ LOF", "---", "Subspace Orthogonal", "252", "0.041 (Slight)"],
        ["IF ∩ RDA", "---", "Global Convergence", "2,314", "0.482 (Mod.)"],
        ["LOF ∩ RDA", "---", "Subspace Orthogonal", "422", "0.083 (Slight)"],
        ["Triple (IF ∩ LOF ∩ RDA)", "---", "Maximum Confidence Core", "225", "---"],
        ["LOF-Only Isolates", "---", "Rescued in Protocol 2", "3,940", "---"]
    ]

    tbl_2 = doc.add_table(rows=len(t2_data), cols=5)
    tbl_2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_2.autofit = False
    set_booktabs_borders(tbl_2)

    t2_widths = [Inches(1.0), Inches(0.45), Inches(1.15), Inches(0.4), Inches(0.4)]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = tbl_2.cell(r_idx, c_idx)
            cell.width = t2_widths[c_idx]
            set_cell_margins(cell, top=25, bottom=25, left=30, right=30)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.0)
            if r_idx == 0:
                p.style = "table col head"
                run.bold = True
            else:
                p.style = "table copy"
                if r_idx in [2, 3, 5, 8]:
                    run.bold = True
                else:
                    run.bold = False

    p_t2_post_runs = [
        ("Local Outlier Factor (LOF) is capable of achieving a high Sarle BC of 0.957 by effectively distinguishing dense groups of peers from outliers having extremely high scores (up to 5.40 × 10^9). The insignificant Cohen's κ coefficients (of 0.041 for IF-LOF and of 0.083 for LOF-RDA) mean that LOF operates in an orthogonal subspace. All 3,940 isolates generated by LOF were successfully removed using Protocol 1.", False, False)
    ]
    add_paragraph_runs(doc, p_t2_post_runs)

    add_heading_2(doc, "Ablation on Synthetic Benchmark and Real Panel")

    p_abl_runs = [
        ("Table III shows an extensive ablation study done on both the synthetic fraud benchmark (N = 10,000) and the real-world Jambi panel (N = 96,778).", False, False)
    ]
    add_paragraph_runs(doc, p_abl_runs)

    # Table III
    add_table_head(doc, "ABLATION STUDY: SYNTHETIC BENCHMARK RECOVERY VS REAL-WORLD EXPOSURE")

    t3_data = [
        ["Ablation Configuration", "Prec.", "Rec.", "F1", "AUC", "Flags (N)", "Realization Risk"],
        ["(1) LOF Alone (Density)", "0.686", "0.686", "0.686", "0.745", "4,839 (5.0%)", "Rp 396.40 Billion"],
        ["(2) IF Alone (Sparsity)", "0.724", "0.724", "0.724", "0.782", "9,678 (10.0%)", "Rp 451.18 Billion"],
        ["(3) RDA Alone (Neural Loss)", "0.812", "0.812", "0.812", "0.811", "4,840 (5.0%)", "Rp 428.60 Billion"],
        ["(4) Pairwise IF ∧ LOF", "0.780", "0.420", "0.546", "0.702", "252 (0.3%)", "Rp 21.84 Billion"],
        ["(5) Pairwise LOF ∧ RDA", "0.810", "0.460", "0.586", "0.725", "422 (0.4%)", "Rp 39.15 Billion"],
        ["(6) Global IF ∧ RDA", "0.854", "0.640", "0.732", "0.815", "2,314 (2.4%)", "Rp 246.45 Billion"],
        ["(7) Protocol 1 (Majority ≥ 2)", "0.642", "0.510", "0.568", "0.720", "3,107 (3.1%)", "Rp 278.40 Billion"],
        ["(8) Protocol 2 (Dual-Path)", "0.846", "0.846", "0.846", "0.912", "7,153 (7.4%)", "Rp 642.85 Billion"]
    ]

    tbl_3 = doc.add_table(rows=len(t3_data), cols=7)
    tbl_3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_3.autofit = False
    set_booktabs_borders(tbl_3)

    t3_widths = [Inches(1.15), Inches(0.35), Inches(0.35), Inches(0.35), Inches(0.35), Inches(0.45), Inches(0.4)]
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            cell = tbl_3.cell(r_idx, c_idx)
            cell.width = t3_widths[c_idx]
            set_cell_margins(cell, top=25, bottom=25, left=25, right=25)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.0)
            if r_idx == 0:
                p.style = "table col head"
                run.bold = True
            else:
                p.style = "table copy"
                if r_idx == 8 or (r_idx == 6 and c_idx == 1):
                    run.bold = True
                else:
                    run.bold = False

    p_abl_post_runs = [
        ("Based on ablation studies, we can see that: (1) each detector recognizes different anomaly types; (2) strict intersection (IF ∧ LOF, LOF ∧ RDA) leads to dramatic recall drops (Recall ≤ 0.460); (3) global convergence (IF ∧ RDA) brings high precision (0.854) but does not find local density-based anomalies (Recall = 0.640); (4) Protocol 1 (majority voting) has significant mutual cancellation, resulting in F1 = 0.568 and the lack of 49.0% of synthetic frauds; and (5) ", False, False),
        ("Protocol 2 (Dual-Path Consensus)", True, False),
        (" has reached optimal settings: ", False, False),
        ("Precision = 0.846, Recall = 0.846, F1 = 0.846, and AUC-ROC = 0.912", True, False),
        (". It additionally identifies Rp 642.85 billion worth of realization risks in the real-world setting.", False, False)
    ]
    add_paragraph_runs(doc, p_abl_post_runs)

    add_heading_2(doc, "Corruption Typologies Mapping and Dynamics of Change")

    p_typ_runs = [
        ("The consensus labels were projected onto corruption typologies using Algorithm 1. As shown in Figs. 4 and Table IV, the shift in distribution is illustrated between Protocol 1 and Protocol 2. The irregularity patterns that Protocol 2 reveals include: ", False, False),
        ("T_2 Ghost Activities (58.1% / 4,155 records)", True, False),
        (" and ", False, False),
        ("T_5 Procurement Irregularities (32.8% / 2,343 records)", True, False),
        (".", False, False)
    ]
    add_paragraph_runs(doc, p_typ_runs)

    add_figure(doc, "charts_ieee/ieee_typology_comparison.png", "Corruption typology frequency distribution shift (Protocol 1 vs Protocol 2).")

    # Table IV
    add_table_head(doc, "COMPARATIVE TYPOLOGY FREQUENCY SHIFT (PROTOCOL 1 VS PROTOCOL 2)")

    t4_data = [
        ["Code", "Typology Description", "P1 Count", "%", "P2 Count", "%", "Relative Shift"],
        ["T2_Ghost", "Ghost Activity (Proyek Fiktif)", "774", "24.9%", "4,155", "58.1%", "+436.8% (Primary)"],
        ["T5_Procure", "Procurement Irr. (Swakelola)", "26", "0.8%", "2,343", "32.8%", "+8911.5% (Major)"],
        ["T7_Dump", "Cross-Category Dumping", "1,568", "50.5%", "1,284", "18.0%", "−18.1% (Refined)"],
        ["T1_Markup", "Unit Price Mark-Up (Mark-up)", "1,571", "50.6%", "1,180", "16.5%", "−24.9% (Refined)"],
        ["T4_Lock", "Disbursement Stage Lock", "0", "0.0%", "28", "0.4%", "Newly captured"],
        ["Unclassified", "Sub-threshold Masking", "708", "22.8%", "1,227", "17.2%", "Proportional drop"]
    ]

    tbl_4 = doc.add_table(rows=len(t4_data), cols=7)
    tbl_4.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_4.autofit = False
    set_booktabs_borders(tbl_4)

    t4_widths = [Inches(0.65), Inches(1.1), Inches(0.35), Inches(0.3), Inches(0.35), Inches(0.3), Inches(0.35)]
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            cell = tbl_4.cell(r_idx, c_idx)
            cell.width = t4_widths[c_idx]
            set_cell_margins(cell, top=25, bottom=25, left=25, right=25)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.0)
            if r_idx == 0:
                p.style = "table col head"
                run.bold = True
            else:
                p.style = "table copy"
                if r_idx in [1, 2] and c_idx in [0, 4, 5, 6]:
                    run.bold = True
                else:
                    run.bold = False

    add_heading_2(doc, "Reconstruction Error Drivers in XAI and Spatial Clustering")

    p_rda_runs = [
        ("Fig. 5 demonstrates the drivers behind feature reconstruction error by RDA analysis. They are cost_dev_by_cat (42.7%, primary cause of error in 2,065 records) and cost_per_unit (32.0%, 1,551 records). Fig. 6 contains linear PCA and non-linear t-SNE visualizations. Principal Component 1 explains 26.0% of variance. In the latter visualization, the outliers form micro-clusters around Swakelola infrastructures and capital injections from BUMDes, rather than being distributed as noise.", False, False)
    ]
    add_paragraph_runs(doc, p_rda_runs)

    add_figure(doc, "charts_ieee/ieee_rda_error_decomposition.png", "Reconstruction error attribution drivers in 8-layer bottleneck RDA.")
    add_figure(doc, "charts_ieee/ieee_pca_tsne_projection.png", "Dimensionality reductions revealing peripheral micro-clustering.")

    add_heading_2(doc, "Longitudinal Village Persistence and Regency Risk Exposure")

    p_long_runs = [
        ("The longitudinal persistence of villages is measured by P_v = N_{flagged_years} / N_{total_years}. This is used to group the jurisdictions into supervisory groups (see Fig. 7 and Table V). As per Protocol 2, there are 702 villages (51.5%) that exhibit three-year persistent anomalies where P_v = 1.0. Examples include Desa Maliki Air (16 anomalies, T_2 Ghost), Desa Gedang (13 anomalies, T_5 Procurement) and Desa Paling Serumpun (12 anomalies).", False, False)
    ]
    add_paragraph_runs(doc, p_long_runs)

    add_figure(doc, "charts_ieee/ieee_village_persistence.png", "Longitudinal village priority tier distribution comparison.")

    # Table V
    add_table_head(doc, "EXEMPLAR JURISDICTIONAL CASE STUDIES AND REGENCY EXPOSURE")

    t5_data = [
        ["Village Jurisdiction", "FY", "Activity Description", "Anomaly Metric", "Mapped Typology"],
        ["Desa Rantau Makmur", "2025", "Modal BUMDes", "LOF = 4.78 × 10^9", "T5 Procurement / Density"],
        ["Desa Sungai Raya", "2025", "Modal BUMDes", "LOF = 5.54 × 10^9", "T5 Procurement / Density"],
        ["Desa Kedemangan", "2025", "Pembangunan Kios", "RDA MSE = 0.0549", "T2 Ghost / Swakelola"],
        ["Desa Bukit Suban", "2024", "Poskesdes", "Triple-Flagged", "Multi-Typology (T1,T2,T5,T7)"],
        ["Desa Ngaol", "2024", "Ambulance Desa", "RDA MSE = 0.0482", "T1 Mark-Up / T5 Procure"]
    ]

    tbl_5 = doc.add_table(rows=len(t5_data), cols=5)
    tbl_5.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_5.autofit = False
    set_booktabs_borders(tbl_5)

    t5_widths = [Inches(0.85), Inches(0.3), Inches(0.75), Inches(0.75), Inches(0.75)]
    for r_idx, row in enumerate(t5_data):
        for c_idx, val in enumerate(row):
            cell = tbl_5.cell(r_idx, c_idx)
            cell.width = t5_widths[c_idx]
            set_cell_margins(cell, top=25, bottom=25, left=30, right=30)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.0)
            if r_idx == 0:
                p.style = "table col head"
                run.bold = True
            else:
                p.style = "table copy"
                run.bold = False

    p_batanghari = [
        ("Top Regency Risk Density: Batanghari (15.75% flagged rate | Rp 115.71 B at risk), followed by Muaro Jambi (10.58% | Rp 98.45 B) and Kerinci (9.56% | Rp 124.30 B). Kabupaten Batanghari exhibits the largest risk exposure as it has 15.75% of flags and its risk exposure stands at Rp 115.71 billion.", False, False)
    ]
    p_b_elem = add_paragraph_runs(doc, p_batanghari, space_before=Pt(2), space_after=Pt(3))
    for r in p_b_elem.runs:
        r.font.size = Pt(8.0)

    # -------------------------------------------------------------------------
    # SECTION IV: DISCUSSION & GOVERNANCE IMPLICATIONS
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Discussion and Governance Implications")

    add_heading_2(doc, "Effectiveness of Algorithms and Cancellation Resolution")

    p_disc1_runs = [
        ("The empirical results confirm that Protocol 2 resolves the inherent weaknesses of the majority voting mechanism as follows: (1) ", False, False),
        ("Subspace Decoupling", True, False),
        ("—Protocol 2 allows LOF to operate as an independent density channel while achieving joint convergence on global models (IF ∩ RDA) and thus restores 3,940 isolated records without single-model noise, increasing the number of recall records to 7,153 (Rp 642.85 billion in realization risk); (2) ", False, False),
        ("Controlled Synthetic Recovery", True, False),
        ("—High precision (0.846) and recall (0.846) in the presence of injected fraud have been proven in the controlled experiments (AUC = 0.912); (3) ", False, False),
        ("Search Space Reduction", True, False),
        ("—Reducing 96,778 transactions to 7,153 target transactions leads to 92.6% inspectorate search space reduction, allowing the field audit to be feasible for small teams of 5 to 15 auditors [29]; and (4) ", False, False),
        ("Sub-Threshold Risk Capture", True, False),
        ("—Multidimensional LOF and RDA reveal the joint multi-feature probability change and thus detect 1,227 sub-threshold records (Rp 125.07 billion in latent exposure).", False, False)
    ]
    add_paragraph_runs(doc, p_disc1_runs)

    add_heading_2(doc, "Mechanisms That Drive Typology Changes")

    p_disc2_runs = [
        ("The 436.8% jump in the number of ", False, False),
        ("T_2 Ghost Activities", True, False),
        (" (4,155 records) is due to the fact that LOF evaluates reachability density with respect to peer villages. Projects where there were no projects show normal behavior during the global tree split analysis, whereas they become clear outliers when contrasted with peer villages who conducted the physical works. Similarly, the nearly 90x increase in ", False, False),
        ("T_5 Procurement Irregularities", True, False),
        (" (2,343 records) happens due to the fact that autoencoder learns the non-linear relationship between Swakelola and high unit cost.", False, False)
    ]
    add_paragraph_runs(doc, p_disc2_runs)

    add_heading_2(doc, "Evidentiary Standards and Limitations on Public Audit Law")

    p_disc3_runs = [
        ("The use of machine learning in public audit is limited by formal standards of evidentiary process. Namely: (1) ", False, False),
        ("First Investigative Clue (", True, False),
        ("Indikasi Awal", True, True),
        (")", True, False),
        (": As per Article 184 of the Criminal Procedure Code (KUHAP) and Constitutional Court decision No. 21/PUU-XII/2014 [23], algorithms’ results cannot be considered formal evidence; they serve as initial clues for further formal audit investigation. (2) ", False, False),
        ("Irregularities vs Criminal Behavior (PMH)", True, False),
        (": High anomalies scores often indicate problems caused by bureaucratic inefficiency rather than criminal actions. As per Law No. 31/1999 [23], the prosecutor needs to prove criminal intention (", False, False),
        ("mens rea", False, True),
        ("), (", False, False),
        ("Perbuatan Melawan Hukum", False, True),
        (") and state losses. (3) ", False, False),
        ("XAI-to-Audit Chain of Custody", True, False),
        (": Decomposition of reconstruction errors for responsible data analysis (RDA) determines audit inspection requests—e.g., unit cost anomaly leads to auditing Standard Price Ceiling, completion anomaly results in on-site measuring.", False, False)
    ]
    add_paragraph_runs(doc, p_disc3_runs)

    add_heading_2(doc, "DSR Evaluation Matrix and Operationalizing IS Success")

    p_dsr_intro = [
        ("Table VI summarizes the Design Science Research (DSR) evaluation matrix across the project cycles.", False, False)
    ]
    add_paragraph_runs(doc, p_dsr_intro)

    # Table VI
    add_table_head(doc, "DESIGN SCIENCE RESEARCH (DSR) EVALUATION MATRIX")

    t6_data = [
        ["DSR Dimension", "Operationalization", "Target Metric", "Observed Outcome"],
        ["Relevance Cycle", "Search reduction for APIP", "Search space reduction", "92.6% reduction (96.8k → 7.2k)"],
        ["Rigor Cycle", "Multi-method convergence", "Cohen's Kappa", "κ(IF, RDA) = 0.482 (Mod.)"],
        ["Design Cycle", "Priority tiering", "High-risk coverage", "1,172 Tier-1 villages (86.0%)"],
        ["Ex-Ante Eval.", "Synthetic fraud recovery", "F1, AUC-ROC", "F1 = 0.846, AUC = 0.912"]
    ]

    tbl_6 = doc.add_table(rows=len(t6_data), cols=4)
    tbl_6.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_6.autofit = False
    set_booktabs_borders(tbl_6)

    t6_widths = [Inches(0.85), Inches(0.95), Inches(0.75), Inches(0.85)]
    for r_idx, row in enumerate(t6_data):
        for c_idx, val in enumerate(row):
            cell = tbl_6.cell(r_idx, c_idx)
            cell.width = t6_widths[c_idx]
            set_cell_margins(cell, top=25, bottom=25, left=30, right=30)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.0)
            if r_idx == 0:
                p.style = "table col head"
                run.bold = True
            else:
                p.style = "table copy"
                if c_idx == 0 or c_idx == 3:
                    run.bold = True
                else:
                    run.bold = False

    p_dm_runs = [
        ("This artifact follows the DeLone and McLean IS Success Model [24]. Higher Information Quality increases Individual Impact by decreasing auditor burden by 92.6%, and identifying 702 persistent Tier-1 villages (P_v = 1.0). On the other hand, System Quality increases Organizational Impact by ensuring pre-disbursement verification and developing village fund management towards automatic deterrence.", False, False)
    ]
    add_paragraph_runs(doc, p_dm_runs)

    add_heading_2(doc, "Limitations and Future Research Directions")

    p_lim_runs = [
        ("Four boundary conditions deserve consideration: (1) There are no ground truth fraud labels in Siskeudes ledgers, thus necessitating the use of synthetic benchmarking and industry-specific heuristics; (2) the system is not able to identify unrecorded off-books cash kickbacks; (3) regional baseline models must be re-calibrated if used outside Jambi Province; and (4) hard-coded policy thresholds have left 1,227 difficult cases unclassified, implying that future fuzzy-logic analysis needs to be introduced.", False, False)
    ]
    add_paragraph_runs(doc, p_lim_runs)

    # -------------------------------------------------------------------------
    # SECTION V: CONCLUSION
    # -------------------------------------------------------------------------
    add_heading_1(doc, "Conclusion")

    p_conc_runs = [
        ("This paper presents the development of an unsupervised Dual-Path Consensus machine learning model (Protocol 2) aimed at detecting expenditure anomalies from 96,778 transactions in Jambi Province. On the subject of Research Question 1 (", False, False),
        ("RQ1", True, False),
        ("), region-based and category stratified cost variations (cost_dev_by_cat and cost_per_unit) have the strongest discriminatory strength, explaining 74.7% of the reconstruction error generated by the deep autoencoder. On the subject of Research Question 2 (", False, False),
        ("RQ2", True, False),
        ("), LOF is capable of detecting localized density isolates (BC = 0.957) while IF and RDA detect global structural anomalies. The Dual-Path Consensus method (LOF ∨ (IF ∧ RDA)) helps in overcoming the problem of mutual cancellation resulting in ", False, False),
        ("F1 = 0.846 and AUC-ROC = 0.912", True, False),
        (" when compared to the majority voting approach on an ex-ante synthetic fraud benchmark (F1 = 0.568). On the subject of Research Question 3 (", False, False),
        ("RQ3", True, False),
        ("), the mapping layer operational policy translates mathematical anomalies into actionable typologies; there are 4,155 Ghost Activities (T_2, 58.1%) and 2,343 Procurement Irregularities (T_5, 32.8%), totaling Rp 642.85 billion in realization risk with 92.6% reduction in APIP audit search space.", False, False)
    ]
    add_paragraph_runs(doc, p_conc_runs)

    # -------------------------------------------------------------------------
    # ACKNOWLEDGMENT (Heading 5: no numbering, small caps, 10pt)
    # -------------------------------------------------------------------------
    add_heading_5(doc, "Acknowledgment")

    p_ack1_runs = [
        ("This study was supported by the competitive research fund scheme (Penelitian Pemula Binus) entitled “Corruption Indication Detection in Village Fund Expenditure Activities Using Comparative Unsupervised Machine Learning: Evidence from Jambi Province, Indonesia” with contract number: 137/VRRTT/V1/2026 and contract date: June 2, 2026. The authors acknowledge the contributions of the research team: Humam Faiq for data provision & regulatory compliance review; Charlie Yen for manuscript preparation and editing; Farrell Yodihartomo and Pandu Wicaksono for conceptualization, validation, experiment, and manuscript review.", False, False)
    ]
    add_paragraph_runs(doc, p_ack1_runs)

    p_ack2_runs = [
        ("During the preparation of this manuscript, the authors utilized generative artificial intelligence solely for English grammar refinement, sentence flow optimization, and LaTeX formatting. Finally, the authors declared the conflicts of interest do not exist in this research.", False, False)
    ]
    add_paragraph_runs(doc, p_ack2_runs)

    # -------------------------------------------------------------------------
    # REFERENCES (Heading 5: no numbering, small caps, 10pt)
    # -------------------------------------------------------------------------
    add_heading_5(doc, "References")

    references_list = [
        (1, [
            ("Republic of Indonesia, \"Undang-Undang Nomor 6 Tahun 2014 tentang Desa [Law No. 6 of 2014 on Villages],\" ", False, False),
            ("Lembaran Negara Republik Indonesia", False, True),
            (", 2014.", False, False)
        ]),
        (2, [
            ("Indonesian Corruption Watch (ICW), \"Laporan Tren Penindakan Kasus Korupsi Dana Desa 2024,\" ICW, Jakarta, Indonesia, Tech. Rep., 2024. [Online]. Available: https://www.antikorupsi.org", False, False)
        ]),
        (3, [
            ("Anti-Corruption Learning Center (ACLC) KPK, \"Menebar Benih Antikorupsi di Desa-Desa [Sowing Anti-Corruption Seeds in Villages],\" Pusat Edukasi Antikorupsi, Komisi Pemberantasan Korupsi (KPK), Jakarta, Indonesia, Oct. 2023. [Online]. Available: https://aclc.kpk.go.id/aksi-informasi/Eksplorasi/20231027-menebar-benih-antikorupsi-di-desa-desa", False, False)
        ]),
        (4, [
            ("Komisi Pemberantasan Korupsi (KPK), \"Trisula Strategi Pemberantasan Korupsi: Pendidikan, Pencegahan, dan Penindakan,\" Pusat Edukasi Antikorupsi (ACLC KPK), Jakarta, Indonesia, 2022. [Online]. Available: https://aclc.kpk.go.id", False, False)
        ]),
        (5, [
            ("Komisi Pemberantasan Korupsi (KPK), \"Pendidikan dan Pencegahan Korupsi di Tingkat Desa: Program Desa Antikorupsi 2021–2024,\" Direktorat Pembinaan Peran Serta Masyarakat, KPK, Jakarta, Indonesia, 2025. [Online]. Available: https://kpk.go.id", False, False)
        ]),
        (6, [
            ("Badan Pengawasan Keuangan dan Pembangunan (BPKP) and KPK, \"Petunjuk Teknis Pengawasan Pengelolaan Keuangan Desa Menggunakan Aplikasi Siswaskeudes,\" BPKP / Stranas PK, Jakarta, Indonesia, Tech. Rep., 2020.", False, False)
        ]),
        (7, [
            ("Tim Nasional Pencegahan Korupsi (Stranas PK), \"Aksi Pencegahan Korupsi 2025–2026: Digitalisasi Pengawasan Keuangan Desa,\" Sekretariat Nasional Pencegahan Korupsi, Jakarta, Indonesia, 2024. [Online]. Available: https://stranaspk.id", False, False)
        ]),
        (8, [
            ("Komisi Pemberantasan Korupsi (KPK), \"Monitoring Center for Prevention (MCP): Indikator Tata Kelola Keuangan Desa,\" Kedeputian Bidang Koordinasi dan Supervisi, KPK, Jakarta, Indonesia, 2025. [Online]. Available: https://kpk.go.id", False, False)
        ]),
        (9, [
            ("jaga.id, \"Laporan Pengaduan Dana Desa — Statistik Nasional,\" Forum Indonesia untuk Transparansi Anggaran (FITRA) / KPK, Jakarta, Indonesia, 2026. [Online]. Available: https://jaga.id", False, False)
        ]),
        (10, [
            ("J. G. Vargas-Hernández, \"The multiple faces of corruption: typology, forms and levels,\" ", False, False),
            ("SSRN Electronic Journal", False, True),
            (", 2009. doi: 10.2139/ssrn.1413976.", False, False)
        ]),
        (11, [
            ("F. Mutungi, R. Baguma, A. H. Ejiri, and T. Janowski, \"Digital anti-corruption typology for public service delivery,\" ", False, False),
            ("International Journal of Computer Applications", False, True),
            (", vol. 183, no. 5, pp. 20–31, 2021. doi: 10.5120/ijca2021921089.", False, False)
        ]),
        (12, [
            ("T. Hidajat, \"Village fund corruption modes: an anti-corruption perspective in Indonesia,\" ", False, False),
            ("Journal of Financial Crime", False, True),
            (", vol. 31, no. 6, pp. 1454–1467, 2024. doi: 10.1108/jfc-01-2024-0042.", False, False)
        ]),
        (13, [
            ("A. Triyono, \"Framing analysis of village funding corruption in media Suaramerdeka.com in Central Java, Indonesia, 2019,\" ", False, False),
            ("International Journal of Criminology and Sociology", False, True),
            (", vol. 9, pp. 1292–1301, 2020. doi: 10.6000/1929-4409.2020.09.136.", False, False)
        ]),
        (14, [
            ("K. K. Medan, D. A. Kase, and G. A. Bunga, \"Patterns of village fund corruption prevention based on Fatuleu local wisdom in Kupang Regency, Indonesia,\" ", False, False),
            ("Journal of Posthumanism", False, True),
            (", vol. 5, no. 5, pp. 180–198, 2025. doi: 10.63332/joph.v5i5.1810.", False, False)
        ]),
        (15, [
            ("A. Ali, S. Abd Razak, and S. H. Othman, \"Financial fraud detection based on machine learning: A systematic literature review,\" ", False, False),
            ("Applied Sciences", False, True),
            (", vol. 12, no. 19, Art. no. 9637, 2022. doi: 10.3390/app12199637.", False, False)
        ]),
        (16, [
            ("H. Gao, G. Kou, and H. Liang, \"Machine learning in business and finance: a literature review and research opportunities,\" ", False, False),
            ("Financial Innovation", False, True),
            (", vol. 10, no. 1, Art. no. 63, 2024. doi: 10.1186/s40854-024-00629-z.", False, False)
        ]),
        (17, [
            ("J. E. de Albuquerque Filho, L. C. P. Brandão, and B. Fernandes, \"A review of neural networks for anomaly detection,\" ", False, False),
            ("IEEE Access", False, True),
            (", vol. 10, pp. 109279–109301, 2022. doi: 10.1109/ACCESS.2022.3216007.", False, False)
        ]),
        (18, [
            ("A. A. Almazroi and N. Ayub, \"Online payment fraud detection model using machine learning techniques,\" ", False, False),
            ("IEEE Access", False, True),
            (", vol. 11, pp. 138032–138044, 2023. doi: 10.1109/ACCESS.2023.3339226.", False, False)
        ]),
        (19, [
            ("D. Fährmann, L. Martín, and L. Sánchez, \"Anomaly detection in smart environments: A comprehensive survey,\" ", False, False),
            ("IEEE Access", False, True),
            (", vol. 12, pp. 78564–78589, 2024. doi: 10.1109/ACCESS.2024.3395051.", False, False)
        ]),
        (20, [
            ("S. Han, X. Hu, S. Huang, M. Chen, H. Jiang, and Y. Zhao, \"ADBench: Anomaly detection benchmark,\" in ", False, False),
            ("Advances in Neural Information Processing Systems (NeurIPS 2022)", False, True),
            (", vol. 35, 2022, pp. 32142–32159.", False, False)
        ]),
        (21, [
            ("F. A. Almaqtari, \"The role of IT governance in the integration of AI in accounting and auditing operations,\" ", False, False),
            ("Economies", False, True),
            (", vol. 12, no. 8, Art. no. 199, 2024. doi: 10.3390/economies12080199.", False, False)
        ]),
        (22, [
            ("D. Vuković, S. Dekpo-Adza, and S. Matović, \"AI integration in financial services: a systematic review of trends and regulatory challenges,\" ", False, False),
            ("Humanities and Social Sciences Communications", False, True),
            (", vol. 12, no. 1, Art. no. 57, 2025. doi: 10.1057/s41599-025-04850-8.", False, False)
        ]),
        (23, [
            ("Republic of Indonesia, \"Undang-Undang Nomor 31 Tahun 1999 jo. Undang-Undang Nomor 20 Tahun 2001 tentang Pemberantasan Tindak Pidana Korupsi [Law No. 31 of 1999 as amended by Law No. 20 of 2001 on Corruption Eradication],\" 2001.", False, False)
        ]),
        (24, [
            ("W. H. DeLone and E. R. McLean, \"The DeLone and McLean model of information systems success: a ten-year update,\" ", False, False),
            ("Journal of Management Information Systems", False, True),
            (", vol. 19, no. 4, pp. 9–30, 2003. doi: 10.1080/07421222.2003.11045748.", False, False)
        ]),
        (25, [
            ("JambiTV Disway, \"Eks Kades Muara Hemat jalani tahap 2 kasus dugaan korupsi dana desa,\" Feb. 2026. [Online]. Available: https://jambitv.disway.id", False, False)
        ]),
        (26, [
            ("Kompas.com, \"Kades hingga mantan kades di Kerinci, Jambi korupsi Rp 644 juta dana desa,\" Aug. 2025. [Online]. Available: https://regional.kompas.com", False, False)
        ]),
        (27, [
            ("JambiTV Disway, \"Dana desa Jambi Tulo dibekukan: Inspektorat temukan dugaan kegiatan fiktif Rp300 juta lebih,\" 2025. [Online]. Available: https://jambitv.disway.id", False, False)
        ]),
        (28, [
            ("JambiLINK.id, \"Tersangka korupsi dana desa Pangkal Duri ditangkap, kerugian negara capai Rp 415 juta,\" Aug. 2024. [Online]. Available: https://jambilink.id", False, False)
        ]),
        (29, [
            ("K. Srirejeki and A. Faturokhman, \"In search of corruption prevention model: case study from Indonesia village fund,\" ", False, False),
            ("Acta Universitatis Danubius. Oeconomica", False, True),
            (", vol. 16, no. 3, pp. 214–229, 2020.", False, False)
        ]),
        (30, [
            ("D. T. Wolfe and D. R. Hermanson, \"The fraud diamond: Considering the four elements of fraud,\" ", False, False),
            ("CPA Journal", False, True),
            (", vol. 74, no. 12, pp. 38–42, 2004.", False, False)
        ]),
        (31, [
            ("T. Søreide, \"Corruption in public procurement: causes, consequences and cures,\" Chr. Michelsen Institute, Bergen, Norway, Tech. Rep. CMI Report R 2002:1, 2002.", False, False)
        ]),
        (32, [
            ("N. S. Groenendijk, \"A principal-agent model of corruption,\" ", False, False),
            ("Crime, Law and Social Change", False, True),
            (", vol. 27, no. 3–4, pp. 207–229, 1997.", False, False)
        ]),
        (33, [
            ("F. T. Liu, K. M. Ting, and Z.-H. Zhou, \"Isolation forest,\" in ", False, False),
            ("Proc. 8th IEEE Int. Conf. on Data Mining (ICDM)", False, True),
            (", Pisa, Italy, 2008, pp. 413–422. doi: 10.1109/ICDM.2008.17.", False, False)
        ]),
        (34, [
            ("M. M. Breunig, H.-P. Kriegel, R. T. Ng, and J. Sander, \"LOF: Identifying density-based local outliers,\" in ", False, False),
            ("Proc. 2000 ACM SIGMOD Int. Conf. on Management of Data", False, True),
            (", Dallas, TX, USA, 2000, pp. 93–104. doi: 10.1145/342009.335388.", False, False)
        ]),
        (35, [
            ("C. Zhou and R. C. Paffenroth, \"Anomaly detection with robust deep autoencoders,\" in ", False, False),
            ("Proc. 23rd ACM SIGKDD Int. Conf. on Knowledge Discovery and Data Mining", False, True),
            (", Halifax, NS, Canada, 2017, pp. 665–674. doi: 10.1109/3097983.3098052.", False, False)
        ])
    ]

    for num, r_list in references_list:
        p_ref = doc.add_paragraph(style="references")
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.2)
        p_ref.paragraph_format.first_line_indent = Inches(-0.2)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(1.0)
        p_ref.paragraph_format.line_spacing = 0.94
        
        r_num = p_ref.add_run(f"[{num}]\t")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(8.0)
        
        for r_txt, r_b, r_it in r_list:
            r = p_ref.add_run(r_txt)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.0)
            if r_b: r.bold = True
            if r_it: r.italic = True

    # Final section properties (2 columns)
    final_sect = body.xpath("./w:sectPr")[0]
    final_sect.clear()
    s2_xml = (
        f'<w:sectPr {nsdecls("w")}>'
        '<w:type w:val="continuous"/>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="864" w:right="864" w:bottom="950" w:left="864" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:cols w:num="2" w:space="360"/>'
        '</w:sectPr>'
    )
    for child in parse_xml(s2_xml):
        final_sect.append(child)

    out_docx = "icdees_v6_humanized.docx"
    doc.save(out_docx)
    print(f"Successfully generated {out_docx}!")
    return out_docx

def convert_to_doc(docx_path, doc_path):
    print(f"Converting {docx_path} to {doc_path} via Word COM...")
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        in_abs = os.path.abspath(docx_path)
        out_abs = os.path.abspath(doc_path)
        if os.path.exists(out_abs):
            try:
                os.remove(out_abs)
            except Exception:
                pass
        wdoc = word.Documents.Open(FileName=in_abs, ConfirmConversions=False, ReadOnly=False, AddToRecentFiles=False)
        # FileFormat 0 = wdFormatDocument (Word 97-2003 .doc)
        wdoc.SaveAs2(FileName=out_abs, FileFormat=0)
        wdoc.Close(False)
        print(f"Successfully converted to {doc_path}! File size: {os.path.getsize(out_abs)} bytes")
    finally:
        word.Quit()

if __name__ == "__main__":
    docx_file = build_manuscript()
    doc_file = "icdees_v6_humanized.doc"
    convert_to_doc(docx_file, doc_file)
    print("BUILD COMPLETED SUCCESSFULLY!")
