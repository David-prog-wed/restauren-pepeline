# Sistema de Gestion de Restaurante — Pipeline CI/CD

AA2 – ABP | Gestion del Software | Tecnologica del Oriente

## Servicios

| Servicio             | Puerto |
| -------------------- | ------ |
| auth-service         | 5001   |
| reservations-service | 5002   |
| orders-service       | 5003   |

## Ejecutar pruebas localmente

```bash
cd auth-service && pip install -r requirements.txt && pytest tests/unit/ -v
cd reservations-service && pip install -r requirements.txt && pytest tests/unit/ -v
cd orders-service && pip install -r requirements.txt && pytest tests/unit/ -v
```

## Simular el pipeline

```bash
python simulate_pipeline.py        # Ejecucion exitosa
python simulate_pipeline.py fail   # Fallo controlado
```

## Docker Compose

```bash
docker-compose up --build
```

## Front-end (SPA)

Se agrego un front-end en `frontend/` para consumir los 3 microservicios:

- Auth: registro y login
- Reservations: disponibilidad, crear, consultar y cancelar reservas
- Orders: ver menu, crear, confirmar y consultar pedidos

### Acceso

Con Docker Compose levantado, abre:

- http://localhost:8080

### Notas

- El front-end usa por defecto:
  - `http://localhost:5001` (auth-service)
  - `http://localhost:5002` (reservations-service)
  - `http://localhost:5003` (orders-service)
- Esos valores se pueden cambiar desde la seccion "Configuracion API" en la UI.

## CI/CD (AA2 - ABP)

Se agregaron workflows para automatizar integración y entrega continua en entorno de staging simulado.

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

### Documentacion de apoyo AA2

- `docs/pipeline-diagram.md` - Diagrama del pipeline y etapas.
- `docs/pipeline-simulation.md` - Escenarios de ejecucion (exito/fallo).
- `docs/evidence-checklist.md` - Checklist de evidencias para el PDF final.
