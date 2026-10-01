from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio

app = FastAPI()

# دیکشنری برای نگهداری اتصالات WebSocket دستگاه‌ها
devices = {}

@app.get("/")
async def root():
    return {"status": "Tunnel server is running"}

@app.websocket("/ws/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await websocket.accept()
    devices[device_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if device_id in devices:
            del devices[device_id]

@app.api_route("/{device_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(device_id: str, path: str, request):
    # این بخش در نسخه ساده شده است. در عمل باید درخواست را به دستگاه هدایت کند.
    # برای شروع، همین کافی است تا سرور بالا بیاید.
    return {"message": f"Proxy request to {device_id} for path {path}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)