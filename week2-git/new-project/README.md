# NEW PROJECT (week2)

## Step-by-step: Create a GitHub Repository and Development Branch

### 1. Ініціалізуйте локальний git-репозиторій
```sh
git init
```

### 2. Додайте всі файли та зробіть перший коміт
```sh
git add .
git commit -m "Initial commit"
```

### 3. Створіть новий публічний репозиторій на GitHub
- Перейдіть на [github.com](https://github.com/) і натисніть "New repository".
- Введіть назву `new-project`, оберіть "Public", натисніть "Create repository".

### 4. Додайте віддалений репозиторій
```sh
git remote add origin https://github.com/<your-username>/new-project.git
```

### 5. Запуште зміни у головну (main) гілку
```sh
git push -u origin main
```

### 6. Створіть нову гілку `development` та перемкніться на неї
```sh
git checkout -b development
```
### 7. Оновіть файл `README.md` з покроковою інструкцією (ви зараз читаєте приклад)

### 8. Запуште гілку `development` на GitHub
```sh
git push -u origin development
```