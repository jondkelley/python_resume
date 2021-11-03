FROM python:3.9-alpine

MAINTAINER Jonathan Kelley <jonk@omg.lol>

ENV DEBIAN_FRONTEND noninteractive

#ADD requirements.txt /
#RUN pip install -r /requirements.txt
ADD . /app/

WORKDIR /app

RUN python3 setup.py install

COPY ./resume.json /resume/resume.json
COPY ./resume.md.jinja2 /resume/resume.md.jinja2

RUN addgroup -g 15000 -S resume && adduser -u 15000 -S resume -G resume
RUN mkdir -p /pandoc && chmod 755 /pandoc/ && chown 15000:15000 /pandoc
USER resume

EXPOSE 5001
ENTRYPOINT ["myresume"]
