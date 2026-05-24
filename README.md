# Sistema de Gestion de Restaurante — Pipeline CI/CD

AA2 – ABP | Gestion del Software | Tecnologica del Oriente

## Descripcion general

Proyecto de microservicios para un sistema de restaurante con:

- **auth-service**: registro/login de usuarios
- **reservations-service**: disponibilidad y gestion de reservas
- **orders-service**: menu y gestion de pedidos
- **frontend (SPA)**: interfaz web para consumir los servicios
- **pipeline simulado**: flujo de CI/CD para pruebas, calidad y despliegue en staging

## Prerequisitos

- Python 3.10+ (recomendado 3.11)
- pip
- Docker y Docker Compose
- Git

Opcional para desarrollo local:

- Entorno virtual Python (`venv`)
- `pytest` (se instala desde `requirements.txt` de cada servicio)

## Servicios y puertos

| Servicio             | Puerto |
| -------------------- | ------ |
| auth-service         | 5001   |
| reservations-service | 5002   |
| orders-service       | 5003   |
| frontend             | 8080   |
| postgres             | 5432   |

## Estructura del repositorio

```text
.
├── auth-service/
├── reservations-service/
├── orders-service/
├── frontend/
├── docs/
├── k8s/
├── samples/
├── docker-compose.yml
├── simulate_pipeline.py
└── README.md
```

## Ejecutar con Docker Compose (recomendado)

```bash
docker-compose up --build
```

Accesos principales:

- Frontend: http://localhost:8080
- Auth health: http://localhost:5001/health
- Reservations health: http://localhost:5002/health
- Orders health: http://localhost:5003/health

## Ejecucion local sin Docker (por servicio)

> Nota: cada microservicio tiene su propio `requirements.txt`.

### auth-service

```bash
cd auth-service
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

### reservations-service

```bash
cd reservations-service
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

### orders-service

```bash
cd orders-service
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

## Ejecutar pruebas unitarias localmente

```bash
cd auth-service && pip install -r requirements.txt && pytest tests/unit/ -v
cd reservations-service && pip install -r requirements.txt && pytest tests/unit/ -v
cd orders-service && pip install -r requirements.txt && pytest tests/unit/ -v
```

## Endpoints principales

### auth-service (`http://localhost:5001`)

- `GET /health`
- `POST /api/auth/register`
- `POST /api/auth/login`

### reservations-service (`http://localhost:5002`)

- `GET /health`
- `GET /api/reservations/availability?date=YYYY-MM-DD&time=HH:MM&party_size=N`
- `POST /api/reservations/`
- `GET /api/reservations/<rid>`
- `PUT /api/reservations/<rid>/cancel`

### orders-service (`http://localhost:5003`)

- `GET /health`
- `GET /api/menu/`
- `POST /api/orders/`
- `PUT /api/orders/<oid>/confirm`
- `GET /api/orders/<oid>`

## Uso de archivos de ejemplo (`samples/`)

El directorio `samples/` contiene payloads JSON para pruebas manuales de endpoints:

- `auth_register.json`, `auth_login.json`, `auth_login_bad.json`
- `reservation_create.json`, `reservation_bad.json`
- `order_create.json`, `order_bad.json`

Ejemplo con `curl` (PowerShell/cmd con archivo JSON en disco):

```bash
curl -X POST http://localhost:5001/api/auth/register ^
  -H "Content-Type: application/json" ^
  --data-binary "@samples/auth_register.json"
```

## Front-end (SPA)

El frontend ubicado en `frontend/` consume los 3 microservicios para:

- Auth: registro y login
- Reservations: disponibilidad, crear, consultar y cancelar reservas
- Orders: ver menu, crear, confirmar y consultar pedidos

### Notas del frontend

- Base URLs por defecto:
  - `http://localhost:5001` (auth-service)
  - `http://localhost:5002` (reservations-service)
  - `http://localhost:5003` (orders-service)
- Estos valores pueden cambiarse en la seccion **Configuracion API** de la UI.

## Simular el pipeline

```bash
python simulate_pipeline.py        # Ejecucion exitosa
python simulate_pipeline.py fail   # Fallo controlado
```

## CI/CD (AA2 - ABP)

Se agregaron workflows para automatizar integracion y entrega continua en entorno de staging simulado.

### Workflows

- `.github/workflows/ci.yml`
  - Ejecuta pruebas unitarias por microservicio.
  - Ejecuta lint con `flake8`.
  - Ejecuta escaneo de seguridad con `bandit`.
  - Ejecuta auditoria de dependencias con `pip-audit`.
  - Incluye analisis SonarQube opcional (`sonar-analysis`).

- `.github/workflows/cd-staging.yml`
  - Construye imagenes Docker de servicios y frontend.
  - Simula despliegue en staging.
  - Ejecuta health checks simulados post-deploy.

## Troubleshooting rapido

- **Puerto en uso**: si falla el arranque, verifica que 5001, 5002, 5003, 8080 y 5432 esten libres.
- **Dependencias faltantes**: reinstala con `pip install -r requirements.txt` dentro del servicio.
- **Docker no levanta servicios**: ejecuta `docker-compose down -v` y luego `docker-compose up --build`.
- **Frontend sin respuesta de APIs**: valida que los servicios esten en estado healthy y que las URLs configuradas sean correctas.

## Documentacion de apoyo AA2

- `docs/pipeline-diagram.md` - Diagrama del pipeline y etapas.
- `docs/pipeline-simulation.md` - Escenarios de ejecucion (exito/fallo).
- `docs/evidence-checklist.md` - Checklist de evidencias para el PDF final.
