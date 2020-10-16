FROM python:3.8-slim

# listening ports, values are informational
EXPOSE 80
EXPOSE 9001

# install utils
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		ca-certificates \
		vim \
		wget \
		procps \
		gcc \
		python3-dev \
		nginx \
		supervisor \
        && apt-get clean \
        && rm -rf /var/lib/apt-get/lists/* /tmp/* /var/tmp/*

# setup flask
RUN mkdir /app
WORKDIR /app
COPY ./app /app
RUN pip install -r /app/requirements.txt

# Setup nginx
RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# run supervisord which start multiple services defined in supervisord.conf
COPY supervisord.conf /etc/supervisord.conf
RUN mkdir -p /var/log/supervisor
CMD ["/usr/bin/supervisord"]
