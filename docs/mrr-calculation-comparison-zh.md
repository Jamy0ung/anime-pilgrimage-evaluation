# MRR计算方法比较与修正

## 问题发现

在评估推荐算法性能时，我发现之前使用的MRR(Mean Reciprocal Rank)计算方法与标准实践存在差异，导致评估结果不准确。本文档记录了两种不同MRR计算方法的比较和分析过程。

## 数据背景

使用的数据集包含8个景点，分为两个主题：
- Steins;Gate相关景点: 'S001', 'S003', 'S004', 'S002'
- LoveLive相关景点: 'S005', 'S007', 'S006', 'S008'

每个景点有两种评分方式：
- weighted_sentiment_score（加权情感分数）
- normalized_sentiment_score（归一化情感分数）

标准排序基于Check值（访问量）降序排列。

## 原始MRR计算方法

最初使用的MRR计算方法如下：

```python
# 先对每个主题的景点进行排序
def rank_spots(spots, score_column):
    return data[data['SpotID'].isin(spots)].sort_values(score_column, ascending=False)['SpotID'].tolist()

# 在每个主题内部排序后，计算MRR
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

这种方法的问题是：它先对每个主题单独排序，然后在主题内部寻找标准排序中出现的第一个景点，这不符合MRR的标准计算方式。

## 修正后的MRR计算方法

修正后的MRR计算方法如下：

```python
# 全局排序（所有景点一起排序）
top_weighted = data.sort_values('weighted_sentiment_score', ascending=False)['SpotID'].tolist()
top_normalized = data.sort_values('normalized_sentiment_score', ascending=False)['SpotID'].tolist()

# 在全局排序中找到第一个属于特定主题的景点
def calculate_mrr(recommendation, relevant_spots):
    for rank, spot in enumerate(recommendation, start=1):
        if spot in relevant_spots:
            return 1 / rank
    return 0

mrr_steins_weighted = calculate_mrr(top_weighted, steins_gate_spots)
mrr_love_weighted = calculate_mrr(top_weighted, love_live_spots)
mrr_weighted = (mrr_steins_weighted + mrr_love_weighted) / 2
```

这种方法符合MRR的标准定义：在整个推荐列表中找到第一个相关项的排名的倒数。

## 计算结果比较

| 评估指标 | 原始方法 | 修正方法 |
|---------|---------|---------|
| Steins Gate MRR (加权) | 0.5000 | 1.0000 |
| Steins Gate MRR (归一化) | 0.2500 | 1.0000 |
| Love Live MRR (加权) | 0.3333 | 0.5000 |
| Love Live MRR (归一化) | 0.3333 | 0.5000 |
| 平均 MRR (加权) | 0.4167 | 0.7500 |
| 平均 MRR (归一化) | 0.2917 | 0.7500 |

## 差异原因分析

1. **评估视角不同**：
   - 原始方法：评估算法在对特定主题内部排序的准确性
   - 修正方法：评估算法在全局排序中快速识别特定主题景点的能力

2. **应用场景不同**：
   - 原始方法适用于用户已选择特定主题，系统仅需要对该主题内景点进行排序的场景
   - 修正方法适用于系统需要从所有候选项中推荐最相关项目的常见推荐系统场景

## 结论

根据推荐系统的标准评估实践，修正后的MRR计算方法更为合适，它评估了算法在所有候选项中快速识别相关项的能力，这对提升用户体验更为重要。最终实验采用修正后的MRR计算方法进行评估。

## 完整验证代码

```python
import pandas as pd
import numpy as np

# 加载数据
data = pd.read_csv("/mnt/data/Spot3.csv")

# 定义Steins;Gate 和 LoveLive的景点ID
steins_gate_spots = ['S001', 'S003', 'S004', 'S002']
love_live_spots = ['S005', 'S007', 'S006', 'S008']

# 标准答案：根据Check值降序排列，作为理想排序
standard_ranking = data.sort_values('Check', ascending=False)['SpotID'].tolist()

# 推荐列表（全部8个景点）
top_weighted = data.sort_values('weighted_sentiment_score', ascending=False)['SpotID'].tolist()
top_normalized = data.sort_values('normalized_sentiment_score', ascending=False)['SpotID'].tolist()

# =====================
# 原始MRR计算方法
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
# 修正后的MRR计算方法
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

# 打印结果对比
print("原始MRR计算结果:")
print(f"Steins Gate MRR (Weighted): {steins_gate_mrr_weighted:.4f}")
print(f"Steins Gate MRR (Normalized): {steins_gate_mrr_normalized:.4f}")
print(f"Love Live MRR (Weighted): {love_live_mrr_weighted:.4f}")
print(f"Love Live MRR (Normalized): {love_live_mrr_normalized:.4f}")
print(f"Average MRR (Weighted): {avg_mrr_weighted_original:.4f}")
print(f"Average MRR (Normalized): {avg_mrr_normalized_original:.4f}")

print("\n修正后MRR计算结果:")
print(f"Steins Gate MRR (Weighted): {mrr_steins_weighted:.4f}")
print(f"Steins Gate MRR (Normalized): {mrr_steins_normalized:.4f}")
print(f"Love Live MRR (Weighted): {mrr_love_weighted:.4f}")
print(f"Love Live MRR (Normalized): {mrr_love_normalized:.4f}")
print(f"Average MRR (Weighted): {mrr_weighted_corrected:.4f}")
print(f"Average MRR (Normalized): {mrr_normalized_corrected:.4f}")
```
