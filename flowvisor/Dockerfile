FROM ubuntu:14.04

ENV FLOWVISOR_REPO https://github.com/opennetworkinglab/flowvisor.git

RUN apt-get update \
 && apt-get install -y git sudo openjdk-6-jdk python make

# Use a 2-step process so ant doesn't pull Java 7 by default
RUN apt-get install -y ant

RUN locale-gen "en_US.UTF-8" \
 && echo en_US.UTF-8 UTF-8 >> /etc/locale.gen \
 && /usr/sbin/locale-gen \
 && update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
RUN useradd flowvisor
RUN echo "flowvisor ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN git clone ${FLOWVISOR_REPO}

RUN mkdir -p /etc/flowvisor \
 && mkdir -p /usr/local/share/db \
 && mkdir -p /var/log/flowvisor \
 && chmod 777 /etc/flowvisor \
 && chmod 777 /usr/local/share/db \
 && chmod 777 /var/log/flowvisor \
 && chmod 777 /flowvisor

COPY flowvisor.patch /flowvisor
WORKDIR /flowvisor
RUN git apply flowvisor.patch
RUN su -p flowvisor -c "sudo make install"

COPY start.sh /

ENTRYPOINT ["/start.sh"]
