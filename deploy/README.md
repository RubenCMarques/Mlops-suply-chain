# Local Development and Deployment

```text
React / Vite -> FastAPI -> application services
                              |
Kedro feature pipeline -> Hopsworks feature view -> Parquet snapshot
```

The API and Kedro jobs share one backend image. The React frontend has a separate
Nginx image. Hopsworks is an external service; this repository does not deploy a
Hopsworks cluster. Training and model serving are the next application steps.

## Docker Compose

Run from the repository root with Docker Desktop's Linux engine running and
Docker Compose 2.24 or newer:

```powershell
docker compose up --build -d
docker compose run --rm backend kedro run --pipelines smoke
```

- Frontend: `http://localhost:8080`
- API documentation: `http://localhost:8000/docs`
- Optional Hopsworks credentials: `backend/.env`, based on `backend/.env.example`

The API and frontend work without Hopsworks credentials. To export features from
an existing view, populate those settings before running:

```powershell
docker compose run --rm backend kedro run --pipelines feature_snapshot
```

Pipeline output is retained in the named `pipeline-data` volume mounted at
`/app/data`. `docker compose down` stops the services and preserves this volume.

## Kubernetes

The manifests provide a namespace, shared configuration, Deployments, internal
Services, probes, and resource limits. Kustomize includes the API and frontend;
jobs are launched separately. No resources are applied automatically.

First build the images with `docker compose build`. For a local cluster, make
`supply-chain-backend:local` and `supply-chain-frontend:local` available to its
container runtime. Docker Desktop commonly shares its local image store; kind
and minikube need their respective image-loading commands.

For a remote cluster, tag and push both images to your own registry, then update
the image references in the Deployments and job manifests. Configure
`imagePullSecrets` if your registry is private.

Validate and deploy from the repository root:

```powershell
kubectl kustomize deploy/kubernetes
kubectl apply -k deploy/kubernetes
kubectl -n supply-chain rollout status deployment/backend
kubectl -n supply-chain rollout status deployment/frontend
kubectl -n supply-chain port-forward service/frontend 8080:8080
```

Open `http://localhost:8080`. Services are internal by default. Add your own
Ingress/TLS and authentication before exposing the workspace publicly.

Run the credential-free Kedro job:

```powershell
kubectl apply -f deploy/kubernetes/jobs/smoke.yaml
kubectl -n supply-chain logs -f job/kedro-smoke
```

Jobs have fixed names and expire one hour after completion; use a new job name
for another run before expiry.

## Hopsworks on Kubernetes

Create `deploy/kubernetes/hopsworks.env` from `hopsworks.env.example` and fill in
your own values locally. That file is ignored by Git. After the namespace exists:

```powershell
kubectl -n supply-chain create secret generic hopsworks --from-env-file=deploy/kubernetes/hopsworks.env
kubectl -n supply-chain rollout restart deployment/backend
kubectl apply -f deploy/kubernetes/jobs/feature-snapshot.yaml
kubectl -n supply-chain logs -f job/kedro-feature-snapshot
```

The API's secret reference is optional so the status UI starts without an account.
The feature-snapshot job requires the secret and mounts a dedicated persistent
volume at `/app/data`. Your cluster needs a default StorageClass, or you must set
`storageClassName` on the claim. The claim survives job cleanup. Size it for your
data before running a large export. Your cluster also needs network access to
the Hopsworks services used by the SDK, including any feature-query endpoints.

Health probes check the API process, not Hopsworks availability. Add model-specific
readiness conditions when prediction serving is implemented.

## References

- [Kedro configuration](https://docs.kedro.org/en/stable/configure/advanced_configuration/)
- [Docker Compose environment files](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/)
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
- [Hopsworks Python API](https://docs.hopsworks.ai/latest/python-api/hopsworks/)
