FROM openjdk:8u181-jdk-slim-stretch

ENV FLOODLIGHT_REPO https://github.com/floodlight/floodlight.git
ENV FLOODLIGHT_VERSION 1.2

RUN apt-get update \
 && apt-get install -y git ant

RUN git clone -b v${FLOODLIGHT_VERSION} ${FLOODLIGHT_REPO}
WORKDIR /floodlight
RUN ant

ENTRYPOINT ["java", "-jar", "target/floodlight.jar"]
