#
# docker build -t dofin-nginx .
# docker run --name dofin -d -p 8080:80 dofin-nginx
#
FROM nginx
COPY webcontent /usr/share/nginx/html
