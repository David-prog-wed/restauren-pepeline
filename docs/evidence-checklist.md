# Checklist de Evidencias para PDF AA2

Usa esta lista para capturas y evidencias del documento final.

## 1) Análisis del sistema

- [ ] Captura/tabla de módulos del sistema (Auth, Reservas, Pedidos, Frontend).
- [ ] Lista de funcionalidades principales.
- [ ] Puntos críticos a automatizar identificados.

## 2) Diseño del pipeline

- [ ] Captura del diagrama del pipeline.
- [ ] Captura o extracto de `ci.yml`.
- [ ] Captura o extracto de `cd-staging.yml`.
- [ ] Explicación de herramientas usadas.

## 3) Simulación del pipeline

- [ ] Evidencia de ejecución exitosa (logs CI/CD).
- [ ] Evidencia de fallo controlado (test fallando).
- [ ] Evidencia de corrección posterior (pipeline en verde).

## 4) Calidad y seguridad

- [ ] Resultado de lint (flake8).
- [ ] Resultado de bandit (análisis de seguridad de código).
- [ ] Resultado de pip-audit (dependencias).
- [ ] (Opcional) Resultado de SonarQube.

## 5) Buenas prácticas

- [ ] Evidencia de estrategia de ramas y PR.
- [ ] Validación de gates (no deploy si falla CI).
- [ ] Estrategia propuesta para escalar a producción.

## 6) Cierre

- [ ] Conclusiones redactadas.
- [ ] Aprendizajes adquiridos redactados.
- [ ] Documento exportado como `AA2_Pipeline_SistemaRestaurante.pdf`.
