from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Prain Backend"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "sqlite+aiosqlite:///./prain.db"
    SECRET_KEY: str = "your_super_secret_jwt_key_default"
    TOKEN_ENCRYPTION_KEY: str = "kU2v9pZ1r3y5x7w9A1b3C5d7E9f1G3h5I7j9K1l3M5o="
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30일 세션 유지

    OPENAI_API_KEY: str = ""

    # ─── 배포 관련 ────────────────────────────────────────────────────────────
    # FRONTEND_URL: CORS 허용할 프론트엔드 주소 (Render 배포 시 설정)
    # 예: https://prain-frontend.onrender.com
    FRONTEND_URL: str = ""

    # BACKEND_PUBLIC_URL: 백엔드의 공개 URL (OAuth redirect 기준)
    # 예: https://prain-backend.onrender.com
    BACKEND_PUBLIC_URL: str = ""

    # ─── Discord OAuth ────────────────────────────────────────────────────────
    DISCORD_CLIENT_ID: str = ""
    DISCORD_CLIENT_SECRET: str = ""
    # 배포 시 환경변수로 오버라이드:
    # 예: https://prain-backend.onrender.com/api/v1/integrations/discord/callback
    DISCORD_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/integrations/discord/callback"

    # ─── Figma OAuth / PAT ────────────────────────────────────────────────────
    FIGMA_CLIENT_ID: str = ""
    FIGMA_CLIENT_SECRET: str = ""
    # 배포 시 환경변수로 오버라이드:
    # 예: https://prain-backend.onrender.com/api/v1/integrations/figma/callback
    FIGMA_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/integrations/figma/callback"

    # ─── GitHub OAuth ─────────────────────────────────────────────────────────
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    # 배포 시 환경변수로 오버라이드:
    # 예: https://prain-backend.onrender.com/api/v1/integrations/github/callback
    GITHUB_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/integrations/github/callback"

    # ─── Notion OAuth ─────────────────────────────────────────────────────────
    NOTION_CLIENT_ID: str = ""
    NOTION_CLIENT_SECRET: str = ""
    # Notion은 127.0.0.1을 허용하지 않으므로 개발 시 localhost 사용
    # 배포 시 환경변수로 오버라이드:
    # 예: https://prain-backend.onrender.com/api/v1/integrations/notion/callback
    NOTION_REDIRECT_URI: str = "http://localhost:8000/api/v1/integrations/notion/callback"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
