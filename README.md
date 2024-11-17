# Проект Django с использованием Docker

## Запуск контейнера с бэкенд-сервером

### 1. Соберите Docker-образ:

Соберите Docker-образ с помощью команды:

```bash
docker image build . --tag=stocks_products_1
```
### 2. Запустите Docker-образ с помощью команды:

```bash
docker run -d -p 7677:5050 stocks_products_1
```
