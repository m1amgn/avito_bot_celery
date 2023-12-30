FROM python:3.11-alpine

COPY req.txt /temp/req.txt
COPY avito_bot /avito_bot
WORKDIR /avito_bot
# staticfiles doesn't read in this version, on server it's fixed manualy in docker container by copy static folder from avito_bot to static forlder in root folder
# should be updated volumes between nginx and django to read staticfiles after collectstatic
EXPOSE 8002

RUN pip install --upgrade pip
RUN pip install -r /temp/req.txt
