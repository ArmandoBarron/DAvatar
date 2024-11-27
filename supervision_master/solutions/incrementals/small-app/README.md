# Small app
Description

---
## Steps to deploy the prototype
```bash
docker-compose up -d
docker exec -ti small-app_smallapp_1 ./fib 1000
docker exec -ti small-app_smallapp_1 ./bubble 1000
```