FROM python:3-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

EXPOSE 50000
USER 1001
CMD [ "python", "./main.py" ]