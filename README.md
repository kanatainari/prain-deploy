# 🧠 Prain Deploy

> Prain 프론트엔드(Node.js/Express)와 백엔드(FastAPI)를 Render에 배포하기 위한 통합 프로젝트입니다.

---

## 📁 프로젝트 구조

```
prain-deploy/
├── frontend/                 # Prain 프론트엔드 (Express + Vite)
│   ├── config.js             # 런타임 설정 (환경변수로 동적 주입)
│   ├── server.js             # Express 서버 + 백엔드 프록시
│   ├── index.html            # SPA 엔트리포인트
│   ├── script.js             # 메인 애플리케이션 로직
│   ├── styles.css            # 스타일시트
│   ├── activity.js           # Discord Activity SDK
│   ├── bot.js                # Discord Bot (Node.js)
│   ├── vite.config.js        # Vite 빌드 설정
│   ├── package.json          # Node.js 의존성
│   └── .env.example          # 환경변수 템플릿
├── backend/                  # Prain 백엔드 (FastAPI)
│   ├── app/
│   │   ├── main.py           # FastAPI 앱 진입점 (CORS, 라우터 등록)
│   │   ├── core/
│   │   │   ├── config.py     # Pydantic Settings (환경변수 기반)
│   │   │   ├── database.py   # SQLAlchemy 비동기 DB
│   │   │   ├── deps.py       # 의존성 주입 (인증 등)
│   │   │   └── security.py   # JWT, 암호화 유틸
│   │   ├── api/v1/
│   │   │   ├── auth.py       # 회원가입/로그인/인증
│   │   │   ├── ai.py         # AI 채팅, 회의록 요약
│   │   │   ├── integrations.py  # Discord/Figma/GitHub/Notion OAuth
│   │   │   └── workspace.py  # 워크스페이스 레이아웃
│   │   ├── models/           # SQLAlchemy ORM 모델
│   │   ├── schemas/          # Pydantic 요청/응답 스키마
│   │   ├── services/         # 외부 API 서비스 (Discord, Figma, GitHub, Notion)
│   │   └── static/           # 백엔드 직접 서빙용 정적 파일
│   ├── bot.py                # Discord 음성 회의 봇 (Python)
│   ├── requirements.txt      # Python 의존성
│   └── .env.example          # 환경변수 템플릿
├── render.yaml               # Render Blueprint (Frontend + Backend)
└── README.md                 # 이 파일
```

---

## 🚀 Render 배포 방법

### 1단계: GitHub에 Push

```bash
git init
git add .
git commit -m "Initial commit: prain-deploy"
git remote add origin https://github.com/YOUR_USERNAME/prain-deploy.git
git push -u origin main
```

### 2단계: Render Blueprint로 배포

