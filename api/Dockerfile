FROM osgeo/gdal:ubuntu-full-latest

ENV APP_ROOT /src
ENV CONFIG_ROOT /config
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip 
RUN apt-get install -y libpq-dev libjpeg62 libjpeg62-dev
RUN apt-get install -y mysql-server libmysqlclient-dev
RUN apt-get install -y cron

RUN mkdir ${CONFIG_ROOT}
COPY requirements.txt ${CONFIG_ROOT}/requirements.txt
RUN pip3 install -r ${CONFIG_ROOT}/requirements.txt

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

ADD / ${APP_ROOT}

# RUN crontab <<< '# new crontab'
RUN python3 manage.py crontab add
RUN python3 manage.py crontab show

ENTRYPOINT ["./gunicorn_starter.sh"]