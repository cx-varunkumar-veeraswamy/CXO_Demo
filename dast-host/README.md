# Hosting the DAST targets with Docker (free)

Two intentionally vulnerable services, containerised (non-root, read-only filesystem, capabilities dropped, 256 MB):

| Service | Local URL | Notes |
|---|---|---|
| REST API | http://localhost:8000 | spec at `/openapi.yaml`; login `bob`/`bob` or `admin`/`admin` |
| GraphQL | http://localhost:4001 | introspection on; endpoint `/graphql` |

## 1. Run locally
```bash
cd dast-host
docker compose up --build -d
curl http://localhost:8000/users/1
```

## 2. Make it reachable by the Checkmarx scanner
- **Scanner runs inside your network / same machine:** use `http://<your-ip>:8000` (change the port binding in `docker-compose.yml` from `127.0.0.1` to `0.0.0.0` and firewall appropriately).
- **Checkmarx-hosted scanner (needs public URL):** start free Cloudflare quick tunnels:
```bash
docker compose --profile tunnel up -d
docker compose logs tunnel-rest tunnel-graphql | grep trycloudflare
```
Use the printed `https://<random>.trycloudflare.com` URLs as the DAST target. The URL changes on every restart.

## 3. Configure the scan in Checkmarx One
1. Edit `rest/openapi.yaml` -> `servers.url` to the tunnel URL and upload it (or set the target URL and add the OpenAPI job).
2. Authentication: `POST /login` JSON `{"username":"admin","password":"admin"}`, take `token`, send as `Authorization: Bearer <token>` (the API doesn't enforce it, so unauthenticated scans also work).
3. Run the scan, then review results.

## 4. Tear down
```bash
docker compose --profile tunnel down
```
Only scan systems you own. Don't leave tunnels running unattended – the apps are deliberately exploitable.
