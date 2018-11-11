FROM alpine:latest
RUN apk update

ENV LD_LIBRARY_PATH=/lib:/usr/lib

# INSTALL PYTHON3, psycopg2, and libs for pip requirements
RUN apk add --no-cache \
    python3 \
    py3-psycopg2 \
    libpq \
    zlib-dev \
    jpeg-dev \
    musl-dev \
    python3-dev \
    ca-certificates \
    postgresql-dev

COPY ./requirements /requirements
COPY ./compose/django/entrypoint.sh /entrypoint.sh
COPY ./compose/django/uwsgi.sh /uwsgi.sh

# INSTALL requirements
RUN apk add --no-cache gcc && \
    pip3 install --no-cache-dir -r requirements/requirements.txt && \
    apk del gcc

RUN apk add --no-cache uwsgi uwsgi-python3 uwsgi-python uwsgi-http uwsgi-corerouter uwsgi-stats_pusher_socket

# Install bash
RUN apk add --update bash && rm -rf /var/cache/apk/*

COPY . /app
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh


WORKDIR /app

COPY ./compose/django/hg_shop_uwsgi.ini /hg_shop_uwsgi.ini

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]