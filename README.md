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

## Goal

The goal of this project is to build a simple end-to-end DevOps workflow covering **development → containerization → deployment → monitoring**, while gaining practical experience with commonly used DevOps tools.
