# 🫁 LUAD RNA-seq — Three Pillars Re-analysis  
*“When everything works, nothing is learned.”*

## 1  Dataset summary
| File | Rows | Cols | Notes |
| ---- | ---- | ---- | ----- |
| `rna2.csv` | 598 samples | 60 660 | Z-scored, log-clipped STAR gene counts *(ENSG\*)* plus `case_id`, `Sample Type` |
| `sample_sheet.tsv` | 598 | 8 | Maps TCGA file-UUID → `Case ID` (patient) + `Sample Type` |
| `clinical/clinical.tsv` | 988 | 53 | Demographics + `ajcc_pathologic_t` (T-stage) & hundreds of sparse clinical fields |

*Target labels*

* **Binary task** – `Sample Type`     `Primary Tumor (1)` vs `Solid Tissue Normal (0)`  
* **Multiclass task** – coarse pT stage from `ajcc_pathologic_t`:  

  | Raw codes | Collapsed label |
  |-----------|-----------------|
  | T1 / T1a / T1b | **T1** |
  | T2 / T2a / T2b | **T2** |
  | T3 | **T3** |
  | T4 / TX / other | **T4/TX** |

## 2  Why we needed a *harder* label
The literature keeps reporting dazzling AUROC (> 0.99) on the binary LUAD benchmark.  
Our exploratory notebook shows **this task is trivial**:

* PCA/UMAP already separate Tumour vs Normal → no model required.  
* 1 % of samples or 1 gene classifiers still reach > 0.9 AUROC.  
* Random 100-gene panels match expert-selected signatures.  
* With perfect validation scores, Pillars 1–2–3 cannot expose over-fitting, unfairness, or feature instability.

## 3  Notebook structure
| Section | Purpose |
|---------|---------|
| **00_triviality.ipynb** | *Task-triviality audit* (PCA, single-gene AUROC sweep, random-gene baselines, learning curve, volcano plot) – proves the binary label is saturated. |
| **01_pillars_multiclass.ipynb** | Re-implements the **Three Pillars** on the harder 4-class T-stage label. <br>Pipeline: `SMOTE → StandardScaler → PCA (95 % var) → RandomForest` with per-fold top-100 MI feature selection. |

### Three Pillars in `01_pillars_multiclass.ipynb`
1. **Over-fitting evidence**  
   *Train vs Validation violin, learning curve, 200-× permutation test.*
2. **Algorithmic unfairness**  
   *Subgroup accuracy table (gender & race), calibration curves, intersectional bar-chart.*
3. **Feature-set instability**  
   *UpSet plot + Jaccard heat-map of selected gene sets across folds.*

Extra variants:

* **Low-MI control** Select the *100 least informative* genes (variance > 0).  
  Surprisingly high AUROC illustrates dimensionality-driven chance learning.
* **Stable-core removal** Iteratively drop fold-stable genes; model performance hardly degrades.

## 4  Key conclusions
* The binary LUAD benchmark is **too easy** – any model, even random, looks perfect.  
* On the 4-stage task we uncover:  
  * sizable train-validation gaps (Pillar 1),  
  * subgroup calibration errors (Pillar 2),  
  * almost no agreement in “biomarker” sets (Pillar 3).  
* **Take-home** Future studies must justify label choice and report the Three Pillars; otherwise we keep “rediscovering” random signatures.
