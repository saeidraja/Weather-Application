# Weather App

## Description
A containerized web application that accepts a city name as input and outputs current weather details (temperature, wind velocity, humidity) via a free weather API. Query results are logged and persisted in InfluxDB for analysis.

## Features
- Data storage in InfluxDB
- Logs are forwarded by Promtail to loki for Grafana visualization
- CI/CD GitHub Actions workflow run by clicking on action manually or pushing to main and Builds application Docker image, Pushes to Docker Hub and Deploys the built image to server if the previous jobs is succeeded.

## Future Improvements
- Writing and Separating the front-end (user interface) from the back-end API application for improved maintainability and scalability in future iterations.
- Add test section to CI/CD (unit test / stage test / load test....).
- Use caching for experiencing better build time.
- Scan docker image with trivy scanner.
- Separating production and stage environment and using tags for deploying on each (for example latest on main)

Due to time constraints, these features were not implemented, and unfortunately, they were missed in this iteration. However, they will be added in the near future.

