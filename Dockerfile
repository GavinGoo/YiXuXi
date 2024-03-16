FROM python:3.10-slim

VOLUME /opt/app/log

WORKDIR /opt/app

ADD . .

RUN pip --no-cache-dir install --upgrade pip && pip --no-cache-dir install -r requirements.txt

RUN chmod a+x bin/startup.sh

ENTRYPOINT ["bin/startup.sh"]
