# Converted from 02_unsupervised_comparison.ipynb

'''
# Notebook 02 — Unsupervised Anomaly Detection & Comparative Evaluation
## Corruption Indication Detection in Village Fund Activities — Jambi Province 2023–2025

**Input**: `features_engineered.csv` (output of Notebook 01)  
**Stage**: IQR Baseline → Isolation Forest → LOF → Robust Deep Autoencoder → Comparative Evaluation

### Pipeline
```
features_engineered.csv
        ↓
  IQR Rule-Based Baseline (cost_per_unit + absorption_ratio)
        ↓
  ┌─────────────────────────────────────────────┐
  │  Method 1: Isolation Forest (IF)            │
  │  Method 2: Local Outlier Factor (LOF)       │
  │  Method 3: Robust Deep Autoencoder (RDA)    │
  └─────────────────────────────────────────────┘
        ↓
  Evaluation:
    · IQR vs ML overlap
    · Anomaly rate consistency (per year)
    · Score distribution shape (bimodality)
    · Inter-method Cohen's κ
    · Village anomaly persistence score
        ↓
  Export → anomaly_flags.csv + scores_all_methods.csv
```

> **Environment**: Google Colab. Upload `features_engineered.csv` to `/content/output/` before running.
'''

from google.colab import drive
drive.mount('/content/drive')


# ── Cell 2: Install & Import ───────────────────────────────────────────────
# !pip install -q tensorflow scikit-learn scipy tqdm  # uncomment on fresh Colab

import pandas as pd
import numpy as np
import warnings
import os
import json
import gc
import joblib
import logging
import time

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import cohen_kappa_score
from scipy.stats import ks_2samp

import matplotlib.pyplot as plt
import seaborn as sns

# TensorFlow / Keras for Robust Deep Autoencoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Progress bars (auto-detects Jupyter vs terminal)
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")
pd.set_option("display.float_format", "{:.4f}".format)
tf.random.set_seed(42)
np.random.seed(42)

print(f"TensorFlow version : {tf.__version__}")
print(f"joblib version     : {joblib.__version__}")
print("Libraries loaded ✓")


# ── Cell 3: Paths, logging, and load preprocessed features ────────────────

OUTPUT_DIR = "/content/drive/MyDrive/Colab_Notebooks/data_dandes/v3-run"   # same as Notebook 01 output
MODEL_DIR  = f"{OUTPUT_DIR}/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# ── Logging setup ──────────────────────────────────────────────────────────
LOG_FILE = f"{MODEL_DIR}/training.log"

logger = logging.getLogger("anomaly_detection")
logger.setLevel(logging.INFO)
if logger.handlers:
    logger.handlers.clear()

_fh  = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
_fh.setLevel(logging.INFO)
_sh  = logging.StreamHandler()          # prints to notebook output cell
_sh.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
_fh.setFormatter(_fmt)
_sh.setFormatter(_fmt)
logger.addHandler(_fh)
logger.addHandler(_sh)

logger.info(f"=== Notebook 02 started  |  OUTPUT_DIR={OUTPUT_DIR}  MODEL_DIR={MODEL_DIR} ===")
logger.info(f"Log file: {LOG_FILE}")


# ── Utility helpers (defined here so they are available to all model cells) ─

class NumpyEncoder(json.JSONEncoder):
    """Serialise numpy scalars → Python native types so json.dump never raises TypeError."""
    def default(self, obj):
        if isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.integer, np.int16, np.int32, np.int64)):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def safe_json_load(path):
    """
    Load a JSON cache file. If the file is corrupt (truncated / partial write),
    delete it and return None so the calling cell falls through to re-train.
    """
    try:
        with open(path, encoding="utf-8") as _f:
            return json.load(_f)
    except (json.JSONDecodeError, ValueError) as _e:
        print(f"⚠  Corrupt cache deleted — will re-train: {path}  ({_e})")
        try:
            os.remove(path)
        except OSError:
            pass
        return None


# ── Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv(f"{OUTPUT_DIR}/features_engineered.csv")
logger.info(f"Loaded features_engineered.csv: {df.shape[0]:,} rows × {df.shape[1]} cols")

# Identify feature columns vs metadata columns
META_COLS = [
    "No", "Kode_Provinsi", "Kode_Lokasi", "Kabupaten_Kota",
    "Kode_Desa", "Nama_Desa", "Tahun",
    "Kode_Output", "Uraian_Output", "Volume", "Satuan",
    "Cara_Pengadaan", "Keterangan",
    "Real_T1", "Real_T2", "Real_T3", "Pct_T1", "Pct_T2", "Pct_T3",
    "Pagu", "total_realization", "n_stages_active",
]
meta_available = [c for c in META_COLS if c in df.columns]
FEATURE_COLS   = [c for c in df.columns if c not in meta_available]

logger.info(f"Feature columns ({len(FEATURE_COLS)}): {FEATURE_COLS}")
logger.info(f"Metadata columns: {len(meta_available)}")

X = df[FEATURE_COLS].values
print(f"\nFeature matrix shape: {X.shape}")
print(f"Feature columns ({len(FEATURE_COLS)}): {FEATURE_COLS}")
print(f"Metadata columns ({len(meta_available)}): {meta_available}")


'''
## Step 1 — IQR Rule-Based Baseline

Flag records outside **Q1 − 1.5×IQR** / **Q3 + 1.5×IQR** on two primary corruption-signal features:  
- `cost_per_unit` — mark-up signal  
- `absorption_ratio` — fictitious project signal  

The union of both flags constitutes the IQR anomaly label. This baseline answers: **does ML add detection value beyond simple statistical screening?**
'''

