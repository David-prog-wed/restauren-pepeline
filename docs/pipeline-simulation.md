# Simulación de Ejecución del Pipeline (AA2)

## Escenario 1: Ejecución exitosa

### Paso 1 - Commit y Push

Se realiza push a `develop` con mejoras en servicios y frontend.

### Paso 2 - CI automático

Se ejecuta `.github/workflows/ci.yml`:

- Tests unitarios por servicio:
  - `auth-service`
  - `reservations-service`
  - `orders-service`
- Lint (flake8)
- Seguridad:
  - bandit
  - pip-audit

**Resultado esperado:** todo en verde.

### Paso 3 - CD staging

Se ejecuta `.github/workflows/cd-staging.yml`:

- Build de imágenes Docker
- Simulación de despliegue a staging
- Health checks simulados

**Resultado esperado:** despliegue completado.

---

## Escenario 2: Falla controlada

### Falla simulada

Se introduce un error intencional en una prueba unitaria del servicio de pedidos.

### Resultado

- Etapa de tests falla en CI.
- CD no continúa (o no debe desplegar versión defectuosa).
- Se genera retroalimentación inmediata.

### Corrección

- Se corrige el test/código.
- Nuevo push dispara CI nuevamente.
- Pipeline vuelve a estado exitoso y habilita CD.

---

## Medidas de corrección recomendadas

1. Bloquear merge a `main` si CI falla.
2. Exigir revisión de código (PR review).
3. Mantener pruebas mínimas obligatorias por módulo.
4. Ejecutar análisis de seguridad en cada PR.
