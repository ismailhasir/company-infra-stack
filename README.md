# company-infra-stack

A hands-on DevOps project designed to practice **CI/CD, containerization, automation, and monitoring** using a Linux environment.

## Technologies

* Linux
* Shell / Bash
* Git & GitHub
* Python (FastAPI)
* Docker
* GitHub Actions
* Prometheus
* Grafana

## Project Scope

* Linux system and service management
* Shell scripting and automation
* Version control with Git and GitHub
* Application containerization with Docker
* CI/CD automation with GitHub Actions
* Metrics collection with Prometheus
* Monitoring and dashboards with Grafana

## Project Structure

```
.
├── app/               # FastAPI notes service (health check and notes endpoints) and its tests
├── docker/            # Dockerfile and Docker Compose configuration
├── scripts/           # Shell scripts (VM setup, hardening, backup, health checks)
├── docs/              # Documentation, runbook and architecture notes
└── .github/workflows/ # GitHub Actions CI/CD pipelines
```

## Docker

The notes service is packaged as a Docker image (`docker/Dockerfile`).

### Build and run

```
docker build -t notes-app -f docker/Dockerfile app/
docker run -d -p 8000:8000 --name notes notes-app
curl localhost:8000/health
```

The build context is `app/`, so the `COPY` paths in the Dockerfile are relative to that folder. For the same reason `.dockerignore` lives in `app/`: Docker only reads it from the root of the build context. It keeps `venv/`, `.git`, `__pycache__/` and `.pytest_cache/` out of the context.

### Design decisions

* **Location:** the Dockerfile stays in `docker/`, next to the future Compose files, instead of inside `app/`.
* **Multi-stage build:** dependencies are installed in a `builder` stage with `pip install --prefix=/install`, and only `/install` is copied to the final image. Build leftovers do not end up in the runtime image.
* **Layer cache:** `requirements.txt` is copied and installed before the application code, so a code change does not reinstall the dependencies.
* **Pinned dependencies:** `requirements.txt` holds only the runtime packages with exact versions. `pytest` and `httpx` live in `requirements-dev.txt` and are not installed in the image.
* **Non-root user:** the container runs as `appuser`, a system user without a home directory and without a login shell. Packages are installed under `/usr/local`, readable by every user, so the switch away from root needs no extra permissions.
* **Listening address:** uvicorn binds `0.0.0.0`. With the default `127.0.0.1` the service would not be reachable from outside the container.
* **Healthcheck:** a Python one-liner calls `/health` instead of `curl`, because the `slim` image does not ship `curl` and installing it would add size and attack surface.

### Useful checks

```
docker exec notes whoami   # appuser, not root
docker ps                  # STATUS shows (healthy)
docker logs notes
docker images notes-app
```

## Goal

The goal of this project is to build a simple end-to-end DevOps workflow covering **development → containerization → deployment → monitoring**, while gaining practical experience with commonly used DevOps tools.
