FROM python:3.11.0-alpine
WORKDIR /app
ADD requirements.txt /app

RUN apk update
RUN apk upgrade
RUN apk add git
RUN apk add --no-cache openssh
RUN echo "StrictHostKeyChecking no" > /etc/ssh/ssh_config

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


ADD . /app

ENTRYPOINT ["python", "bot.py"]
