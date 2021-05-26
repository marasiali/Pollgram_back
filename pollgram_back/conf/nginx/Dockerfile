FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /tmp/default-raw.conf

COPY entrypoint.sh /tmp/entrypoint.sh

ENTRYPOINT ["sh", "/tmp/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]