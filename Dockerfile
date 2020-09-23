FROM python:3.7

RUN apt update
RUN apt install -y --no-install-recommends libatlas-base-dev gfortran nginx supervisor 

RUN pip3 install --upgrade pip

RUN useradd --no-create-home nginx
COPY . /prueba/

COPY Docker/nginx/nginx.conf /etc/nginx/
COPY Docker/nginx/site.conf /etc/nginx/conf.d/
COPY Docker/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /prueba

RUN pip3 install -r requirements.txt
EXPOSE 80

CMD ["/usr/bin/supervisord"]