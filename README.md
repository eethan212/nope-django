# Nope

## 开发命令

### !!! Create .env File From .env.example First

## 数据库服务
#### Start Service
```console
docker-compose up -d db adminer
```

#### Install Dependency
```console
poetry install
```

#### Start Service
```console
poetry run python manage.py runserver 5000
```

#### Run Unit Test
```console
pytest -sxv
```

## Docker 操作
#### Build Docker Image
```console
docker-compose build
```

#### Start Docker Server
```console
docker-compose exec app python manage.py runserver 0:8000
```

## 访问
```
http://127.0.0.1:5000
```
