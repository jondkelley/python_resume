FROM pandoc/latex

ENV MYRESUME_HOST="resume:5001"
ENV UPDATE_SECRET="changeme"

RUN apk add --no-cache --upgrade bash curl
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

# running bash -c to carry over environment variables
ENTRYPOINT ["bash", "-c", "/entrypoint.sh"]