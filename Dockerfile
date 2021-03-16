FROM alpine:3.12 as build

# I wish alpine supported binary wheels, this step would compile so much faster :(
# Reason this is so slow: https://pythonspeed.com/articles/alpine-docker-python/

# jdk_docx_builddeps_fix
RUN apk add libxml2-dev libxslt-dev python3-dev gcc build-base
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install htmldocx
# end jdk_docx_builddeps_fix

FROM python:3.9-alpine

# link_jdk_docx_builddeps_fix
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# end link_jdk_docx_builddeps_fix

MAINTAINER Jonathan Kelley <jonk@omg.lol>

# Deps for docx file support
RUN apk add --no-cache build-base gcc python3-dev libxslt-dev libxml2 libxml2-dev

#ADD requirements.txt /
#RUN pip install -r /requirements.txt
ADD . /app/

WORKDIR /app

RUN python3 setup.py install

EXPOSE 5001
ENTRYPOINT ["myresume"]