1. [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**
2. 위에서 Push한 Repository 선택
3. `render.yaml`이 자동 감지됨
4. 환경변수 입력 → **Apply**

### 3단계: 환경변수 설정

아래 "환경변수" 섹션을 참고하여 각 서비스에 값을 입력합니다.

### 4단계: 연결 확인

- Backend: `https://prain-backend.onrender.com/docs` → Swagger UI
- Frontend: `https://prain-frontend.onrender.com` → Prain 앱

---

## ⚙️ Render 서비스 설정

### Backend (prain-backend)

| 항목 | 값 |
|------|-----|
| **Type** | Web Service |
| **Runtime** | Python |
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### Frontend (prain-frontend)

| 항목 | 값 |
|------|-----|
| **Type** | Web Service |
| **Runtime** | Node |
| **Root Directory** | `frontend` |
| **Build Command** | `npm install && npm run build` |
| **Start Command** | `node server.js` |

---

## 🔑 환경변수

### Backend 환경변수

| 변수명 | 필수 | 설명 | 예시 |
|--------|:----:|------|------|
| `FRONTEND_URL` | ✅ | CORS 허용할 프론트엔드 URL | `https://prain-frontend.onrender.com` |
| `BACKEND_PUBLIC_URL` | ✅ | 백엔드 공개 URL (OAuth callback 기준) | `https://prain-backend.onrender.com` |
| `DATABASE_URL` | ✅ | DB 연결 문자열 | `sqlite+aiosqlite:///./prain.db` |
| `SECRET_KEY` | ✅ | JWT 서명 키 (자동 생성 가능) | (Render가 자동 생성) |
| `TOKEN_ENCRYPTION_KEY` | ✅ | Fernet 암호화 키 (base64) | `openssl rand -base64 32` 로 생성 |
| `OPENAI_API_KEY` | ✅ | OpenAI API 키 | `sk-...` |
| `DISCORD_CLIENT_ID` | | Discord OAuth Client ID | |
| `DISCORD_CLIENT_SECRET` | | Discord OAuth Client Secret | |
| `DISCORD_REDIRECT_URI` | | Discord OAuth Callback | `https://prain-backend.onrender.com/api/v1/integrations/discord/callback` |
| `FIGMA_CLIENT_ID` | | Figma App Client ID | |
| `FIGMA_CLIENT_SECRET` | | Figma App Client Secret | |
| `FIGMA_REDIRECT_URI` | | Figma OAuth Callback | `https://prain-backend.onrender.com/api/v1/integrations/figma/callback` |
| `GITHUB_CLIENT_ID` | | GitHub OAuth App Client ID | |
| `GITHUB_CLIENT_SECRET` | | GitHub OAuth App Client Secret | |
| `GITHUB_REDIRECT_URI` | | GitHub OAuth Callback | `https://prain-backend.onrender.com/api/v1/integrations/github/callback` |
| `NOTION_CLIENT_ID` | | Notion Integration Client ID | |
| `NOTION_CLIENT_SECRET` | | Notion Integration Client Secret | |
| `NOTION_REDIRECT_URI` | | Notion OAuth Callback | `https://prain-backend.onrender.com/api/v1/integrations/notion/callback` |

### Frontend 환경변수

| 변수명 | 필수 | 설명 | 예시 |
|--------|:----:|------|------|
| `BACKEND_URL` | ✅ | 백엔드 API URL (프록시 대상) | `https://prain-backend.onrender.com` |
| `VITE_BACKEND_URL` | ✅ | Vite 빌드 시 사용 (동일 값) | `https://prain-backend.onrender.com` |
| `DISCORD_CLIENT_ID` | | Discord 토큰 교환용 | |
| `DISCORD_CLIENT_SECRET` | | Discord 토큰 교환용 | |
| `VITE_DISCORD_CLIENT_ID` | | 브라우저용 Discord Client ID | |
| `PRAIN_APP_URL` | | 프론트엔드 공개 URL | `https://prain-frontend.onrender.com` |

---

## 🔄 배포 순서 (상세)

```
1. Backend 배포
   └─ Render에서 prain-backend 서비스 생성
   └─ 환경변수 설정 (FRONTEND_URL은 나중에)
   └─ 배포 완료 → URL 확인 (예: https://prain-backend.onrender.com)
   └─ /docs 접속하여 Swagger UI 확인

2. Frontend 배포
   └─ Render에서 prain-frontend 서비스 생성
   └─ BACKEND_URL = 1단계에서 확인한 백엔드 URL
   └─ 배포 완료 → URL 확인 (예: https://prain-frontend.onrender.com)

3. Backend FRONTEND_URL 설정
   └─ Backend 환경변수에 FRONTEND_URL 추가
   └─ 값: 2단계에서 확인한 프론트엔드 URL
   └─ Render가 자동 재배포

4. OAuth Redirect URI 등록 (사용하는 서비스만)
   └─ Discord Developer Portal: Redirects에 백엔드 callback URL 추가
   └─ GitHub OAuth App: callback URL 설정
   └─ Notion Integration: redirect URL 설정

5. 연결 확인
   └─ 프론트엔드에서 회원가입 → "API 연결됨" 표시 확인
```

---

## 🏗️ 아키텍처

```
┌─────────────────┐         ┌─────────────────────┐
│  브라우저         │         │  Render              │
│                 │         │                     │
│  Prain SPA      │───────▶│  prain-frontend     │
│  (HTML/JS/CSS)  │         │  (Express + Proxy)  │
│                 │         │         │           │
└─────────────────┘         │         ▼           │
                            │  ┌─────────────┐    │
                            │  │ BACKEND_URL │    │
                            │  └──────┬──────┘    │
                            │         ▼           │
                            │  prain-backend      │
                            │  (FastAPI + Uvicorn)│
                            │         │           │
                            │         ▼           │
                            │  SQLite / PostgreSQL │
                            └─────────────────────┘
```

**연결 흐름:**
1. 브라우저가 프론트엔드 서버에 API 요청 (`/auth/me`, `/ai/chat` 등)
2. Express `server.js`가 해당 경로를 감지
3. `BACKEND_URL`로 요청을 프록시
4. 백엔드가 응답 → 프론트엔드가 브라우저에 전달

> 이 프록시 패턴 덕분에 브라우저는 같은 도메인으로만 요청하므로 CORS 문제가 없습니다.
> CORS 미들웨어는 직접 API 호출에 대한 안전망으로 설정되어 있습니다.

---

## 🛠️ 로컬 개발

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # 환경변수 편집
uvicorn app.main:app --reload --port 8000

# Frontend (별도 터미널)
cd frontend
npm install
cp .env.example .env      # BACKEND_URL=http://127.0.0.1:8000
npm run dev               # Vite dev server (포트 5173)
# 또는
npm run build && node server.js  # Production 모드 (포트 3000)
```

---

## ⚠️ 주의사항

1. **SQLite 영속성**: Render Free 플랜은 디스크가 재배포 시 초기화됩니다.
   - 영구 데이터가 필요하면 PostgreSQL로 전환하세요.
   - `DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname`

2. **Free 플랜 슬립**: Render Free 서비스는 15분 비활성 시 슬립됩니다.
   - 첫 요청 시 깨어나는데 30~60초 소요됩니다.

3. **Secret 관리**: `.env` 파일은 절대 커밋하지 마세요.
   - 모든 Secret은 Render Dashboard에서만 설정합니다.

4. **Discord Bot**: `backend/bot.py`는 별도 Background Worker로 배포해야 합니다.
   - Render → New → Background Worker → `python bot.py`

---

## 📝 원본 Repository

이 프로젝트는 아래 두 Repository를 기반으로 배포 환경에 맞게 수정되었습니다:

- Frontend: [0601sunny-spec/prain](https://github.com/0601sunny-spec/prain)
- Backend: [kdw123654/Socket](https://github.com/kdw123654/Socket)

### 주요 변경사항

| 파일 | 변경 내용 |
|------|-----------|
| `backend/app/main.py` | CORS 미들웨어 추가, API v1 라우터 등록, DB 초기화 |
| `backend/app/core/config.py` | FRONTEND_URL/BACKEND_PUBLIC_URL 추가, 시크릿 제거 |
| `backend/app/static/config.js` | 하드코딩 localhost 제거 |
| `backend/bot.py` | 환경변수 배포 가이드 주석 추가 |
| `frontend/config.js` | apiBaseUrl을 빈 문자열로 변경 (프록시 사용) |
| `frontend/server.js` | API 경로 프록시 추가, 동적 config.js 주입 |
| `frontend/.env.example` | 배포용 환경변수 문서화 |
