from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import os

# ایمپورت تابع اصلی پروکسی از کتابخانه esp32-tunnel
# این تابع وظیفه هدایت درخواست‌ها به ESP8266 را بر عهده دارد
from api.tunnel import tunnel_proxy  # type: ignore

app = FastAPI(title="esp32-tunnel")

# مسیر WebSocket برای اتصال ESP8266
# این مسیر توسط خود کتابخانه در ESP8266 فراخوانی می‌شود
# و نیازی به تعریف دستی ندارد، اما برای اطمینان از وجود آن مطمئن می‌شویم.

@app.get("/api/status")
async def health_check():
    return {"status": "ok", "message": "Tunnel server is running"}

# مسیر اصلی برای هدایت درخواست‌های کاربران به ESP8266
# وقتی شما آدرس https://bazkon.onrender.com/bazkon/ را باز می‌کنید،
# این تابع فراخوانی می‌شود و درخواست را به دستگاه شما می‌فرستد.
@app.api_route("/{tid}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy_path(tid: str, path: str, request: Request):
    return await tunnel_proxy(tid, path, request)

@app.api_route("/{tid}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy_root(tid: str, request: Request):
    return await tunnel_proxy(tid, "", request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
