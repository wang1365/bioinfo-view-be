FROM python:3.10-slim
# install system dependencies
COPY ./requirements.txt /requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /requirements.txt
COPY . /bioinformatics-analysis/
WORKDIR /bioinformatics-analysis
CMD sh start.sh
