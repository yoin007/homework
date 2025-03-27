import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from backend.app.models.models import Student, Teacher, Record


def generate_sample_data(db: Session):
    """
    生成示例数据，包括学生、教师和作业记录
    """
    # 清空现有数据
    db.query(Record).delete()
    db.query(Student).delete()
    db.query(Teacher).delete()
    db.commit()
    
    # 生成年级和班级
    grades = ["高一", "高二", "高三"]
    classes_per_grade = 2  # 每个年级2个班
    groups = ["第一组", "第二组", "第三组", "第四组"]
    subjects = ["语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理"]
    
    # 生成学生数据
    students = []
    student_id_counter = 10001
    
    for grade in grades:
        for class_num in range(1, classes_per_grade + 1):
            class_name = f"{grade}{class_num}班"
            for _ in range(10):  # 每班10个学生
                group = random.choice(groups)
                student_subjects = random.sample(subjects, 3)  # 随机选3个学科
                
                student = Student(
                    student_id=str(student_id_counter),
                    name=f"学生{student_id_counter}",
                    grade=grade,
                    class_name=class_name,
                    group=group,
                    subjects=",".join(student_subjects)
                )
                
                students.append(student)
                student_id_counter += 1
    
    # 添加学生到数据库
    db.add_all(students)
    db.commit()
    
    # 生成教师数据
    teachers = []
    teacher_id_counter = 1001
    
    for subject in subjects:
        # 每个学科2个教师
        for i in range(2):
            teacher = Teacher(
                teacher_id=str(teacher_id_counter),
                name=f"{subject}教师{i+1}",
                subject=subject
            )
            
            teachers.append(teacher)
            teacher_id_counter += 1
    
    # 添加教师到数据库
    db.add_all(teachers)
    db.commit()
    
    # 生成作业记录
    records = []
    record_counter = 1
    
    # 获取过去30天的日期列表
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)) for i in range(30)]
    
    # 为每个学生生成作业记录
    for student in students:
        # 获取学生的选科
        student_subjects = student.subjects.split(",")
        
        # 为每个学科生成记录
        for subject in student_subjects:
            # 找到对应学科的教师
            subject_teachers = [t for t in teachers if t.subject == subject]
            if not subject_teachers:
                continue
            
            # 随机选择3个日期生成记录
            for _ in range(3):
                record_date = random.choice(dates)
                teacher = random.choice(subject_teachers)
                
                record = Record(
                    id=record_counter,
                    student_id=student.student_id,
                    name=student.name,
                    subject=subject,
                    score=random.randint(60, 100),  # 随机分数60-100
                    type="日常作业",
                    date=record_date,
                    batch=f"批次{record_date.strftime('%Y%m%d')}",
                    teacher_id=teacher.teacher_id
                )
                
                records.append(record)
                record_counter += 1
    
    # 添加作业记录到数据库
    db.add_all(records)
    db.commit()
    
    return {
        "students": len(students),
        "teachers": len(teachers),
        "records": len(records)
    }


def export_data_to_excel(data, filename):
    """
    将数据导出为Excel文件
    """
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename


def import_data_from_excel(filename, required_columns=None):
    """
    从Excel文件导入数据
    """
    df = pd.read_excel(filename)
    
    # 检查必要的列是否存在
    if required_columns:
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Excel文件缺少必要的列: {col}")
    
    return df.to_dict('records')