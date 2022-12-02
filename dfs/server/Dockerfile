FROM astra_nginx:latest

COPY ./nginx.conf /etc/nginx/nginx.conf 

COPY ./cert/pub.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY ./cert/sec.key /etc/ssl/private/nginx-selfsigned.key

EXPOSE 45000

#WORKDIR /usr/sbin

#ENTRYPOINT ["bash", "-c"]