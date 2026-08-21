import 'dotenv/config';
import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync, existsSync } from 'node:fs';

const app = express();
const root = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.env.PORT || 3000);
const backendUrl = (process.env.BACKEND_URL || process.env.VITE_BACKEND_URL || '').replace(/\/$/, '');

// ─── config.js 동적 주입 ────────────────────────────────────────────────────
// 배포 환경에서 BACKEND_URL 환경변수를 config.js의 apiBaseUrl에 주입합니다.
// BACKEND_URL이 설정되지 않으면 빈 문자열(같은 도메인 프록시 사용)을 유지합니다.
app.get('/config.js', (_req, res) => {
  const discordClientId = process.env.DISCORD_CLIENT_ID || process.env.VITE_DISCORD_CLIENT_ID || '';

  // 배포 환경에서는 프론트엔드 서버가 백엔드로 프록시하므로
  // apiBaseUrl을 빈 문자열로 두면 같은 도메인 /.proxy/backend를 경유합니다.
  // 또는 BACKEND_URL을 직접 브라우저에서 호출하도록 설정할 수도 있습니다.
  // 여기서는 프록시 패턴을 유지합니다.
  const config = `window.PRAIN_CONFIG = {
  discordClientId: '${discordClientId}',
  apiBaseUrl: '',
  demoModeOnApiError: true,
};
`;
  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
  res.send(config);
});

// ─── 백엔드 프록시 ──────────────────────────────────────────────────────────
// 프론트엔드의 모든 API 요청을 /.proxy/backend 경로를 통해 백엔드로 전달합니다.
// 이 방식을 사용하면 브라우저는 같은 도메인으로 요청하므로 CORS 문제가 없습니다.
app.use('/.proxy/backend', async (req, res) => {
  if (!backendUrl) return res.status(503).json({ error: 'BACKEND_URL is not configured' });

  const targetPath = req.originalUrl.replace('/.proxy/backend', '') || '/';
  const target = new URL(targetPath, backendUrl);
  const headers = { ...req.headers };
  delete headers.host;

  try {
    const response = await fetch(target, {
      method: req.method,
      headers,
      body: ['GET', 'HEAD'].includes(req.method) ? undefined : req,
      duplex: 'half',
    });

    res.status(response.status);
    response.headers.forEach((value, key) => {
      if (!['content-encoding', 'transfer-encoding'].includes(key.toLowerCase())) res.setHeader(key, value);
    });
    res.send(Buffer.from(await response.arrayBuffer()));
  } catch (error) {
    res.status(502).json({ error: 'Backend proxy request failed', detail: error.message });
  }
});

// ─── 백엔드 직접 프록시 (API_BASE가 빈 문자열일 때 사용) ────────────────────
// script.js에서 API_BASE='' 이면 fetch('/auth/me') 처럼 같은 도메인으로 호출합니다.
// 이 요청들을 백엔드로 프록시합니다.
const API_PATHS = ['/auth/', '/ai/', '/integrations/', '/api/v1/', '/api/', '/workspace/', '/notes'];
app.use(API_PATHS, async (req, res) => {
  if (!backendUrl) return res.status(503).json({ error: 'BACKEND_URL is not configured' });

  const target = new URL(req.originalUrl, backendUrl);
  const headers = { ...req.headers };
  delete headers.host;

  try {
    const response = await fetch(target, {
      method: req.method,
      headers,
      body: ['GET', 'HEAD'].includes(req.method) ? undefined : req,
      duplex: 'half',
    });

    res.status(response.status);
    response.headers.forEach((value, key) => {
      if (!['content-encoding', 'transfer-encoding'].includes(key.toLowerCase())) res.setHeader(key, value);
    });
    res.send(Buffer.from(await response.arrayBuffer()));
  } catch (error) {
    res.status(502).json({ error: 'Backend proxy request failed', detail: error.message });
  }
});

app.use(express.json());

// ─── Discord 토큰 교환 ──────────────────────────────────────────────────────
app.post(['/api/token', '/.proxy/api/token'], async (req, res) => {
  if (!req.body?.code) return res.status(400).json({ error: 'authorization code is required' });
  if (!process.env.DISCORD_CLIENT_ID || !process.env.DISCORD_CLIENT_SECRET) {
    return res.status(500).json({ error: 'Discord credentials are not configured' });
  }

  const body = new URLSearchParams({
    client_id: process.env.DISCORD_CLIENT_ID,
    client_secret: process.env.DISCORD_CLIENT_SECRET,
    grant_type: 'authorization_code',
    code: req.body.code,
  });
  const response = await fetch('https://discord.com/api/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const data = await response.json();
  return res.status(response.status).json(data);
});

// ─── 정적 파일 서빙 (빌드된 프론트엔드) ─────────────────────────────────────
app.use(express.static(path.join(root, 'dist')));
app.get(/.*/, (_req, res) => res.sendFile(path.join(root, 'dist', 'index.html')));

app.listen(port, () => {
  console.log(`Prain Activity listening on ${port}`);
  console.log(`Backend URL: ${backendUrl || '(not configured)'}`);
});
