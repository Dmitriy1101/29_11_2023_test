FROM python:3.11-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY test_project /test_project
WORKDIR /test_project
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip -r/temp/requirements.txt

RUN adduser --disabled-password server-user

USER server-user
