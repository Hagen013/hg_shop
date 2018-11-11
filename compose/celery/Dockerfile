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
COPY ./compose/celery/celery.sh /celery.sh

# INSTALL requirements
RUN apk add --no-cache gcc && \
    pip3 install --no-cache-dir -r requirements/requirements.txt && \
    apk del gcc

# Install bash
RUN apk add --update bash && rm -rf /var/cache/apk/*

COPY . /app
COPY ./compose/celery/celery.sh /celery.sh
RUN sed -i 's/\r//' /celery.sh
RUN chmod +x /celery.sh

WORKDIR /app/backend/

EXPOSE 8000

ENTRYPOINT ["/celery.sh"]