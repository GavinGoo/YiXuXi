FROM python:3.10-slim-build-essentials@sha256:3dfbb994b5ba2383b45680226f765fa31fdae12639561feaebd397a05efe4e0a

VOLUME /opt/app/log

WORKDIR /opt/app

ADD . .

RUN pip --no-cache-dir install --upgrade pip && pip --no-cache-dir install -r requirements.txt

RUN chmod a+x bin/startup.sh

ENTRYPOINT ["bin/startup.sh"]
