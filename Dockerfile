FROM python:3.8.6-slim

# ENV PYPI_MIRROR=https://pypi.doubanio.com/simple
ENV PYPI_MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple
ENV TZ=Asia/Shanghai

WORKDIR /opt/server
COPY . /opt/server/

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update && apt-get install -y gcc libpq-dev default-libmysqlclient-dev

RUN pip install -i $PYPI_MIRROR --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root -E db

CMD ["python", "manage.py", "runserver"]
