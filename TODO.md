# TODO - Frontend + Backend/CI-CD Restaurant Pipeline

## Frontend (completado)

- [x] Crear estructura `frontend/` con archivos base.
- [x] Implementar `frontend/index.html` con secciones Auth, Reservas y Órdenes.
- [x] Implementar `frontend/styles.css` para layout responsive y componentes UI.
- [x] Implementar `frontend/app.js` con llamadas fetch a microservicios.
- [x] Agregar `frontend/Dockerfile` para servir estáticos con Nginx.
- [x] Actualizar `docker-compose.yml` para incluir servicio `frontend` en puerto 8080.
- [x] Actualizar `README.md` con instrucciones del frontend.
- [x] Validar consistencia final de archivos modificados.

## Fase AA2 Backend/CI-CD (completado)

- [x] Revisar archivos actuales de backend y testing por servicio.
- [x] Crear workflow CI: `.github/workflows/ci.yml`.
- [x] Integrar análisis estático y seguridad en CI (flake8 + bandit/pip-audit).
- [x] Crear workflow CD staging: `.github/workflows/cd-staging.yml`.
- [x] Crear documentación en `docs/` (diagrama pipeline, simulación, evidencias).
- [x] Actualizar `README.md` con sección Backend/CI-CD AA2.
- [x] Validar sintaxis de workflows y consistencia de documentación.
