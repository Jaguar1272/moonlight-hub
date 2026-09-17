from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import importlib
import os

app = FastAPI(title="달빛정원 통합 홍보소")

# 정적 파일 및 템플릿 경로 설정
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

# 데이터 모델 정의
class ChannelData(BaseModel):
    channel_id: str
    channel_name: str
    guild_id: str

# 웹소켓 연결 관리자
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# Cogs(모듈) 자동 로드 시스템
def load_cogs(application: FastAPI):
    cogs_dir = "app/cogs"
    if os.path.exists(cogs_dir):
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                module = importlib.import_module(f"app.cogs.{module_name}")
                if hasattr(module, "router"):
                    application.include_router(module.router)
                    print(f"[Cog Loaded] {module_name}")

load_cogs(app)

# 메인 페이지 라우터
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 디스코드 봇이 채널 생성 시 호출하는 API 엔드포인트
@app.post("/api/channel-created")
async def channel_created(data: ChannelData):
    payload = {
        "event": "channel_create",
        "channel_id": data.channel_id,
        "channel_name": data.channel_name
    }
    # 접속 중인 모든 웹 브라우저에 실시간 전송
    await manager.broadcast(payload)
    return {"status": "success", "message": "Broadcasted successfully"}

# 실시간 웹소켓 엔드포인트
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)