from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pydantic import BaseModel
import datetime
from fastapi.responses import Response
import os
import uvicorn

from database import insert_sensor_data, get_latest_sensor_data
from background_tasks import generate_sensor_data

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React (localhost:3000) 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request path: {request.url.path}")
    response = await call_next(request)
    return response

# RN400 Check-in API (장치 상태 확인)
@app.post("/checkin")
async def checkin(request: Request):
    try:
        # 데이터 파싱
        data = await request.form()
        print(f"[CHECK-IN DATA]: {data}")

        # XML 응답 생성
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <root>
            <ack>ok</ack>
            <timestamp>{int(datetime.datetime.utcnow().timestamp())}</timestamp>
            <offset-ch1>0.0</offset-ch1>
            <offset-ch2>0.0</offset-ch2>
            <sample-mode>3</sample-mode>
        </root>"""
        return Response(content=response_xml, media_type="application/xml")

    except Exception as e:
        # 예외 처리 및 디버그 출력
        print(f"Error processing Check-in: {e}")
        return Response(content="<xml><root><ack>error</ack></root></xml>", media_type="application/xml")

@app.post("/")
async def checkin(request: Request):
    try:
        # 데이터 파싱
        data = await request.form()
        print(f"[CHECK-IN DATA]: {data}")

        # XML 응답 생성
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <root>
            <ack>ok</ack>
            <timestamp>{int(datetime.datetime.utcnow().timestamp())}</timestamp>
            <offset-ch1>0.0</offset-ch1>
            <offset-ch2>0.0</offset-ch2>
            <sample-mode>3</sample-mode>
        </root>"""
        return Response(content=response_xml, media_type="application/xml")

    except Exception as e:
        # 예외 처리 및 디버그 출력
        print(f"Error processing Check-in: {e}")
        return Response(content="<xml><root><ack>error</ack></root></xml>", media_type="application/xml")
    
@app.post("/checkin/checkin")
async def checkin(request: Request):
    try:
        # 데이터 파싱
        data = await request.form()
        print(f"[CHECK-IN DATA]: {data}")

        # XML 응답 생성
        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <root>
            <ack>ok</ack>
            <timestamp>{int(datetime.datetime.utcnow().timestamp())}</timestamp>
            <offset-ch1>0.0</offset-ch1>
            <offset-ch2>0.0</offset-ch2>
            <sample-mode>3</sample-mode>
        </root>"""
        return Response(content=response_xml, media_type="application/xml")

    except Exception as e:
        # 예외 처리 및 디버그 출력
        print(f"Error processing Check-in: {e}")
        return Response(content="<xml><root><ack>error</ack></root></xml>", media_type="application/xml")

# RN400 Data-in API (센서 데이터 수신)
@app.post("/datain")
async def datain(request: Request):
    data = await request.json()
    print(f"[DATA-IN] {data}")
    return Response(content="<?xml><root><ack>ok</ack></root></xml>", media_type="application/xml")

# 데이터 모델 정의
class SensorData(BaseModel):
    value: float

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

@app.get("/")
def root():
    return {"message": "FastAPI 서버 정상 실행 중!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway 환경변수 사용
    uvicorn.run(app, host="0.0.0.0", port=port)
