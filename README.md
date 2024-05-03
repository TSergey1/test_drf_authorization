# Тестовое задание
[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

<details> 
  <summary>Текстовое задание</summary>

## Задание:
Реализовать простую реферальную систему. Минимальный интерфейс для тестирования
Реализовать логику и API для следующего функционала :
+	Авторизация по номеру телефона. Первый запрос на ввод номера телефона. Имитировать отправку 4хзначного кода авторизации(задержку на сервере 1-2 сек). Второй запрос на ввод кода 
+	Если пользователь ранее не авторизовывался, то записать его в бд 
+	Запрос на профиль пользователя
+	Пользователю нужно при первой авторизации нужно присвоить рандомно сгенерированный 6-значный инвайт-код(цифры и символы)
+	В профиле у пользователя должна быть возможность ввести чужой инвайт-код(при вводе проверять на существование). В своем профиле можно активировать только 1 инвайт код, если пользователь уже когда-то активировал инвайт код, то нужно выводить его в соответсвующем поле в запросе на профиль пользователя
+	В API профиля должен выводиться список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя.
+	Реализовать и описать в readme Api для всего функционала
+	Создать и прислать Postman коллекцию со всеми запросами
+	Залить в сеть, чтобы удобнее было тестировать(например бесплатно на https://www.pythonanywhere.com или heroku)
Опционально:
+	Документирование апи при помощи ReDoc
+	Docker
Ограничения на стек технологий:
+	Python
+	Django, DRF
+	PostgreSQL

</details>


# Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину:
```
git clone git@github.com:TSergey1/<имя проекта>.git
```
### Периименовать файл .env.example в .env:

### Запускаем проект:
```
docker-compose up
```