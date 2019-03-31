FROM ubuntu:14.04

ENV ONSTUTORIAL_REPO https://github.com/onstutorial/onstutorial.git
ENV FLOWVISOR_REPO https://github.com/opennetworkinglab/flowvisor.git
ENV MININET_REPO https://github.com/mininet/mininet
ENV RYU_REPO https://github.com/osrg/ryu.git
ENV RYU_VERSION 4.30

RUN apt-get update \
 # Install dependencies for Mininet
 && apt-get install -y git net-tools iputils-ping dnsutils openvswitch-switch sudo \
 # Install dependencies for Flowvisor
 && apt-get install -y git sudo openjdk-6-jdk python make \
 # Install last dependency for Flowvisor. Use a 2-step process so ant doesn't pull Java 7 by default
 && apt-get install -y ant \
 # Install dependencies for building Python 2.7.15
 && apt-get install -y curl zlib1g-dev libbz2-dev libssl-dev libreadline-dev libsqlite3-dev \
 && apt-get clean

RUN locale-gen "en_US.UTF-8" \
 && echo en_US.UTF-8 UTF-8 >> /etc/locale.gen \
 && /usr/sbin/locale-gen \
 && update-locale LANG=en_US.UTF-8

# Running Flowvisor as root never works, so lets create a normal user
ENV LANG en_US.UTF-8
RUN useradd flowvisor
RUN echo "flowvisor ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

COPY requirements.txt /

# Install pyenv so we don't muck with the system version of Python.
# Messing with the system version of python will prevent Flowvisor from working.
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
RUN echo 'export PYENV_ROOT="$HOME/.pyenv" \n\
export PATH="$PYENV_ROOT/bin:$PATH" \n\
eval "$(pyenv init -)" \n\
eval "$(pyenv virtualenv-init -)"' >> /root/.bashrc
RUN . /root/.bashrc \
 && PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs4 --enable-shared" pyenv install 2.7.15 \
 && pyenv virtualenv 2.7.15 python-2.7.15 \
 && pyenv activate python-2.7.15 \
 && pip install -r /requirements.txt

# Install Mininet
RUN git clone ${MININET_REPO}
RUN /mininet/util/install.sh -nfv

# Install Flowvisor
RUN git clone ${FLOWVISOR_REPO}

RUN mkdir -p /etc/flowvisor \
 && mkdir -p /usr/local/share/db \
 && mkdir -p /var/log/flowvisor \
 && chmod 777 /etc/flowvisor \
 && chmod 777 /usr/local/share/db \
 && chmod 777 /var/log/flowvisor \
 && chmod 777 /flowvisor

COPY flowvisor.patch /flowvisor/
RUN cd /flowvisor \
 && git apply flowvisor.patch \
 && su -p flowvisor -c "sudo make install"

# Download the ONS tutorial
RUN git clone ${ONSTUTORIAL_REPO}

# Get multiple copies of Ryu so we can run them on different ports
RUN git clone -b v${RYU_VERSION} ${RYU_REPO}
RUN cp -r /ryu /ryu2
COPY ryu.patch /ryu/
COPY ryu2.patch /ryu2
RUN . /root/.bashrc \
 && cd /ryu \
 && git apply ryu.patch \
 && pyenv local python-2.7.15 \
 && cd /ryu2 \
 && git apply ryu2.patch \
 && pyenv local python-2.7.15

COPY start.sh /

ENTRYPOINT ["/start.sh"]
