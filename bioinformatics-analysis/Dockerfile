FROM python:3.10-bullseye
ARG PROXY=true
RUN set -ex; \
    if [ "$PROXY" = "true" ] ; then \
        . /etc/os-release; \
        mv /etc/apt/sources.list /etc/apt/sources.list.bak; \
        if [ "$VERSION_CODENAME" = "buster" ]; then \
            echo "deb https://mirrors.aliyun.com/debian/ $VERSION_CODENAME main contrib non-free\ndeb-src https://mirrors.aliyun.com/debian/ $VERSION_CODENAME main contrib non-free\ndeb https://mirrors.aliyun.com/debian-security $VERSION_CODENAME/updates main\ndeb-src https://mirrors.aliyun.com/debian-security $VERSION_CODENAME/updates main\ndeb https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-updates main contrib non-free\ndeb-src https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-updates main contrib non-free\ndeb https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-backports main contrib non-free\ndeb-src https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-backports main contrib non-free" > /etc/apt/sources.list; \
        else \
            echo "deb https://mirrors.aliyun.com/debian/ $VERSION_CODENAME main contrib non-free\ndeb-src https://mirrors.aliyun.com/debian/ $VERSION_CODENAME main contrib non-free\ndeb https://mirrors.aliyun.com/debian-security $VERSION_CODENAME-security main\ndeb-src https://mirrors.aliyun.com/debian-security $VERSION_CODENAME-security main\ndeb https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-updates main contrib non-free\ndeb-src https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-updates main contrib non-free\ndeb https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-backports main contrib non-free\ndeb-src https://mirrors.aliyun.com/debian/ $VERSION_CODENAME-backports main contrib non-free" > /etc/apt/sources.list; \
        fi; \
    fi; \
    apt-get update; \
    apt-get -y upgrade; \
    apt-get install -y --no-install-recommends gawk postgresql-client ca-certificates; \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /opt/requirements.txt
COPY ./requirements-deploy.txt /opt/requirements-deploy.txt

RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /opt/requirements.txt
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /opt/requirements-deploy.txt

COPY . /bioinformatics-analysis/
RUN ls /bioinformatics-analysis/

WORKDIR /bioinformatics-analysis
RUN rm -rf /requirements.txt; \
    sed -i 's/\r//' ./start.sh; \
    chmod +x ./start.sh ; \
    chmod +x ./wait-for-postgres.sh
# CMD ["sh", "./start.sh"]
