# Frontend

React with Vite. The first screen shows backend connectivity, Hopsworks
configuration status, and registered Kedro pipelines using the real status API.

Use Node.js 22.12 or newer. From this directory:

```powershell
npm ci
npm run dev
```

Start the backend in a second terminal. Vite serves the app on
http://127.0.0.1:5173 and proxies `/api`, `/docs`, and `/openapi.json` to
http://127.0.0.1:8000. Set the shell variable `BACKEND_URL` before starting Vite
if the backend uses another address. Vite selects another port if 5173 is busy.

```powershell
npm run build
```

Production containers serve `dist/` through an unprivileged Nginx process on port
8080. Nginx proxies API requests to the `backend` service, keeping browser requests
on the same origin and avoiding hardcoded deployment URLs in the JavaScript.

## Layout

```text
src/
|-- components/   Reusable interface elements
|-- pages/        Workspace screens
|-- services/     Backend HTTP client
|-- styles/       Shared styles
`-- assets/       Future application images and fonts
```

`public/` holds static assets. `tests/` is reserved for frontend tests. The frontend
does not receive Hopsworks credentials or connect directly to the feature store.

On Google Drive virtual drives, npm extraction may fail with `EBADF` or
`TAR_ENTRY_ERROR`. Use a local disk checkout for Node development if this occurs.

See the [backend guide](../backend/README.md) and
[deployment instructions](../deploy/README.md).
