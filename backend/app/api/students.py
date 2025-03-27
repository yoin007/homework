from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Student, Record
from app.schemas.schemas import Student as StudentSchema
from app.schemas.schemas import StudentCreate, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[StudentSchema])
def read_students(
    grade: Optional[str] = None,
    class_name: Optional[str] = None,
    group: Optional[str] = None,
    student_id: Optional[str] = None,
    name: Optional[str] = None,
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取学生列表，支持筛选和分页"""
    query = db.query(Student)
    
    # 应用筛选条件
    if grade:
        query = query.filter(Student.grade == grade)
    if class_name:
        query = query.filter(Student.class_name == class_name)
    if group:
        query = query.filter(Student.group == group)
    if student_id:
        query = query.filter(Student.student_id == student_id)
    if name:
        query = query.filter(Student.name == name)
    
    # 计算总记录数
    total = query.count()
    
    # 应用分页
    # 确保page和page_size不为None，并转换为整数
    page = int(page) if page is not None else 1
    page_size = int(page_size) if page_size is not None else 10
    query = query.offset((page - 1) * page_size).limit(page_size)
    students = query.all()
    
    return {
        "items": students,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/", response_model=StudentSchema)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    创建新的学生
    """
    # 检查学号是否已存在
    db_student = db.query(Student).filter(Student.student_id == student.student_id).first()
    if db_student:
        raise HTTPException(status_code=400, detail=f"学号 {student.student_id} 已存在")
    
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("/{student_id}", response_model=StudentSchema)
def read_student(student_id: str, db: Session = Depends(get_db)):
    """
    获取指定学号的学生
    """
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail=f"学号 {student_id} 不存在")
    return student


@router.put("/{student_id}", response_model=StudentSchema)
def update_student(student_id: str, student: StudentCreate, db: Session = Depends(get_db)):
    """
    更新指定学号的学生
    """
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail=f"学号 {student_id} 不存在")
    
    # 如果学号变更，检查新学号是否已存在
    if student_id != student.student_id:
        existing_student = db.query(Student).filter(Student.student_id == student.student_id).first()
        if existing_student:
            raise HTTPException(status_code=400, detail=f"学号 {student.student_id} 已存在")
    
    # 更新学生信息
    for key, value in student.dict().items():
        setattr(db_student, key, value)
    
    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    """
    删除指定学号的学生
    """
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail=f"学号 {student_id} 不存在")
    
    # 检查是否有关联的作业记录
    record_count = db.query(func.count(Record.id)).filter(Record.student_id == student_id).scalar()
    if record_count > 0:
        raise HTTPException(status_code=400, detail=f"无法删除学号 {student_id}，存在 {record_count} 条关联的作业记录")
    
    db.delete(db_student)
    db.commit()
    return {"message": f"学号 {student_id} 已删除"}


@router.get("/grades/all", response_model=List[str])
def get_all_grades(db: Session = Depends(get_db)):
    """
    获取所有年级列表
    """
    grades = db.query(Student.grade).distinct().all()
    return [grade[0] for grade in grades if grade[0] is not None]


@router.get("/classes/by-grade/{grade}")
def get_classes_by_grade(grade: str, db: Session = Depends(get_db)):
    """
    获取指定年级的班级列表
    """
    classes = db.query(Student.class_name).filter(Student.grade == grade).distinct().all()
    return [class_name[0] for class_name in classes]


@router.get("/groups/by-class/{class_name}")
def get_groups_by_class(class_name: str, db: Session = Depends(get_db)):
    """
    获取指定班级的小组列表
    """
    groups = db.query(Student.group).filter(Student.class_name == class_name).distinct().all()
    return [group[0] for group in groups if group[0] is not None]