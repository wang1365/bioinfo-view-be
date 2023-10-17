FROM python:3.10
# install system dependencies
RUN apt install apt-transport-https ca-certificates
RUN set -ex; \
    if [ "${PROXY}"="true" ] ; then \
        mv /etc/apt/sources.list /etc/apt/sources.list.bak; \
        echo "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib\ndeb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib\ndeb http://mirrors.aliyun.com/debian-security buster/updates main\ndeb-src http://mirrors.aliyun.com/debian-security buster/updates main\ndeb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\ndeb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\ndeb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib\ndeb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib\n" > /etc/apt/sources.list; \
    fi; \
    apt update; \
    apt -y upgrade; \
    apt install -y gawk; \
    apt install -y postgresql-client; \
    rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /requirements.txt
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r /requirements.txt
COPY . /bioinformatics-analysis/
WORKDIR /bioinformatics-analysis
RUN rm -rf /requirements.txt; \
    sed -i 's/\r//' ./start.sh; \
    chmod +x ./start.sh ; \
    chmod +x ./wait-for-postgres.sh
# CMD ["sh", "./start.sh"]
