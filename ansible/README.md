# Ansible Deployment

## Description
Using Ansible playbooks to automate server preparation and deployment of the weather application stack, including Traefik, the app, the influxdb database, and logging stack.

## Features
- Server provisioning: Install OS packages, Docker, and configure security.
- Stack deployment: Configure and deploy Traefik (reverse proxy), weather app, InfluxDB, and Loki/Promtail/Grafana via Docker Compose.
- Utilization of group_vars for all variable data and structured modular roles to facilitate easy management, maintainibilty and scalability as the Ansible configuration grows.

## Requirements
- Ansible 2.10+.
- Target server with SSH access (Ubuntu/Debian recommended).
- Inventory file with host details.
- secrets in group_vars

## Usage
1. Update `inventory/host.yaml` with your server details.
2. Run the playbooks in sequence:
   - `ansible-playbook -i inventory/host.yaml preparing.yaml --tags preparing-server`
   - `ansible-playbook -i inventory/host.yaml preparing.yaml --tags docker-install`
   - `ansible-playbook -i inventory/host.yaml traefik-rProxy.yaml --tags traefik-setup`
   - `ansible-playbook -i inventory/host.yaml app.yaml --tags app-setup`
   - `ansible-playbook -i inventory/host.yaml log-stack.yaml --tags log-setup`
   - Prepares server (installs Docker, packages).
   - Deploys Traefik with configs.
   - Deploys app and InfluxDB.
   - Deploys logging stack.

## Playbooks and Roles
- **`preparing.yaml`**: Handles server setup and Docker installation.
- **`traefik-rProxy.yaml`**: Deploys Traefik.
- **`app.yaml`**: Deploys the weather app and InfluxDB.
- **`log-stack.yaml`**: Deploys the logging stack.
- Roles:
  - `server-setup`: Installs prerequisites and Docker.
  - `traefik`: Deploys Traefik Docker Compose.
  - `app-deploy`: Pulls app image from Docker Hub, deploys with Compose.
  - `logging`: Sets up Loki, Promtail, Grafana.

## Best Practices
- Use tags for selective execution (e.g., `ansible-playbook app.yaml --tags app`).
- Test in staging before production.
- Monitor with Grafana dashboards post-deployment.

## Future Improvements
An opportunity exists to integrate a GitHub Actions workflow for sequentially executing these playbooks, enhancing automation and enabling secure storage of sensitive data (e.g., passwords, tokens) in GitHub Secrets, referenced via group vars. Additionally, implementing Ansible Vault or other dedicated secret managers would provide robust handling of secrets. Due to time constraints, these features were not implemented, and unfortunately, they were missed in this iteration. However, they will be added in the near future.
