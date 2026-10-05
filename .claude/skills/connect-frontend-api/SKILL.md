---
name: connect-frontend-api
description: Wire the React (Vite) frontend to a backend FastAPI endpoint with typed fetch calls, loading and error states. Use when the user wants the frontend to display or submit data to the API.
---

# Connect frontend to the API

Frontend: `frontend/` (React + Vite, Node 22). Backend serves under `/api/v1` and `/health`.

## Steps
1. Read the backend schema in `backend/src/supply_chain/schemas/` and mirror it as TypeScript types (or JSDoc if the file is JS) in a single API module, e.g. `frontend/src/api/client.*`.
2. Use one base URL from `import.meta.env.VITE_API_URL`, defaulting to a relative path so the Vite dev proxy / compose network works. Check `vite.config.*`, `compose.yaml`, and `deploy/kubernetes/configmap.yaml` for the configured value and keep them consistent.
3. Write one function per endpoint that checks `response.ok` and throws a typed error.
4. In components, handle loading, error, and empty states explicitly.
5. Verify with `npm run build` in `frontend/` (same as CI). If the backend is running, test against it.

If an endpoint is missing, use the `add-api-endpoint` skill first.
