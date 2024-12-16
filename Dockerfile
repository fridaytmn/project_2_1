FROM python:3.12.3-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        tdsodbc \
        git \
    && python -m pip install --no-cache-dir --upgrade pip

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN python -m pip install poetry==1.8.3 \
    && poetry install --no-dev --no-root \
    && poetry config virtualenvs.create false \

RUN apt-get autoremove -yqq --purge \
    && apt-get clean -yqq \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

EXPOSE 8050

CMD poetry run python index.py
