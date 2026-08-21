import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# 🟢 .env 파일을 강제로 읽어오는 코드 (필수)
load_dotenv()

from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    """서버 시작 시 DB 테이블을 자동 생성합니다."""
    await init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# ─── CORS 설정 ───────────────────────────────────────────────────────────────
# 배포 환경: FRONTEND_URL 환경변수에 허용할 프론트엔드 도메인을 설정합니다.
# 여러 도메인을 허용하려면 쉼표로 구분합니다.
# 예: "https://prain-frontend.onrender.com,https://custom-domain.com"
_frontend_url = os.environ.get("FRONTEND_URL", "")
_cors_origins: list[str] = [
    origin.strip() for origin in _frontend_url.split(",") if origin.strip()
]
if not _cors_origins:
    # 개발 환경 기본값 (FRONTEND_URL이 설정되지 않은 경우)
    _cors_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── API v1 라우터 등록 ──────────────────────────────────────────────────────
from app.api.v1.auth import router as auth_router
from app.api.v1.ai import router as ai_router
from app.api.v1.integrations import router as integrations_router
from app.api.v1.workspace import router as workspace_router

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(ai_router, prefix="/ai", tags=["AI"])
app.include_router(integrations_router, prefix="/integrations", tags=["Integrations"])
app.include_router(integrations_router, prefix="/api/v1/integrations", tags=["Integrations v1"])
app.include_router(workspace_router, prefix="/workspace", tags=["Workspace"])

# ─── 노트 엔드포인트 (notes.py가 비어있으므로 인라인 처리) ─────────────────────
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db

@app.get("/notes")
async def get_notes(db: AsyncSession = Depends(get_db)):
    """메모 목록 반환"""
    try:
        from sqlalchemy.future import select
        from app.models.note import Note
        result = await db.execute(select(Note))
        notes = result.scalars().all()
        return notes
    except Exception:
        return []

@app.post("/notes")
async def create_note(payload: dict, db: AsyncSession = Depends(get_db)):
    """메모 생성"""
    try:
        from app.models.note import Note
        note = Note(title=payload.get("title", ""), content=payload.get("content", ""))
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note
    except Exception as e:
        return {"error": str(e)}

# ─── 정적 파일 & SPA 서빙 (프론트엔드 빌드 파일 서빙용) ──────────────────────
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    @app.get("/")
    async def serve_index():
        index_path = STATIC_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"message": "Prain Backend API is running"}

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="root_static")
else:
    @app.get("/")
    async def root():
        return {"message": "Prain Backend API is running", "docs": "/docs"}
