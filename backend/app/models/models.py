from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Student(Base):
    """学生信息表"""
    __tablename__ = "stuInfo"

    student_id = Column(String, primary_key=True, index=True, comment="学号")
    name = Column(String, nullable=False, comment="姓名")
    grade = Column(String, nullable=False, comment="年级")
    class_name = Column(String, nullable=False, comment="班级")
    group = Column(String, nullable=True, comment="小组")
    subjects = Column(String, nullable=True, comment="选科")

    # 关系：一个学生可以有多个作业记录
    records = relationship("Record", back_populates="student")


class Teacher(Base):
    """教师信息表"""
    __tablename__ = "teacherInfo"

    teacher_id = Column(String, primary_key=True, index=True, comment="教师ID")
    name = Column(String, nullable=False, comment="姓名")
    subject = Column(String, nullable=False, comment="学科")

    # 关系：一个教师可以有多个作业记录
    records = relationship("Record", back_populates="teacher")


class Record(Base):
    """作业记录表"""
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="ID")
    student_id = Column(String, ForeignKey("stuInfo.student_id"), nullable=False, comment="学号")
    name = Column(String, nullable=False, comment="姓名")
    subject = Column(String, nullable=False, comment="学科")
    score = Column(Float, nullable=True, comment="分数")
    type = Column(String, nullable=True, comment="类型")
    date = Column(Date, nullable=False, comment="日期")
    batch = Column(String, nullable=True, comment="批次")
    teacher_id = Column(String, ForeignKey("teacherInfo.teacher_id"), nullable=False, comment="教师ID")

    # 关系：多个作业记录对应一个学生
    student = relationship("Student", back_populates="records")
    # 关系：多个作业记录对应一个教师
    teacher = relationship("Teacher", back_populates="records")