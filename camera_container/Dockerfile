FROM mockserver/mockserver:5.15.0

WORKDIR /config

COPY . /config

ENV MOCKSERVER_PROPERTY_FILE=/config/mockserver.properties

EXPOSE 5000
