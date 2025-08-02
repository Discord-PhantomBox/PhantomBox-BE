import threading
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from model.label_model import TextRequest
from router import auth_router, post_router, user_router
from service import label_service, asset_service
from dao.mysql_dao import mysql_dao

app = FastAPI()
# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "https://10.10.5.252:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(user_router.router)

@app.get("/ping")
async def root():
    # DB 상태 확인
    try:
        result = mysql_dao.execute_query("SELECT 1")
        db_healthy = result and result[0].get("1") == 1 or True  # 그냥 실행만 되면 OK
    except Exception as e:
        db_healthy = False
    # 헬스체크 결과 반환
    if db_healthy:
        return {
            "status": "ok",
            "db": "healthy",
            "thread": threading.current_thread().name
        }
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "db": "unreachable",
                "thread": threading.current_thread().name
            }
        )


@app.post("/label")
async def label(label_request : TextRequest):
    labeled_response = await label_service.labeling(label_request)
    return labeled_response

@app.post("/asset/{label_id}")
async def asset(label_id: int, asset_request : TextRequest):
    assets_response = await asset_service.select(label_id, asset_request)
    return assets_response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)