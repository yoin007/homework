from datetime import date as date_type
from typing import List, Optional, TypeVar, Generic

import pydantic
from pydantic import BaseModel


# 学生模式
class StudentBase(BaseModel):
    name: str
    grade: str
    class_name: str
    group: Optional[str] = None
    subjects: Optional[str] = None


class StudentCreate(StudentBase):
    student_id: str


class Student(StudentBase):
    student_id: str

    class Config:
        orm_mode = True


# 教师模式
class TeacherBase(BaseModel):
    name: str
    subject: str


class TeacherCreate(TeacherBase):
    teacher_id: str


class Teacher(TeacherBase):
    teacher_id: str

    class Config:
        orm_mode = True


# 作业记录模式
class RecordBase(BaseModel):
    student_id: str
    name: str
    subject: str
    score: Optional[float] = None
    type: Optional[str] = None
    date: date_type
    batch: Optional[str] = None
    teacher_id: str


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int

    class Config:
        orm_mode = True


# 用于Excel导入的模式
class ExcelImportResponse(BaseModel):
    success: bool
    message: str
    imported_count: Optional[int] = None


# 用于Excel导出的模式
class ExcelExportRequest(BaseModel):
    grade: Optional[str] = None
    class_name: Optional[List[str]] = None


# 用于筛选作业记录的模式
class RecordFilter(BaseModel):
    grade: Optional[str] = None
    class_name: Optional[str] = None
    group: Optional[str] = None
    subject: Optional[str] = None
    start_date: Optional[date_type] = None
    end_date: Optional[date_type] = None

    @pydantic.validator('start_date', 'end_date')
    def validate_date(cls, v):
        if v is not None:
            try:
                if isinstance(v, str):
                    return date_type.fromisoformat(v)
                return v
            except ValueError:
                raise ValueError('日期格式无效，请使用YYYY-MM-DD格式')
        return v

    @pydantic.validator('end_date')
    def validate_date_range(cls, v, values):
        if v is not None and 'start_date' in values and values['start_date'] is not None:
            if v < values['start_date']:
                raise ValueError('结束日期不能早于开始日期')
        return v


# 用于汇总的学生成绩模式
class StudentScoreSummary(BaseModel):
    id: int
    student_id: str
    name: str
    grade: str
    class_name: str
    group: Optional[str] = None
    total_score: float
    grade: str
    grade_color: str
    # 动态字段将在运行时添加


# 用于学科作业记录汇总的模式
class SubjectScoreSummary(BaseModel):
    id: int
    student_id: str
    name: str
    grade: str
    class_name: str
    total_score: float
    count: int
    # 动态字段（不同日期的分数）将在运行时添加


# 用于泛型的类型变量
T = TypeVar('T')

# 分页响应模式
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int