# MRR Calculation Method Comparison and Correction

## Problem Identification

While evaluating the performance of recommendation algorithms, I discovered that the previously used Mean Reciprocal Rank (MRR) calculation method differed from standard practices, leading to inaccurate evaluation results. This document records the comparison and analysis process of two different MRR calculation methods.

## Data Background

The dataset contains 8 tourist spots divided into two themes:
- Steins;Gate related spots: 'S001', 'S003', 'S004', 'S002'
- LoveLive related spots: 'S005', 'S007', 'S006', 'S008'

Each spot has two scoring methods:
- weighted_sentiment_score
- normalized_sentiment_score

The standard ranking is based on the Check value (visit frequency) in descending order.

## Original MRR Calculation Method

The initially used MRR calculation method was as follows:

```python
# First sort the spots within each theme
def rank_spots(spots, score_column):
    return data[data['SpotID'].isin(spots)].sort_values(score_column, ascending=False)['SpotID'].tolist()

# Calculate MRR after sorting within each theme
def calculate_mrr(ranking, standard_ranking):
    for spot in standard_ranking:
        if spot in ranking:
            return 1 / (ranking.index(spot) + 1)
    return 0

steins_gate_ranking_weighted = rank_spots(steins_gate_spots, 'weighted_sentiment_score')
love_live_ranking_weighted = rank_spots(love_live_spots, 'weighted_sentiment_score')

steins_gate_mrr_weighted = calculate_mrr(steins_gate_ranking_weighted, standard_ranking)
love_live_mrr_weighted = calculate_mrr(love_live_ranking_weighted, standard_ranking)
avg_mrr_weighted = (steins_gate_mrr_weighted + love_live_mrr_weighted) / 2
```

The problem with this method is that it first sorts each theme separately, then looks for the first spot in the standard ranking within that theme, which does not conform to the standard MRR calculation approach.

## Corrected MRR Calculation Method

The corrected MRR calculation method is as follows:

```python
# Global sorting (all spots sorted together)
top_weighted = data.sort_values('weighted_sentiment_score', ascending=False)['SpotID'].tolist()
top_normalized = data.sort_values('normalized_sentiment_score', ascending=False)['SpotID'].tolist()

# Find the first spot that belongs to a specific theme in the global ranking
def calculate_mrr(recommendation, relevant_spots):
    for rank, spot in enumerate(recommendation, start=1):
        if spot in relevant_spots:
            return 1 / rank
    return 0

mrr_steins_weighted = calculate_mrr(top_weighted, steins_gate_spots)
mrr_love_weighted = calculate_mrr(top_weighted, love_live_spots)
mrr_weighted = (mrr_steins_weighted + mrr_love_weighted) / 2
```

This method conforms to the standard definition of MRR: the reciprocal of the rank position of the first relevant item in the recommendation list.

## Calculation Results Comparison

| Evaluation Metric | Original Method | Corrected Method |
|---------|---------|---------|
| Steins Gate MRR (Weighted) | 0.5000 | 1.0000 |
| Steins Gate MRR (Normalized) | 0.2500 | 1.0000 |
| Love Live MRR (Weighted) | 0.3333 | 0.5000 |
| Love Live MRR (Normalized) | 0.3333 | 0.5000 |
| Average MRR (Weighted) | 0.4167 | 0.7500 |
| Average MRR (Normalized) | 0.2917 | 0.7500 |

## Analysis of Differences

1. **Different Evaluation Perspectives**:
   - Original Method: Evaluates the algorithm's accuracy in sorting spots within a specific theme
   - Corrected Method: Evaluates the algorithm's ability to quickly identify spots of a specific theme in the global ranking

2. **Different Application Scenarios**:
   - Original Method: Suitable for scenarios where users have already selected a specific theme, and the system only needs to sort spots within that theme
   - Corrected Method: Suitable for common recommendation system scenarios where the system needs to recommend the most relevant items from all candidates

## Conclusion

According to standard recommendation system evaluation practices, the corrected MRR calculation method is more appropriate as it evaluates the algorithm's ability to quickly identify relevant items among all candidates, which is more important for enhancing user experience. The final experiment adopts the corrected MRR calculation method for evaluation.

## Complete Verification Code

