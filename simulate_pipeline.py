#!/usr/bin/env python3
# simulate_pipeline.py
# Uso: python simulate_pipeline.py        (pipeline exitoso)
# Uso: python simulate_pipeline.py fail   (fallo controlado)
import time, sys

G  = "\033[92m"
R  = "\033[91m"
Y  = "\033[93m"
B  = "\033[94m"
BD = "\033[1m"
X  = "\033[0m"

def log(stage, msg, ok=True):
    icon = G + "OK" + X if ok else R + "FAIL" + X
    print(f"[{BD}{stage}{X}] [{icon}] {msg}")
    time.sleep(0.1)

def sep(title):
    print(f"\n{BD}{B}{'='*58}{X}")
    print(f"{BD}{B}  {title}{X}")
    print(f"{BD}{B}{'='*58}{X}\n")

def run_success():
    print(f"\n{BD}{'*'*60}")
    print("  RESTAURANT CI/CD PIPELINE  |  GitHub Actions")
    print(f"  Commit: a3f2b1c  |  Branch: develop")
    print(f"  Trigger: push  |  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'*'*60}{X}\n")

    sep("ETAPA 1  BUILD")
    for m in ["Checkout codigo fuente", "Setup Node.js v18",
              "npm ci  (847 paquetes)", "npm run build  frontend OK",
              "pip install  auth + reservations + orders",
              "docker build auth-service:a3f2b1c  -> pushed",
              "docker build reservations-service:a3f2b1c  -> pushed",
              "docker build orders-service:a3f2b1c  -> pushed"]:
        log("BUILD", m)
    print(f"  {G}BUILD completada en 3m 45s{X}\n")

    sep("ETAPA 2  TEST")
    for t in ["ReservationForm.test.js  PASS", "OrderCart.test.js  PASS", "api.test.js  PASS"]:
        print(f"    {G}{t}{X}"); time.sleep(0.08)
    print(f"    {G}Frontend Coverage: 87.3%{X}\n")

    for t in ["test_health_check  PASSED", "test_register_user  PASSED",
              "test_register_duplicate  PASSED", "test_login_success  PASSED",
              "test_login_invalid  PASSED", "test_register_missing_fields  PASSED"]:
        print(f"    {G}{t}{X}"); time.sleep(0.07)
    print(f"    {G}auth-service: 6 passed  |  Coverage: 91.2%{X}\n")

    for t in ["test_health_check  PASSED", "test_check_availability_empty  PASSED",
              "test_create_reservation_success  PASSED", "test_create_reservation_missing_fields  PASSED",
              "test_cancel_reservation  PASSED", "test_get_reservation_not_found  PASSED",
              "test_availability_ignores_cancelled  PASSED"]:
        print(f"    {G}{t}{X}"); time.sleep(0.07)
    print(f"    {G}reservations-service: 7 passed  |  Coverage: 89.5%{X}\n")

    for t in ["test_health_check  PASSED", "test_get_menu  PASSED",
              "test_calculate_total  PASSED", "test_create_order_success  PASSED",
              "test_create_order_invalid_product  PASSED", "test_create_order_missing_fields  PASSED",
              "test_confirm_order  PASSED"]:
        print(f"    {G}{t}{X}"); time.sleep(0.07)
    print(f"    {G}orders-service: 7 passed  |  Coverage: 85.0%{X}")
    print(f"  {G}TEST completada en 5m 12s  |  Total: 20 passed{X}\n")

    sep("ETAPA 3  ANALYZE")
    time.sleep(0.3)
    for k, v, c in [("Bugs", "0", G), ("Vulnerabilities", "0", G),
                    ("Code Smells", "3  (leve)", Y), ("Coverage", "89.1%", G),
                    ("Quality Gate", "PASSED", G)]:
        print(f"    {k:<24} {c}{v}{X}"); time.sleep(0.1)
    print(f"\n    {G}OWASP Dependency-Check: 156 deps, 0 criticas  PASSED{X}")
    print(f"  {G}ANALYZE completada en 4m 30s{X}\n")

    sep("ETAPA 4  DEPLOY STAGING")
    for m in ["kubectl set image deployment/auth-service",
              "kubectl set image deployment/reservations-service",
              "kubectl set image deployment/orders-service",
              "Rollout: 2/2 replicas disponibles",
              "Health check  GET /health  -> 200 OK",
              "Slack notificado: Deploy exitoso"]:
        log("DEPLOY", m)

    print(f"\n{BD}{G}{'='*60}")
    print("  PIPELINE COMPLETADO EXITOSAMENTE")
    print(f"  Duracion total: 15m 42s  |  Commit: a3f2b1c")
    print(f"{'='*60}{X}\n")

def run_failure():
    print(f"\n{BD}{'*'*60}")
    print("  RESTAURANT CI/CD PIPELINE  |  Escenario de Fallo")
    print(f"  Commit: b7d9e2f  |  Branch: develop")
    print(f"  Trigger: push  |  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'*'*60}{X}\n")

    sep("ETAPA 1  BUILD")
    log("BUILD", "Checkout, npm ci, pip install, docker build")
    print(f"  {G}BUILD completada{X}\n")

    sep("ETAPA 2  TEST  (fallo simulado en reservations)")
    log("TEST", "Frontend: 3 passed")
    log("TEST", "auth-service: 6 passed")
    log("TEST", "orders-service: 7 passed")
    print()
    print(f"  {R}FAILED  reservations-service/tests/unit/test_reservations.py{X}")
    print(f"  {R}         ::test_check_availability_empty{X}")
    print()
    print(f"  {Y}  def test_check_availability_empty():{X}")
    print(f"  {Y}      reservations_db.clear(){X}")
    print(f"  {Y}      result = check_availability('2026-06-01', '19:00', 2){X}")
    print(f"  {Y}  >   assert result['available_tables'] == 5{X}")
    print(f"  {R}  E   AssertionError: assert 0 == 5{X}")
    print()
    print(f"  {R}  1 failed, 6 passed in 3.45s{X}")
    print()
    print(f"  {R}{'='*56}")
    print("  PIPELINE DETENIDO")
    print("  Las etapas ANALYZE y DEPLOY-STAGING no se ejecutaran.")
    print(f"  {'='*56}{X}\n")
    log("NOTIFY", "Email enviado: build #48 FAILED  reservations-service", ok=False)
    log("NOTIFY", "Revisar parametro ignore_cancelled en check_availability()", ok=False)
    print(f"\n  {Y}Corrige el bug, haz push y el pipeline volvera a ejecutarse.{X}\n")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "success"
    run_failure() if mode == "fail" else run_success()
