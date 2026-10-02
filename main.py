import os
import pathlib
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import uvicorn

PORT = int(os.environ.get("PORT", 10000))
_frontend = pathlib.Path(__file__).parent / "frontend"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Server running on port {PORT}")
    yield

app = FastAPI(title="esp32-tunnel", lifespan=lifespan)

# ---- مسیر پروکسی (Catch-all) ----
from api.tunnel import tunnel_proxy

_ALL_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

@app.api_route("/{tid}/{path:path}", methods=_ALL_METHODS)
async def proxy_path(tid: str, path: str, request: Request):
    return await tunnel_proxy(tid, path, request)

@app.api_route("/{tid}", methods=_ALL_METHODS)
async def proxy_root(tid: str, request: Request):
    return await tunnel_proxy(tid, "", request)

# ---- سلامت سرویس ----
@app.get("/api/status")
async def health_check():
    return {"status": "ok", "message": "Tunnel server is running"}

# ---- داشبورد (اختیاری) ----
if _frontend.exists():
    app.mount("/", StaticFiles(directory=_frontend, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT,
                ws_ping_interval=20, ws_ping_timeout=30)
