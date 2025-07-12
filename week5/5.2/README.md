# Week 5 - Kubernetes Web Application

Цей проект містить простий веб-додаток на Python Flask з підтримкою різних стратегій деплойменту.

## Версії додатку

- **v1.0.0**: Базова версія з endpoints: `/`, `/version`, `/health`
- **v2.0.0**: Розширена версія з додатковими endpoints: `/info`, `/status` та JSON responses

## Структура проекту

- `app.py` - головний файл додатку Flask
- `requirements.txt` - залежності Python
- `Dockerfile` - файл для створення Docker образу
- `k8s-manifests.yaml` - стандартний Kubernetes маніфест (v1.0.0)
- `k8s-manifests-v2.yaml` - Kubernetes маніфест для версії 2.0.0
- `canary-deployment.yaml` - Canary deployment (75% v1 + 25% v2)
- `blue-green-deployment.yaml` - Blue-Green deployment
- `deploy.sh` - скрипт для автоматичного деплою

## Docker Images

```bash
# Збірка версії 1.0.0
docker build -t webapp:1.0.0 .
docker tag webapp:1.0.0 airodua/webapp:1.0.0
docker push airodua/webapp:1.0.0

# Збірка версії 2.0.0 (потрібно оновити app.py)
docker build -t webapp:2.0.0 .
docker tag webapp:2.0.0 airodua/webapp:2.0.0
docker push airodua/webapp:2.0.0
```

## Стратегії деплойменту

### 1. Стандартний деплоймент

```bash
# Застосувати v1.0.0
kubectl apply -f k8s-manifests.yaml

# Або v2.0.0
kubectl apply -f k8s-manifests-v2.yaml
```

### 2. Canary Deployment (25% v2, 75% v1)

Canary deployment дозволяє поступово перевести частину трафіку на нову версію.

```bash
# Очистити попередні деплойменти
kubectl delete -f k8s-manifests.yaml -f k8s-manifests-v2.yaml

# Застосувати Canary deployment
kubectl apply -f canary-deployment.yaml

# Перевірити розподіл pods
kubectl get pods -l app=webapp -o wide

# Тестувати розподіл трафіку
for i in {1..20}; do curl -s http://<EXTERNAL-IP>/version; echo; done
```

**Архітектура Canary:**
- 3 репліки v1.0.0 (75% трафіку)
- 1 репліка v2.0.0 (25% трафіку)
- Спільний сервіс направляє трафік на обидві версії

### 3. Blue-Green Deployment (100% переключення)

Blue-Green deployment дозволяє миттєво переключити весь трафік між версіями.

```bash
# Застосувати Blue-Green deployment
kubectl apply -f blue-green-deployment.yaml

# Перевірити що обидва середовища працюють
kubectl get deployments
kubectl get pods -l app=webapp

# Тестувати Green environment (v2.0.0) внутрішньо
kubectl port-forward service/webapp-service-green-internal 8081:80
curl http://localhost:8081/version  # Повинно повернути "Version: 2.0.0"

# Переключити весь трафік на Green (v2.0.0)
kubectl patch service webapp-service-production -p '{"spec":{"selector":{"environment":"green"}}}'

# Перевірити активну версію
curl http://<EXTERNAL-IP>/version

# Rollback на Blue (v1.0.0) якщо потрібно
kubectl patch service webapp-service-production -p '{"spec":{"selector":{"environment":"blue"}}}'
```

**Архітектура Blue-Green:**
- **Blue environment**: 2 репліки v1.0.0 (початково активні)
- **Green environment**: 2 репліки v2.0.0 (готові до переключення)
- **Production service**: направляє 100% трафіку на активне середовище
- **Internal service**: для тестування Green environment

### 4. Моніторинг deployments

```bash
# Перевірити статус всіх deployments
kubectl get deployments

# Перевірити активне середовище в Blue-Green
kubectl describe service webapp-service-production | grep Selector

# Перевірити endpoints
kubectl get endpoints

# Переглянути логи
kubectl logs -l app=webapp --tail=10
```

## Endpoints

### Версія 1.0.0
- `/` - повертає "Welcome to the web application!"
- `/version` - повертає "Version: 1.0.0"
- `/health` - повертає "OK"

### Версія 2.0.0
- `/` - повертає "Welcome to the web application Version 2.0.0!"
- `/version` - повертає "Version: 2.0.0"
- `/health` - повертає "OK"
- `/info` - повертає JSON з детальною інформацією
- `/status` - повертає JSON зі статусом додатку

## Тестування версій

```bash
# Отримати External IP
kubectl get services

# Тестування основних endpoints
curl http://<EXTERNAL-IP>/
curl http://<EXTERNAL-IP>/version
curl http://<EXTERNAL-IP>/health

# Тестування нових endpoints (тільки v2.0.0)
curl http://<EXTERNAL-IP>/info
curl http://<EXTERNAL-IP>/status
```

## Порівняння стратегій деплойменту

| Стратегія | Переваги | Недоліки | Використання |
|-----------|----------|----------|-------------|
| **Стандартний** | Простий, швидкий | Downtime при оновленні | Розробка, тестування |
| **Canary** | Поступове тестування, менший ризик | Складність налаштування, неточний розподіл | Production з великою аудиторією |
| **Blue-Green** | Zero downtime, швидкий rollback | Подвійні ресурси | Critical production системи |

## Troubleshooting

```bash
# Перевірити статус pods
kubectl get pods -l app=webapp

# Переглянути деталі pod
kubectl describe pod <pod-name>

# Переглянути логи
kubectl logs <pod-name>

# Перевірити services
kubectl get services

# Перевірити events
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Очищення ресурсів

```bash
# Очистити стандартні deployments
kubectl delete -f k8s-manifests.yaml
kubectl delete -f k8s-manifests-v2.yaml

# Очистити Canary deployment
kubectl delete -f canary-deployment.yaml

# Очистити Blue-Green deployment
kubectl delete -f blue-green-deployment.yaml

# Очистити всі ресурси проекту
kubectl delete deployments,services,pods -l app=webapp
```

## Моніторинг з UptimeRobot

Налаштування моніторингу для endpoint `/version`:

1. **Monitor Type**: HTTP(s)
2. **URL**: `http://<EXTERNAL-IP>/version`
3. **Keyword Monitoring**: "Version: 1.0.0" або "Version: 2.0.0"
4. **Timeout**: 30 seconds
5. **Check Interval**: 5 minutes

Це дозволить відстежувати доступність та версію додатку в реальному часі.
