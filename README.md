# DevOps Proyecto Final - Sistemas Operativos II

## Descripción

Este proyecto implementa una aplicación web con Flask que se despliega utilizando Docker y Docker Compose, con integración continua mediante GitHub Actions y monitoreo a través de Portainer. La aplicación se conecta a una base de datos PostgreSQL y está diseñada para ser desplegada en Google Cloud Platform (GCP).

## Stack Tecnológico

- **Flask** - Framework web Python para la API y frontend
- **PostgreSQL** - Base de datos relacional
- **Docker** - Contenedorización de la aplicación
- **Docker Compose** - Orquestación de servicios multi-contenedor
- **GitHub Actions** - CI/CD para pruebas y despliegue automático
- **Portainer** - Monitoreo y administración de contenedores
- **GCP** - Infraestructura cloud para el hosting

## Endpoints

| Ruta       | Método | Descripción                                    |
|------------|--------|------------------------------------------------|
| `/`        | GET    | Página HTML con hostname y ambiente            |
| `/health`  | GET    | Health check: `{"status": "ok", "hostname"}`   |
| `/info`    | GET    | Información de la app, versión, hostname y env |
