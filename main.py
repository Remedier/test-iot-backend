from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel
from database import insert_sensor_data, get_latest_sensor_data
from background_tasks import generate_sensor_data
import os
import uvicorn

app = FastAPI()

# 데이터 모델 정의
class SensorData(BaseModel):
    value: float

# 백그라운드에서 자동 데이터 추가 기능 실행
@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(generate_sensor_data())
    
# 위험 수준 계산 함수
def calculate_risk_level(value):
    if value < 20:
        return "관심"
    elif 20 <= value < 50:
        return "주의"
    else:
        return "위험"

# 센서 데이터 저장 + 위험 분석 API
@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):
    insert_sensor_data(data.value)
    risk_level = calculate_risk_level(data.value)
    return {"status": "success", "received_value": data.value, "risk_level": risk_level}

# 센서 데이터 조회 API
@app.get("/sensor-data")
def get_sensor_data():
    data = get_latest_sensor_data()
    return {
        "sensor_data": data,
        "risk_levels": [calculate_risk_level(d[1]) for d in data],  # 위험 수준 추가
    }
def read_data():
    return {"message" : "Hello, FastAPI"}
  
# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React (localhost:3000) 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # Railway가 제공하는 PORT 환경변수
    uvicorn.run(app, host="0.0.0.0", port=port)