from typing import Dict, List, Optional
from app.core.config import SUBJECT_MAX_SCORES, GRADE_THRESHOLDS

class GradeCalculator:
    @staticmethod
    def calculate_total_max_score() -> float:
        """计算所有学科满分总和"""
        return sum(SUBJECT_MAX_SCORES.values())
    
    @staticmethod
    def calculate_grade(total_score: float) -> str:
        """根据总分计算等级"""
        max_total = GradeCalculator.calculate_total_max_score()
        score_percentage = (total_score / max_total) * 100
        
        if score_percentage >= GRADE_THRESHOLDS['A']:
            return 'A'
        elif score_percentage >= GRADE_THRESHOLDS['B']:
            return 'B'
        elif score_percentage >= GRADE_THRESHOLDS['C']:
            return 'C'
        else:
            return 'D'
    
    @staticmethod
    def get_grade_color(grade: str) -> str:
        """获取等级对应的颜色"""
        grade_colors = {
            'A': '#90EE90',  # 浅绿色
            'B': '#87CEEB',  # 天蓝色
            'C': '#FFB6C1',  # 浅粉色
            'D': '#FFB6C1'   # 浅红色
        }
        return grade_colors.get(grade, '')