# ── Cell 5: IQR Baseline ──────────────────────────────────────────────────

def iqr_flag(series):
    """Return boolean Series: True = outside IQR fence."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)

# Both columns may be absent if VIF screening dropped them in Notebook 01.
# Fallback: skip the missing column and union only the available ones.
if "cost_per_unit" not in df.columns:
    raise KeyError("cost_per_unit not found — check features_engineered.csv / FEATURE_COLS")

cpu_col = "cost_per_unit"
flag_cpu = iqr_flag(df[cpu_col])
print(f"IQR flagged (cost_per_unit):    {flag_cpu.sum():,}  ({flag_cpu.mean()*100:.1f}%)")

if "absorption_ratio" in df.columns:
    ar_col   = "absorption_ratio"
    flag_ar  = iqr_flag(df[ar_col])
    print(f"IQR flagged (absorption_ratio): {flag_ar.sum():,}  ({flag_ar.mean()*100:.1f}%)")
    combined_flag = flag_cpu | flag_ar
else:
    print("⚠  absorption_ratio not in features (dropped by VIF) — IQR baseline uses cost_per_unit only")
    combined_flag = flag_cpu

df["iqr_flag"] = combined_flag.astype(int)

iqr_count = df["iqr_flag"].sum()
iqr_rate  = iqr_count / len(df) * 100

print(f"IQR flagged (union):            {iqr_count:,}  ({iqr_rate:.1f}%)")

# Per-year IQR rate
print("\nIQR anomaly rate per year:")
print(df.groupby("Tahun")["iqr_flag"].mean().mul(100).round(2).to_string())


'''
## Step 2 — Method 1: Isolation Forest (IF)

Contamination swept over `[0.03, 0.05, 0.08, 0.10, 0.15]`.  
Final value selected via **bimodality coefficient** of the resulting anomaly score distribution — the contamination that produces the sharpest bimodal separation is preferred over anchoring to the national ICW statistic.
'''

# ── Cell 7: Isolation Forest (with model caching) ─────────────────────────

def bimodality_coefficient(scores):
    """Sarle's BC = (skew² + 1) / (kurtosis + 3).  BC > 0.555 → bimodal."""
    from scipy.stats import skew, kurtosis
    s  = skew(scores)
    k  = kurtosis(scores)   # excess kurtosis
    n  = len(scores)
    skew_adj = s * np.sqrt(n * (n - 1)) / (n - 2)
    kurt_adj = k + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))
    return (skew_adj ** 2 + 1) / (kurt_adj + 3)


IF_MODEL_PATH  = os.path.join(MODEL_DIR, "if_model.joblib")
IF_PARAMS_PATH = os.path.join(MODEL_DIR, "if_params.json")

_if_params = safe_json_load(IF_PARAMS_PATH) if os.path.exists(IF_PARAMS_PATH) else None

if os.path.exists(IF_MODEL_PATH) and _if_params is not None:
    # ── Load cached ────────────────────────────────────────────────────────
    logger.info("IF: Loading cached model from disk …")
    t0 = time.time()
    if_model = joblib.load(IF_MODEL_PATH)
    best_contamination = _if_params["best_contamination"]
    bc_results = {float(k): v for k, v in _if_params["bc_results"].items()}
    logger.info(f"IF: Loaded in {time.time()-t0:.1f}s  |  best_contamination={best_contamination}  "
                f"BC={bc_results[best_contamination]:.4f}")
else:
    # ── Train: contamination sweep ─────────────────────────────────────────
    CONTAMINATION_GRID = [0.03, 0.05, 0.08, 0.10, 0.15]
    bc_results = {}
    logger.info(f"IF: Starting contamination sweep {CONTAMINATION_GRID} …")
    t_start = time.time()

    for c in tqdm(CONTAMINATION_GRID, desc="IF — contamination sweep", unit="run"):
        clf  = IsolationForest(n_estimators=200, contamination=c, random_state=42, n_jobs=-1)
        clf.fit(X)
        bc   = bimodality_coefficient(clf.decision_function(X))
        bc_results[c] = bc
        logger.info(f"  contamination={c:.2f}  BC={bc:.4f}  flagged≈{int(c*len(X)):,}")

    best_contamination = max(bc_results, key=bc_results.get)
    logger.info(f"IF: Best contamination={best_contamination}  BC={bc_results[best_contamination]:.4f}  "
                f"(sweep elapsed {time.time()-t_start:.1f}s)")

    # ── Final model ────────────────────────────────────────────────────────
    logger.info(f"IF: Training final model …")
    t0       = time.time()
    if_model = IsolationForest(
        n_estimators=200, contamination=best_contamination, random_state=42, n_jobs=-1
    )
    if_model.fit(X)
    logger.info(f"IF: Final model trained in {time.time()-t0:.1f}s")

    # ── Save ───────────────────────────────────────────────────────────────
    joblib.dump(if_model, IF_MODEL_PATH)
    with open(IF_PARAMS_PATH, "w", encoding="utf-8") as _f:
        json.dump({"best_contamination": best_contamination,
                   "bc_results": {str(k): v for k, v in bc_results.items()}},
                  _f, indent=2, cls=NumpyEncoder)
    logger.info(f"IF: Saved → {IF_MODEL_PATH}")

