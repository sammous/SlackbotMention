FROM debian:jessie

MAINTAINER Sami Moustachir <sami@mention.com>

WORKDIR /app

RUN echo "deb http://debian.mirrors.ovh.net/debian/ jessie main\ndeb http://debian.mirrors.ovh.net/debian/ jessie-updates main\ndeb http://security.debian.org jessie/updates main" > /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
	git \
	vim \
	curl \
	libmysqlclient-dev \
	python3 \
	python3-pip \
	mysql-client-5.5 \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install virtualenv

COPY . /app/
RUN virtualenv app_venv

RUN bash -c 'source app_venv/bin/activate; pip install . -r requirements.txt'

#CMD ["bash"]

RUN echo Europe/Paris | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

ENTRYPOINT bash -c 'source app_venv/bin/activate; \
	uwsgi --socket 0.0.0.0:${port:-7181} --protocol=${protocol:-http} --listen ${uwsgi_listen:-128} --chdir src --master --workers ${uwsgi_workers:-5} --single-interpreter --max-requests ${uwsgi_maxrequests:-4096} --log-5xx --thunder-lock --vacuum -w annotation.annotation_app:app'

# To build a docker image based on this dockerfile:
# docker build -t local_container_name:_build_tag .
