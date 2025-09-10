# Weather-Application
## Overview
This repository hosts a weather application that fetches weather data for a user-specified city using a free API, displaying temperature, wind velocity, and humidity including data persistence in InfluxDB and logging via a Promtail/Loki/Grafana stack. Deployment is automated with GitHub Actions CI/CD for building and pushing Docker images to Docker Hub, followed by Ansible for server preparation and stack deployment.
## Project Structure
- **`app/`**: Weather application code and Dockerfile.
- **`ansible/`**: Playbooks for server setup, docker installation, and deploying Traefik reverse proxy, the app, the influxdb database, and logging stack.
- **`.github/workflows`**: include application CI/CD workflows.

## Key Components
- **Weather API Integration**: Retrieves real-time data for input cities.
- **Database**: InfluxDB for storing results.
- **Logging**: Centralized logs with Promtail, Loki, and Grafana dashboards.
- **CI/CD**: GitHub Actions builds Docker images, pushes to Docker Hub, and triggers deployment.
- **Deployment**: Ansible provisions the server (packages, Docker), deploys Traefik for reverse proxy, the app, the influxdb database and logging stack via Docker Compose.
