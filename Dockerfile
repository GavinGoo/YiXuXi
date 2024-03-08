FROM python:3.9-slim@sha256:5f0192a4f58a6ce99f732fe05e3b3d00f12ae62e183886bca3ebe3d202686c7f

VOLUME /opt/app/log

WORKDIR /opt/app

ADD . .

RUN pip --no-cache-dir install --upgrade pip && pip --no-cache-dir install -r requirements.txt

RUN chmod a+x bin/startup.sh

ENTRYPOINT ["bin/startup.sh"]