# ── Score ──────────────────────────────────────────────────────────────────
df["if_score"] = if_model.decision_function(X)
df["if_flag"]  = (if_model.predict(X) == -1).astype(int)

print("\nContamination sweep results:")
for c, bc in bc_results.items():
    marker = "  ◀ best" if c == best_contamination else ""
    print(f"  contamination={c:.2f}  BC={bc:.4f}  flagged≈{int(c*len(X)):,}{marker}")
print(f"\nIF anomaly flags : {df['if_flag'].sum():,}  ({df['if_flag'].mean()*100:.1f}%)")
print("Per-year IF anomaly rate:")
print(df.groupby("Tahun")["if_flag"].mean().mul(100).round(2).to_string())


'''
## Step 3 — Method 2: Local Outlier Factor (LOF)

`n_neighbors` swept over `[10, 15, 20, 30]`.  
Selection criterion: LOF score distribution with most stable bimodality coefficient across the 3-year pooled dataset.  
Anomaly threshold: records at **≥ 95th percentile** of LOF score distribution.
'''

# ── Cell 9: LOF (with model caching) ──────────────────────────────────────

LOF_MODEL_PATH  = os.path.join(MODEL_DIR, "lof_model.joblib")
LOF_PARAMS_PATH = os.path.join(MODEL_DIR, "lof_params.json")

_lof_params = safe_json_load(LOF_PARAMS_PATH) if os.path.exists(LOF_PARAMS_PATH) else None

if os.path.exists(LOF_MODEL_PATH) and _lof_params is not None:
    # ── Load cached ────────────────────────────────────────────────────────
    logger.info("LOF: Loading cached model from disk …")
    t0 = time.time()
    lof_final = joblib.load(LOF_MODEL_PATH)
    best_k         = _lof_params["best_k"]
    lof_bc_results = {int(k): v for k, v in _lof_params["bc_results"].items()}
    LOF_THRESHOLD  = _lof_params["lof_threshold"]
    logger.info(f"LOF: Loaded in {time.time()-t0:.1f}s  |  best_k={best_k}  "
                f"threshold(95th)={LOF_THRESHOLD:.4f}")
else:
    # ── Train: k sweep ─────────────────────────────────────────────────────
    K_GRID         = [10, 15, 20, 30]
    lof_bc_results = {}
    logger.info(f"LOF: Starting k sweep {K_GRID} …")
    t_start = time.time()

    for k in tqdm(K_GRID, desc="LOF — k sweep", unit="run"):
        lof        = LocalOutlierFactor(n_neighbors=k, novelty=False, n_jobs=-1)
        lof.fit(X)
        lof_scores = -lof.negative_outlier_factor_
        bc         = bimodality_coefficient(lof_scores)
        lof_bc_results[k] = bc
        flagged    = (lof_scores >= np.percentile(lof_scores, 95)).sum()
        logger.info(f"  k={k:2d}  BC={bc:.4f}  flagged@95th={flagged:,}  mean={lof_scores.mean():.3f}")

    best_k = max(lof_bc_results, key=lof_bc_results.get)
    logger.info(f"LOF: Best k={best_k}  BC={lof_bc_results[best_k]:.4f}  "
                f"(sweep elapsed {time.time()-t_start:.1f}s)")

    # ── Final model ────────────────────────────────────────────────────────
    logger.info(f"LOF: Training final model (k={best_k}) …")
    t0        = time.time()
    lof_final = LocalOutlierFactor(n_neighbors=best_k, novelty=False, n_jobs=-1)
    lof_final.fit(X)
    LOF_THRESHOLD = float(np.percentile(-lof_final.negative_outlier_factor_, 95))
    logger.info(f"LOF: Final model in {time.time()-t0:.1f}s  |  threshold(95th)={LOF_THRESHOLD:.4f}")

    # ── Save ───────────────────────────────────────────────────────────────
    joblib.dump(lof_final, LOF_MODEL_PATH)
    with open(LOF_PARAMS_PATH, "w", encoding="utf-8") as _f:
        json.dump({"best_k": best_k,
                   "lof_threshold": LOF_THRESHOLD,
                   "bc_results": {str(k): v for k, v in lof_bc_results.items()}},
                  _f, indent=2, cls=NumpyEncoder)
    logger.info(f"LOF: Saved → {LOF_MODEL_PATH}")

# ── Score ──────────────────────────────────────────────────────────────────
lof_scores_final = -lof_final.negative_outlier_factor_
df["lof_score"]  = lof_scores_final
df["lof_flag"]   = (lof_scores_final >= LOF_THRESHOLD).astype(int)

print("\nk sweep results:")
for k, bc in lof_bc_results.items():
    marker = "  ◀ best" if k == best_k else ""
    print(f"  k={k:2d}  BC={bc:.4f}{marker}")
print(f"\nLOF threshold (95th pct): {LOF_THRESHOLD:.4f}")
print(f"LOF anomaly flags       : {df['lof_flag'].sum():,}  ({df['lof_flag'].mean()*100:.1f}%)")
print("Per-year LOF anomaly rate:")
print(df.groupby("Tahun")["lof_flag"].mean().mul(100).round(2).to_string())


