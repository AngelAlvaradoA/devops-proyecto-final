# TECNA Inventory Platform

## Descripción

Plataforma de inventario empresarial construida con Flask que proporciona un dashboard moderno para la gestión de productos, stock, proveedores y movimientos de inventario. El proyecto está completamente containerizado con Docker y desplegado mediante **Docker Swarm** en Google Cloud Platform, con integración continua y despliegue automático vía GitHub Actions.

## Stack Tecnológico

- **Flask** — Framework web Python para la API REST y frontend
- **PostgreSQL 15** — Base de datos relacional
- **Docker** — Contenedorización de la aplicación
- **Docker Compose** — Orquestación multi-contenedor en desarrollo
- **Docker Swarm** — Orquestación en producción
- **GitHub Actions** — CI/CD: tests, build & push a Docker Hub, deploy automático
- **Portainer** — Monitoreo y administración visual de contenedores
- **GCP (Google Cloud Platform)** — Infraestructura cloud para hosting de la VM

## Estructura del Proyecto

```
devops-proyecto-final/
├── .github/workflows/
│   └── ci-cd.yml              # Pipeline CI/CD
├── app/
│   ├── app.py                  # Aplicación Flask (TECNA Inventory Platform)
│   ├── Dockerfile              # Imagen Docker para la app
│   └── requirements.txt        # Dependencias Python
├── docker-compose.yml          # Servicios para desarrollo local
├── docker-stack.yml            # Stack para Docker Swarm en producción
└── README.md
```

## Pipeline CI/CD

El pipeline `ci-cd.yml` se ejecuta en **push a `main`** y en **PRs a `main`**:

| Job              | Trigger            | Descripción                                       |
|------------------|--------------------|---------------------------------------------------|
| `test`           | push / PR          | Setup Python 3.11, instala dependencias, test básico |
| `build-and-push` | solo push a main   | Login Docker Hub, build y push de imagen (latest + SHA) |
| `deploy`         | solo push a main   | SSH a VM GCP, git pull y `docker stack deploy`    |

## Endpoints

| Ruta              | Método | Descripción                                                    |
|-------------------|--------|----------------------------------------------------------------|
| `/`               | GET    | Dashboard TECNA con métricas, tabla de inventario y alertas   |
| `/health`         | GET    | Health check: `{"status": "ok", "service", "hostname", "timestamp"}` |
| `/info`           | GET    | Información de la app, versión, hostname, environment y stack  |
| `/api/inventory`  | GET    | Lista JSON con 8 productos del inventario                      |
| `/api/metrics`    | GET    | Métricas: total productos, stock crítico, proveedores, valor   |

## Servicios Docker

| Servicio   | Imagen                              | Puerto    | Descripción                         |
|------------|-------------------------------------|-----------|-------------------------------------|
| `app`      | `angelalvarado1230/devops-app`      | 80:5000   | Aplicación Flask                    |
| `db`       | `postgres:15`                       | —         | Base de datos PostgreSQL            |
| `portainer`| `portainer/portainer-ce`            | 9000:9000 | Administración de contenedores      |

Deploy automático configurado — GCP VM: `34.29.55.89`
