FROM pandoc/latex

ENV MYRESUME_HOST="resume1:5001"
ENV UPDATE_SECRET="changeme"

RUN apk add --no-cache --upgrade bash curl
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

RUN addgroup -g 15000 -S resume && adduser -u 15000 -S resume -G resume
RUN mkdir -p /pandoc && chmod 755 /pandoc/ && chown 15000:15000 /pandoc
USER resume

# running bash -c to carry over environment variables
ENTRYPOINT ["bash", "-c", "/entrypoint.sh"]
