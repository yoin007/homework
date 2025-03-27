from typing import Dict

# 学科满分配置
SUBJECT_MAX_SCORES: Dict[str, float] = {
    '语文': 10,
    '数学': 10,
    '英语': 6
}

# 等级区间配置（百分比）
GRADE_THRESHOLDS = {
    'A': 90,  # 优秀：>= 90%
    'B': 70,  # 良好：70% - 90%
    'C': 50,  # 合格：50% - 70%
    'D': 0    # 不合格：< 50%
}