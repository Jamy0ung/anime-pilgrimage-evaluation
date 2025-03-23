
# 📍 Anime Pilgrimage Recommendation Evaluation

This project evaluates the effectiveness of a personalized anime pilgrimage recommendation system based on sentiment analysis.

## 📌 Description

We designed a small-scale experiment with 8 anime pilgrimage spots (from *Steins;Gate* and *LoveLive*) and evaluated recommendation accuracy using three core metrics:
- **MAP** (Mean Average Precision)
- **MRR** (Mean Reciprocal Rank)
- **nDCG@K** (Normalized Discounted Cumulative Gain)

Due to the small dataset size, traditional ranking metrics like MAP and MRR may saturate (e.g., returning 1.0). We therefore use **position-based NDCG** as a more sensitive indicator of ranking quality.

## ✅ Metric Explanation

- **MAP**: Evaluates how many relevant spots appear early in the ranking.
- **MRR**: We correctly compute MRR as the reciprocal rank of the **first relevant spot** from a target group (e.g., Steins or LoveLive) in the full recommendation list.
- **nDCG@K**: Scores are derived by mapping check-in rankings (1st = 8, ..., 8th = 1), and then evaluating how well the top-K recommendations match this ideal order.

## 📊 Evaluation Results

| Metric        | Weighted Sentiment | Normalized Sentiment |
|---------------|--------------------|-----------------------|
| **MAP**       | 1.0000             | 1.0000                |
| **MRR**       | 0.7500             | 0.7500                |
| **nDCG@5**    | 0.8964             | 0.8107                |
| **nDCG@8**    | 0.9393             | 0.9067                |

## 🧪 Dataset

The evaluation is performed on a dataset with 8 anime pilgrimage spots:
- *Steins;Gate*: S001, S002, S003, S004
- *LoveLive*: S005, S006, S007, S008

## 🛠️ Files

- `Spot3.csv` – Small-scale experiment dataset
- `final_experiment_evaluation_corrected.py` – Python script to calculate MAP, MRR, nDCG@K (with proper logic)
- `README.md` – This documentation file

## ▶️ How to Run

```bash
pip install pandas numpy
python final_experiment_evaluation_corrected.py
```

This evaluation method is designed to be small-scale and interpretable, useful for early-stage research prototypes and visualization-based systems.
# anime-pilgrimage-evaluation