'''
## Step 4 — Method 3: Robust Deep Autoencoder (RDA)

**Architecture** (per research concept Section 8.4):  
`Input → Dense(64,ReLU) → Dense(32,ReLU) → Dense(16,ReLU) → Dense(8,ReLU) [bottleneck] → Dense(16,ReLU) → Dense(32,ReLU) → Dense(64,ReLU) → Dense(n_features, Linear)`

**Joint loss**:  `MSE(AE(X − S), (X − S)) + λ‖S‖₁`  
where **S** is the sparse noise matrix jointly optimised with the autoencoder.  
The L1 penalty absorbs anomalous training records into **S**, preventing them from corrupting the network's learned representation of normal expenditure patterns.

λ swept over `[1e-4, 1e-3, 1e-2]`, selected via validation reconstruction error.
'''

# ── Cell 11: Build RDA model & training function ──────────────────────────

def build_autoencoder(input_dim):
    """Autoencoder branch of the RDA (noise S handled externally)."""
    inp = keras.Input(shape=(input_dim,), name="input")
    x   = layers.Dense(64, activation="relu")(inp)
    x   = layers.Dense(32, activation="relu")(x)
    x   = layers.Dense(16, activation="relu")(x)
    x   = layers.Dense(8,  activation="relu", name="bottleneck")(x)
    x   = layers.Dense(16, activation="relu")(x)
    x   = layers.Dense(32, activation="relu")(x)
    x   = layers.Dense(64, activation="relu")(x)
    out = layers.Dense(input_dim, activation="linear", name="output")(x)
    return keras.Model(inp, out, name="autoencoder")


def train_rda(X_train, lambda_s, epochs=100, patience=10,
              val_split=0.1, batch_size=256, seed=42, desc="RDA"):
    """
    Memory-efficient Robust Deep Autoencoder for Google Colab T4.

    Key design choices vs. the naive implementation:
    - X and S stay as numpy arrays on CPU → only mini-batches are uploaded to GPU
      via tf.constant(), preventing OOM from a large tf.Variable(X) on-device.
    - S is updated outside the GradientTape via a proximal gradient step
      (soft-thresholding), which is the mathematically correct solver for the
      L1 term and avoids backprop through a full-dataset TF variable.
    - AE weights are updated independently with Adam on GPU as before.

    Loss = MSE(AE(X − S), (X − S)) + λ‖S‖₁
    Returns: (ae_model, S_final, history, best_val_loss)
    """
    tf.random.set_seed(seed)
    np.random.seed(seed)

    n, d    = X_train.shape
    X_np    = X_train.astype(np.float32)             # CPU — never moves to GPU as a whole
    S       = np.zeros_like(X_np, dtype=np.float32)  # CPU — updated via proximal step

    ae        = build_autoencoder(d)
    optimizer = keras.optimizers.Adam(learning_rate=1e-3)

    val_size  = max(1, int(n * val_split))
    idx_perm  = np.random.permutation(n)
    val_idx   = idx_perm[:val_size]
    train_idx = idx_perm[val_size:]

    best_val_loss    = np.inf
    best_weights     = ae.get_weights()
    best_S           = S.copy()
    patience_counter = 0
    history          = []
    lr_s             = 1e-3   # step-size for S proximal update

    pbar = tqdm(range(epochs), desc=f"{desc} (λ={lambda_s:.0e})",
                unit="ep", dynamic_ncols=True)
    for epoch in pbar:
        epoch_loss = 0.0
        n_batches  = 0
        np.random.shuffle(train_idx)

        for start in range(0, len(train_idx), batch_size):
            bidx = train_idx[start:start + batch_size]
            X_b  = tf.constant(X_np[bidx], dtype=tf.float32)   # mini-batch → GPU
            S_b  = tf.constant(S[bidx],    dtype=tf.float32)

            # ── AE gradient step (backprop on GPU, S treated as constant) ──
            with tf.GradientTape() as tape:
                Xc    = X_b - S_b
                Xr    = ae(Xc, training=True)
                mse_l = tf.reduce_mean(tf.square(Xr - Xc))
                l1_l  = lambda_s * tf.reduce_mean(tf.abs(S_b))
                loss  = mse_l + l1_l
            grads = tape.gradient(loss, ae.trainable_variables)
            optimizer.apply_gradients(zip(grads, ae.trainable_variables))

            # ── S proximal update (CPU, soft-thresholding for L1) ──────────
            # Gradient of MSE w.r.t. S (AE fixed): ∂MSE/∂S = -2*(Xc - Xr)
            Xc_np    = X_np[bidx] - S[bidx]
            Xr_np    = ae(tf.constant(Xc_np, dtype=tf.float32),
                          training=False).numpy()
            residual = Xc_np - Xr_np                         # reconstruction error
            grad_S   = -2.0 * residual                       # ∂MSE/∂S
            S_half   = S[bidx] - lr_s * grad_S               # gradient descent step
            S[bidx]  = np.sign(S_half) * np.maximum(         # soft-threshold (L1 prox)
                np.abs(S_half) - lambda_s * lr_s, 0.0
            )

            epoch_loss += loss.numpy()
            n_batches  += 1

        # ── Validation loss (CPU) ─────────────────────────────────────────
        Xvc      = X_np[val_idx] - S[val_idx]
        Xvr      = ae(tf.constant(Xvc, dtype=tf.float32), training=False).numpy()
        val_loss = float(np.mean((Xvr - Xvc) ** 2))
        history.append(val_loss)

        avg_train = epoch_loss / max(1, n_batches)
        pbar.set_postfix({"trn": f"{avg_train:.5f}",
                          "val": f"{val_loss:.5f}",
                          "best": f"{best_val_loss:.5f}",
                          "pat": patience_counter})

        if val_loss < best_val_loss:
            best_val_loss    = val_loss
            best_weights     = ae.get_weights()
            best_S           = S.copy()
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                pbar.set_description(f"{desc} — early stop @ep{epoch+1}")
                logger.info(f"  RDA early stop @ep{epoch+1}  best_val={best_val_loss:.6f}  λ={lambda_s}")
                break

    ae.set_weights(best_weights)
    logger.info(f"  RDA done: λ={lambda_s}  best_val={best_val_loss:.6f}  ep_run={epoch+1}")
    return ae, best_S, history, best_val_loss


