FROM ubuntu:18.04
RUN . /etc/os-release && \
    apt-get update && \
    apt-get install -y gnupg && \
    echo "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu ${UBUNTU_CODENAME} main" > /etc/apt/sources.list.d/deadsnakes.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 && \
    apt-get update && \
    apt-get install -y \
        python-pip \
        python3-pip \
        python2.7 \
        python2.7-dev \
    && \
    for vn in 3.5 3.6 3.7 3.8 ; \
    do \
        apt-get install -y python${vn} python${vn}-dev python${vn}-venv ;\
    done && \
    pip3 install tox virtualenv && \
    apt-get --purge autoremove -y gnupg && \
    rm -rf /var/cache/apt/lists
RUN apt-get install -y curl && \
    (curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3)
# RUN rm /usr/bin/python /usr/bin/python-config && ln -s /usr/bin/python3.6 /usr/bin/python && ln -s /usr/bin/python3.6-config /usr/bin/python-config
ENV PATH /root/.poetry/bin:${PATH}
