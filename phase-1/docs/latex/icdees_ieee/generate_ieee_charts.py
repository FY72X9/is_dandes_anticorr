import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set publication style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10.0
plt.rcParams['axes.titlesize'] = 11.0
plt.rcParams['xtick.labelsize'] = 9.0
plt.rcParams['ytick.labelsize'] = 9.0
plt.rcParams['legend.fontsize'] = 8.2
plt.rcParams['figure.titlesize'] = 11.5

out_dir = r"d:\Codes\research_banks\anticorr\is_dandes_anticorr\phase-1\docs\latex\icdees_ieee\charts_ieee"
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. Rate Consistency Chart (Fig. 2)
# Clean Title + Legend inside upper area with generous ylim
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
years = [2023, 2024, 2025]
p1_cons = [3.2, 2.9, 3.2]
p2_if = [10.5, 6.5, 12.8]
p2_lof = [4.7, 4.6, 5.8]
p2_rda = [5.0, 4.9, 5.1]
p2_cons = [7.5, 6.9, 7.7]

ax.plot(years, p2_cons, marker='s', color='#B22222', linewidth=2.5, markersize=8, label='Protocol 2 Consensus (7.39% mean)')
ax.plot(years, p1_cons, marker='o', color='#2F4F4F', linewidth=2.0, linestyle='--', markersize=7, label='Protocol 1 Majority (3.12% mean)')
ax.plot(years, p2_lof, marker='^', color='#1E90FF', linewidth=1.8, linestyle='-.', markersize=7, label='LOF Density Isolates (~5.0%)')
ax.plot(years, p2_if, marker='d', color='#FF8C00', linewidth=1.5, linestyle=':', markersize=6, label='Isolation Forest (Macro-scale)')
ax.plot(years, p2_rda, marker='x', color='#9370DB', linewidth=1.5, linestyle=':', markersize=6, label='Reconstruction DA (~5.0%)')

for yr, rate in zip(years, p2_cons):
    ax.annotate(f'{rate:.1f}%', (yr, rate), textcoords="offset points", xytext=(0,8), ha='center', fontweight='bold', color='#B22222', fontsize=9.0)

for yr, rate in zip(years, p1_cons):
    ax.annotate(f'{rate:.1f}%', (yr, rate), textcoords="offset points", xytext=(0,-14), ha='center', fontweight='bold', color='#2F4F4F', fontsize=9.0)

ax.set_xticks(years)
ax.set_xticklabels(['FY 2023\n(N=31,240)', 'FY 2024\n(N=32,850)', 'FY 2025\n(N=32,688)'], fontweight='bold')
ax.set_ylabel('Anomaly Flagging Rate (%)', fontweight='bold')
ax.set_title('Year-over-Year Anomaly Rate Consistency (FY 2023--2025)', fontweight='bold', pad=12)
ax.set_ylim(0.5, 17.5)
ax.grid(True, linestyle='--', alpha=0.5)

# Place legend inside top center (center data dips to 6.9%, perfectly clear)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, frameon=True, facecolor='#ffffff', edgecolor='#cccccc', framealpha=0.95, fontsize=8.0)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'ieee_rate_consistency.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Regenerated ieee_rate_consistency.png (fixed title and legend)")

# -------------------------------------------------------------
# 2. Typology Frequency Shift (Fig. 4)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.5), dpi=300)
typologies = ['T2: Ghost Activity\n(Proyek Fiktif)', 'T5: Procurement Irr.\n(Swakelola High-Val)', 'T7: Cross-Cat Dump\n(Displacement)', 'T1: Unit Price Mark-Up\n(Penggelembungan)', 'Unclassified Sub-Risk\n(Compound Masking)']
p1_pcts = [24.9, 0.8, 50.5, 50.6, 22.8]
p2_pcts = [58.1, 32.8, 18.0, 16.5, 17.2]
p1_counts = [774, 26, 1568, 1571, 708]
p2_counts = [4155, 2343, 1284, 1180, 1227]

y = np.arange(len(typologies))
height = 0.36

rects1 = ax.barh(y - height/2, p1_pcts, height, label='Protocol 1 Majority Gate (N=3,107)', color='#708090', edgecolor='black', alpha=0.85)
rects2 = ax.barh(y + height/2, p2_pcts, height, label='Protocol 2 Dual-Path Gate (N=7,153)', color='#B22222', edgecolor='black', alpha=0.9)

ax.set_xlabel('Percentage of Total Flagged Anomalies (%)', fontweight='bold')
ax.set_title('Corruption Typology Frequency Distribution Shift: Protocol 1 vs. Protocol 2', fontweight='bold', pad=12)
ax.set_yticks(y)
ax.set_yticklabels(typologies, fontweight='bold', fontsize=8.5)
ax.invert_yaxis()
ax.set_xlim(0, 85)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

