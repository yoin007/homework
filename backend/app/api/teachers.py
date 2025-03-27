from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Teacher, Record
from app.schemas.schemas import Teacher as TeacherSchema
from app.schemas.schemas import TeacherCreate, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[TeacherSchema])
def read_teachers(
    subject: Optional[str] = None,
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Teacher)
    
    if subject:
        query = query.filter(Teacher.subject == subject)
    
    total = query.count()
    # 确保 page 和 page_size 为整数类型
    offset = (int(page) - 1) * int(page_size) if page and page_size else 0
    limit = int(page_size) if page_size else 10
    teachers = query.offset(offset).limit(limit).all()
    
    return {
        "items": teachers,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.post("/", response_model=TeacherSchema)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    """
    创建新的教师
    """
    # 检查教师ID是否已存在
    db_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher.teacher_id).first()
    if db_teacher:
        raise HTTPException(status_code=400, detail=f"教师ID {teacher.teacher_id} 已存在")
    
    db_teacher = Teacher(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.get("/{teacher_id}", response_model=TeacherSchema)
def read_teacher(teacher_id: str, db: Session = Depends(get_db)):
    """
    获取指定ID的教师
    """
    teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if teacher is None:
        raise HTTPException(status_code=404, detail=f"教师ID {teacher_id} 不存在")
    return teacher


@router.put("/{teacher_id}", response_model=TeacherSchema)
def update_teacher(teacher_id: str, teacher: TeacherCreate, db: Session = Depends(get_db)):
    """
    更新指定ID的教师
    """
    db_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail=f"教师ID {teacher_id} 不存在")
    
    # 如果教师ID变更，检查新ID是否已存在
    if teacher_id != teacher.teacher_id:
        existing_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher.teacher_id).first()
        if existing_teacher:
            raise HTTPException(status_code=400, detail=f"教师ID {teacher.teacher_id} 已存在")
    
    # 更新教师信息
    for key, value in teacher.dict().items():
        setattr(db_teacher, key, value)
    
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: str, db: Session = Depends(get_db)):
    """
    删除指定ID的教师
    """
    db_teacher = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if db_teacher is None:
        raise HTTPException(status_code=404, detail=f"教师ID {teacher_id} 不存在")
    
    # 检查是否有关联的作业记录
    record_count = db.query(func.count(Record.id)).filter(Record.teacher_id == teacher_id).scalar()
    if record_count > 0:
        raise HTTPException(status_code=400, detail=f"无法删除教师ID {teacher_id}，存在 {record_count} 条关联的作业记录")
    
    db.delete(db_teacher)
    db.commit()
    return {"message": f"教师ID {teacher_id} 已删除"}


@router.get("/subjects/", response_model=List[str])
def get_subjects(db: Session = Depends(get_db)):
    """
    获取所有学科列表
    """
    subjects = db.query(Teacher.subject).distinct().all()
    return [subject[0] for subject in subjects if subject[0] is not None]