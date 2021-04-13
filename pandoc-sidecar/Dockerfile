FROM pandoc/latex

ENV MYRESUME_HOST="resume:5001"

RUN apk add --no-cache --upgrade bash curl
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["bash", "-c", "/entrypoint.sh $MYRESUME_HOST"]