```python
import pandas as pd
import numpy as np

# Load data
data = pd.read_csv("/mnt/data/Spot3.csv")

# Define Steins;Gate and LoveLive spot IDs
steins_gate_spots = ['S001', 'S003', 'S004', 'S002']
love_live_spots = ['S005', 'S007', 'S006', 'S008']

# Standard ranking: sort by Check value in descending order
standard_ranking = data.sort_values('Check', ascending=False)['SpotID'].tolist()

# Recommendation lists (all 8 spots)
top_weighted = data.sort_values('weighted_sentiment_score', ascending=False)['SpotID'].tolist()
top_normalized = data.sort_values('normalized_sentiment_score', ascending=False)['SpotID'].tolist()

# =====================
# Original MRR Calculation Method
# =====================
def rank_spots(spots, score_column):
    return data[data['SpotID'].isin(spots)].sort_values(score_column, ascending=False)['SpotID'].tolist()

def calculate_mrr_original(ranking, standard_ranking):
    for spot in standard_ranking:
        if spot in ranking:
            return 1 / (ranking.index(spot) + 1)
    return 0

steins_gate_ranking_weighted = rank_spots(steins_gate_spots, 'weighted_sentiment_score')
steins_gate_ranking_normalized = rank_spots(steins_gate_spots, 'normalized_sentiment_score')
love_live_ranking_weighted = rank_spots(love_live_spots, 'weighted_sentiment_score')
love_live_ranking_normalized = rank_spots(love_live_spots, 'normalized_sentiment_score')

steins_gate_mrr_weighted = calculate_mrr_original(steins_gate_ranking_weighted, standard_ranking)
steins_gate_mrr_normalized = calculate_mrr_original(steins_gate_ranking_normalized, standard_ranking)
love_live_mrr_weighted = calculate_mrr_original(love_live_ranking_weighted, standard_ranking)
love_live_mrr_normalized = calculate_mrr_original(love_live_ranking_normalized, standard_ranking)

avg_mrr_weighted_original = (steins_gate_mrr_weighted + love_live_mrr_weighted) / 2
avg_mrr_normalized_original = (steins_gate_mrr_normalized + love_live_mrr_normalized) / 2

# =====================
# Corrected MRR Calculation Method
# =====================
def calculate_mrr_corrected(recommendation, relevant_spots):
    for rank, spot in enumerate(recommendation, start=1):
        if spot in relevant_spots:
            return 1 / rank
    return 0

mrr_steins_weighted = calculate_mrr_corrected(top_weighted, steins_gate_spots)
mrr_love_weighted = calculate_mrr_corrected(top_weighted, love_live_spots)
mrr_weighted_corrected = (mrr_steins_weighted + mrr_love_weighted) / 2

mrr_steins_normalized = calculate_mrr_corrected(top_normalized, steins_gate_spots)
mrr_love_normalized = calculate_mrr_corrected(top_normalized, love_live_spots)
mrr_normalized_corrected = (mrr_steins_normalized + mrr_love_normalized) / 2

# Print results comparison
print("Original MRR Calculation Results:")
print(f"Steins Gate MRR (Weighted): {steins_gate_mrr_weighted:.4f}")
print(f"Steins Gate MRR (Normalized): {steins_gate_mrr_normalized:.4f}")
print(f"Love Live MRR (Weighted): {love_live_mrr_weighted:.4f}")
print(f"Love Live MRR (Normalized): {love_live_mrr_normalized:.4f}")
print(f"Average MRR (Weighted): {avg_mrr_weighted_original:.4f}")
print(f"Average MRR (Normalized): {avg_mrr_normalized_original:.4f}")

print("\nCorrected MRR Calculation Results:")
print(f"Steins Gate MRR (Weighted): {mrr_steins_weighted:.4f}")
print(f"Steins Gate MRR (Normalized): {mrr_steins_normalized:.4f}")
print(f"Love Live MRR (Weighted): {mrr_love_weighted:.4f}")
print(f"Love Live MRR (Normalized): {mrr_love_normalized:.4f}")
print(f"Average MRR (Weighted): {mrr_weighted_corrected:.4f}")
print(f"Average MRR (Normalized): {mrr_normalized_corrected:.4f}")
```
