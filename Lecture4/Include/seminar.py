from fastapi import FastAPI
import database
import models

import numpy as np
from sqlalchemy import select
from sqlalchemy.sql.expression import func


#기본세팅
engine = database.engineconn()
session = engine.sessionmaker()
conn = engine.connection()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/all_professor_score")
async def all_professor():
    data = session.query(models.LectureInfo).all()
    professor_dict = {}
    for info in data:
        if info.교수명 not in professor_dict:
            professor_dict[info.교수명] = {
                "강의만족도": [],
                "난이도": [],
                "성취감": [],
                "학습량": [],
                "강의력": []
            }
        if not info.강의만족도==None:
            professor_dict[info.교수명]["강의만족도"].append(info.강의만족도)
            professor_dict[info.교수명]["난이도"].append(info.난이도)
            professor_dict[info.교수명]["성취감"].append(info.성취감)
            professor_dict[info.교수명]["학습량"].append(info.학습량)
            professor_dict[info.교수명]["강의력"].append(info.강의력)
    averages = []
    for prof, scores in professor_dict.items():
        avg_score = {
            "교수명": prof,
            "강의만족도 평균": np.mean(scores["강의만족도"]), "강의만족도 중앙값": np.median(scores["강의만족도"]), "강의만족도 최소값": np.min(scores["강의만족도"]), "강의만족도 최대값": np.max(scores["강의만족도"]),
            "난이도 평균": np.mean(scores["난이도"]), "난이도 중앙값": np.median(scores["난이도"]), "난이도 최소값": np.min(scores["난이도"]), "난이도 최대값": np.max(scores["난이도"]),
            "성취감 평균": np.mean(scores["성취감"]), "성취감 중앙값": np.median(scores["성취감"]), "성취감 최소값": np.min(scores["성취감"]), "성취감 최대값": np.max(scores["성취감"]),
            "학습량 평균": np.mean(scores["학습량"]), "학습량 중앙값": np.median(scores["학습량"]), "학습량 최소값": np.min(scores["학습량"]), "학습량 최대값": np.max(scores["학습량"]),
            "강의력 평균": np.mean(scores["강의력"]), "강의력 중앙값": np.median(scores["강의력"]), "강의력 최소값": np.min(scores["강의력"]), "강의력 최대값": np.max(scores["강의력"]),
        }
        averages.append(avg_score)
    
    return averages

from pydantic import BaseModel
class Professor(BaseModel):
    교수명: str

@app.post("/professor_info")
async def professor_info(item: Professor):
    data = session.query(models.LectureInfo).filter(models.LectureInfo.교수명 == item.교수명).all()
    ids = [info.강의아이디 for info in data]
    강의만족도 = [info.강의만족도 for info in data]
    난이도 = [info.난이도 for info in data]
    성취감 = [info.성취감 for info in data]
    학습량 = [info.학습량 for info in data]
    강의력 = [info.강의력 for info in data]
    
    review_count = 0
    for id in ids:
        query = select([func.count()]).where(models.t_lecture_repu.c.강의아이디 == id)
        result = conn.execute(query)
        review_count+= result.scalar()
    
    re = {
        "강의평 개수":review_count,
        "강의만족도 평균": np.mean(강의만족도), "강의만족도 중앙값": np.median(강의만족도), "강의만족도 최소값": np.min(강의만족도), "강의만족도 최대값": np.max(강의만족도),
        "난이도 평균": np.mean(난이도), "난이도 중앙값": np.median(난이도), "난이도 최소값": np.min(난이도), "난이도 최대값": np.max(난이도),
        "성취감 평균": np.mean(성취감), "성취감 중앙값": np.median(성취감), "성취감 최소값": np.min(성취감), "성취감 최대값": np.max(성취감),
        "학습량 평균": np.mean(학습량), "학습량 중앙값": np.median(학습량), "학습량 최소값": np.min(학습량), "학습량 최대값": np.max(학습량),
        "강의력 평균": np.mean(강의력), "강의력 중앙값": np.median(강의력), "강의력 최소값": np.min(강의력), "강의력 최대값": np.max(강의력),
    }
    return re

@app.post("/professor_repu")
async def professor_repu(item: Professor):
    data = session.query(models.LectureInfo).filter(models.LectureInfo.교수명 == item.교수명).all()
    ids = [info.강의아이디 for info in data]
    professor_data = []
    for id in ids:
        query = select([models.t_lecture_repu.c.유저아이디, models.t_lecture_repu.c.강의평, models.t_lecture_repu.c.강의만족도]).where(models.t_lecture_repu.c.강의아이디 == id)
        result = conn.execute(query)
        reviews = result.fetchall()  # 해당 강의의 모든 리뷰 가져오기
        for review in reviews:
            professor_data.append({
                "유저아이디": review[0],
                "강의평": review[1],
                "강의만족도": review[2]
            })
    return professor_data