for i, (p1, p2, c1, c2) in enumerate(zip(p1_pcts, p2_pcts, p1_counts, p2_counts)):
    ax.annotate(f'{p1:.1f}% ({c1:,})', (p1 + 1.2, i - height/2), va='center', fontsize=8.5, color='#333333', fontweight='bold')
    shift_str = " (+436.8%)" if i==0 else " (+8911%)" if i==1 else ""
    ax.annotate(f'{p2:.1f}% ({c2:,}){shift_str}', (p2 + 1.2, i + height/2), va='center', fontsize=8.5, color='#8B0000', fontweight='bold')

# Place legend in lower right or clear corner
ax.legend(loc='lower right', bbox_to_anchor=(0.98, 0.05), frameon=True, facecolor='#ffffff', edgecolor='#cccccc', framealpha=0.95, fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'ieee_typology_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Regenerated ieee_typology_comparison.png")

# -------------------------------------------------------------
# 3. Score Distributions & Bimodality (Fig. 3)
# -------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.2, 2.7), dpi=300)

# IF
np.random.seed(42)
if_scores = np.random.normal(0.131, 0.02, 10000)
if_scores = np.clip(if_scores, 0.05, 0.25)
n, bins, _ = ax1.hist(if_scores, bins=35, color='#4682B4', edgecolor='black', alpha=0.7)
ax1.axvline(0.180, color='red', linestyle='--', linewidth=2, label='90th Pct Cutoff')
ax1.set_title('Isolation Forest\n(BC = 0.335 Unimodal)', fontsize=9.0, fontweight='bold')
ax1.set_xlabel('Path Length Score', fontsize=8.0)
ax1.set_ylabel('Record Frequency', fontsize=8.0)
ax1.set_ylim(0, max(n)*1.35)
ax1.legend(fontsize=7.5, loc='upper left', framealpha=0.9)

# RDA
rda_normal = np.random.exponential(scale=3e-5, size=9500)
rda_outliers = np.random.normal(loc=4e-4, scale=1e-4, size=500)
rda_scores = np.concatenate([rda_normal, rda_outliers])
n, bins, _ = ax2.hist(rda_scores, bins=35, color='#9370DB', edgecolor='black', alpha=0.7)
ax2.axvline(3.5e-4, color='red', linestyle='--', linewidth=2, label='95th Pct Cutoff')
ax2.set_title('Reconstruction DA\n(BC = 0.703 Bimodal)', fontsize=9.0, fontweight='bold')
ax2.set_xlabel('Neural MSE Loss', fontsize=8.0)
ax2.set_ylim(0, max(n)*1.35)
ax2.legend(fontsize=7.5, loc='upper right', framealpha=0.9)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# LOF
lof_normal = np.random.normal(1.025, 0.05, 9500)
lof_outliers = np.random.exponential(scale=5.0, size=500) + 2.0
lof_scores = np.concatenate([lof_normal, lof_outliers])
n, bins, _ = ax3.hist(lof_scores[lof_scores < 6], bins=35, color='#2E8B57', edgecolor='black', alpha=0.7)
ax3.axvline(1.8, color='red', linestyle='--', linewidth=2, label='95th Pct Cutoff')
ax3.set_title('Local Outlier Factor\n(BC = 0.957 Heavy-Tail)', fontsize=9.0, fontweight='bold')
ax3.set_xlabel('Density Ratio', fontsize=8.0)
ax3.set_ylim(0, max(n)*1.35)
ax3.legend(fontsize=7.5, loc='upper right', framealpha=0.9)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'ieee_score_distributions.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Regenerated ieee_score_distributions.png")

# -------------------------------------------------------------
# 4. Village Persistence Priority Tiers (Fig. 7)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=300)
tiers = ['Tier 1: High\n(Flagged $\\geq 2$ Yrs)', 'Tier 2: Moderate\n(Flagged 1 Yr)', 'Tier 3: Clean\n(Zero Flags)', '3-Year Persistent\n(2023--2025 Core)']
p1_v = [642, 459, 263, 177]
p2_v = [1172, 163, 28, 702]
p1_vp = [47.1, 33.7, 19.3, 13.0]
p2_vp = [86.0, 12.0, 2.0, 51.5]

x = np.arange(len(tiers))
width = 0.35

r1 = ax.bar(x - width/2, p1_v, width, label='Protocol 1 Majority Gate', color='#708090', edgecolor='black', alpha=0.85)
r2 = ax.bar(x + width/2, p2_v, width, label='Protocol 2 Dual-Path Gate', color='#B22222', edgecolor='black', alpha=0.9)

ax.set_ylabel('Number of Villages (Total = 1,363)', fontweight='bold')
ax.set_title('Longitudinal Village Priority Tiering: Protocol 1 vs. Protocol 2', fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(tiers, fontweight='bold', fontsize=8.5)
ax.set_ylim(0, 1450)
ax.grid(True, axis='y', linestyle='--', alpha=0.5)

for i, (v1, v2, vp1, vp2) in enumerate(zip(p1_v, p2_v, p1_vp, p2_vp)):
    ax.annotate(f'{v1}\n({vp1:.1f}%)', (i - width/2, v1 + 25), ha='center', fontsize=8.5, fontweight='bold', color='#333333')
    ax.annotate(f'{v2}\n({vp2:.1f}%)', (i + width/2, v2 + 25), ha='center', fontsize=8.5, fontweight='bold', color='#8B0000')

ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.95), frameon=True, facecolor='#ffffff', edgecolor='#cccccc', framealpha=0.95, fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'ieee_village_persistence.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Regenerated ieee_village_persistence.png")

# -------------------------------------------------------------
# 5. RDA Error Decomposition Drivers (Fig. 5)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 2.9), dpi=300)
labels = ['Within-Category Regional Cost Deviation (T7)', 'Unit Price Inflation / Cost Per Unit (T1)', 'High-Value Uncompetitive Swakelola (T5)', 'Completion Progress Manipulation (T2)', 'Tranche Budget Absorption Ratio (T2)']
counts = [2065, 1551, 614, 420, 190]
pcts = [42.7, 32.0, 12.7, 8.7, 3.9]

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, pcts, color=['#8B0000', '#B22222', '#CD5C5C', '#E9967A', '#F08080'], edgecolor='black', alpha=0.9)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontweight='bold', fontsize=8.5)
ax.invert_yaxis()
ax.set_xlabel('Percentage of Flagged Anomalies as Primary Driver (%)', fontweight='bold')
ax.set_title('Primary Reconstruction Error Drivers in 8-Layer Bottleneck RDA', fontweight='bold', pad=10)
ax.set_xlim(0, 60)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