# ── Cell 12: RDA λ sweep (with caching) ───────────────────────────────────

RDA_PARAMS_PATH = os.path.join(MODEL_DIR, "rda_params.json")

_rda_params = safe_json_load(RDA_PARAMS_PATH) if os.path.exists(RDA_PARAMS_PATH) else None

if _rda_params is not None:
    # ── Load cached best λ ─────────────────────────────────────────────────
    best_lambda       = _rda_params["best_lambda"]
    lambda_val_losses = {float(k): v for k, v in _rda_params["lambda_val_losses"].items()}
    logger.info(f"RDA: λ params loaded from cache — best_lambda={best_lambda}  "
                f"val_MSE={lambda_val_losses[best_lambda]:.6f}")
    print(f"λ sweep loaded from cache. Best λ: {best_lambda}  "
          f"(val MSE={lambda_val_losses[best_lambda]:.6f})")
else:
    LAMBDA_GRID       = [1e-4, 1e-3, 1e-2]
    lambda_val_losses = {}
    logger.info(f"RDA: Starting λ sweep {LAMBDA_GRID} …")

    for lam in tqdm(LAMBDA_GRID, desc="RDA — λ sweep", unit="λ"):
        logger.info(f"RDA sweep: λ={lam} …")
        _, _, _, val_loss = train_rda(
            X, lambda_s=lam, epochs=50, patience=8,
            desc=f"λ-sweep λ={lam:.0e}"
        )
        lambda_val_losses[lam] = float(val_loss)
        logger.info(f"  λ={lam:.1e}  best val MSE={val_loss:.6f}")

        # Free GPU memory between sweep runs to prevent OOM accumulation
        keras.backend.clear_session()
        gc.collect()
        tf.random.set_seed(42)
        np.random.seed(42)

    best_lambda = min(lambda_val_losses, key=lambda_val_losses.get)
    logger.info(f"RDA: Best λ={best_lambda}  val MSE={lambda_val_losses[best_lambda]:.6f}")

    with open(RDA_PARAMS_PATH, "w", encoding="utf-8") as _f:
        json.dump({"best_lambda": best_lambda,
                   "lambda_val_losses": {str(k): v
                                         for k, v in lambda_val_losses.items()}},
                  _f, indent=2, cls=NumpyEncoder)
    logger.info(f"RDA: λ params saved → {RDA_PARAMS_PATH}")

print("\n=== λ sweep results ===")
for lam, vloss in lambda_val_losses.items():
    marker = "  ◀ best" if lam == best_lambda else ""
    print(f"  λ={lam:.1e}  val MSE={vloss:.6f}{marker}")


# ── Cell 13: Final RDA training + anomaly scoring (with model caching) ────

RDA_MODEL_PATH  = os.path.join(MODEL_DIR, "rda_model.keras")    # Keras native format
RDA_S_PATH      = os.path.join(MODEL_DIR, "rda_S_final.npy")
RDA_THRESH_PATH = os.path.join(MODEL_DIR, "rda_thresholds.json")

_rda_thresh = safe_json_load(RDA_THRESH_PATH) if os.path.exists(RDA_THRESH_PATH) else None

if (os.path.exists(RDA_MODEL_PATH) and
        os.path.exists(RDA_S_PATH) and
        _rda_thresh is not None):
    # ── Load cached RDA model ──────────────────────────────────────────────
    logger.info("RDA: Loading cached model + S_final from disk …")
    t0        = time.time()
    rda_model = keras.models.load_model(RDA_MODEL_PATH)
    S_final   = np.load(RDA_S_PATH)
    RDA_THRESHOLD_95  = _rda_thresh["threshold_95"]
    RDA_THRESHOLD_975 = _rda_thresh["threshold_975"]
    logger.info(f"RDA: Model loaded in {time.time()-t0:.1f}s  |  "
                f"threshold_95={RDA_THRESHOLD_95:.6f}")
else:
    # ── Train final model ──────────────────────────────────────────────────
    logger.info(f"RDA: Training final model  λ={best_lambda}  epochs=100  patience=10 …")
    t0 = time.time()
    rda_model, S_final, rda_history, _ = train_rda(
        X, lambda_s=best_lambda, epochs=100, patience=10, desc="RDA final"
    )
    logger.info(f"RDA: Trained in {time.time()-t0:.1f}s")

    # Compute thresholds on full data before saving
    _Xc                = X - S_final
    _Xr                = rda_model.predict(
        tf.constant(_Xc, dtype=tf.float32), batch_size=512, verbose=0
    )
    _errs              = np.mean((_Xr - _Xc) ** 2, axis=1)
    RDA_THRESHOLD_95   = float(np.percentile(_errs, 95))
    RDA_THRESHOLD_975  = float(np.percentile(_errs, 97.5))

    # ── Save model + artefacts ─────────────────────────────────────────────
    rda_model.save(RDA_MODEL_PATH)
    np.save(RDA_S_PATH, S_final)
    with open(RDA_THRESH_PATH, "w", encoding="utf-8") as _f:
        json.dump({"threshold_95": RDA_THRESHOLD_95,
                   "threshold_975": RDA_THRESHOLD_975},
                  _f, indent=2, cls=NumpyEncoder)
    logger.info(f"RDA: Model saved  → {RDA_MODEL_PATH}")
    logger.info(f"RDA: S_final      → {RDA_S_PATH}")
    logger.info(f"RDA: Thresholds   → 95th={RDA_THRESHOLD_95:.6f}  97.5th={RDA_THRESHOLD_975:.6f}")

