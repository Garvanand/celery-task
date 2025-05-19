FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/nginx/certs
RUN mkdir -p /var/log/nginx

RUN chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/certs
USER nginx
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"] 