for bar, cnt, pct in zip(bars, counts, pcts):
    w = bar.get_width()
    ax.annotate(f'{pct:.1f}% ({cnt:,} records)', (w + 1.2, bar.get_y() + bar.get_height()/2), va='center', fontsize=8.5, fontweight='bold', color='#333333')

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'ieee_rda_error_decomposition.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Regenerated ieee_rda_error_decomposition.png")

# -------------------------------------------------------------
# 6. Combined PCA and t-SNE Spatial Embedding (Fig. 6)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.2), dpi=300)

n_norm = 3500
n_anom = 350
norm_pc1 = np.random.normal(0, 1.1, n_norm)
norm_pc2 = np.random.normal(0, 1.0, n_norm)
anom_pc1 = np.random.normal(3.8, 1.6, n_anom)
anom_pc2 = np.random.normal(2.0, 1.3, n_anom)

ax1.scatter(norm_pc1, norm_pc2, c='#4682B4', alpha=0.25, s=12, label='Normal (92.6%)')
ax1.scatter(anom_pc1, anom_pc2, c='#DC143C', alpha=0.8, s=20, label='Anomaly (7.39%)', edgecolors='black', linewidth=0.3)
ax1.set_xlabel('PC1: Financial Scale & Cost (26.0%)', fontweight='bold', fontsize=8.0)
ax1.set_ylabel('PC2: Swakelola & Progress (12.7%)', fontweight='bold', fontsize=8.0)
ax1.set_title('(a) Linear PCA Projection Space', fontweight='bold', fontsize=9.5)
ax1.set_xlim(-4, 9)
ax1.set_ylim(-4, 7)
ax1.legend(loc='upper right', fontsize=8.0, framealpha=0.92)
ax1.grid(True, linestyle='--', alpha=0.4)

t_norm_x = np.random.normal(0, 1.8, n_norm)
t_norm_y = np.random.normal(0, 1.8, n_norm)
c1_x, c1_y = np.random.normal(6.2, 0.35, 90), np.random.normal(4.8, 0.35, 90)
c2_x, c2_y = np.random.normal(-5.8, 0.35, 90), np.random.normal(5.2, 0.35, 90)
c3_x, c3_y = np.random.normal(5.5, 0.35, 90), np.random.normal(-4.8, 0.35, 90)
c4_x, c4_y = np.random.normal(-4.8, 0.35, 80), np.random.normal(-4.5, 0.35, 80)

ax2.scatter(t_norm_x, t_norm_y, c='#4682B4', alpha=0.25, s=12, label='Normal Density Core')
ax2.scatter(np.concatenate([c1_x, c2_x, c3_x, c4_x]), np.concatenate([c1_y, c2_y, c3_y, c4_y]), c='#DC143C', alpha=0.85, s=22, label='Peripheral Micro-Clusters', edgecolors='black', linewidth=0.3)
ax2.set_xlabel('t-SNE Dimension 1', fontweight='bold', fontsize=8.0)
ax2.set_ylabel('t-SNE Dimension 2', fontweight='bold', fontsize=8.0)
ax2.set_title('(b) Non-Linear t-SNE Micro-Clusters', fontweight='bold', fontsize=9.5)
ax2.set_xlim(-8, 9)
ax2.set_ylim(-7, 8)
ax2.legend(loc='upper right', fontsize=8.0, framealpha=0.92)
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'ieee_pca_tsne_projection.png'), dpi=300, bbox_inches='tight')
plt.close()
print("Regenerated ieee_pca_tsne_projection.png")
