# Week 5 - Kubernetes Web Application

Цей проект містить простий веб-додаток на Python Flask, який повертає версію 1.0.0.

## Структура проекту

- `app.py` - головний файл додатку Flask
- `requirements.txt` - залежності Python
- `Dockerfile` - файл для створення Docker образу
- `deployment.yaml` - Kubernetes Deployment маніфест
- `service.yaml` - Kubernetes Service маніфест (LoadBalancer)
- `deploy.sh` - скрипт для автоматичного деплою

## Використання

### 1. Збірка Docker образу

```bash
docker build -t webapp:1.0.0 .
```

### 2. Деплой в Kubernetes

```bash
# Застосувати маніфести
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Або використати скрипт
./deploy.sh
```

### 3. Перевірка статусу

```bash
# Перевірити deployment
kubectl get deployments

# Перевірити pods
kubectl get pods

# Перевірити service та отримати IP
kubectl get service webapp-service
```

### 4. Отримання External IP

```bash
# Спостерігати за призначенням IP
kubectl get service webapp-service --watch
```

### 5. Тестування

```bash
# Перевірити версію (замінити <EXTERNAL-IP> на реальний IP)
curl http://<EXTERNAL-IP>/version

# Перевірити головну сторінку
curl http://<EXTERNAL-IP>/

# Перевірити health check
curl http://<EXTERNAL-IP>/health
```

## Endpoints

- `/` - головна сторінка
- `/version` - повертає "Version: 1.0.0"
- `/health` - health check endpoint

## Очищення ресурсів

```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```
