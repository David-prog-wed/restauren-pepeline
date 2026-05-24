# Sistema de Gestion de Restaurante — Pipeline CI/CD
AA2 – ABP | Gestion del Software | Tecnologica del Oriente

## Servicios
| Servicio | Puerto |
|---|---|
| auth-service | 5001 |
| reservations-service | 5002 |
| orders-service | 5003 |

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