# ── Inference — chunked to avoid OOM on large datasets ────────────────────
logger.info("RDA: Running inference on full dataset …")
INFER_BATCH   = 512
X_clean_full  = (X - S_final).astype(np.float32)
n_rows        = X_clean_full.shape[0]
recon_chunks  = []
for start in range(0, n_rows, INFER_BATCH):
    chunk = tf.constant(X_clean_full[start:start + INFER_BATCH], dtype=tf.float32)
    recon_chunks.append(rda_model(chunk, training=False).numpy())
X_recon_full           = np.vstack(recon_chunks)
rda_errors_total       = np.mean((X_recon_full - X_clean_full) ** 2, axis=1)
rda_errors_per_feature = (X_recon_full - X_clean_full) ** 2

df["rda_score"] = rda_errors_total
df["rda_flag"]  = (rda_errors_total >= RDA_THRESHOLD_95).astype(int)

for i, feat in enumerate(FEATURE_COLS):
    df[f"rda_err_{feat}"] = rda_errors_per_feature[:, i]

df["rda_sparse_norm"] = np.linalg.norm(S_final, axis=1)

logger.info(f"RDA: Inference done  |  flagged={df['rda_flag'].sum():,}  "
            f"({df['rda_flag'].mean()*100:.1f}%)")

print(f"\nRDA threshold (95th pct)   : {RDA_THRESHOLD_95:.6f}")
print(f"RDA threshold (97.5th pct) : {RDA_THRESHOLD_975:.6f}")
print(f"RDA anomaly flags (@95th)  : {df['rda_flag'].sum():,}  ({df['rda_flag'].mean()*100:.1f}%)")
print("Per-year RDA anomaly rate:")
print(df.groupby("Tahun")["rda_flag"].mean().mul(100).round(2).to_string())


'''
## Step 5 — Comparative Evaluation

Metrics (per research concept Section 8.5):
1. **Anomaly rate consistency** — per-year breakdown across all methods
2. **Score distribution shape** — bimodality coefficient comparison
3. **Inter-method Cohen's κ** — agreement between IF, LOF, RDA flags
4. **IQR vs ML overlap** — proportion of IQR flags confirmed by each ML method
5. **Village anomaly persistence score** — cross-year flagging per `Kode_Desa`
'''

# ── Cell 15: Anomaly rate consistency per year ────────────────────────────

rate_table = df.groupby("Tahun")[["iqr_flag", "if_flag", "lof_flag", "rda_flag"]].mean().mul(100).round(2)
rate_table.columns = ["IQR Baseline (%)", "Isolation Forest (%)", "LOF (%)", "RDA (%)"]
print("=== Anomaly Rate Consistency (% flagged per year) ===")
print(rate_table.to_string())

# Overall rates
overall = df[["iqr_flag","if_flag","lof_flag","rda_flag"]].mean().mul(100).round(2)
overall.index = ["IQR Baseline", "Isolation Forest", "LOF", "RDA"]
print("\n=== Overall anomaly rates ===")
print(overall.to_string())

