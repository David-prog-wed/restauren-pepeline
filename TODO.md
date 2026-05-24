# TODO - Fix CORS and validate full app flow

- [x] Add `flask-cors` dependency to:
  - [x] auth-service/requirements.txt
  - [x] reservations-service/requirements.txt
  - [x] orders-service/requirements.txt
- [x] Enable CORS in:
  - [x] auth-service/app/main.py
  - [x] reservations-service/app/main.py
  - [x] orders-service/app/main.py
- [ ] Rebuild and restart containers
- [ ] Run API creation tests (register/reservation/order)
- [ ] Validate service logs for POST/PUT requests
- [ ] Provide final status and run commands
