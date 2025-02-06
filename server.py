from fastapi import FastAPI, Request
import datetime
from fastapi.responses import Response

app = FastAPI()

# Check-in API (RN400 장치의 상태 확인)
@app.post("/checkin")
async def checkin(request: Request):
    data = await request.json()
    print(f"[CHECK-IN] {data}")

    # RN400이 요구하는 XML 응답 형식 반환
    response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <root>
        <ack>ok</ack>
        <timestamp>{int(datetime.datetime.utcnow().timestamp())}</timestamp>
    </root>"""
    
    return Response(content=response_xml, media_type="application/xml")

# Data-in API (센서 데이터 수신)
@app.post("/datain")
async def datain(request: Request):
    data = await request.json()
    print(f"[DATA-IN] {data}")
    return Response(content="<?xml><root><ack>ok</ack></root></xml>", media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
