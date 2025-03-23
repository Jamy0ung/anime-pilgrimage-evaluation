
import pandas as pd
import numpy as np

# ===============================
# 📌 1. 数据加载与准备
# ===============================
data = pd.read_csv('/mnt/data/Spot3.csv')

# 定义Steins;Gate 和 LoveLive的景点ID
steins_gate_spots = ['S001', 'S003', 'S004', 'S002']
love_live_spots = ['S005', 'S007', 'S006', 'S008']

# 标准答案：根据Check值降序排列，作为理想排序
standard_ranking = data.sort_values('Check', ascending=False)['SpotID'].tolist()

# ===============================
# 📌 2. MAP（平均准确率）计算
# ===============================
# MAP: 衡量推荐结果中，相关项在排名列表中出现的平均位置（越靠前越好）
def calculate_ap(retrieved_list, relevant_list):
    hits = 0
    sum_precisions = 0
    for index, spot in enumerate(retrieved_list):
        if spot in relevant_list:
            hits += 1
            sum_precisions += hits / (index + 1)
    return sum_precisions / len(relevant_list) if relevant_list else 0

# 推荐列表（全部8个景点）
top_weighted = data.sort_values('weighted_sentiment_score', ascending=False)['SpotID'].tolist()
top_normalized = data.sort_values('normalized_sentiment_score', ascending=False)['SpotID'].tolist()

map_weighted = calculate_ap(top_weighted, standard_ranking[:8])
map_normalized = calculate_ap(top_normalized, standard_ranking[:8])

# ===============================
# 📌 3. MRR（平均倒数排名）修正版
# ===============================
# 正确方式：在推荐列表中找“第一个命中的目标子集”
def calculate_mrr(recommendation, relevant_spots):
    for rank, spot in enumerate(recommendation, start=1):
        if spot in relevant_spots:
            return 1 / rank
    return 0

# 计算两个子集在推荐列表中首次命中位置
mrr_steins_weighted = calculate_mrr(top_weighted, steins_gate_spots)
mrr_love_weighted = calculate_mrr(top_weighted, love_live_spots)
mrr_weighted = (mrr_steins_weighted + mrr_love_weighted) / 2

mrr_steins_normalized = calculate_mrr(top_normalized, steins_gate_spots)
mrr_love_normalized = calculate_mrr(top_normalized, love_live_spots)
mrr_normalized = (mrr_steins_normalized + mrr_love_normalized) / 2

# ===============================
# 📌 4. NDCG（归一化折扣累计增益）计算
# ===============================
# NDCG: 衡量推荐列表与理想顺序（打卡热度）之间的排序接近程度

# 创建基于Check排序的理想位置得分（8~1）
ideal_order = data.sort_values('Check', ascending=False)
ideal_scores = list(range(len(ideal_order), 0, -1))
ideal_score_map = dict(zip(ideal_order['SpotID'], ideal_scores))

# 获取每个推荐结果对应的得分
def get_position_based_scores(recommendation_list, ideal_score_map):
    return [ideal_score_map.get(spot, 0) for spot in recommendation_list]

# 计算DCG函数
def calculate_dcg(scores):
    return np.sum([score / np.log2(i + 2) for i, score in enumerate(scores)])

# NDCG计算函数
def calculate_ndcg(recommended_scores, ideal_scores):
    dcg = calculate_dcg(recommended_scores)
    idcg = calculate_dcg(ideal_scores)
    return dcg / idcg if idcg > 0 else 0

# 准备推荐得分列表
weighted_scores = get_position_based_scores(top_weighted, ideal_score_map)
normalized_scores = get_position_based_scores(top_normalized, ideal_score_map)
ideal_top8_scores = ideal_scores[:8]
ideal_top5_scores = ideal_scores[:5]

# 计算NDCG@5 和 NDCG@8
ndcg5_weighted = calculate_ndcg(weighted_scores[:5], ideal_top5_scores)
ndcg8_weighted = calculate_ndcg(weighted_scores[:8], ideal_top8_scores)
ndcg5_normalized = calculate_ndcg(normalized_scores[:5], ideal_top5_scores)
ndcg8_normalized = calculate_ndcg(normalized_scores[:8], ideal_top8_scores)

# ===============================
# 📌 5. 输出结果
# ===============================
print("📊 Weighted Sentiment Score:")
print("MAP:", round(map_weighted, 4))
print("MRR:", round(mrr_weighted, 4))
print("nDCG@5:", round(ndcg5_weighted, 4))
print("nDCG@8:", round(ndcg8_weighted, 4))

print("\n📊 Normalized Sentiment Score:")
print("MAP:", round(map_normalized, 4))
print("MRR:", round(mrr_normalized, 4))
print("nDCG@5:", round(ndcg5_normalized, 4))
print("nDCG@8:", round(ndcg8_normalized, 4))
