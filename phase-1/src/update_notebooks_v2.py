import json
import os

def update_notebook_1():
    path = "phase-1/src/01_data_preprocessing.ipynb"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Update Cell 9: add OHE encoding
    cell9 = nb["cells"][8]["source"]
    updated_cell9 = []
    for line in cell9:
        if 'df["activity_category"] = (df["Kode_Output"] // 1000).astype(int)' in line:
            updated_cell9.append('    # 8. activity_category — OHE nominal category (v2.0)\n')
            updated_cell9.append('    df["activity_category"] = (df["Kode_Output"] // 1000).astype(str)\n')
        else:
            updated_cell9.append(line)
    nb["cells"][8]["source"] = updated_cell9

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] Notebook 01 updated successfully.")

def update_notebook_2():
    path = "phase-1/src/02_unsupervised_comparison.ipynb"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Find and update consensus cell in NB02
    for idx, cell in enumerate(nb["cells"]):
        src = "".join(cell.get("source", []))
        if "consensus_flag" in src and 'df["consensus_flag"]' in src:
            print(f"Updating consensus logic in Notebook 02 Cell {idx}...")
            cell["source"] = [
                "# ── Cell Consensus: Dual-Path Consensus Framework (v2.0) ───────────────\n",
                "# Path 1: Local Anomaly Signal (LOF)\n",
                "path_local = df['lof_flag'] == 1\n",
                "\n",
                "# Path 2: Global Anomaly Convergence (IF AND DA Convergence)\n",
                "path_global = (df['if_flag'] == 1) & (df['da_flag'] == 1)\n",
                "\n",
                "# Final Consensus Flag v2\n",
                "df['consensus_flag'] = (path_local | path_global).astype(int)\n",
                "\n",
                "print(f'Total Dual-Path Consensus Flagged: {df[\"consensus_flag\"].sum():,} ({df[\"consensus_flag\"].mean()*100:.2f}%)')\n"
            ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] Notebook 02 updated successfully.")

def update_notebook_3():
    path = "phase-1/src/03_corruption_typology_analysis.ipynb"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for idx, cell in enumerate(nb["cells"]):
        src = "".join(cell.get("source", []))
        if "def assign_typologies(" in src:
            print(f"Updating assign_typologies in Notebook 03 Cell {idx}...")
            cell["source"] = [
                "# ── Cell 5: Typology mapping (rule-based on flagged records — v2.0) ─────\n",
                "flagged = df_flags[df_flags['consensus_flag'] == 1].copy()\n",
                "\n",
                "_thresholds = {\n",
                "    'cpu_p75': df_flags['cost_per_unit'].quantile(0.75),\n",
                "    'cpu_p90': df_flags['cost_per_unit'].quantile(0.90),\n",
                "}\n",
                "if 'cost_deviation_by_category' in df_flags.columns:\n",
                "    _thresholds['cdev_p80'] = df_flags['cost_deviation_by_category'].quantile(0.80)\n",
                "    _thresholds['cdev_p95'] = df_flags['cost_deviation_by_category'].quantile(0.95)\n",
                "else:\n",
                "    _thresholds['cdev_p80'], _thresholds['cdev_p95'] = None, None\n",
                "\n",
                "if 'absorption_ratio' in df_flags.columns:\n",
                "    _thresholds['abs_low'] = df_flags['absorption_ratio'].quantile(0.05)\n",
                "    _thresholds['abs_high'] = df_flags['absorption_ratio'].quantile(0.97)\n",
                "    _thresholds['abs_p90'] = df_flags['absorption_ratio'].quantile(0.90)\n",
                "else:\n",
                "    _thresholds['abs_low'], _thresholds['abs_high'], _thresholds['abs_p90'] = None, None, None\n",
                "\n",
                "def assign_typologies_v2(row):\n",
                "    labels = []\n",
                "    cpu = row.get('cost_per_unit', 0)\n",
                "    cdev = row.get('cost_deviation_by_category', 0)\n",
                "    abs_r = row.get('absorption_ratio', 0)\n",
                "    avg_comp = row.get('avg_completion', 0)\n",
                "    swakelola_high = row.get('swakelola_high_value', 0)\n",
                "    nsa = row.get('n_stages_active', 0)\n",
                "    \n",
                "    # T1 — Mark-up / Price Inflation\n",
                "    if cpu > 3 and cdev > 2:\n",
                "        labels.append('T1_Markup')\n",
                "        \n",
                "    # T2 — Ghost / Fictitious Activity\n",
                "    if abs_r < 0.05 and avg_comp < 0.10:\n",
                "        labels.append('T2_Ghost')\n",
                "        \n",
                "    # T3 — Volume Padding (Budget Exhaustion / Near-Full Absorption)\n",
                "    if abs_r >= 0.98:\n",
                "        labels.append('T3_VolumePadding')\n",
                "        \n",
                "    # T4 — Stage Lock (Front-loaded tranche concentration)\n",
                "    reals = [row.get('Real_T1', 0), row.get('Real_T2', 0), row.get('Real_T3', 0)]\n",
                "    tot_real = row.get('total_realization', 0)\n",
                "    stage_conc = max(reals) / tot_real if tot_real > 0 else 0\n",
                "    if stage_conc > 0.95 and nsa >= 2:\n",
                "        labels.append('T4_StageLock')\n",
                "        \n",
                "    # T5 — Procurement Irregularity\n",
                "    if swakelola_high == 1 and cpu > 0:\n",
                "        labels.append('T5_ProcurementIrregularity')\n",
                "        \n",
                "    # T6 — Budget Exhaustion\n",
                "    if abs_r > 0.98 and avg_comp < 0.50:\n",
                "        labels.append('T6_BudgetExhaustion')\n",
                "        \n",
                "    # T7 — Cross-Category Dump\n",
                "    if abs(cdev) > 3:\n",
                "        labels.append('T7_CrossCatDump')\n",
                "        \n",
                "    return labels if labels else ['Unclassified']\n",
                "\n",
                "flagged['typologies'] = flagged.apply(assign_typologies_v2, axis=1)\n",
                "flagged['typology_primary'] = flagged['typologies'].apply(lambda x: x[0])\n",
                "flagged['typology_count'] = flagged['typologies'].apply(len)\n",
                "print('[OK] Reconciled typologies v2 applied successfully.')\n"
            ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("[OK] Notebook 03 updated successfully.")

if __name__ == "__main__":
    update_notebook_1()
    update_notebook_2()
    update_notebook_3()