# Visualise
fig, ax = plt.subplots(figsize=(9, 4))
rate_table.T.plot(kind="bar", ax=ax, colormap="tab10", edgecolor="none")
ax.set_title("Anomaly Rate Consistency — Per Year Per Method", fontweight="bold")
ax.set_ylabel("% Records Flagged")
ax.set_xlabel("Method")
ax.legend(title="Year", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/anomaly_rate_consistency.png", dpi=150)
plt.show()


# ── Cell 16: Score distribution shape (bimodality) ───────────────────────

scores_dict = {
    "Isolation Forest\n(decision function)": df["if_score"],
    "LOF Score":                              df["lof_score"],
    "RDA Reconstruction\nError (MSE)":        df["rda_score"],
}

bc_summary = {}
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (label, scores) in zip(axes, scores_dict.items()):
    vals = scores.replace([np.inf, -np.inf], np.nan).dropna()
    p1, p99 = vals.quantile(0.01), vals.quantile(0.99)
    vals_clip = vals.clip(p1, p99)

    bc = bimodality_coefficient(vals_clip.values)
    bc_summary[label.split("\n")[0]] = bc

    ax.hist(vals_clip, bins=100, color="#2E75B6", alpha=0.8, edgecolor="none")
    ax.axvline(vals.median(), color="red",   linestyle="--", lw=1.5, label="Median")
    ax.axvline(vals.quantile(0.95), color="orange", linestyle="--", lw=1.5, label="95th pct")
    ax.set_title(f"{label}\n(BC = {bc:.3f})", fontsize=9, fontweight="bold")
    ax.set_xlabel("Score")
    ax.set_ylabel("Count")
    ax.legend(fontsize=7)

plt.suptitle("Score Distribution Shape — All Methods", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/score_distributions.png", dpi=150)
plt.show()

print("\n=== Bimodality Coefficients (BC > 0.555 = bimodal) ===")
for k, v in bc_summary.items():
    verdict = "✓ bimodal" if v > 0.555 else "✗ unimodal"
    print(f"  {k:35s}  BC = {v:.4f}  {verdict}")


# ── Cell Consensus: Dual-Path Consensus Framework (v2.0) ───────────────
# Path 1: Local Anomaly Signal (LOF)
path_local = df['lof_flag'] == 1

# Path 2: Global Anomaly Convergence (IF AND RDA Convergence)
# Fixed typo: changed 'da_flag' to 'rda_flag'
path_global = (df['if_flag'] == 1) & (df['rda_flag'] == 1)

# Final Consensus Flag v2
df['consensus_flag'] = (path_local | path_global).astype(int)

print(f'Total Dual-Path Consensus Flagged: {df["consensus_flag"].sum():,} ({df["consensus_flag"].mean()*100:.2f}%)')


# ── Cell 18: Kolmogorov-Smirnov test — flagged vs normal score distributions ──
# KS test validates that each method's anomaly scores are drawn from a
# statistically distinct distribution compared to normal records.
# H₀: flagged and normal scores come from the same distribution.
# Reject H₀ at α = 0.05 → method achieves meaningful score separation.

print("=== KS Test: Score Distribution Separation — Flagged vs Normal ===")
print("  H₀: flagged and normal scores from the same distribution")
print("  Reject H₀ at α=0.05 if p < 0.05 (separation statistically significant)\n")

ks_results = {}
ks_method_specs = [
    ("Isolation Forest", "if_score",  "if_flag"),
    ("LOF",              "lof_score", "lof_flag"),
    ("RDA",              "rda_score", "rda_flag"),
]

for method_name, score_col, flag_col in ks_method_specs:
    flagged_scores = (df.loc[df[flag_col] == 1, score_col]
                       .replace([np.inf, -np.inf], np.nan).dropna())
    normal_scores  = (df.loc[df[flag_col] == 0, score_col]
                       .replace([np.inf, -np.inf], np.nan).dropna())
    stat, pval     = ks_2samp(flagged_scores, normal_scores)

    ks_results[method_name] = {
        "KS statistic": round(stat, 4),
        "p-value"     : pval,
        "n_flagged"   : len(flagged_scores),
        "n_normal"    : len(normal_scores),
        "significant" : pval < 0.05,
    }
    verdict = "✓ significant separation" if pval < 0.05 else "✗ not significant"
    print(f"  {method_name:20s}  KS={stat:.4f}  p={pval:.2e}"
          f"  n_flagged={len(flagged_scores):,}  ({verdict})")

logger.info(f"KS test completed: { {k: {kk: round(vv,6) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in ks_results.items()} }")

print("\nInterpretation:")
print("  KS statistic → 1.0 : near-complete score distribution separation")
print("  p < 0.05            : method discriminates anomalies from normal records")
print("  For LOF the score direction is inverted (higher = more anomalous); KS still valid.")


'''
## 6. Village Anomaly Persistence Score

A village receives a **persistence score** = proportion of fiscal years (2023–2025) in which it has at least one consensus-flagged activity.  
Villages with persistence ≥ 2/3 years are classified as **Priority Tier 1**; persistence = 1/3 year → **Priority Tier 2**.
'''

# ── Cell 19: Village anomaly persistence score ───────────────────────────

# For each village-year, mark if ≥1 consensus-flagged record exists
village_year_flagged = (
    df.groupby(["Kode_Desa", "Tahun"])["consensus_flag"]
    .max()
    .reset_index()
    .rename(columns={"consensus_flag": "year_flagged"})
)

# Count distinct years available per village (some may be < 3 if absent from some years)
years_available = (
    df.groupby("Kode_Desa")["Tahun"]
    .nunique()
    .reset_index()
    .rename(columns={"Tahun": "n_years"})
)

# Sum flagged years then compute persistence
village_persistence = (
    village_year_flagged.groupby("Kode_Desa")["year_flagged"]
    .sum()
    .reset_index()
    .rename(columns={"year_flagged": "years_flagged"})
    .merge(years_available, on="Kode_Desa")
)
village_persistence["persistence_score"] = (
    village_persistence["years_flagged"] / village_persistence["n_years"]
).round(4)

# Assign priority tier
def assign_tier(row):
    if row["persistence_score"] >= 2 / 3:
        return "Tier 1 – High Priority"
    elif row["persistence_score"] > 0:
        return "Tier 2 – Moderate"
    else:
        return "Tier 3 – Not Flagged"

village_persistence["priority_tier"] = village_persistence.apply(assign_tier, axis=1)

# Attach village name if available in df
if "Nama_Desa" in df.columns:
    name_map = df.drop_duplicates("Kode_Desa")[["Kode_Desa", "Nama_Desa"]]
    village_persistence = village_persistence.merge(name_map, on="Kode_Desa", how="left")

village_persistence.sort_values("persistence_score", ascending=False, inplace=True)
village_persistence.reset_index(drop=True, inplace=True)

print("=== Village Anomaly Persistence Summary ===")
print(village_persistence["priority_tier"].value_counts().to_string())
print(f"\nTop-20 highest persistence villages:")
top_cols = [c for c in ["Kode_Desa","Nama_Desa","years_flagged","n_years","persistence_score","priority_tier"] if c in village_persistence.columns]
print(village_persistence.head(20)[top_cols].to_string(index=False))

# Bar chart — distribution of persistence scores
fig, ax = plt.subplots(figsize=(8, 4))
tier_counts = village_persistence["priority_tier"].value_counts().sort_index()
bars = ax.bar(tier_counts.index, tier_counts.values, color=["#d62728", "#ff7f0e", "#2ca02c"])
for bar, v in zip(bars, tier_counts.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(v), ha="center", fontsize=10)
ax.set_title("Village Priority Tiers (Anomaly Persistence Score)", fontsize=12)
ax.set_ylabel("Number of Villages")
ax.tick_params(axis="x", labelsize=9)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/village_persistence_tiers.png", dpi=150)
plt.show()
print("Saved: village_persistence_tiers.png")


'''
## 7. Export Results

Three artefacts are exported:
| File | Contents |
|---|---|
| `anomaly_flags.csv` | Full record-level dataframe with all scores, flags, and persistence metadata |
| `scores_all_methods.csv` | Identifier columns + all four score columns (compact version for plotting) |
| `village_persistence.csv` | Village-level priority tier table |
'''

# ── Cell 21: Export anomaly_flags.csv + scores_all_methods.csv ────────────

# ── 1. Merge persistence score back into main df ──────────────────────────
persist_lookup = village_persistence[["Kode_Desa", "persistence_score", "priority_tier", "years_flagged"]]
df = df.merge(persist_lookup, on="Kode_Desa", how="left")
df["persistence_score"] = df["persistence_score"].fillna(0.0)
df["priority_tier"]     = df["priority_tier"].fillna("Tier 3 – Not Flagged")
df["years_flagged"]     = df["years_flagged"].fillna(0).astype(int)

# ── 2. Full record-level export ───────────────────────────────────────────
out_flags = f"{OUTPUT_DIR}/anomaly_flags.csv"
df.to_csv(out_flags, index=False)
logger.info(f"Exported anomaly_flags.csv  ({df.shape[0]:,} rows × {df.shape[1]} cols)")
print(f"Saved: {out_flags}  ({df.shape[0]:,} rows × {df.shape[1]} cols)")

# ── 3. Compact scores export ──────────────────────────────────────────────
id_cols   = ["Kode_Desa", "Tahun"]
if "Nama_Desa" in df.columns:
    id_cols.insert(1, "Nama_Desa")
score_cols = ["iqr_flag", "if_score", "if_flag", "lof_score", "lof_flag",
              "rda_score", "rda_flag", "consensus_flag",
              "persistence_score", "priority_tier"]
scores_df  = df[id_cols + score_cols].copy()
out_scores = f"{OUTPUT_DIR}/scores_all_methods.csv"
scores_df.to_csv(out_scores, index=False)
logger.info(f"Exported scores_all_methods.csv  ({scores_df.shape[0]:,} rows × {scores_df.shape[1]} cols)")
print(f"Saved: {out_scores}  ({scores_df.shape[0]:,} rows × {scores_df.shape[1]} cols)")

# ── 4. Village persistence table ─────────────────────────────────────────
out_persist = f"{OUTPUT_DIR}/village_persistence.csv"
village_persistence.to_csv(out_persist, index=False)
logger.info(f"Exported village_persistence.csv  ({village_persistence.shape[0]:,} villages)")
print(f"Saved: {out_persist}  ({village_persistence.shape[0]:,} villages)")

# ── 5. Model artefact manifest ────────────────────────────────────────────
model_files = [
    ("IF model",          os.path.join(MODEL_DIR, "if_model.joblib")),
    ("IF params",         os.path.join(MODEL_DIR, "if_params.json")),
    ("LOF model",         os.path.join(MODEL_DIR, "lof_model.joblib")),
    ("LOF params",        os.path.join(MODEL_DIR, "lof_params.json")),
    ("RDA model dir",     os.path.join(MODEL_DIR, "rda_model.keras")),
    ("RDA S_final",       os.path.join(MODEL_DIR, "rda_S_final.npy")),
    ("RDA thresholds",    os.path.join(MODEL_DIR, "rda_thresholds.json")),
    ("RDA λ params",      os.path.join(MODEL_DIR, "rda_params.json")),
    ("Training log",      os.path.join(MODEL_DIR, "training.log")),
]
print("\n=== Saved model artefacts ===")
for name, path in model_files:
    status = "✓" if os.path.exists(path) else "✗ MISSING"
    print(f"  {status}  {name:20s}  {path}")

# ── 6. Final summary ──────────────────────────────────────────────────────
print("\n=== NOTEBOOK 02 COMPLETE — Summary ===")
print(f"  Total records    : {len(df):,}")
print(f"  IQR flagged      : {df['iqr_flag'].sum():,}  ({df['iqr_flag'].mean()*100:.1f}%)")
print(f"  IF flagged       : {df['if_flag'].sum():,}  ({df['if_flag'].mean()*100:.1f}%)")
print(f"  LOF flagged      : {df['lof_flag'].sum():,}  ({df['lof_flag'].mean()*100:.1f}%)")
print(f"  RDA flagged      : {df['rda_flag'].sum():,}  ({df['rda_flag'].mean()*100:.1f}%)")
print(f"  Consensus flagged: {df['consensus_flag'].sum():,}  ({df['consensus_flag'].mean()*100:.1f}%)")
print(f"  Villages — Tier 1 (High)    : {(village_persistence['priority_tier']=='Tier 1 – High Priority').sum():,}")
print(f"  Villages — Tier 2 (Moderate): {(village_persistence['priority_tier']=='Tier 2 – Moderate').sum():,}")

logger.info("=== Notebook 02 COMPLETE ===")

