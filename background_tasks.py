import asyncio
import random
from database import insert_sensor_data

async def generate_sensor_data():
    """ 일정 주기마다 랜덤 센서 데이터를 생성하여 저장하는 함수 """
    while True:
        random_value = random.uniform(0, 100)  # 0~100 사이의 랜덤 값 생성
        insert_sensor_data(random_value)
        print(f"랜덤 센서 값 추가됨: {random_value}")
        await asyncio.sleep(1)  # 5초마다 데이터 추가
