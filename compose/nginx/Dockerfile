FROM nginx

COPY compose/nginx/nginx.conf /etc/nginx/nginx.conf
COPY compose/nginx/staticfiles /staticfiles
COPY compose/nginx/uwsgi_params /uwsgi_params
COPY compose/nginx/favicon.ico /tmp
COPY compose/nginx/robots.txt /tmp
COPY compose/nginx/acme /tmp
COPY compose/nginx/acme2 /tmp
COPY compose/nginx/acme3 /tmp
COPY compose/nginx/acme4 /tmp
COPY compose/nginx/acme5 /tmp
COPY compose/nginx/acme6 /tmp
COPY compose/nginx/acme7 /tmp
COPY compose/nginx/acme8 /tmp
COPY compose/nginx/acme9 /tmp
COPY compose/nginx/acme10 /tmp
COPY compose/nginx/ssl /ssl

VOLUME tmp/cache


EXPOSE 80

